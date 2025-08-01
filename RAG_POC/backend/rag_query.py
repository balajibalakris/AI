import os
import json
import google.generativeai as genai

# Load API key from environment variable
genai.configure(api_key="AIzaSyD3mYxeXzN1rNdbHvO4nD5wajU4xXOzd9k")
# Load the error-solution data
with open("migration_errors.json") as f:
    data = json.load(f)

# Ask user for a query
user_query = input("\n❓ Describe your error or issue: ")

# Simple keyword-based search (upgrade later to vector-based RAG if needed)
matched_contexts = []
for item in data:
    if any(word.lower() in item["error"].lower() or word.lower() in item["context"].lower()
           for word in user_query.split()):
        matched_contexts.append(item)

# If no match found, use entire dataset as fallback context
if not matched_contexts:
    matched_contexts = data

# Build prompt
context_str = "\n\n".join(
    [f"Error: {e['error']}\nContext: {e['context']}\nSolution: {e['solution']}" for e in matched_contexts]
)

prompt = f"""
You are an assistant helping developers debug migration issues.
Here are some known errors and solutions:\n\n{context_str}

Now answer this question from a developer:\n{user_query}
"""

# Send to Gemini
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(prompt)

print("\n💡 Gemini Suggestion:")
print(response.text)

