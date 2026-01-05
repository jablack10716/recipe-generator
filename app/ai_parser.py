import os
import json
from typing import Dict, Any
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import google.generativeai as genai

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model provider selection
AI_MODEL_PROVIDER = os.getenv("AI_MODEL_PROVIDER", "ollama").lower()

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Configure Gemini if key is available
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def clean_html(html_content: str) -> str:
    """
    Clean HTML content to reduce token usage.
    Removes scripts, styles, and other non-content elements.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove script and style elements
    for script in soup(["script", "style", "svg", "nav", "footer", "header"]):
        script.decompose()
        
    # Get text content with some structure preservation
    text = soup.get_text(separator="\n", strip=True)
    
    # Truncate if too long (rough token estimation)
    # Grok has a large context window, but let's be reasonable
    return text[:50000] 

def parse_recipe_with_ai(url: str, html_content: str) -> Dict[str, Any]:
    """
    Parse recipe data from HTML content using the configured AI provider.
    Supports: ollama or gemini
    """
    cleaned_text = clean_html(html_content)
    
    if AI_MODEL_PROVIDER == "ollama":
        return parse_with_ollama(url, cleaned_text)
    elif AI_MODEL_PROVIDER == "gemini":
        return parse_with_gemini(url, cleaned_text)
    else:
        raise ValueError(f"Unknown AI provider: {AI_MODEL_PROVIDER}. Use 'ollama' or 'gemini'")


def parse_with_ollama(url: str, cleaned_text: str) -> Dict[str, Any]:
    """Parse recipe using local Ollama model"""
    prompt = f"""
    You are a recipe extraction API. Output ONLY valid JSON with these keys:
    - title: str
    - ingredients: str (newline separated list, one ingredient per line with amount)
    - instructions: str (newline separated list, one step per line)
    - prep_time_minutes: int or null
    - cook_time_minutes: int or null
    - servings: str or null
    - image_url: str or null

    IMPORTANT for ingredients: Format each ingredient on its own line with the amount included.
    Example: "2 cups all-purpose flour" NOT "all-purpose flour - 2 cups"
    Example: "1 teaspoon vanilla extract" NOT "vanilla extract (1 tsp)"

    If data is missing, use null or empty string appropriately.

    Source URL: {url}
    Page text:
    {cleaned_text}
    """

    body = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": "You are a recipe extraction API. Only output JSON."},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "format": "json"
    }

    try:
        resp = requests.post(f"{OLLAMA_HOST}/api/chat", json=body, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        message = data.get("message", {}).get("content", "")
        if not message:
            raise ValueError("No response content from Ollama")

        content = message.strip()
        parsed = json.loads(content)
        
        # Ensure newlines are actual newlines, not escaped strings
        ingredients = parsed.get("ingredients") or ""
        instructions = parsed.get("instructions") or ""
        
        # If the AI returned literal \n strings, replace them with actual newlines
        if isinstance(ingredients, str) and "\\n" in ingredients:
            ingredients = ingredients.replace("\\n", "\n")
        if isinstance(instructions, str) and "\\n" in instructions:
            instructions = instructions.replace("\\n", "\n")
        
        # Clean up tab characters and extra whitespace
        if isinstance(ingredients, str):
            ingredients = ingredients.replace("\t", "").replace("\r", "")
            lines = [" ".join(line.split()) for line in ingredients.split("\n")]
            ingredients = "\n".join(line for line in lines if line.strip())
        
        if isinstance(instructions, str):
            instructions = instructions.replace("\t", "").replace("\r", "")
            lines = [" ".join(line.split()) for line in instructions.split("\n")]
            instructions = "\n".join(line for line in lines if line.strip())

        return {
            "title": parsed.get("title") or "",
            "source_url": url,
            "ingredients": ingredients,
            "instructions": instructions,
            "prep_time_minutes": parsed.get("prep_time_minutes"),
            "cook_time_minutes": parsed.get("cook_time_minutes"),
            "servings": str(parsed.get("servings") or ""),
            "image_url": parsed.get("image_url") or "",
        }
    except Exception as e:
        print(f"Ollama parsing error: {e}")
        return {}


def parse_with_gemini(url: str, cleaned_text: str) -> Dict[str, Any]:
    """Parse recipe using Google Gemini"""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set")
    
    prompt = f"""
    You are a recipe extraction API. Extract recipe details from the following web page content.
    
    Return ONLY a valid JSON object with these keys:
    - title: str
    - ingredients: str (newline separated list, one ingredient per line with amount)
    - instructions: str (newline separated list, one step per line)
    - prep_time_minutes: int or null
    - cook_time_minutes: int or null
    - servings: str or null
    - image_url: str or null
    
    IMPORTANT for ingredients: Format each ingredient on its own line with the amount and measurement included.
    Example format:
    2 ounces rye whiskey
    1 ounce sweet vermouth
    2 dashes Angostura bitters
    1 maraschino cherry
    
    Do NOT use formats like:
    - "rye whiskey - 2 oz"
    - "rye whiskey (2 oz)"
    - "2 oz - rye whiskey"
    
    Put the amount FIRST, then the ingredient name.
    
    If data is missing, use null or empty string appropriately.
    
    Source URL: {url}
    Page text:
    {cleaned_text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        content = response.text.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        
        # Ensure newlines are actual newlines, not escaped strings
        ingredients = parsed.get("ingredients") or ""
        instructions = parsed.get("instructions") or ""
        
        # If the AI returned literal \n strings, replace them with actual newlines
        if isinstance(ingredients, str) and "\\n" in ingredients:
            ingredients = ingredients.replace("\\n", "\n")
        if isinstance(instructions, str) and "\\n" in instructions:
            instructions = instructions.replace("\\n", "\n")
        
        # Clean up tab characters and extra whitespace
        if isinstance(ingredients, str):
            ingredients = ingredients.replace('\\t', '').replace('\t', '')
            ingredients = ingredients.replace('\\r', '').replace('\r', '')
            lines = [' '.join(line.split()) for line in ingredients.split('\n')]
            ingredients = '\n'.join(line for line in lines if line.strip())
        
        if isinstance(instructions, str):
            instructions = instructions.replace('\\t', '').replace('\t', '')
            instructions = instructions.replace('\\r', '').replace('\r', '')
            lines = [' '.join(line.split()) for line in instructions.split('\n')]
            instructions = '\n'.join(line for line in lines if line.strip())
        
        return {
            "title": parsed.get("title") or "",
            "source_url": url,
            "ingredients": ingredients,
            "instructions": instructions,
            "prep_time_minutes": parsed.get("prep_time_minutes"),
            "cook_time_minutes": parsed.get("cook_time_minutes"),
            "servings": str(parsed.get("servings") or ""),
            "image_url": parsed.get("image_url") or "",
        }
    except Exception as e:
        print(f"Gemini parsing error: {e}")
        return {}



