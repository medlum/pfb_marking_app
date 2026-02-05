#components/intern_learning_journal.py

import streamlit as st
from pypdf import PdfReader
from streamlit_pdf_viewer import pdf_viewer
from docx import Document
from intern_learning_journal_utils import *
import ast
import json
from utils_twilio_coffee import buymecoffee_btn_css, buymecoffee
from utils_inference import initialize_inferenceclient, model_list
from utils_help_msg import *


# ---------set css-------------#
#st.markdown(btn_css, unsafe_allow_html=True)
#st.markdown(image_css, unsafe_allow_html=True)

# Initialize the Inference Client with the API key 
client = initialize_inferenceclient()

# ------- create side bar --------#
with st.sidebar:
    #st.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    st.subheader("INT6 Learning Journal Assignment")
    #st.write(":gray[*(Upload by group by NPIS as a zip file)*]")

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
    #evaluate_btn = st.sidebar.button(":material/search_insights: Evaluate Report", type="primary")
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

    extracted_contents = extract_and_read_files(group_zip)

    for key in extracted_contents:

        if 'msg_history' not in st.session_state:
            st.session_state.msg_history = []

        st.session_state.msg_history.append({"role": "system", 
                                            "content": f"{system_message}"})
        
        st.session_state.msg_history.append({"role": "system", 
                                            "content": f"Here are the marking rubrics: {rubric}"})
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"Mark the following report for student name: {key}" })
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"{extracted_contents[key]}" })
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"Mark the report with high standard and be stringent when awarding marks." })
        

        st.subheader(f":blue[{key}]")

#        with st.expander(f":grey[*Submitted report*]"):
#            
#            # [0] refers to suffix from [file.suffix.lower(), data]
#            if extracted_contents[key][0] == '.docx':
#                # [1] refers to data from [file.suffix.lower(), data]
#                st.markdown(extracted_contents[key][1], unsafe_allow_html=True)
#               
#                # [3:10] is the location of where the title and main text of the report
#                # the other index position does not have meaningful full texts.
#                #for i in extracted_contents[key][1][3:10]:
#                #    # why?
#                #    if len(i) == 2:
#                #        st.write(f"{i[0]}: {i[1]}")
#                #    else:
#                #        st.write(f"{i[0]}")
#
#
#            elif extracted_contents[key][0] == '.pdf':
#                st.write(extracted_contents[key][1])

        #if evaluate_btn:
        #try:
            
        #with st.status("Evaluating report...", expanded=False) as status:
        if key not in st.session_state.evaluation_results:
            with st.spinner("Evaluating report..."):
                
                try:
                #-------- use together API ------#
                    #placeholder = st.empty()
                    stream = client.chat.completions.create(
                        model=model_id,
                        messages=st.session_state.msg_history,
                        temperature=0.2,
                        max_tokens=5524,
                        top_p=0.7,
                        stream=True,
                        )
                
                    collected_response = ""

                    #for chunk in stream:
                    #    collected_response += chunk.choices[0].delta.content
                    #    placeholder.text(collected_response.replace("{", " ").replace("}", " "))

                    for chunk in stream:
                        if not chunk.choices: continue

                        delta = chunk.choices[0].delta

                        if hasattr(delta, "content") and delta.content:
                            collected_response += delta.content
                            #placeholder.text(
                            #    collected_response.replace("{", " ").replace("}", " ")
                            #    )
                    #status.update(label="Report evaluation completed...", state="complete", expanded=True)


                    
                    # display response
                    #st.write(dict(collected_response))
                    #print(collected_response)

                

                except Exception as e:
                    st.error(f"Error generating response: {e}")

            try:
                actual_dict = ast.literal_eval(collected_response)
                data.append(actual_dict)

                # 1. Get the raw feedback and the original report text
                #feedback_str = actual_dict.get("Feedback", "")
                #report_format = extracted_contents[key][0]
                #report_body = extracted_contents[key][1]

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
        df = process_data(data)
        st.dataframe(df)


