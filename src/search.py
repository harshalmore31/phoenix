import scrapy
import requests
import json
import urllib.parse
import os

def format_search_result(item):
    """Formats a single search result item into a user-friendly string."""
    title = item.get("title", "N/A")
    link = item.get("link", "N/A")
    snippet = item.get("snippet", "N/A")
    return f"""
   Title: {title}
   URL: {link}
   Snippet: {snippet}
   ----------
"""

class JinaReaderSpider(scrapy.Spider):
    name = 'jina_reader_spider'
    allowed_domains = []  # Make it dynamic

    def __init__(self, url=None, *args, **kwargs):
        super(JinaReaderSpider, self).__init__(*args, **kwargs)
        if not url:
            raise Exception("Error! the URL argument is required")
        self.start_urls = [url]
        parsed_domain = scrapy.utils.url.urlparse(url).netloc
        self.allowed_domains = [parsed_domain]
        self.jina_api_key = os.getenv("jina_api_key")  # get from env
        self.search_query_suffix = "review"

    def fetch_with_r_jina(self, url, headers=None):
       """Fetches content using r.jina.ai."""
       if not headers:
            headers = {}
       url = f"https://r.jina.ai/{url}"
       print(f"Fetching with r.jina.ai: {url}")
       response = requests.get(url, headers=headers)
       response.raise_for_status()
       return response.text

    def fetch_with_s_jina(self, query, headers=None):
        """Fetches and formats search results using s.jina.ai with API key authentication."""
        if not self.jina_api_key:
            print("Jina API key is missing. Set jina_api_key environment variable.")
            return "Jina API key missing"
        if not headers:
            headers = {}
        encoded_query = urllib.parse.quote(query)
        url = f"https://s.jina.ai/{encoded_query}"
        headers['Authorization'] = f'Bearer {self.jina_api_key}'
        headers['X-Retain-Images'] = 'none'
        print(f"Fetching with s.jina.ai: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        try:
           data = response.json()
        except:
           return "Could not format result to JSON. Ensure that the response is JSON (No Streaming). Use headers such as Accept: application/json"
        total_results = data.get("searchInformation", {}).get("totalResults", "0")
        print(f"Total Results: {total_results}")
        if total_results != "0":
            formatted_results = "\n".join(format_search_result(item) for item in data.get("items", []))
            return formatted_results
        else:
           print("No results found")
           return ""

    def parse(self, response):
       content_type = response.headers.get("Content-Type")
       if content_type:
           try:
               if isinstance(content_type, bytes):
                    content_type = content_type.decode('utf-8', errors='ignore').lower()
               else:
                   content_type = content_type.lower()

               if "text" in content_type:
                   # Extract the title
                    title = response.css('h1::text').get()
                    if not title:
                        title = response.url

                    # Extract all links
                    links = response.css('a::attr(href)').getall()

                    # Example: Using r.jina.ai to read the content of the current page
                    try:
                        r_jina_content = self.fetch_with_r_jina(response.url)
                    except:
                         r_jina_content = "Could not fetch data with r.jina.ai"


                    # Example: Using s.jina.ai to search for reviews related to the title
                    try:
                        s_jina_results = self.fetch_with_s_jina(f"{title} {self.search_query_suffix}", headers={'Accept': 'application/json'})
                    except:
                         s_jina_results = "Could not fetch data with s.jina.ai"
                 # Save data to file
                    with open('scraped_data.txt', 'a', encoding='utf-8') as file:
                       file.write(f"Title: {title}\n")
                       file.write(f"Links: {links}\n")
                       file.write(f"Content fetched from r.jina.ai:\n{r_jina_content}\n--------------------\n")
                       file.write(f"Google Search Results (s.jina.ai):\n{s_jina_results}\n--------------------\n\n")

                    # follow links and recursively scrap it
                    for link in links:
                       yield response.follow(link, callback=self.parse)
               else:
                   print(f"Skipping non-text resource: {response.url}")
           except Exception as e:
                  print(f"Error in parsing headers: {e} on {response.url}")
       else:
          print(f"No content type on {response.url}")