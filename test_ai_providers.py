import os
from dotenv import load_dotenv

load_dotenv()

# Test HTML content
test_html = """
<html>
<body>
    <h1>Classic Chocolate Chip Cookies</h1>
    <div class="ingredients">
        <h2>Ingredients:</h2>
        <ul>
            <li>2 cups all-purpose flour</li>
            <li>1 cup butter, softened</li>
            <li>3/4 cup sugar</li>
            <li>2 eggs</li>
            <li>2 cups chocolate chips</li>
        </ul>
    </div>
    <div class="instructions">
        <h2>Instructions:</h2>
        <ol>
            <li>Preheat oven to 375°F</li>
            <li>Mix butter and sugar until creamy</li>
            <li>Add eggs and mix well</li>
            <li>Gradually add flour</li>
            <li>Stir in chocolate chips</li>
            <li>Bake for 10-12 minutes</li>
        </ol>
    </div>
    <p>Prep Time: 15 minutes</p>
    <p>Cook Time: 12 minutes</p>
    <p>Servings: 24 cookies</p>
</body>
</html>
"""

test_url = "https://example.com/chocolate-chip-cookies"

def test_provider(provider_name: str):
    """Test a specific AI provider"""
    print(f"\n{'='*60}")
    print(f"Testing {provider_name.upper()}")
    print(f"{'='*60}")
    
    # Set the provider
    os.environ["AI_MODEL_PROVIDER"] = provider_name
    
    try:
        # Import after setting env var
        from app.ai_parser import parse_recipe_with_ai
        
        result = parse_recipe_with_ai(test_url, test_html)
        
        if result and result.get("title"):
            print(f"✓ {provider_name.upper()} is working!")
            print(f"Title: {result.get('title')}")
            print(f"Ingredients found: {bool(result.get('ingredients'))}")
            print(f"Instructions found: {bool(result.get('instructions'))}")
            return True
        else:
            print(f"✗ {provider_name.upper()} returned empty result")
            return False
            
    except Exception as e:
        print(f"✗ {provider_name.upper()} failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing AI Recipe Parsers")
    print(f"Current provider in .env: {os.getenv('AI_MODEL_PROVIDER', 'not set')}")
    
    results = {}
    
    # Test Ollama
    if os.getenv("OLLAMA_HOST"):
        results["ollama"] = test_provider("ollama")
    else:
        print("\n[Skipping Ollama - OLLAMA_HOST not set]")
    
    # Test Gemini
    if os.getenv("GEMINI_API_KEY"):
        results["gemini"] = test_provider("gemini")
    else:
        print("\n[Skipping Gemini - GEMINI_API_KEY not set]")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for provider, success in results.items():
        status = "✓ Working" if success else "✗ Failed"
        print(f"{provider.upper()}: {status}")
    
    print(f"\nTo switch providers, edit AI_MODEL_PROVIDER in .env file")
    print(f"Options: ollama, gemini")
