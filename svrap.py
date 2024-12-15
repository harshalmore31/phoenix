import requests
import json
import time


def get_google_search_results(api_key, cx, query, num_results=10):
    """Fetches search results from the Google Custom Search API."""

    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": num_results,
        "start": 1  # Try removing this line to test without the start argument
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        results = data.get("items", [])
        return results
    except requests.exceptions.RequestException as e:
         print(f"Error during API request: {e}")
         return []
    except json.JSONDecodeError as e:
        print(f"Error decoding json: {e}")
        return []
    
if __name__ == "__main__":
    # Replace with your actual API key, CSE ID and search term
    api_key = "AIzaSyCO2O3zzU80DmlCEycjmQGMoE9Fd0Sbch4"  # Replace this!
    cx = "017576662512468239146:omuauf_lfve"  # Replace this!
    query = "best gaming laptop under 1500"

    results = get_google_search_results(api_key, cx, query)

    if results:
         print(json.dumps(results, indent=4))
         print("-------------")
        # You can now loop through the list and print whatever specific field you need
         for item in results:
              print("Title:", item.get("title"))
              print("URL:", item.get("link"))
              print("Snippet:", item.get("snippet"))
              print("------------")

    else:
        print("No results found.")