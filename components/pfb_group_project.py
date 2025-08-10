import streamlit as st
from huggingface_hub import InferenceClient
from pfb_group_sys_msg import *
from pfb_group_utils import *
import ast
import pandas as pd
from utils_twilio_coffee import buymecoffee_btn_css, buymecoffee
from utils_inference import initialize_inferenceclient, model_list
from utils_help_msg import *
import json

# --- Initialize the Inference Client with the API key ----#
client = initialize_inferenceclient()

def aggregate_output(final_output_dict, output_dict):
    for key, value in output_dict.items():
        if key == "Team members":
            # skip because it's the same across all outputs
            if key not in final_output_dict:
                final_output_dict[key] = value
            continue

        if key not in final_output_dict:
            final_output_dict[key] = value
        else:
            # Sum numeric values
            if isinstance(value, (int, float)):
                final_output_dict[key] += value
            # Concatenate strings
            elif isinstance(value, str):
                final_output_dict[key] += " " + value

    return final_output_dict


def process_data(data):
    df = pd.DataFrame(data)

    df['Total'] = (
        df['Program Correctness'] + 
        df.get('Code Readability', 0) + 
        df.get('Code Efficiency', 0) + 
        df.get('Documentation', 0) + 
        df.get('Assignment Specifications', 0)
    )

    cols = [
        'Team members', 
        'Program Correctness', 
        'Code Readability', 
        'Code Efficiency', 
        'Documentation', 
        'Assignment Specifications', 
        'Total', 
        'Feedback'
    ]

    existing_cols = [col for col in cols if col in df.columns]
    return df[existing_cols] 


def sanitize_llm_response(response_text, required_keys, default_value=0):
    """
    Parses LLM response and ensures all required keys are present with defaults.
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



# ------- create side bar --------#
with st.sidebar:
    #st.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    st.subheader(f"PFB Group Assignment")
    #st.write(":gray[*Upload by project group in a zip file*]")
    model_id = st.selectbox(":grey[AI model]", 
                            model_list,
                            index=0,
                            help=model_help)
    

    upload_student_report = st.file_uploader(":grey[Upload a zip file (by project group level)]", type=["zip"], help=zip_help)
    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)
    st.markdown(buymecoffee_btn_css, unsafe_allow_html=True)
    if st.button("☕ Buy me coffee"):
        buymecoffee()

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
    data = [] 
    output_dict = {}
    final_output_dict =   { }  

 
    for folder, contents in extracted_content.items():
            
        if contents["team_members"]:

            st.text(contents["team_members"]) 
            st.subheader(f":red[summary_report.txt]")

            #------------------------------------------------------------#
            #-------- code section for the marking of output       ------#
            #------------------------------------------------------------#
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
                                                .replace('Team members', '**:orange[Team members]**')
                                                .replace(f'Program Correctness', f':orange[{item[0]}]')
                                                .replace('Feedback', '**:orange[Feedback]**')
                                                )
                                        
                                # Sanitize and parse LLM response
                                if collected_response.strip():
                                    required_keys_output = [
                                        "Team members",
                                        f"Program Correctness",
                                        "Feedback"
                                    ]
                                    output_dict = sanitize_llm_response(collected_response, required_keys_output)

                                    final_output_dict = aggregate_output(final_output_dict, output_dict)
                                
                                else:
                                    st.error("No response received from output evaluation")
                                    output_dict = {}
                            
                            except Exception as e:
                                st.error(e)

                    ## delete 'msg_history_output' after marking each output
                    del st.session_state.msg_history_output
                    
            except Exception as e:
                # create 'msg_history_output' for marking the output
                #if 'msg_history_output' not in st.session_state:
                #    st.session_state.msg_history_output = []

                #st.session_state.msg_history_output.append({"role": "user", 
                #                                            "content": f"Fail to generate output from the python code"})
                
                st.error(f":red[*Unable to generate summary reports*]")
                
            #------------------------------------------------------------#
            #-------- code section for the marking of python code -------#
            #------------------------------------------------------------#
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
                                    .replace('Team members', '**:orange[Student Name]**')
                                    .replace('Code Readability', '**:orange[Code Readability]**')
                                    .replace('Code Efficiency', '**:orange[ Code Efficiency]**')
                                    .replace('Documentation', '**:orange[Documentation]**')
                                    .replace('Assignment Specifications', '**:orange[Assignment Specifications]**')
                                    .replace('Feedback', '**:orange[Feedback]**')
                                    )

                        # Sanitize and parse LLM response
                        if collected_response.strip():
                            required_keys_code = [
                                "Team members",
                                "Code Readability",
                                "Code Efficiency",
                                "Documentation",
                                "Assignment Specifications",
                                "Feedback"
                            ]
                            code_dict = sanitize_llm_response(collected_response, required_keys_code)
                        else:
                            st.error("No response received from code evaluation")
                            code_dict = {}

                    except Exception as e:
                        st.error(e)

                # del msg_history_code
                del st.session_state.msg_history_code
                #status.update(label="Evaluation completed for code...", state="complete", expanded=True)

            # Merge dictionaries with fallbacks
    try:

        st.write(final_output_dict)
        # Extract feedback from both dictionaries (default to empty string if missing)
        code_feedback = code_dict.get("Feedback", "")
        output_feedback = final_output_dict.get("Feedback", "")

        # Concatenate feedbacks, separating with a newline if both exist
        combined_feedback = "\n".join(filter(None, [code_feedback, output_feedback]))

        # Merge the dictionaries
        merged_data = {**code_dict, **final_output_dict}

        # Override the Feedback field with the combined one
        merged_data["Feedback"] = combined_feedback

        # Ensure required keys are present with default 0 values
        required_final_keys = [
            "Team members",
            "Program Correctness",
            "Code Readability",
            "Code Efficiency",
            "Documentation",
            "Assignment Specifications",
            "Feedback",
        ]

        for key in required_final_keys:
            if key not in merged_data:
                merged_data[key] = 0  # Default fallback

        data.append(merged_data)

    except Exception as e:
        st.error(f"Error merging evaluations: {e}") 

    
    if data:
        # write to dataframe
        df = process_data(data)
        st.write(df)
