import requests
import json
import os
from mistralai import Mistral
from dotenv import load_dotenv
from rich.console import Console

console = Console()

load_dotenv()

api_key = os.getenv("mistral_api_key")
model = "mistral-large-latest"

def internet_search(search: str):
     """
     Fetches search results from the Google Custom Search API.
     :param search: Query to search for
     """
     print("Browsing through Google Search !")
     api_key = "AIzaSyCO2O3zzU80DmlCEycjmQGMoE9Fd0Sbch4"  # Replace this with your API key
     cx = "6260a17ad62ad4c3b"  # Your NEW Programmable Search Engine ID

     complete_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={search}"
     response = requests.get(complete_url)
     response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
     data = response.json()

     # Print debug information
     total_results = data.get("searchInformation", {}).get("totalResults", "0")
     print(f"Total Results: {total_results}")

     if total_results != "0":
          return data.get("items", []) #return the results
     else:
          print("No results found")
          return []

def parse_results_with_llm(results):
     """
     Parses the search results using the LLM model.
     :param results: List of search results
     """
     client = Mistral(api_key=api_key)
     messages = [
          {
               "role": "user",
               "content": f"Please summarize the following search results: {json.dumps(results)}"
          }
     ]

     chat_response = client.chat.complete(
          model=model,
          messages=messages
     )

     summary = chat_response.choices[0].message.content
     console.print(f"[bold red]{summary}[/bold red]")
     return summary

if __name__ == "__main__":
     results = internet_search("CIA vs KGB unheard")
     if results:
          print("---- Search Results -----")
          print(json.dumps(results, indent=4))
          print("--------------------")
          summary = parse_results_with_llm(results)
          print("---- Summary -----")
          print(summary)
