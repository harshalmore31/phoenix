from IPython.display import HTML, Markdown, display
import google.generativeai as genai
from google import genai
from google.genai.types import (
    FunctionDeclaration,
    GenerateContentConfig,
    GoogleSearch,
    Part,
    Retrieval,
    SafetySetting,
    Tool,
    ToolCodeExecution,
    VertexAISearch,
)
import os
from dotenv import load_dotenv
import keyboard
# from functions.perplex import research

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) #Replace with your Google Generative AI key

google_search_tool = Tool(google_search=GoogleSearch())

MODEL_ID = "gemini-2.0-flash-exp"  # @param {type: "string"}

response = client.models.generate_content(
    model=MODEL_ID,
    contents="When is the next total solar eclipse in the United States?",
    config=GenerateContentConfig(tools=[google_search_tool]),
)

display(Markdown(response.text))

print(response.candidates[0].grounding_metadata)

HTML(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
