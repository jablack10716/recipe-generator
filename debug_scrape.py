from recipe_scrapers import scrape_me
import requests

url = "https://www.foodnetwork.com/recipes/food-network-kitchen/the-best-carbonara-7260325"

print(f"Testing URL: {url}")

# Test 1: recipe-scrapers
print("\n--- Testing recipe-scrapers ---")
try:
    # wild_mode removed in v15
    scraper = scrape_me(url)
    print(f"Title: {scraper.title()}")
    print("Success!")
except Exception as e:
    print(f"recipe-scrapers failed: {e}")

# Test 2: requests (used by AI parser)
print("\n--- Testing requests (for AI parser) ---")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
try:
    resp = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        print("Successfully fetched page content.")
    else:
        print("Failed to fetch page content.")
except Exception as e:
    print(f"Requests failed: {e}")
