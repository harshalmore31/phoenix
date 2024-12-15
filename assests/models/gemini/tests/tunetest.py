import google.generativeai as genai
from IPython.display import Markdown, HTML
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("gemini_api2_key")) # call through env variables 

for model_info in genai.list_tuned_models():
    print(model_info.name)

# model = genai.GenerativeModel("tunedModels/mentalhealthassistant-31whez6ss3vn")
# response = model.generate_content(contents=input("User_input : "))
# print(response.text)

model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content(contents="Who won Wimbledon this year?",
                                  tools='google_search_retrieval')
print(response.text)