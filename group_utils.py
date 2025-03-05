import zipfile
import os
import subprocess
from pathlib import Path
import shutil
import csv
from group_data import *
from charset_normalizer import from_path
import streamlit as st
import pandas as pd


def is_valid_zip(zip_path):
    """Checks if a file is a valid ZIP archive."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            return zip_file.testzip() is None
    except zipfile.BadZipFile:
        return False

def extract_zip_file(zip_path, extract_folder):
    """Extracts a single ZIP file to a specified folder."""
    if is_valid_zip(zip_path):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)
    else:
        print("Invalid ZIP file.")

def extract_and_read_files(main_zip_path):
    extract_folder = "extracted_files"
    
    # Clear previous extractions
    if Path(extract_folder).exists():
        shutil.rmtree(extract_folder)
    
    # Extract main ZIP file
    extract_zip_file(main_zip_path, extract_folder)
    
    # Process extracted contents
    extracted_data = {}
    for folder in Path(extract_folder).iterdir():  
        
        if folder.is_dir():  
            folder_name = str(folder.relative_to(extract_folder))
            extracted_data[folder_name] = {"team_members": None, "python_files": [], 'summary': []}

            for txt_file in folder.glob("*.txt"):  
                if "team" in txt_file.stem.lower() or "member" in txt_file.stem.lower():
                    print(f"team-related file found: {txt_file}")
            
                    # Process team members
                    #team_members_file = folder / txt_file
                    #if txt_file.exists():
                    with open(txt_file, "r", encoding="utf-8") as f:
                        extracted_data[folder_name]["team_members"] = f.read()
            
            # Locate Python files
            for py_file in folder.glob("*.py"):  
                try:
                    result = from_path(py_file)
                    encoding = result.best().encoding if result.best() else "utf-8"
                except Exception:
                    encoding = "utf-8"  # Fallback
                
                try:
                    with open(py_file, "r", encoding=encoding, errors="replace") as f:
                        extracted_data[folder_name]["python_files"].append((py_file.name, f.read()))
                except Exception as e:
                    print(f"Error reading {py_file.name}: {e}")
            
            # Locate main.py 
            for subfolder in folder.glob("main.py"):
                # if main.py
                if subfolder.name:
                    for key in all_data_dict:
                        # Part 1
                        # locate folder contain the word 'csv' 
                        # then locate the csv files in the folder
                        # to overwrite it with test data 
                        for folder in subfolder.parent.iterdir():
                            if folder.is_dir() and "csv" in folder.name.lower():
                                print(f"CSV-related folder found: {folder}")
                                csv_reports_folder = subfolder.parent / folder.name
                                #for file in folder.iterdir():
                                #    print(f" - {file}")
                                
                
                        if csv_reports_folder.exists():
                            #print(f"CSV reports folder found: {csv_reports_folder}")
                            for csv_file in csv_reports_folder.glob("*.csv"):
                            
                                if 'cash' in csv_file.stem.lower():
                                    with open(csv_file, 'w', newline='') as file:
                                        writer = csv.writer(file)
                                        test_data = all_data_dict[key][0] #coh
                                        writer.writerows(test_data)

                                if 'profit' in csv_file.stem.lower():
                                    with open(csv_file, 'w', newline='') as file:
                                        writer = csv.writer(file)
                                        test_data = all_data_dict[key][1] #pnl
                                        writer.writerows(test_data)

                                if 'overhead' in csv_file.stem.lower():
                                    with open(csv_file, 'w', newline='') as file:
                                        writer = csv.writer(file)
                                        test_data = all_data_dict[key][2] #overheads
                                        writer.writerows(test_data)
                        
                        else:
                            print(f"CSV reports folder not found in {os.getcwd()}.")
                            #extracted_data[folder_name]["summary"] = f"CSV reports folder not found in {os.getcwd()}."

                        # Part 2: Then execute main.py which will 
                        # read csv files that contain test data
                        # and write to summary_report.txt
                        original_cwd = os.getcwd()  
                        try:
                            main_error_flag = False
                            # Change the working directory to the folder containing main.py
                            os.chdir(subfolder.parent)
                            # Run the main.py script
                            subprocess.run(['python3', subfolder.name], check=True)
                        except Exception as e:
                            #st.error(f"Error running: {subfolder.parent}: {e}")
                            st.error(main_py_error)
                            main_error_flag = True
                            #extracted_data[folder_name]["summary"].append(f"Error running {subfolder.name}: {e}"
                        finally:
                            # Change back to the original working directory
                            os.chdir(original_cwd)

                        # Part 3: Find the summary.txt after main.py is executed
                        # Need to use this summary to check against correct output
                        if not main_error_flag:
                            for file in subfolder.parent.glob("*.txt"):
                                if 'summary' in file.stem.lower():
                                    with open(file, "r", encoding="utf-8") as f:
                                        extracted_data[folder_name]["summary"].append((key,f.read()))
                                    #print(f.read())
                        else:
                            st.warning("Unable to generate summary reports")
                else: 
                    for file in subfolder.parent.glob("*.txt"):
                        if 'summary' in file.stem.lower():
                            with open(file, "r", encoding="utf-8") as f:
                                extracted_data[folder_name]["summary"].append("MAIN.PY NOT FOUND")
    return extracted_data



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

zip_help = ":blue[Upload a zip file by project group.]"

intro_var = """
:blue[While AI marking can help with consistency and efficiency, it's crucial to review and verify the marks and feedback generated.]
"""

disclaimer_var = "Disclaimer: This AI-powered tool is designed to assist in marking reports by providing helpful suggestions and evaluations. However, it may occasionally make errors or misinterpret content. Final judgment and accuracy should be verified by a qualified evaluator."

creator_var = "Andy Oh is the creator behind this AI-powered tool, designed to transform how educators manage their workload by introducing an innovative solution to streamline their tasks." 

summary_report_var = "Use it as a reference source when evaluating the summary report generated by students."

main_py_error = ":red[*Error running 'main.py'. It could be missing python files or code errors like IndexError during the program execution using our test data*]."

app_usage_text = """

This app is free to use, but permission is required before access. 
Upon approval, you will receive a User ID and Password. 
To request access, please email: andy_oh18@yahoo.com.\n

This app relies on HuggingFace endpoint API for model inference. 
By default, users will utilize the developer's access token. 
However, frequent usage may hit token limits, impacting performance and availability.
For a more reliable experience, we recommend subscribing to a Hugging Face Pro account for $9 per month and generating your own access token. 
You can start, cancel, and resume your subscription anytime.
Once you have your access token, enter it in the access token field to proceed.

Learn more: https://huggingface.co
"""