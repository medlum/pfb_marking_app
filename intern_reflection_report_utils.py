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
    #extract_folder = "extracted_files"
    extract_folder = st.session_state.user_id
    st.write("From intern_reflection_report_utils:", st.session_state.user_id)

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
                    data = "\n".join([para.text for para in doc.paragraphs])
                    print(data)
                    #data = [[cell.text for cell in row.cells] for table in doc.tables for row in table.rows]
                
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

#extracted_contents = extract_and_read_files('sample_int6.zip')
#for i in extracted_contents:
#    st.write(extracted_contents[i])

def process_data(data):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)

    # Sum the values in 'Program Correctness', 'Code Readability', 'Code Efficiency', 'Documentation', and 'Assignment Specifications'
    df['Total'] = df['Introduction (4 marks)'] + df['OJT Plan (6 marks)'] + df['Analysis and reflection on 3 experiences (Total 30 marks)'] + df[ 'Showcase of accomplished task/achievement (20 marks)'] + df['Diversity and Inclusion (10 marks)'] + df['Influence of internship on future plan (20 marks)'] + df['Quality of writing (10 marks)']

    
    cols = ['Student Name', 
            'Introduction (4 marks)', 
             'OJT Plan (6 marks)', 
            'Analysis and reflection on 3 experiences (Total 30 marks)', 
            'Showcase of accomplished task/achievement (20 marks)', 
            'Diversity and Inclusion (10 marks)',
            'Influence of internship on future plan (20 marks)',
            'Quality of writing (10 marks)',
            'Total', 
            'Feedback']

    return df[cols]

system_message = """
1. Your primary task is to evaluate students' written assignments based on a structured marking rubric.  
2. Follow the instructions to mark:
    - Refer closely to the provided marking rubric to ensure accurate and consistent grading.
    - Evaluate each criterion individually, assigning marks strictly according to the rubric.
    - Maintain a high academic standard throughout the assessment.
    - Do not exceed the maximum marks allocated for any criterion.
    - Provide detailed and constructive feedback, identifying specific strengths and weaknesses of the report.
    - Offer actionable suggestions for improvement in areas where the report falls short.
    - Highlight any sentences or sections that require revision or enhancement.
    - Justify the marks awarded for each criterion with clear, evidence-based reasoning.
    - Incorporate explanations of the mark allocation within the feedback for each criterion.
    - Return the marks and feedback in a dictionary : 
      {
          'Student Name': str,
          'Introduction (4 marks)': float,
          'OJT Plan (6 marks)': float,
          'Analysis and reflection on 3 experiences (Total 30 marks)': float,
          'Showcase of accomplished task/achievement (20 marks)': float,
          'Diversity and Inclusion (10 marks)': float,
          'Influence of internship on future plan (20 marks)': float,
          'Quality of writing (10 marks)': float,
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
