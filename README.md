# To run app:

```
$ export OPENAI_API_KEY="your_api_key_here"

$ pip install -r requirements.txt

$ streamlit run app.py
```

# Assumptions:

- (Only if running app locally) User has an OpenAI API key.
- Resumes contain the candidate's name.
- Job description and resumes are all in English.

# Approach:

1. Collecting user input
   - Job description (text)
   - Resumes (uploaded file in PDF or .txt format, or text)
      - User can select number of resumes to input manually
2. Embedding generation and similarity calculation
   - Embeddings for job description and resume text generated using SentenceTransformers ```all-MiniLM-L6-v2``` model
   - ```sklearn``` cosine similarity function used to calculate similarity between job description and each resume
3. Displaying top candidates
   - 5 candidates with highest similarity scores are displayed in descending order by similarity
   - Candidate name is returned by OpenAI model ```gpt-4o-mini```
   - ```gpt-4o-mini``` also generates a summary on why the candidate is a good fit for the job.

