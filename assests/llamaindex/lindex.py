# bring in our LLAMA_CLOUD_API_KEY
from dotenv import load_dotenv
load_dotenv()

# bring in deps
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import google.generativeai as genai
from rich.console import Console
import os
console = Console()

# Set up parser
parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

# Use SimpleDirectoryReader to parse the file
file_extractor = {".csv": parser}
documents = SimpleDirectoryReader(input_files=[r'src\backend\Items.csv'], file_extractor=file_extractor).load_data()

for doc in documents:
    print(doc.text)
    print("-" * 50) 

# Get Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Join all document text into a single string for context
context = "\n\n".join([doc.text for doc in documents])


# Define system instructions for Gemini with context injection
system_instructions = f"""
You are an helpful and informative assistant , you will answer from the following context and give as per user's query

Context:
{context}
"""

# Instantiate the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=system_instructions
)

# Start chat session
chat_session = model.start_chat(
    history=[]
)

# User query
while 1:
    user_query = input("Query : ")
    # Send query and get response from Gemini
    response = chat_session.send_message(user_query)
    console.print(f"[bold red]{response.text}[/bold red]")
# print("\nGemini Response:")
# print(response.text)
