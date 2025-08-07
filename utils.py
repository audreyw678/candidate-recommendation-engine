import streamlit as st
from pypdf import PdfReader
import numpy as np
from transformers import pipeline
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        best_indices = np.argsort(similarities.flatten())[-5:][::-1]
        for i in best_indices:
            name = find_name(resumes[i])
            sim = similarities[i][0]
            summary = generate_summary(resumes[i], job_description)
            with st.container(border=True):
                st.text(f"Candidate name: {name}")
                st.text(f"Similarity score: {str(sim)}")
                st.text(f"Why this candidate may be a good fit: {summary}")

def find_name(resume):
    prompt = f"Given the following resume:\n{resume}\nReturn the candidate's name."
    response = client.chat.completions.create(model="gpt-4o-mini-2024-07-18",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=20, temperature=0, n=1,stop=None)
    name = response.choices[0].message.content.strip()
    return name

def generate_summary(resume, description):
    prompt = f"Given the following resume:\n{resume}\n\nAnd job description:\n{description}\n\In 1-2 sentences, summarize why this candidate may be a good fit for the job."
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=80, temperature=0.3, n=1,stop=None)
    answer = response.choices[0].message.content.strip()
    return answer
