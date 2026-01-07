import streamlit as st
from utils_entry import *


# Configure the Streamlit app with a title, layout, icon, and initial sidebar state
st.set_page_config(page_title="Marking App",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Initialize session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "access_token" not in st.session_state:
    st.session_state.access_token = None


# Handle navigation

# set up nav page (login is located utils_entry_pt.py)

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out (to delete data)", icon=":material/logout:")

pfb_group_project = st.Page("components/pfb_group_project.py", 
                   title="PFB Group Project ( Python Code )", 
                   icon=":material/terminal:", 
                   default=True)

pfb_research_report = st.Page("components/pfb_research_report.py", 
                   title="PFB Group Project ( Research Report )", 
                   icon=":material/description:")

pfb_drones_individual_assignment = st.Page("components/pfb_drones_individual_assignment.py", 
                   title="PFB Individual Assignment ( DeliveryMax )", 
                   icon=":material/code_blocks:")

# pfb_individual_assignment = st.Page("components/pfb_individual_assignment.py", 
#                    title="PFB Individual Assignment ( SKU )", 
#                    icon=":material/code_blocks:")


intern_learning_journal = st.Page("components/intern_learning_journal.py", 
                   title="INT6 Learning Journal Assignment", 
                   icon=":material/draft:")

intern_reflection_report = st.Page("components/intern_reflection_report.py", 
                   title="INT6 Reflection Report", 
                   icon=":material/article:")


if st.session_state.logged_in:

    st.sidebar.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    #st.sidebar.text_input("Enter huggingface token")

    if st.session_state.user_id in ("zengxing" ,"charles", "lester", "andy"): 

        pg = st.navigation(
            {   
                "Marking Components": [pfb_group_project,
                                    pfb_research_report, 
                                    pfb_drones_individual_assignment,
                                    #pfb_individual_assignment, 
                                    intern_learning_journal,
                                    intern_reflection_report],
                                    
                "Account": [logout_page],

            }
        )

    else:
          pg = st.navigation(
            {   
                "Marking Components": [intern_learning_journal,
                                    intern_reflection_report],
                                    
                "Account": [logout_page],
            }
        )


else:
    pg = st.navigation([login_page])

pg.run()

