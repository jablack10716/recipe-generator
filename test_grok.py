from openai import OpenAI

# Read API key from .env
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("XAI_API_KEY")

if not api_key:
    print("ERROR: XAI_API_KEY not found in .env")
    exit(1)

print(f"Testing Grok with API key: {api_key[:20]}...")

try:
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    response = client.chat.completions.create(
        model="grok-2",
        messages=[{"role": "user", "content": "Say 'Grok works!' and nothing else."}],
        max_tokens=50,
    )
    
    print("✓ Grok is working!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"✗ Grok test failed: {e}")
    import traceback
    traceback.print_exc()
