import streamlit as st
from huggingface_hub import InferenceClient
from individual_utils import *
from individual_sys_msg import *
from charset_normalizer import from_path
import ast

# set up page config
#st.set_page_config(page_title="Assistive Marking AI Tool",
#                   layout="wide",
#                   initial_sidebar_state="expanded")


# setup css
st.markdown(btn_css, unsafe_allow_html=True)
st.markdown(image_css, unsafe_allow_html=True)

# Initialize the Inference Client with the API key 
client = InferenceClient(token=st.secrets.api_keys.huggingfacehub_api_token)

# create sidebar for upload, clear messages
with st.sidebar:
    st.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    st.subheader(f":blue[*PFB Individual Assignment Only*]")
    st.write(":red[*Upload a zip file up class level*]")
    model_id = st.selectbox(":grey[Select an AI model]", 
                            ["Qwen/Qwen2.5-72B-Instruct",
                             "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
                             "meta-llama/Llama-3.3-70B-Instruct"],
                            index=2,
                            help=model_help)
    
    upload_student_report = st.file_uploader(":grey[Upload a ZIP file]", type=["zip"], help=upload_help)
    #evaluate_btn = st.button(":material_search_insights: Evaluate Report", type="primary")
    #clear_btn = st.button(":material_refresh: Clear History", type="primary")
    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)

# store 'merged_data' dict variable in each iteration
data = [] 

if upload_student_report:
    # display the correct output for reference  
    st.sidebar.markdown(":blue[Marking Reference]", help=summary_report_var)
    with st.sidebar.expander("Summary Report"):
        st.code(SpaceSummary)
    with st.sidebar.expander("Marking rubrics"):
        st.write(mark_rubrics_output_reference)
        st.write(mark_rubrics_code)


    # extraction zip file on a class level
    extracted_content = extract_and_read_files(upload_student_report)

    # iterate over each subfolder (assignment submission)
    for folder, contents in extracted_content.items():
        # create msg_history_output for marking the output
        if 'msg_history_output' not in st.session_state:
            st.session_state.msg_history_output = []
        # create msg_history_output for marking the code
        if 'msg_history_code' not in st.session_state:
            st.session_state.msg_history_code = []

        # display student's name    
        st.write("---")
        st.subheader(f":blue[{contents["student name"]}]") 

        # display student's python code
        with st.expander(f":grey[*PYTHON FILE*]"):
            st.code(contents["python file"], language="python")

        # append system instruction, student's name, student's python code and rubrics to history 
        st.session_state.msg_history_code.append({"role": "system", "content": f"{system_message_code}"})
        st.session_state.msg_history_code.append({"role": "system", "content": f"This is the marking rubrics for python code: {mark_rubrics_code}"})
        st.session_state.msg_history_code.append({"role": "user", "content": f"Student name:\n{contents["student name"]}."})   
        st.session_state.msg_history_code.append({"role": "user", "content": f"This is the python code from the student:\n{contents["python file"]}"})
       
        # evaluate student's python code 
        with st.status("Evaluating code...", expanded=True) as status:
            with st.empty():
                stream = client.chat_completion(
                    model=model_id,
                    messages=st.session_state.msg_history_code,
                    temperature=0.1,
                    max_tokens=5524,
                    top_p=0.7,
                    stream=True,
                )
                
                collected_response = ""

                for chunk in stream:
                    if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                        collected_response += chunk.choices[0].delta.content
                        st.text(collected_response.replace('{','').replace('}',''))

                # Convert string to dict
                code_dict = ast.literal_eval(collected_response)
                del st.session_state.msg_history_code
                status.update(label="Code evaluation completed...", state="complete", expanded=True)


        # append system instruction, student's name and rubrics to history        
        st.session_state.msg_history_output.append({"role": "system", "content": f"{system_message_output}"})   
        st.session_state.msg_history_output.append({"role": "system", "content": f"This is the marking rubrics for the output: {mark_rubrics_output}"})
        st.session_state.msg_history_output.append({"role": "user", "content": f"Student name:\n{contents["student name"]}."})
        
        try:
            # display student's output
            with st.expander(f":grey[*OUTPUT*]"):
                st.code(contents['summary'])
            # append  student's output to history
            st.session_state.msg_history_output.append({"role": "user", "content": f"This is output from the student:\n{contents['summary']}"})
            
        except Exception as e:
            # if contents['summary'] fails, append a failed message to history 
            # 'system_message_output' contains instruction to assign zero marks when there is a fail message.
            st.session_state.msg_history_output.append({"role": "user", "content": f"Student did not produce an output"})
            st.error(f":red[*Unable to generate summary reports*]")


        # evaluate student's output
        with st.status("Evaluating output...", expanded=True) as status:
            with st.empty():
                stream = client.chat_completion(
                    model=model_id,
                    messages=st.session_state.msg_history_output,
                    temperature=0.1,
                    max_tokens=5524,
                    top_p=0.7,
                    stream=True,
                )
                
                collected_response = ""

                for chunk in stream:
                    if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                        collected_response += chunk.choices[0].delta.content
                        st.text(collected_response.replace('{','').replace('}',''))

                # Convert string to dict
                output_dict = ast.literal_eval(collected_response)
                del st.session_state.msg_history_output
                status.update(label="Output evaluation completed...", state="complete", expanded=True)
        
        # Concatentate code_dict and output_dict to combine the evaluation for one student
        merged_data = {**code_dict, **output_dict}
        merged_data['Feedback'] = f"{code_dict['Feedback']} {output_dict['Feedback']}"
        data.append(merged_data)


if data:
    # write to dataframe
    df = process_data(data)
    st.write(df)
            
#if clear_btn:
#    for key in st.session_state.keys():
#        del st.session_state[key]
#    st.cache_data.clear()    

