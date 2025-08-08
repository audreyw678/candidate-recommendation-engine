# To run app locally (requires OpenAI API key):

```
$ export OPENAI_API_KEY="your_api_key_here"
$ pip install -r requirements.txt
$ streamlit run app.py
```

# To run app via Streamlit Cloud:
Go to https://candidate-recommendation.streamlit.app/

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

# Known Issues:
- The app sporadically displays the following error:
   ```
   NotImplementedError: Cannot copy out of meta tensor; no data! Please use torch.nn.Module.to_empty() instead of torch.nn.Module.to() when moving module from meta to a different device.
   ```
   This issue is almost always fixed by simply reloading the page.
