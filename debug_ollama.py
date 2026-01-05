import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

prompt = """You are a recipe extraction API. Output ONLY valid JSON with these keys:
- title: str
- ingredients: str
- instructions: str

Example input: "Chocolate Cake. Ingredients: flour, sugar. Instructions: Mix and bake."
Example output: {"title": "Chocolate Cake", "ingredients": "flour\\nsugar", "instructions": "Mix and bake"}

Now extract from this:
Title: Test Cookie Recipe
Ingredients: flour, butter
Instructions: Mix all ingredients. Bake at 350F.
"""

body = {
    "model": OLLAMA_MODEL,
    "messages": [
        {"role": "system", "content": "You are a recipe extraction API. Only output valid JSON, no other text."},
        {"role": "user", "content": prompt},
    ],
    "stream": False,
    "format": "json"
}

print(f"Testing Ollama at {OLLAMA_HOST}")
print(f"Model: {OLLAMA_MODEL}")
print(f"\nRequest body:")
print(json.dumps(body, indent=2))

try:
    resp = requests.post(f"{OLLAMA_HOST}/api/chat", json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    print(f"\n✓ Response received!")
    print(f"\nFull response:")
    print(json.dumps(data, indent=2))
    
    message = data.get("message", {}).get("content", "")
    print(f"\nMessage content:")
    print(message)
    
    if message:
        try:
            parsed = json.loads(message)
            print(f"\n✓ Successfully parsed JSON:")
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError as e:
            print(f"\n✗ Failed to parse as JSON: {e}")
            print(f"Raw content: {repr(message)}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
