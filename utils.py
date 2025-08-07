import streamlit as st
from pypdf import PdfReader
import numpy as np

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

def display_candidates(resumes, similarities, job_description):
    candidate_list = st.container()
    with candidate_list:
        best_indices = np.argsort(similarities.flatten())[-5][::-1]
        for i in best_indices:
            name = find_name(resumes[i])
            sim = similarities[i]
            summary = generate_summary(resumes[i], job_description)

            with st.container(border=True):
                st.text(f"Candidate name: {name}")
                st.text(f"Similarity score: {str(sim)}")
                st.text(f"Why this candidate may be a good fit: {summary}")

def find_name():
    return

def generate_summary():
    return