import zipfile
from pathlib import Path
import shutil
import re
import pandas as pd
import streamlit as st
from docx import Document
from pypdf import PdfReader

def extract_and_read_files(zip_path):
    # Define extraction path
    extract_folder = "extracted_files"

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
            cleaned_text = re.sub(r"\b(BA|NP|PM|AM)\b", "", folder_name)
            cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
            student_name = " ".join(re.findall(r"\b[A-Z]+\b", cleaned_text))

            
            for file in folder.glob("*.*"):

                if file.suffix.lower() == ".docx":
                    doc = Document(file)
                    #data = "\n".join([para.text for para in doc.paragraphs])
                    data = [[cell.text for cell in row.cells] for table in doc.tables for row in table.rows]
                
                elif file.suffix.lower() == ".pdf":
                    data = ""
                    reader = PdfReader(file)
                    for page in reader.pages:
                        data += page.extract_text()

                else:
                    st.error(".docx or .pdf files not found")
            
                if student_name not in extracted_data:
                    # store values as a list with file extension and extracted data
                    extracted_data[student_name] = [file.suffix.lower(), data]
    
    return extracted_data


def process_data(data):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)

    # Sum the values in 'Program Correctness', 'Code Readability', 'Code Efficiency', 'Documentation', and 'Assignment Specifications'
    df['Total'] = df['Review and update progress on the OJT plan (10 marks)'] + df['Progress on achieving personal and professional goals (15 marks)'] + df['Reflection on skills acquired (Total: 60 marks)'] + df[ 'Quality of writing (15 marks)'] 

    
    cols = ['Student Name', 
            'Review and update progress on the OJT plan (10 marks)', 
            'Progress on achieving personal and professional goals (15 marks)', 
            'Reflection on skills acquired (Total: 60 marks)', 
            'Quality of writing (15 marks)', 
            'Total', 
            'Feedback']

    return df[cols]

system_message = """
1. Your primary task is to evaluate students' written assignments based on a structured marking rubric.  
2. Follow the instructions to mark:
    - Refer to the provided marking rubric to ensure accurate grading.
    - Assess each criterion separately, assigning marks accordingly.  
    - Do not assign more than the maximum mark in each marking criterion.
    - Provide a detail feedback for by identifying specific strengths and weaknesses of the report, offering constructive criticism on areas needing improvement. 
    - Provide reasons on the marks given for each criterion.
    - Tally the marks in each criterion.
    - Comment on why the marks are given for each criteria as part of the feedback.
    - Return the marks and feedback in a dictionary : 
      {
          'Student Name': str,
          'Review and update progress on the OJT plan (10 marks)': float,
          'Progress on achieving personal and professional goals (15 marks)': float,
          'Reflection on skills acquired (Total: 60 marks)': float,
          'Quality of writing (15 marks)': float
          'Feedback' : str
      
      }  
    - Use single quotation '' for strings in the dictionary.
    - Your answer should only contain the returned dictionary and nothing else. 
"""


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

intro_var = """
:blue[While AI marking can help with consistency and efficiency, it's crucial to review and verify the marks and feedback generated.]
"""

disclaimer_var = "Disclaimer: This AI-powered tool is designed to assist in marking reports by providing helpful suggestions and evaluations. However, it may occasionally make errors or misinterpret content. Final judgment and accuracy should be verified by a qualified evaluator."


model_help = ":blue[Models with less parameters have faster inference speed but often at the expense of a more quality answer.]"

rubrics_help = ":blue[Upload a set of marking rubrics with a **criterion** column in PDF.]"

report_help =":blue[Report with more than 3,000 words may experience '*max limit token error*'. Click on **Clear History** and try again.]"
