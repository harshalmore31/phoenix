import requests
  
def duckduckgo_search(query):
    """Performs a DuckDuckGo search and returns the results."""
    url = "https://api.duckduckgo.com/?q=" + query + "&format=json"
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for bad status codes
    return response.json()

results = duckduckgo_search("Best phone under 30k")
print(results)


