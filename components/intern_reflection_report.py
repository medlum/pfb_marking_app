import streamlit as st
from huggingface_hub import InferenceClient
from pypdf import PdfReader
from streamlit_pdf_viewer import pdf_viewer
from docx import Document
from intern_reflection_report_utils import *
import ast
from utils_twilio_coffee import buymecoffee_btn_css, buymecoffee
from utils_inference import initialize_inferenceclient, model_list
from utils_help_msg import *
# ---------set css-------------#
#st.markdown(btn_css, unsafe_allow_html=True)

# --- Initialize the Inference Client with the API key ----#
client = initialize_inferenceclient()
    

# ------- create side bar --------#
with st.sidebar:
    #st.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    st.subheader("INT6 Reflection Report")
    #st.write(":gray[*(Upload by group by NPIS as a zip file)*]")

    model_id = st.selectbox(":grey[AI model]", 
                        model_list,
                        index=0,
                        help=model_help)
    
    pdf = './data/intern_reflection_report_rubrics.pdf'
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
                                            "content": f"{extracted_contents[key][1]}" })
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"Mark the report with high standard and be stringent when awarding marks." })
        

        st.subheader(f":blue[{key}]")

        with st.expander(f":grey[*Submitted report*]"):
            
            st.write(extracted_contents[key][1])

        #-------- use together API ------#
        with st.status("Evaluating report...", expanded=True) as status:
            
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
                    collected_response += chunk.choices[0].delta.content
                
                # display in json
                st.json(collected_response)

            except Exception as e:
                st.error(f"Error generating response: {e}")

            try:
                actual_dict = ast.literal_eval(collected_response)
                data.append(actual_dict)

            except Exception as e:
                st.error(f"Error @ast.literal_eval(collected_response): {e}")
            
        status.update(label="Report evaluation completed...", state="complete", expanded=True)

        #-------- use hugging face API ------#
        #if evaluate_btn:
#        try:
#            with st.status("Evaluating report...", expanded=True) as status:
#
#                with st.empty():
#
#                    try:
#                        stream = client.chat_completion(
#                            model=model_id,
#                            messages=st.session_state.msg_history,
#                            temperature=0.2,
#                            max_tokens=5524,
#                            top_p=0.7,
#                            stream=True
#                            )
#                        
#                        collected_response = ""
#                        
#                        for chunk in stream:
#                            if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
#                                collected_response += chunk.choices[0].delta.content
#                                st.text(collected_response.replace('{','').replace('}','').replace("'",""))
#                        
#                        actual_dict = ast.literal_eval(collected_response)
#                        data.append(actual_dict)
#                        status.update(label="Report evaluation completed...", state="complete", expanded=False)
#                    
#                    except Exception as e:
#                        st.error(e)
#
#        except Exception as e:
#            st.error(f"Error generating response: {e}")
        
        del st.session_state.msg_history

    if data:
        st.subheader(f":orange[Marks Summary]")
        df = process_data(data)
        st.dataframe(df)



