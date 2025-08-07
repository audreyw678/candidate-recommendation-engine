import streamlit as st
from pypdf import PdfReader

def process_files(resume_files, resume_texts):
    all_resumes = []
    for file in resume_files:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            all_resumes.append(text.strip())
        else:
            text = file.read().decode("utf-8")
            all_resumes.append(text.strip())
    for txt in resume_texts:
        all_resumes.append(txt.strip())
    return all_resumes

