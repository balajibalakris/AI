import os
import json
import numpy as np
from sklearn.neighbors import NearestNeighbors
import google.generativeai as genai
import sys

# Get query from CLI argument
query = sys.argv[1] if len(sys.argv) > 1 else "default query"

# Setup Gemini
genai.configure(api_key="APIKEY")

# Load data
with open("indexed_data.json") as f:
    docs = json.load(f)

embeddings = np.load("embeddings.npy")
nn = NearestNeighbors(n_neighbors=3, metric="cosine").fit(embeddings)

# Embed query
query_embedding = genai.embed_content(
    model="models/embedding-001",
    content=query,
    task_type="retrieval_query"
)["embedding"]

# Find top matches
_, indices = nn.kneighbors([query_embedding])

context_str = ""
for i in indices[0]:
    entry = docs[i]
    context_str += f"\nError: {entry['error']}\nContext: {entry['context']}\nSolution: {entry['solution']}\n"

# prompt = f"""
# You are an assistant for helping developers debug migration issues.

# Here are some known examples:\n{context_str}\n
# Now answer this developer's question:\n{query}
# """
prompt = f"""
You are a Java/Spring migration assistant.

Given the user query and examples, respond strictly in **JSON format** using this structure:

{{
  "issue": "<short description of the main error>",
  "possible_cause": "<brief explanation of why it likely occurred>",
  "solution_steps": [
    {{
      "title": "Short title or step label",
      "steps": ["step 1", "step 2", "..."],
      "explanation": "Why this set of steps works"
    }},
    {{
      "title": "Alternative fix",
      "steps": ["..."],
      "explanation": "Optional secondary method explanation"
    }}
  ]
}}

Context:\n{context_str}

User Question:\n{query}
"""


response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)

# Final result
print(response.text.strip())
