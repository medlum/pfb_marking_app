import streamlit as st
from huggingface_hub import InferenceClient
from pfb_research_report_utils import *
from pypdf import PdfReader
from docx import Document
from pfb_research_report_sys_msg import *
from utils_inference import initialize_inferenceclient, model_list
from utils_twilio_coffee import buymecoffee_btn_css, buymecoffee
from utils_help_msg import *

# Initialize the Inference Client with the API key 
client = initialize_inferenceclient()

# ------- initialize first system message --------#
if 'msg_history' not in st.session_state:
    st.session_state.msg_history = []
    system_message = """
    1. You are an AI assistant to a Ngee Ann Polytechnic lecturer.
    2. Prompt the user to upload the marking rubrics and student's report if it is not available in your system.
    """
    st.session_state.msg_history.append(
        {"role": "system", "content": f"{system_message}"}
    )



# ------- create side bar --------#
with st.sidebar:
    #st.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    st.subheader("PFB Research Report")
    model_id = st.selectbox(":grey[AI model]", 
                            model_list,
                            index=0,
                            help=model_help)
    
    upload_student_report = st.file_uploader(
        ":gray[Upload a research report (single file in .docx or .pdf)]", type=['docx', 'pdf'])
    
    st.markdown(
        f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)
    
    st.markdown(buymecoffee_btn_css, unsafe_allow_html=True)
    if st.button("☕ Buy me coffee"):
        buymecoffee()
    

# --- extract rubrics in pdf and add to session state---#
#if upload_mark_rubric is not None:
    
try:
    upload_mark_rubric = './data/research_marking_rubrics.pdf'
    mark_rubric = ""
    reader = PdfReader(upload_mark_rubric)
    for page in reader.pages:
        mark_rubric += page.extract_text()
    st.session_state.msg_history.append({
        "role": "system",
        "content": f"Use this marking rubrics to reference for assigning marks: {mark_rubric}"
    })
except Exception as e:
    st.error(f"Error processing marking rubrics: {e}")

# --- extract text in docs and add to session state---#
if upload_student_report is not None:
    
    if upload_student_report.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        try:
            doc = Document(upload_student_report)
            student_report = "\n".join([para.text for para in doc.paragraphs])
            st.sidebar.write(student_report)
            st.session_state.msg_history.append({
                "role": "system",
                "content": f"Mark this report: {student_report}"
            })
        except Exception as e:
            st.error(f"Error processing student report in docx format: {e}")
            

    
    elif upload_student_report.type == 'application/pdf':
        try:
            student_report = ""
            reader = PdfReader(upload_student_report)
            for page in reader.pages:
                student_report += page.extract_text()
            #st.write(student_report)
            st.session_state.msg_history.append({
                "role": "system",
                "content": f"Mark this report: {student_report}"
            })
        except Exception as e:
            st.error(f"Error processing student report: {e}")

# ------- if evaluate button click, set mark task to system --------#
#if evaluate_btn:
    try:
        system_message = """
        1. Your primary task is to evaluate students' written assignments based on a structured marking rubric.  
        2. Follow the instructions to mark:
            - Refer to the provided marking rubric to ensure accurate grading.
            - Assess each criterion separately, assigning marks accordingly.  
            - Do not assign more than the maximum mark in each marking criterion.
            - Provide a detail feedback for by identifying specific strengths and weaknesses of the report, offering constructive criticism on areas needing improvement. 
            - Provide reasons on the marks given for each criterion.
            - Tally the marks in each criterion.
            - Return the output with the areas, mark, feedback in a table.
            - Return the total mark and an overall feedback in strings.    
        """
        st.session_state.msg_history.append({
            "role": "system", "content": f"{system_message}"
        })

        st.session_state.msg_history.append({
            "role": "user", "content": f"Mark the report."
        })
        with st.empty():
            try:

                stream = client.chat.completions.create(
                model=model_id,
                messages=st.session_state.msg_history,
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
                        st.write(collected_response)

                del st.session_state.msg_history

            except Exception as e:
                st.error(e)
                
    except Exception as e:
        st.error(f"Error generating response: {e}")
    


