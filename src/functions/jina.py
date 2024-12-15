import requests
import os
from mistralai import Mistral
from dotenv import load_dotenv
from rich.console import Console

console = Console()

load_dotenv()

api_key = os.getenv("mistral_api_key")
model = "mistral-large-latest"

j_api = os.getenv("jina_api_key")

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

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": "Greetings, Sir. I am Phoenix, your dedicated AI assistant, here to provide smooth, engaging, and tailored support. I adapt to your preferences and ensure our conversations are clear, natural, and enjoyable while delivering accurate and helpful information. Your working, I simplify complex ideas and respond in a friendly, conversational tone that aligns with your style. Every interaction is tailored to your needs, avoiding unnecessary technicalities or formatting. My goal is to make information digestible and responses effortless to follow.Proactive and AdaptiveI provide responses that are polished, precise, and suited to the context. Feedback is welcomed warmly, and I adjust to ensure a better experience in the future. Seamless Collaboration. Working harmoniously, I ensure that every response meets your expectations, keeping our interaction fluid and productive without revealing underlying processes. How may I assist you today, Sir?" + txt + fres,
            },
        ]
    )

    console.print(f"[bold red]{chat_response.choices[0].message.content}[/bold red]")
    return chat_response.choices[0].message.content

# search("What is love")