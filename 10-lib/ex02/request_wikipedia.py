import sys
import requests
import json
from dewiki import from_string


def get_wikipedia_content(search_term, language="en"):
    """Fetch content from Wikipedia for a given search term."""
    url = f"https://{language}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": search_term,
        "redirects": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()))

        if "extract" in page:
            return from_string(page["extract"])
        else:
            print("Error: No content found for this term.")
            return None

    except requests.RequestException as e:
        print(f"Error: Failed to fetch data from Wikipedia - {e}")
        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 request_wikipedia.py <search_term>")
        sys.exit(1)
    
    lang = input("Choose your language: English 'en', Français 'fr'\n")

    if lang not in ['en', 'fr']:
        print("Language must be 'en' or 'fr'")
        sys.exit(1)

    search_term = sys.argv[1]
    cleaned_search_term = search_term.replace(" ", "_")
    content = get_wikipedia_content(search_term, lang)

    if content:
        file_name = f"{cleaned_search_term}.wiki"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Content written to {file_name}")
    else:
        print("Error: No file created due to missing content or an error.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
