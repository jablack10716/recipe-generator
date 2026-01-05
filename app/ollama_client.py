import json
import os
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def clean_html_for_llm(html_content: str) -> str:
    """Strip scripts/styles and return text to reduce tokens."""
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["script", "style", "svg", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text[:50000]


def parse_recipe_with_ollama(url: str, html_content: str) -> Dict[str, Any]:
    """Call a local Ollama model to extract recipe JSON."""
    cleaned_text = clean_html_for_llm(html_content)

    prompt = f"""
    You are a recipe extraction API. Output ONLY valid JSON with these keys:
    - title: str
    - ingredients: str (newline separated list)
    - instructions: str (newline separated list)
    - prep_time_minutes: int or null
    - cook_time_minutes: int or null
    - servings: str or null
    - image_url: str or null

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
    }

    resp = requests.post(f"{OLLAMA_HOST}/api/chat", json=body, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    message = None
    if isinstance(data, dict):
        message = data.get("message", {}).get("content") or data.get("response")
    if not message:
        raise ValueError("No response content from Ollama")

    content = message.strip()
    parsed = json.loads(content)

    return {
        "title": parsed.get("title") or "",
        "source_url": url,
        "ingredients": parsed.get("ingredients") or "",
        "instructions": parsed.get("instructions") or "",
        "prep_time_minutes": parsed.get("prep_time_minutes"),
        "cook_time_minutes": parsed.get("cook_time_minutes"),
        "servings": str(parsed.get("servings") or ""),
        "image_url": parsed.get("image_url") or "",
    }
