import streamlit as st
from huggingface_hub import InferenceClient
from research_report_utils import *
from pypdf import PdfReader
from streamlit_pdf_viewer import pdf_viewer
from docx import Document
from research_report_sys_msg import *

# ---------set css-------------#
st.markdown(btn_css, unsafe_allow_html=True)
st.markdown(image_css, unsafe_allow_html=True)

# --- Initialize the Inference Client with the API key ----#
try:
    client = InferenceClient(
        token=st.secrets.api_keys.huggingfacehub_api_token)
except Exception as e:
    st.error(f"Error initializing Inference Client: {e}")
    st.stop()


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

# ------- write chat conversations of session state --------#
for msg in st.session_state.msg_history:
    if msg['role'] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# ------- create side bar --------#
with st.sidebar:
    #st.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    st.subheader("PFB Research Report")
    #st.write(":gray[*Upload as a single report in .docx or .pdf*]")
    model_id = st.selectbox(":gray[Select an AI model]",
                            ["Qwen/Qwen2.5-72B-Instruct",
                             "meta-llama/Llama-3.3-70B-Instruct",
                             "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"],
                            index=1,
                            help=model_help)

   # upload_mark_rubric = st.file_uploader(
   #     ":blue[**Upload marking rubrics**]", 'pdf', help=rubrics_help)
    
    upload_student_report = st.file_uploader(
        ":gray[Upload a reseach report (single file in .docx or .pdf)]", type=['docx', 'pdf'])

    evaluate_btn = st.button(
        ":material/search_insights: Evaluate Report", type="primary")
    #clear_btn = st.button(":material/refresh: Clear History", type="primary")
    st.markdown(
        f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)

# --- extract rubrics in pdf and add to session state---#
#if upload_mark_rubric is not None:
    
try:
    upload_mark_rubric = './research_marking_rubrics.pdf'
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
button_pressed = ""

if evaluate_btn:
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

        button_pressed = "Mark the report."
    
    except Exception as e:
        st.error(f"Error during evaluation: {e}")

# ---- Input field for users to continue the conversation -----#
if user_input := (st.chat_input("How would you like to refine the report?") or button_pressed):

    st.session_state.msg_history.append(
        {"role": "user", "content": user_input})
    
    if not button_pressed:
        st.chat_message("user").write(user_input)
    
    try:
        with st.empty():
            stream = client.chat_completion(
                model=model_id,
                messages=st.session_state.msg_history,
                temperature=0.2,
                max_tokens=5524,
                top_p=0.7,
                stream=True,
            )
            collected_response = ""
            for chunk in stream:
                if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                    collected_response += chunk.choices[0].delta.content
                    st.chat_message("assistant").write(collected_response)
           
        del st.session_state.msg_history

    except Exception as e:
        st.error(f"Error generating response: {e}")
    


#if clear_btn:
#    try:
#        del st.session_state.msg_history
#        st.rerun()
#    except Exception as e:
#        st.error(f"Error clearing history: {e}")



