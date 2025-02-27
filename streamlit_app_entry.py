import pathlib
import io
import requests
import streamlit as st
from pathlib import Path
import shutil

extracted_files_path = Path("./extracted_files")
extracted_pyfiles_path = Path("./extracted_pyfiles")
import streamlit as st


def find_user_credentials(user_id, password):
    users = st.secrets["users"]
    for user in users:
        if user['user_id'] == user_id and user['password'] == password:
            return True

    return None

def login():
    user_id = st.text_input(f":blue[User ID]")
    password = st.text_input(":blue[Password]", type="password")
    login_state = find_user_credentials(user_id, password)
    if login_state:
        with st.status("Logging in...", expanded=False):
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.success(f"Successfully authenticated as: {user_id}")
            st.rerun()


def logout():

    st.session_state.logged_in = False

    st.session_state.user_id = None

    if Path("./extracted_files").exists():
        shutil.rmtree('./extracted_files')

    if Path("./extracted_pyfiles").exists():
        shutil.rmtree('./extracted_pyfiles')

    st.session_state.clear()

    st.rerun()
