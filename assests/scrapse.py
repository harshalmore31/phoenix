import asyncio
import os
import requests
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from bs4 import BeautifulSoup
import json
from markitdown import MarkItDown

# Configure output directory
os.makedirs("outputs", exist_ok=True)

# Query to search on Google
SEARCH_QUERY = input("Search Query: ")

def internet_search(search: str) -> list:
    """
    Fetches search results from the Google Custom Search API.
    :param search: Query to search for
    :return: List of result links
    """
    print("Browsing through Google Search!")
    api_key = os.getenv("GOOGLE_API_KEY")  # Replace with your API key in environment variables
    cx = os.getenv("GOOGLE_CX")  # Replace with your Programmable Search Engine ID in environment variables

    complete_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={search}"
    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Print debug information
        total_results = data.get("searchInformation", {}).get("totalResults", "0")
        print(f"Total Results: {total_results}")

        if total_results != "0":
            results = [{"title": item.get("title"), "link": item.get("link")} for item in data.get("items", []) if "link" in item]

            # Save search results to a JSON file
            with open("outputs/search_results.json", "w", encoding="utf-8") as file:
                json.dump(results, file, indent=4, ensure_ascii=False)

            print("Search results saved to outputs/search_results.json")
            return [result["link"] for result in results]
        else:
            print("No results found")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []

async def main() -> None:
    # Fetch search results
    search_results = internet_search(SEARCH_QUERY)

    # Limit to top 5 filtered URLs
    filtered_urls = search_results[:5]

    if not filtered_urls:
        print("No websites found in search results.")
        return

    crawler = PlaywrightCrawler(
        # Limit the crawl to the number of filtered URLs.
        max_requests_per_crawl=len(filtered_urls),
    )

    extracted_data = []

    # Define the default request handler, which will process each filtered URL.
    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')

        try:
            # Introduce a delay before processing the next request
            await asyncio.sleep(5)  # Add a 5-second delay

            # Extract the content of the page
            raw_html = await context.page.content()
            soup = BeautifulSoup(raw_html, 'html.parser')

            # Clean and parse the content
            title = soup.title.string if soup.title else "No Title"
            body_text = soup.get_text(separator='\n', strip=True)
            extracted_data.append({"url": context.request.url, "title": title, "content": body_text})
            context.log.info(f'Content saved for {context.request.url}')


        except Exception as e:
            context.log.error(f"An error occurred while processing {context.request.url}: {e}")

    # Run the crawler with the filtered URLs
    await crawler.run(filtered_urls)

    # Process with markitdown and save to output.md
    md = MarkItDown()
    md_content = ""
    for item in extracted_data:
        md_content+= f"## {item['title']}\n\n"
        md_content+= f"**URL:** {item['url']}\n\n"
        md_content+= f"{item['content']}\n\n"
        md_content+= "---" + "\n\n"
    result = md.convert(md_content)
    with open("output.md",'a') as f:
        f.write(result.text_content)
    print("Extracted data saved to output.md")

if __name__ == '__main__':
    asyncio.run(main())