import os
import requests

# Test Ollama connection
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

print(f"Testing Ollama at {OLLAMA_HOST}...")
print(f"Using model: {OLLAMA_MODEL}")

try:
    # First check if Ollama is running
    response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
    response.raise_for_status()
    print("✓ Ollama is running!")
    
    # Check available models
    models = response.json().get("models", [])
    if models:
        print(f"Available models: {[m['name'] for m in models]}")
    else:
        print("No models found. You may need to pull a model first.")
        print(f"Run: ollama pull {OLLAMA_MODEL}")
    
    # Test a simple chat completion
    print(f"\nTesting chat with model {OLLAMA_MODEL}...")
    body = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": "Say 'Ollama works!' and nothing else."}],
        "stream": False,
    }
    
    response = requests.post(f"{OLLAMA_HOST}/api/chat", json=body, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    message = data.get("message", {}).get("content", "")
    print("✓ Ollama chat is working!")
    print(f"Response: {message}")
    
except requests.exceptions.ConnectionError:
    print("✗ Could not connect to Ollama.")
    print("Make sure Ollama is running. Try: ollama serve")
except requests.exceptions.Timeout:
    print("✗ Request timed out. Ollama may be slow or unresponsive.")
except Exception as e:
    print(f"✗ Ollama test failed: {e}")
    import traceback
    traceback.print_exc()
