import streamlit as st
from huggingface_hub import InferenceClient
from group_sys_msg import *
from group_utils import *
import ast
import pandas as pd
from twilio_utils import floating_button_css,floating_button_html



# ---------set css and buy me coffee-------------#
st.markdown(btn_css, unsafe_allow_html=True)
#st.markdown(image_css, unsafe_allow_html=True)

# buymecoffee button
st.markdown(floating_button_css, unsafe_allow_html=True)
st.markdown(floating_button_html, unsafe_allow_html=True)
# --- Initialize the Inference Client with the API key ----#
try:
    client = InferenceClient(token=st.session_state.hf_access_token[0])
    
except Exception as e:
    st.error(f"Error initializing Inference Client: {e}")
    st.stop()

# ------- create side bar --------#
with st.sidebar:
    #st.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    st.subheader(f"PFB Group Assignment")
    #st.write(":gray[*Upload by project group in a zip file*]")
    model_id = st.selectbox(":grey[Select an AI model]", 
                            ["Qwen/Qwen2.5-72B-Instruct",
                             "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
                             "meta-llama/Llama-3.3-70B-Instruct"],
                            index=2,
                            help=model_help)
    upload_student_report = st.file_uploader(":grey[Upload a zip file (by project group level)]", type=["zip"], help=zip_help)
    #evaluate_btn = st.button(":material_search_insights: Evaluate Report", type="primary")
    #clear_btn = st.button(":material_refresh: Clear History", type="primary")
    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)

# to store marks from each output
program_correctness_data = []

if upload_student_report:

    # display marking references
    st.sidebar.markdown(":blue[Marking References]", help=summary_report_var)
    with st.sidebar.expander(f":grey[*Output for Decreasing Trend*]"):
        st.code(output_decreasing)
    with st.sidebar.expander(f":grey[*Output for Increasing Trend*]"):
        st.code(output_increasing)
    with st.sidebar.expander(f":grey[*Output for Volatile Trend*]"):
        st.code(output_volatile)
    with st.sidebar.expander(f":grey[*Marking rubrics for summary report*]"):
        st.write(mark_rubrics_output_reference)
    with st.sidebar.expander(f":grey[*Marking rubrics for code*]"):
        st.write(mark_rubrics_code)

    # extract and read zip file
    extracted_content = extract_and_read_files(upload_student_report)
     
 
    for folder, contents in extracted_content.items():
            
        if contents["team_members"]:

            st.text(contents["team_members"]) 
            st.subheader(f":red[summary_report.txt]")

            #-------- code section for the marking of output ------#
            try:

                # iterate over the decreasing, increasing and volatile output 
                for index, item in enumerate(contents['summary']):

                    # create 'msg_history_output' for marking the output
                    if 'msg_history_output' not in st.session_state:
                        st.session_state.msg_history_output = []

                    # append output system message
                    st.session_state.msg_history_output.append({"role": "system", 
                                                        "content": f"{system_message_output}"})   
                    # append output team members names 
                    st.session_state.msg_history_output.append({"role": "user", 
                                                                "content": f"Mark this assignment for {contents["team_members"]}."})
                    # append output marking rubrics
                    # it was concatenated as a list for the ease of iteration in sys_message.py
                    st.session_state.msg_history_output.append({"role": "system", 
                                                                "content": f"This is the marking rubrics for the output: {mark_rubrics_list[index]}"})
                    # append student's output
                    st.session_state.msg_history_output.append({"role": "user", 
                                                                "content": f"This is output from the students for '{item[0]}':\n{item[1]}"})
                    
                    # display output
                    with st.expander(f":blue[*{item[0]}*]"):
                        st.code(item[1])

                    # marking the output by llm
                    
                    with st.status(f"Evaluating {item[0]}", expanded=True) as status:
                        with st.empty():
                            try:
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
                                # append to program_correctness_data
                                program_correctness_data.append(output_dict)
                                # delete 'msg_history_output' after marking each output
                                del st.session_state.msg_history_output
                                status.update(label=f"Evaluation completed for {item[0]}...", state="complete", expanded=True)
                            
                            except Exception as e:
                                st.error(e)
                                
                        #sms_txt = f"⚠️ <{st.session_state.user_id}> Output evaluation ✅"
                        #send_sms_txt(sms_txt)
            
            except Exception as e:
                # create 'msg_history_output' for marking the output
                if 'msg_history_output' not in st.session_state:
                    st.session_state.msg_history_output = []

                st.session_state.msg_history_output.append({"role": "user", 
                                                            "content": f"Fail to generate output from the python code"})
                
                st.error(f":red[*Unable to generate summary reports*]")
                
                #sms_txt = f"⚠️ <{st.session_state.user_id}> Summary reports ❌"
                #send_sms_txt(sms_txt)

            #-------- code section for the marking of python code ------#
            st.write("---")
            st.subheader(f":red[Python code]")

            # create 'msg_history_code' for marking the code
            if 'msg_history_code' not in st.session_state:
                st.session_state.msg_history_code = []

                # append team members, system instructions and mark rubrics for code
                st.session_state.msg_history_code.append({"role": "user", 
                                                                    "content": f"Mark this assignment for {contents["team_members"]}."})
                st.session_state.msg_history_code.append({"role": "system", "content": f"{system_message_code}"})
                st.session_state.msg_history_code.append({"role": "system", 
                                                    "content": f"This is the marking rubrics for reference: {mark_rubrics_code}"})

            # iterate over each python files
            for filename, item in contents["python_files"]:
                
                # append each python file 
                st.session_state.msg_history_code.append({"role": "user", 
                                                          "content": f"Python filename: {filename}\nPython code:\n{item}"})
                #display code for each file
                with st.expander(f":blue[*{filename}*]"):
                    st.code(item, language="python")
            
            # llm to mark all three files of python code 
            with st.status("Evaluating...", expanded=True) as status:
                with st.empty():
                    try:
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
                        # del msg_history_code
                        del st.session_state.msg_history_code
                        status.update(label="Evaluation completed for code...", state="complete", expanded=True)
                    except Exception as e:
                        st.error(e)
      

if program_correctness_data:
    # sum the marks for each output 
    program_correctness_marks = sum(item["Output marks"] for item in program_correctness_data)
    # concatenate feedback from each output
    feedback_list = [item["Feedback"] for item in program_correctness_data]
    consolidated_feedback = " ".join(feedback_list)

    # Output structure
    output = {
        "Team members": program_correctness_data[0]["Team members"],
        "Program Correctness": program_correctness_marks,
        "Code Readability": code_dict["Code Readability"], 
        "Code Efficiency": code_dict["Code Efficiency"],
        "Documentation":code_dict["Documentation"],
        "Assignment Specifications": code_dict["Assignment Specifications"],
        "Consolidated Feedback": f"{consolidated_feedback} {code_dict['Feedback']}"
    }
    
    st.write("---")
    st.subheader(f":red[Marks Summary]")
    st.dataframe(output)
    st.write(f":grey[*Program Correctness is the sum of the output marks from evaluation of summary_report.txt*]")
    #sms_txt = f"⚠️ <{st.session_state.user_id}> Marks Summary ✅"
    #send_sms_txt(sms_txt)

# code_dict is a dict the generated responses from llm 
# { 'Team_members': ,
#   'Code Readability': ,
#   'Code Efficiency': ,
#   'Documentation':,
#   'Assignment Specifications': 
# }
