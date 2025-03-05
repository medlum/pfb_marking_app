
import streamlit as st
from pathlib import Path
import shutil
from group_utils import intro_var, app_usage_text
from twilio_utils import send_sms_txt, floating_button_css,floating_button_html


extracted_files_path = Path("./extracted_files")
extracted_pyfiles_path = Path("./extracted_pyfiles")

def find_user_credentials(user_id, password):
    users = st.secrets["users"]
    for user in users:
        if user['user_id'] == user_id and user['password'] == password:
            return True

    return None



def login():

    col1, col2, col3 = st.columns([1,1,1])
    col2.subheader(":orange[Assistive AI Marking Tool]", help=intro_var)
    user_id = col2.text_input(f":gray[User ID]")
    hf_access_token = col2.text_input(label=":gray[Access token]", 
                                      type='password',
                                      placeholder="optional")
    password = col2.text_input(":gray[Password]", type="password")
    col2.markdown(f'<span style="text-align: justify; font-size:12px; color:gray;">{app_usage_text}</span>', unsafe_allow_html=True)
    
    # buymecoffee button
    st.markdown(floating_button_css, unsafe_allow_html=True)
    st.markdown(floating_button_html, unsafe_allow_html=True)
    
    login_state = find_user_credentials(user_id, password)


    if login_state:
        with st.status("Logging in...", expanded=False):
            
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            col2.success(f"Successfully authenticated as: {user_id}")

            sms_txt = f"LOGIN ALERT: {st.session_state.user_id}."
            send_sms_txt(sms_txt)
            
            if hf_access_token :
                st.write('hf_access_token is not None')
                st.session_state.hf_access_token = hf_access_token     
            else: 

                st.session_state.hf_access_token = st.secrets.api_keys.huggingfacehub_api_token, 
                # st.session_state.hf_access_token contains a tuple -> (xxxx, )
            st.rerun()

def logout():

    sms_txt = f"LOGOUT ALERT: {st.session_state.user_id}."
    send_sms_txt(sms_txt)

    st.session_state.logged_in = False
    st.session_state.user_id = None

    if Path("./extracted_files").exists():
        shutil.rmtree('./extracted_files')

    if Path("./extracted_pyfiles").exists():
        shutil.rmtree('./extracted_pyfiles')

    st.session_state.clear()

    st.rerun()
