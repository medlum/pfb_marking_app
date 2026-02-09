#components/intern_learning_journal.py

import streamlit as st
from pypdf import PdfReader
from streamlit_pdf_viewer import pdf_viewer
from docx import Document
from intern_learning_journal_utils import *
import ast
from utils_twilio_coffee import buymecoffee_btn_css, buymecoffee
from utils_inference import initialize_inferenceclient, model_list
from utils_help_msg import *

# Initialize the Inference Client with the API key 
client = initialize_inferenceclient()

# ------- create side bar --------#
with st.sidebar:
    st.subheader("INT6 Learning Journal Assignment")
    model_id = st.selectbox(":grey[AI model]", 
                            model_list,
                            index=0,
                            help=model_help)
    
    pdf = './data/intern_learng_journey_rubrics.pdf'
    rubric = ""
    reader = PdfReader(pdf)
    for page in reader.pages:
        rubric += page.extract_text()
    group_zip = st.sidebar.file_uploader(":gray[Upload a zip file (by NPIS grouping level)]", type=['zip'], help='Zip file should contain students submission by NPIS grouping')
    st.write(":grey[Data is de-identified using UUIDs prior to AI analysis. These randomized identifiers ensure privacy during cloud processing, while original identities are restored locally only during the final reporting stage.]")
    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)
    
    st.markdown(buymecoffee_btn_css, unsafe_allow_html=True)
    if st.button("☕ Buy me coffee"):
        buymecoffee()


# --- extract text in docs and add to session state---#
if group_zip is not None:

    data = []
    # 1. Initialize a storage key at the top of your script (outside the loop)
    if "evaluation_results" not in st.session_state:
        st.session_state.evaluation_results = {}
    
    extracted_contents, sid_map = extract_and_read_files(group_zip) 

    for key in extracted_contents:

        if 'msg_history' not in st.session_state:
            st.session_state.msg_history = []

        st.session_state.msg_history.append({"role": "system", 
                                            "content": f"{system_message}"})
        
        st.session_state.msg_history.append({"role": "system", 
                                            "content": f"Here are the marking rubrics: {rubric}"})
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"Mark the following report for student identifier: {key}" })
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"{extracted_contents[key]}" })
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"Mark the report with high standard and be stringent when awarding marks." })
        

        st.subheader(f":blue[{key}]")


        if key not in st.session_state.evaluation_results:
            with st.spinner("Evaluating report..."):
                
                try:
                    # -------- use together API (NON-STREAMING) -------- #
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=st.session_state.msg_history,
                        temperature=0.2,
                        max_tokens=5524,
                        top_p=0.7,
                        stream=False,   # ✅ important
                    )

                    # 1️⃣ Get model output
                    collected_response = response.choices[0].message.content

                    # 2️⃣ Get token usage
                    usage = response.usage
                    print("Prompt tokens:", usage.prompt_tokens)
                    print("Completion tokens:", usage.completion_tokens)
                    print("Total tokens:", usage.total_tokens)

                    #cost= inference_cost(usage=usage, input_price=0.30, output_price=0.30)
                    #print(f"Inference Cost: ${cost:.6f}")

                except Exception as e:
                    st.error(f"Error generating response: {e}")

            try:
                actual_dict = ast.literal_eval(collected_response)
                data.append(actual_dict)

                feedback_raw = actual_dict.get("Feedback", "")
                report_text = extracted_contents[key][1]

                # 2. Apply highlighting
                #highlighted_content = highlight_original_sentences(report_body, feedback_str)
                highlighted_content = highlight_original_sentences(report_text, feedback_raw)

                # 2. Clean the feedback string for the summary (removes the edits here)
                clean_feedback = clean_feedback_text(feedback_raw)

                # 3. Display the expander with highlighted content
                with st.expander(f":grey[*Submitted report (Highlighted)*]"):
                    # Use unsafe_allow_html=True to render the <span> tags
                    st.markdown(highlighted_content, unsafe_allow_html=True)
                    # Generate the PDF
                    pdf_file = create_pdf_with_highlights(highlighted_content, key)
                    
                    if pdf_file:
                        st.download_button(
                            label="📥 Download Annotated PDF",
                            data=pdf_file,
                            file_name=f"Evaluation_{key}.pdf",
                            mime="application/pdf"
                        )                
                    
                # 4. Display the AI Feedback separately below it
                st.markdown("### AI Feedback")
                st.markdown(clean_feedback)

            except Exception as e:
                st.error(f"Error @ast.literal_eval(collected_response): {e}")
        
    
    
    del st.session_state.msg_history

    if data:
        st.subheader(f":orange[Marks Summary]")
        df = process_data(data, sid_map)
        st.dataframe(df)


