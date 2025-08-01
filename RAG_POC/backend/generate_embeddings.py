import json
import os
import numpy as np
import google.generativeai as genai
from tqdm import tqdm

# Step 1: Configure Gemini
genai.configure(api_key="AIzaSyD3mYxeXzN1rNdbHvO4nD5wajU4xXOzd9k")
# Step 2: Load your migration error dataset
with open("migration_errors.json") as f:
    data = json.load(f)

texts = [f"{entry['error']} {entry['context']}" for entry in data]

# Step 3: Generate embeddings
embeddings = []
for text in tqdm(texts, desc="Generating embeddings"):
    response = genai.embed_content(
    model="models/embedding-001",
    content=text,
    task_type="retrieval_document"
)
    embeddings.append(response["embedding"])

# Step 4: Save embeddings for future use
np.save("embeddings.npy", np.array(embeddings))

# Save original data too (index aligned)
with open("indexed_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Embeddings generated and saved!")

