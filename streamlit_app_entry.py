import pathlib
import io
import requests
import streamlit as st
from pathlib import Path
import shutil
from group_utils import intro_var

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
    password = col2.text_input(":gray[Password]", type="password")
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
