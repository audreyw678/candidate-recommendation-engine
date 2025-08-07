import streamlit as st
import utils
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')     # Hugging Face model for sentence similarity
utils.load_phi3()

if "show_candidates" not in st.session_state:
    st.session_state.show_candidates = False

st.header("Candidate Recommendation Engine")

# job description input
with st.container():
    job_description = st.text_area("Input job description", height="content")

st.divider()

with st.container():
    col1, div, col2 = st.columns([0.45, 0.1, 0.45])

    # resume input via file upload
    with col1:
        resume_files = st.file_uploader(
            "Upload resumes in .pdf or .txt format", accept_multiple_files=True, type=["pdf", "txt"]
        )

    with div:
        st.html("<p style='text-align: center; font-weight: bold'>AND/OR</p>")

    # resume input via text input
    with col2:
        resume_texts = []
        num_resumes = st.number_input("Number of resumes to input manually", min_value=1, step=1)
        for i in range(num_resumes):
            resume_texts.append(st.text_area("Paste resume " + str(i+1) + " text here", key=i))

    # submission button
    _, center, _ = st.columns([0.4, 0.2, 0.4])

    def handle_click():
        st.session_state.show_candidates = True

    with center:
        st.button("Find best candidates", on_click=handle_click)

st.divider()

if st.session_state.show_candidates:
    if any(key not in st.session_state for key in ["all_resumes", "resume_embeddings", "job_embedding", "similarities"]):
        st.session_state.all_resumes = utils.process_files(resume_files, resume_texts)
        st.session_state.resume_embeddings = embedding_model.encode(st.session_state.all_resumes)
        st.session_state.job_embedding = embedding_model.encode(job_description)
        st.session_state.similarities = cosine_similarity(st.session_state.resume_embeddings, st.session_state.job_embedding.reshape(1, -1))
    utils.display_candidates(st.session_state.all_resumes, st.session_state.similarities, job_description)