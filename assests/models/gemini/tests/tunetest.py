import google.generativeai as genai
from IPython.display import Markdown, HTML
genai.configure(api_key="") # call through env variables 

for model_info in genai.list_tuned_models():
    print(model_info.name)

model = genai.GenerativeModel("tunedModels/mentalhealthassistant-31whez6ss3vn")
response = model.generate_content(contents=input("User_input : "))
print(response.text)

# model = genai.GenerativeModel('gemini-1.5-flash')
# response = model.generate_content(contents="Who won Wimbledon this year?",
#                                   tools='google_search_retrieval')
# Markdown(response.candidates[0].content.parts[0].text)

# response = model.generate_content()