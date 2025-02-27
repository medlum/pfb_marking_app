import zipfile
from pathlib import Path
from charset_normalizer import from_path
import shutil
import subprocess
import os
import re
import pandas as pd
import streamlit as st
def extract_and_read_files(zip_path):
    # Define extraction path
    extract_folder = "extracted_pyfiles"

        # Clear previous data
    if Path(extract_folder).exists():
        shutil.rmtree(extract_folder)

    # Extract ZIP file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)

    extracted_data = {}

    for folder in Path(extract_folder).iterdir(): 

        if folder.is_dir():  

            # extract student name from the each subfolder
            # which contains name as standard label from brightspace 
            folder_name = str(folder.relative_to(extract_folder))
            cleaned_text = re.sub(r"\b(BA|NP|PM)\b", "", folder_name)
            cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
            student_name = " ".join(re.findall(r"\b[A-Z]+\b", cleaned_text))
            
            shutil.copy('SpaceUsage.csv', folder)

            for py_file in folder.glob("*.py"):  
                
                try:
                    result = from_path(py_file)
                    encoding = result.best().encoding if result.best() else "utf-8"
                    with open(py_file, "r", encoding=encoding) as f:
                        student_report = f.read()

                except Exception:
                    encoding = "utf-8"  # Fallback

                if folder_name not in extracted_data:
                    extracted_data[folder_name] = {}

                extracted_data[folder_name]["student name"] = student_name
                extracted_data[folder_name]["python file"] = student_report

                original_cwd = os.getcwd()  

                try:
                    main_error_flag = False
                    os.chdir(py_file.parent)
                    subprocess.run(['python3', py_file.name], check=True)
                
                except Exception as e:
                    st.error(f"*Error with {py_file.name} for {student_name}*.")
                    main_error_flag = True
                
                finally:
                #  Change back to the original working directory
                   os.chdir(original_cwd)

            if not main_error_flag:
                for file in folder.glob("*.txt"):
                    if 'summary' in file.stem.lower():
                        #print(f"summary-related file found: {file}")
                        with open(file, "r", encoding="utf-8") as f:
                            extracted_data[folder_name]["summary"] = f.read()
                #else:
                #    st.warning(f"Unable to generate summary reports to due error with {py_file.name} for {student_name} , check source code")
    return extracted_data
         
#
#extracted_contents = extract_and_read_files('PFB Individual Project Sample.zip')

#for folder, contents in extracted_contents.items():
#    #if contents["student name"]:
#
#    print(f"Mark this assignment for student name:\n{contents["student name"]}.")
#    print(f"This is the submitted python code:\n{contents["python file"]}")    
#    print(f"This is output generated from the python code:\n{contents['summary']}")   



def process_data(data):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)

    # Sum the values in the second and third columns, and store the result in 'Program Correctness'
    df['Program Correctness'] = df['Output for Efficient Transit Payment Summary'] + df['Output for Top 5 of 20 SKUs']
    # Sum the values in 'Program Correctness', 'Code Readability', 'Code Efficiency', 'Documentation', and 'Assignment Specifications'
    df['Total'] = df['Program Correctness'] + df['Code Readability'] + df['Code Efficiency'] + df['Documentation'] + df['Assignment Specifications']

    
    cols = ['Student Name', 
            'Program Correctness', 
            'Code Readability', 
            'Code Efficiency', 
            'Documentation', 
            'Assignment Specifications', 
            'Total', 
            'Feedback']

    return df[cols]


# custom CSS for buttons
btn_css = """
<style>
    .stButton > button {
        color: #383736; 
        border: none; /* No border */
        padding: 5px 22px; /* Reduced top and bottom padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block */
        font-size: 8px !important;
        margin: 4px 2px; /* Some margin */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 30px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background transition */
    }
    .stButton > button:hover {
        color: #383736; 
        background-color: #c4c2c0; /* Darker green on hover */
    }
</style>
"""

image_css = """
<style>
.stImage img {
    border-radius: 50%;
    #border: 5px solid #f8fae6;
}
</style>

"""


model_help = ":blue[Models with less parameters have faster inference speed but often at the expense of a more quality answer.]"

rubrics_help = ":blue[Upload a set of marking rubrics with a **criterion** column in PDF.]"

report_help =":blue[Report with more than 3,000 words may experience '*max limit token error*'. Click on **Clear History** and try again.]"

eval_btn_help = ":blue[Click to evaluate the internship report]"

intro_var = """
:blue[While AI marking can help with consistency and efficiency, it's crucial to review and verify the marks and feedback generated.]
"""

disclaimer_var = "Disclaimer: This AI-powered tool is designed to assist in marking reports by providing helpful suggestions and evaluations. However, it may occasionally make errors or misinterpret content. Final judgment and accuracy should be verified by a qualified evaluator."

creator_var = "Andy Oh is the creator behind this AI-powered tool, designed to transform how educators manage their workload by introducing an innovative solution to streamline their tasks." 

summary_report_var = "Use it as a reference source when evaluating the summary report generated by students."

upload_help = "Ensure it is a class level zip file from BrightSpace"