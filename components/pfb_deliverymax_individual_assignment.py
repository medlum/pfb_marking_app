import streamlit as st
from huggingface_hub import InferenceClient
from pfb_deliverymax_individual_utils import *
from pfb_deliverymax_individual_sys_msg import *
from charset_normalizer import from_path
import ast
import json
from utils_twilio_coffee import buymecoffee_btn_css, buymecoffee
from utils_inference import initialize_inferenceclient, model_list
from utils_help_msg import *

# Initialize the Inference Client with the API key 
client = initialize_inferenceclient()

# Helper function to sanitize LLM responses
def sanitize_llm_response(response_text, required_keys, default_value=0):
    """
    Parses LLM response and ensures all required keys are present with defaults.ß
    """
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON from LLM: {e}")
        data = {}

    # Fill in missing keys with default value
    for key in required_keys:
        if key not in data:
            data[key] = default_value

    return data

# create sidebar for upload, clear messages
with st.sidebar:
    
    st.subheader(f"PFB Individual Assignment")
    model_id = st.selectbox(":grey[AI model]", 
                            model_list,
                            index=0,
                            help=model_help)
    
    upload_student_report = st.file_uploader(":grey[Upload a ZIP file (by class level)]", type=["zip"])

    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)

    st.markdown(buymecoffee_btn_css, unsafe_allow_html=True)
    if st.button("☕ Buy me coffee"):
        buymecoffee()

# store 'merged_data' dict variable in each iteration
data = [] 

if upload_student_report:
    # display the correct output for reference  
    st.sidebar.markdown(":blue[Marking Reference]", help=summary_report_var)
    with st.sidebar.expander("Summary Report"):
        st.code(OutputSummary)
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
        # create msg_history_code for marking the code
        if 'msg_history_code' not in st.session_state:
            st.session_state.msg_history_code = []

        # display student's name    
        st.write("---")
        st.subheader(f":blue[{contents['student name']}]") 

        # display student's python code
        with st.expander(f":grey[*PYTHON FILE*]"):
            st.code(contents["python file"], language="python")
        
        #------ MARK PYTHON CODE -----#
        # append system instruction, student's name, student's python code and rubrics to history 
        st.session_state.msg_history_code.append({"role": "system", "content": f"{system_message_code}"})
        st.session_state.msg_history_code.append({"role": "system", "content": f"This is the marking rubrics for python code: {mark_rubrics_code}"})
        st.session_state.msg_history_code.append({"role": "user", "content": f"Student name:\n{contents['student name']}."})   
        st.session_state.msg_history_code.append({"role": "user", "content": f"This is the python code from the student:\n{contents['python file']}"})
       
        # evaluate student's python code 
        code_dict = {}  # Initialize before try block
        with st.status("Evaluating code...", expanded=True) as status:
            try:
                with st.empty():
                    stream = client.chat.completions.create(
                        model=model_id,
                        messages=st.session_state.msg_history_code,
                        temperature=0.2,
                        max_tokens=5524,
                        top_p=0.7,
                        stream=True,
                    )
                    
                    collected_response = ""
                    for chunk in stream:
                        # Check if chunk has choices and delta content
                        if (hasattr(chunk, 'choices') and 
                            len(chunk.choices) > 0 and 
                            hasattr(chunk.choices[0], 'delta') and 
                            hasattr(chunk.choices[0].delta, 'content')):
                            content = chunk.choices[0].delta.content or ""
                            collected_response += content
                            st.write(collected_response.replace('{','').replace('}','').replace('"','')
                                     .replace('Student Name', '**:orange[Student Name]**')
                                     .replace('Code Readability', '**:orange[Code Readability]**')
                                     .replace('Code Efficiency', '**:orange[ Code Efficiency]**')
                                     .replace('Documentation', '**:orange[Documentation]**')
                                     .replace('Assignment', '**:orange[Assignment]**')
                                     .replace('Specifications', '**:orange[Specifications]**')
                                     .replace('Feedback', '**:orange[Feedback]**')
                                     
                            )

                    # Sanitize and parse LLM response
                    if collected_response.strip():
                        required_keys_code = [
                            "Student Name",
                            "Code Readability",
                            "Code Efficiency",
                            "Documentation",
                            "Assignment Specifications",
                            "Feedback"
                        ]
                        code_dict = sanitize_llm_response(collected_response, required_keys_code)

                        #st.text_area("LLM Raw Output (Code)", collected_response, height=300)
                    else:
                        st.error("No response received from code evaluation")
                        code_dict = {}

                    if 'msg_history_code' in st.session_state:
                        del st.session_state.msg_history_code
                    status.update(label="Code evaluation completed...", state="complete", expanded=False)
            
            except Exception as e:
                st.error(f"Error evaluating code: {e}")
                code_dict = {}  # fallback empty dict

        #------ MARK OUTPUT  -----#
        # append system instruction, student's name and rubrics to history        
        st.session_state.msg_history_output.append({"role": "system", "content": f"{system_message_output}"})   
        st.session_state.msg_history_output.append({"role": "system", "content": f"This is the marking rubrics for the output: {mark_rubrics_output}"})
        st.session_state.msg_history_output.append({"role": "user", "content": f"Student name:\n{contents['student name']}."})
        
        try:
            # display student's output
            with st.expander(f":grey[*OUTPUT*]"):
                st.code(contents['summary'])
            # append  student's output to history
            st.session_state.msg_history_output.append({"role": "user", "content": f"This is output from the student:\n{contents['summary']}"})
            
        except Exception as e:
            # if contents['summary'] fails, append a failed message to history 
            st.session_state.msg_history_output.append({"role": "user", "content": f"Student did not produce an output"})
            st.error(f":red[*Unable to generate summary reports*]")

        # evaluate student's output
        output_dict = {}  # Initialize before try block
        with st.status("Evaluating output...", expanded=True) as status:
            with st.empty():
                try:
                    stream = client.chat.completions.create(
                        model=model_id,
                        messages=st.session_state.msg_history_output,
                        temperature=0.2,
                        max_tokens=5524,
                        top_p=0.7,
                        stream=True,
                    )
                    
                    collected_response = ""
                    for chunk in stream:
                        # Check if chunk has choices and delta content
                        if (hasattr(chunk, 'choices') and 
                            len(chunk.choices) > 0 and 
                            hasattr(chunk.choices[0], 'delta') and 
                            hasattr(chunk.choices[0].delta, 'content')):
                            content = chunk.choices[0].delta.content or ""
                            collected_response += content
                            st.write(collected_response.replace('{','').replace('}','').replace('"','')
                                     .replace('Student Name', '**:orange[Student Name]**')
                                     .replace('Output for DeliveryMax Summary', '**:orange[Output for DeliveryMax Summary]**')
                                     .replace('Output for Top 5 of 15 programs', '**:orange[Output for Top 5 of 15 programs]**')
                                     .replace('Feedback', '**:orange[Feedback]**')
                                     )

                    # Sanitize and parse LLM response
                    if collected_response.strip():
                        required_keys_output = [
                            "Student Name",
                            "Output for DeliveryMax Summary",
                            "Output for Top 5 of 15 programs",
                            "Feedback"
                        ]
                        output_dict = sanitize_llm_response(collected_response, required_keys_output)

                        #st.text_area("LLM Raw Output (Output)", collected_response, height=300)
                    else:
                        st.error("No response received from output evaluation")
                        output_dict = {}

                    if 'msg_history_output' in st.session_state:
                        del st.session_state.msg_history_output
                    status.update(label="Output evaluation completed...", state="complete", expanded=False)

                except Exception as e:
                    st.error(f"Error evaluating output: {e}")
                    output_dict = {}  # fallback empty dict
        
        # Merge dictionaries with fallbacks
        try:
            # Extract feedback from both dictionaries (default to empty string if missing)
            code_feedback = code_dict.get("Feedback", "")
            output_feedback = output_dict.get("Feedback", "")

            # Concatenate feedbacks, separating with a newline if both exist
            combined_feedback = "\n".join(filter(None, [code_feedback, output_feedback]))

            # Merge the dictionaries
            merged_data = {**code_dict, **output_dict}

            # Override the Feedback field with the combined one
            merged_data["Feedback"] = combined_feedback

            # Ensure required keys are present with default 0 values
            required_final_keys = [
                "Student Name",
                "Program Correctness",
                "Code Readability",
                "Code Efficiency",
                "Documentation",
                "Assignment Specifications",
                "Output for DeliveryMax Summary",
                "Output for Top 5 of 15 programs",
                "Feedback"
            ]

            for key in required_final_keys:
                if key not in merged_data:
                    merged_data[key] = 0  # Default fallback

            # Compute derived score
            merged_data["Program Correctness"] = (
                merged_data.get("Output for DeliveryMax Summary", 0) +
                merged_data.get("Output for Top 5 of 15 programs", 0)
            )

            data.append(merged_data)

        except Exception as e:
            st.error(f"Error merging evaluations: {e}")

# Final DataFrame processing
if data:
    # write to dataframe
    df = process_data(data)
    st.write(df)
