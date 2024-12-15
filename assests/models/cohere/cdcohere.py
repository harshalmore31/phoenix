import os
import cohere
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("cohere_api_key")

co = cohere.ClientV2(api_key)
response = co.chat(
    model="command-r-plus", 
    messages=[
        {"role": "user",
          "content": "hello world!"}
          ]
)
print(response.message.content[0].text)


