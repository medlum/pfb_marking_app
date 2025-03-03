import streamlit as st
from streamlit_app_entry import *

# Configure the Streamlit app with a title, layout, icon, and initial sidebar state
st.set_page_config(page_title="PFB Marking App",
                   layout="wide",
                   initial_sidebar_state="expanded")
# Initialize session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# set up nav page (login is located utils_entry_pt.py)

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

group_project = st.Page("components/group_project.py", 
                   title="PFB Group Project -  Python code", 
                   icon=":material/terminal:", 
                   default=True)

individual_assignment = st.Page("components/individual_assignment.py", 
                   title="PFB Individual Assignment", 
                   icon=":material/code_blocks:")

research_report = st.Page("components/research_report.py", 
                   title="PFB Group Project - Research report", 
                   icon=":material/description:")

intern_learning_journal = st.Page("components/intern_learning_journal.py", 
                   title="INT6 Learning Journal Assignment", 
                   icon=":material/description:")

intern_reflection_report = st.Page("components/intern_reflection_report.py", 
                   title="INT6 Reflection Report", 
                   icon=":material/description:")



if st.session_state.logged_in:
    
    st.sidebar.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    #st.sidebar.text_input("Enter huggingface token")

    pg = st.navigation(
        {   
            "Marking Components": [group_project, research_report, 
                                   individual_assignment, 
                                   intern_learning_journal,
                                   intern_reflection_report],
                                   
            "Account": [logout_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()

