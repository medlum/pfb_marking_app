import streamlit as st
from huggingface_hub import InferenceClient
from pypdf import PdfReader
from streamlit_pdf_viewer import pdf_viewer
from docx import Document
#from intern_learning_journal_sys_msg import *
from intern_learning_journal_utils import *
import ast
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


# ------- create side bar --------#
with st.sidebar:
    #st.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    st.subheader("INT6 Learning Journal Assignment")
    #st.write(":gray[*(Upload by group by NPIS as a zip file)*]")

    model_id = st.selectbox(":gray[Select an AI model]",
                            ["Qwen/Qwen2.5-72B-Instruct",
                             "meta-llama/Llama-3.3-70B-Instruct",
                             "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"],
                            index=1,
                            help=model_help)
    
    pdf = './intern_learng_journey_rubrics.pdf'
    rubric = ""
    reader = PdfReader(pdf)
    for page in reader.pages:
        rubric += page.extract_text()
    
    group_zip = st.sidebar.file_uploader(":gray[Upload a zip file (by NPIS grouping level)]", type=['zip'], help='Zip file should contain students submission by NPIS grouping')

    evaluate_btn = st.sidebar.button(":material/search_insights: Evaluate Report", type="primary")
    
    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)
    

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
                                            "content": f"{extracted_contents[key]}" })
        

        st.subheader(f":blue[{key}]")

        with st.expander(f":grey[*Submitted report*]"):
            
            # [0] refers to suffix from [file.suffix.lower(), data]
            if extracted_contents[key][0] == '.docx':
                # [1] refers to data from [file.suffix.lower(), data]
                # [3:10] is the location of where the title and main text of the report
                # the other index position does not have meaningful full texts.
                for i in extracted_contents[key][1][3:10]:
                    # why?
                    if len(i) == 2:
                        st.write(f"{i[0]}: {i[1]}")
                    else:
                        st.write(f"{i[0]}")

            elif extracted_contents[key][0] == '.pdf':
                st.write(extracted_contents[key][1])

        if evaluate_btn:
            try:
                with st.status("Evaluating report...", expanded=True) as status:
                    with st.empty():
                        stream = client.chat_completion(
                            model=model_id,
                            messages=st.session_state.msg_history,
                            temperature=0.6,
                            max_tokens=5524,
                            top_p=0.7,
                            stream=True
                            )
                        collected_response = ""
                        for chunk in stream:
                            if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                                collected_response += chunk.choices[0].delta.content
                                st.text(collected_response.replace('{','').replace('}','').replace("'",""))
                        
                        actual_dict = ast.literal_eval(collected_response)
                        data.append(actual_dict)
                    
                        status.update(label="Report evaluation completed...", state="complete", expanded=False)
            
            except Exception as e:
                st.error(f"Error generating response: {e}")
            
            del st.session_state.msg_history

    if data:
        st.subheader(f":orange[Marks Summary]")
        df = process_data(data)
        st.dataframe(df)

            