import requests, json

def internet_search(search :str) -> str:
    print("Browsing through Google Search !")
    api_key = "AIzaSyCO2O3zzU80DmlCEycjmQGMoE9Fd0Sbch4"
    complete_url = "https://www.googleapis.com/customsearch/v1?key="+api_key+f"&cx=017576662512468239146:omuauf_lfve&q={search}"
    response = requests.get(complete_url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    x = response.json()
    print(x)