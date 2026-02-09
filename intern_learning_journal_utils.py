#intern_learning_journal_utils.py
import zipfile
from pathlib import Path
import shutil
import re
import pandas as pd
import streamlit as st
from docx import Document
from pypdf import PdfReader
import mammoth
from xhtml2pdf import pisa
import io
import uuid


def inference_cost(usage, input_price, output_price):
    """
    usage: response.usage from Together SDK
    prices: USD per 1M tokens
    """
    input_cost = usage.prompt_tokens / 1_000_000 * input_price
    output_cost = usage.completion_tokens / 1_000_000 * output_price
    return input_cost + output_cost



STUDENT_ID_PATTERN = re.compile(r"\b[A-Za-z]\d{8}[A-Za-z]\b")

def generate_sid():
    return f"SID_{uuid.uuid4().hex[:8]}"


def deidentify_text(text, student_name, sid, sid_map):
    """
    Replace student name and student ID with SID (case-insensitive for name)
    """

    # --- Case-insensitive replacement for student name ---
    if student_name:
        name_pattern = re.compile(re.escape(student_name), re.IGNORECASE)
        text = name_pattern.sub(sid, text)

    # --- Replace student IDs by pattern ---
    matches = STUDENT_ID_PATTERN.findall(text)

    for student_id in matches:
        sid_map[sid]["student_id"] = student_id
        text = text.replace(student_id, sid)

    print(f"{student_name} ({''.join(matches)}) : {sid}")

    return text

def create_pdf_with_highlights(highlighted_html, student_name):
    # Create a wrapper with some CSS for the PDF
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333; }}
            .header {{ text-align: center; color: #4a4a4a; border-bottom: 1px solid #ccc; padding-bottom: 10px; }}
            /* Ensure our suggestion boxes look good in the PDF */
            .annotation-box {{ 
                border-left: 3px solid #ffa500; 
                padding: 10px; 
                margin: 15px 0; 
                background-color: #fff9e6; 
            }}
            .original {{ background-color: yellow; font-weight: bold; }}
            .suggestion {{ color: #2e7d32; font-style: italic; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Internship Learning Journal Evaluation</h1>
            <p><strong>Student:</strong> {student_name}</p>
        </div>
        <div class="content">
            {highlighted_html}
        </div>
    </body>
    </html>
    """
    
    result = io.BytesIO()
    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=result)
    
    if pisa_status.err:
        return None
    
    result.seek(0)
    return result

def clean_feedback_text(feedback_text):
    """
    Removes the Original/Suggestion blocks from the feedback text
    so the summary remains high-level.
    """
    import re
    
    # This pattern matches 'Original: "..."', 'Suggestion: "..."', 
    # and any whitespace/newlines immediately following them.
    pattern = r'Original:\s*["“].*?["”]\s*Suggestion:\s*["“].*?["”]\s*'
    
    # re.DOTALL ensures it catches everything even if spread across lines
    cleaned_text = re.sub(pattern, "", feedback_text, flags=re.DOTALL)
    
    # Optional: Clean up triple newlines that might be left over
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text).strip()
    
    return cleaned_text

def highlight_original_sentences(report_text, feedback_text):
    """
    Finds pairs of Original/Suggestion in feedback and embeds 
    the suggestion directly into the report text.
    """
    import re
    
    # Regex to find the pair: Original: "..." followed by Suggestion: "..."
    # This handles standard (") and curly (“ ”) quotes
    pattern = r'Original:\s*["“](.*?)["”].*?Suggestion:\s*["“](.*?)["”]'
    
    # finditer lets us loop through all matches found in the feedback
    matches = re.finditer(pattern, feedback_text, re.DOTALL)
    
    highlighted_report = report_text
    
    for match in matches:
        original = match.group(1).strip()
        suggestion = match.group(2).strip()
        
        if original in highlighted_report:
            # Create a 'callout' style HTML block
            # The original is highlighted yellow, suggestion is in green italics below it
            annotation_html = f"""
            <div style="border-left: 3px solid #ffa500; padding-left: 10px; margin: 10px 0; background-color: #fff9e6; border-radius: 5px;">
                <span style="background-color: #ffff00; color: black; font-weight: bold;">{original}</span><br>
                <span style="color: #2e7d32; font-size: 0.85rem; font-style: italic;">
                    <strong>💡 Suggestion:</strong> {suggestion}
                </span>
            </div>
            """
            # Replace the plain text with our new HTML block
            highlighted_report = highlighted_report.replace(original, annotation_html)
            
    return highlighted_report

def extract_and_read_files(zip_path):
    extract_folder = st.session_state.user_id

    if Path(extract_folder).exists():
        shutil.rmtree(extract_folder)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    extracted_data = {}
    sid_map = {}

    for folder in Path(extract_folder).iterdir():
        if not folder.is_dir():
            continue

        # --- Extract student name from folder ---
        folder_name = str(folder.relative_to(extract_folder))
        cleaned_text = re.sub(r"\b(BA|NP|PM|AM)\b", "", folder_name)
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
        student_name = " ".join(re.findall(r"\b[A-Z]+\b", cleaned_text))

        sid = generate_sid()
        sid_map[sid] = {"student_name": student_name, "student_id": None}

        for file in folder.glob("*.*"):
            if file.suffix.lower() == ".docx":

                def ignore_images(image):
                    return {}

                result = mammoth.convert_to_html(file, convert_image=ignore_images)
                data = result.value

            elif file.suffix.lower() == ".pdf":
                data = ""
                reader = PdfReader(file)
                for page in reader.pages:
                    data += page.extract_text()

            else:
                continue

            # 🔐 De-identify content
            data = deidentify_text(data, student_name, sid, sid_map)

            extracted_data[sid] = [file.suffix.lower(), data]

    return extracted_data, sid_map


def process_data(data, sid_map):
    df = pd.DataFrame(data)

    # --- Add SID as first column ---
    df.insert(0, "SID", df["Student Name"])

    # --- Re-identify + normalize name ---
    df["Student Name"] = (
        df["Student Name"]
        .map(lambda sid: sid_map.get(sid, {}).get("student_name", sid))
        .str.upper()
    )

    # --- Compute total ---
    df['Total'] = (
        df['Review and update progress on the OJT plan (10 marks)'] +
        df['Progress on achieving personal and professional goals (15 marks)'] +
        df['Reflection on skills acquired (Total: 60 marks)'] +
        df['Quality of writing (15 marks)']
    )

    cols = [
        'SID',
        'Student Name',
        'Review and update progress on the OJT plan (10 marks)',
        'Progress on achieving personal and professional goals (15 marks)',
        'Reflection on skills acquired (Total: 60 marks)',
        'Quality of writing (15 marks)',
        'Total',
        'Feedback'
    ]

    return df[cols]

#    - Incorporate explanations of the mark allocation within the feedback for each criterion.

system_message = """
1. Your task is to assess student written assignments using a structured marking rubric.

2. Follow these marking guidelines:
    - Refer closely to the rubric and assign marks per criterion, without exceeding maximum scores.
    - Assign marks with appropriate variation to reflect the quality of each response—avoid giving uniform or overly rounded scores unless well justified.
    - Maintain a high academic standard in grading and feedback.
    - Justify all marks with clear, evidence-based reasoning.

3. Provide detailed, constructive feedback:
    - Structure feedback using line breaks for each major rubric criterion. Use paragraph spacing for clarity.
    - Always refer to “the report” (not “the student”) in your comments.
    - Include at least one direct quote from the report per rubric criterion that requires improvement.
    - For each quote, suggest a revised version that improves formality, clarity, specificity, or conciseness.
    - Follow this format for all sentence-level improvements:
    
        Original: "quoted sentence from the report"  
        Suggestion: "formal, refined version of the sentence"

    - Apply structured frameworks like SMART goals where relevant.
    
    Examples:
        Original: "These are interesting insights and new knowledge to me."  
        Suggestion: "These observations provided valuable insights and deepened my understanding of premium pricing mechanisms."

        Original: "Strengthen my interpersonal skills and expand my network."  
        Suggestion: "By the end of my internship, I aim to initiate at least one meaningful conversation each week with a colleague or mentor to improve my interpersonal communication and expand my professional network."

        Original: "These hands-on experiences have been instrumental in shaping my knowledge and boosting my confidence..."  
        Suggestion: "These hands-on experiences have significantly shaped my knowledge and confidence in client interactions. They also helped me improve how I present myself professionally..."

        Original: "...allowing me to observe how FCs interact with clients..."  
        Suggestion: "...which allowed me to observe how FCs manage client interactions, appointments, and financial products..."

4. Return your response as a dictionary with the following structure:

    {
      "Student Name": str,
      "Review and update progress on the OJT plan (10 marks)": float,
      "Progress on achieving personal and professional goals (15 marks)": float,
      "Reflection on skills acquired (Total: 60 marks)": float,
      "Quality of writing (15 marks)": float,
      "Feedback": '''Multiline feedback here. Use double quotes inside if quoting student content.'''
    }

    - Use double quotes (") for all dictionary keys and string values, except for the "Feedback" value.
    - Enclose the "Feedback" value in triple single quotes (''') to preserve formatting and line breaks.
    - Return only the dictionary and nothing else.
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

