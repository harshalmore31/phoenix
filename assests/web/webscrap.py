from bs4 import BeautifulSoup
import requests

url = "https://adalflow.sylph.ai/contributor/contribution.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# Now you can find elements like:
title = soup.find('h1').text
links = soup.find_all('a')
with open('scraped_data.txt', 'w') as file:
    file.write(f"Title: {title}\n")
    file.write("Links:\n")
    for link in links:
        file.write(f"{link.get('href')}\n")