import requests
import os
from mistralai import Mistral
from dotenv import load_dotenv
from rich.console import Console
import google.generativeai as genai

console = Console()

load_dotenv()

# api_key = os.getenv("mistral_api_key")
# model = "mistral-large-latest"

api_key = os.getenv("gemini_api_key1")



j_api = os.getenv("jina_api_key1")

def search(txt :str) -> str:
    text = txt
    url = 'https://s.jina.ai/'+text
    headers = {
        'Authorization': f'Bearer {j_api}',
        'X-Retain-Images': 'none'
    }

    response = requests.get(url, headers=headers)

    fres = response.text
    print(fres)

    genai.configure(api_key=api_key)

    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }

    # Enhanced System Instructions for Gemini
    system_instructions = f"""
    You are an expert summarization assistant. Your task is to analyze the provided content, which consists of text extracted from multiple web pages related to the user's search query.
    Your goal is to create a concise yet comprehensive summary that captures the key information from all documents.

    Focus on:
    - Identifying the main points, arguments, and facts presented in each document.
    - Synthesizing the information to eliminate redundancies.
    - Highlighting any common themes, contrasting views, or unique insights found across the documents.
    - Presenting the summary in a clear, coherent, and easy-to-understand manner.
    -  Avoid conversational filler and be as direct and factual as possible.
    - The response must be in markdown format.

    The user's query is: {txt}

    The following are the extracted contents from multiple sources. Generate the summary based on the given content.

    """
    # Send prompt to Gemini with the extracted content
    model = genai.GenerativeModel(
      model_name="gemini-2.0-flash-exp",
      generation_config=generation_config,
      system_instruction=system_instructions
    )

    chat_session = model.start_chat(
      history=[
      ]
    )


    response = chat_session.send_message(fres + txt)
    
    console.print(f"[bold red]{response.text}[/bold red]")

search(input("Search Query : "))