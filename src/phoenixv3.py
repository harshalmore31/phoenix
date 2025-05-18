from langchain_community.chat_models import ChatLiteLLM
from dotenv import load_dotenv
load_dotenv()   

llm = ChatLiteLLM(
    model="gemini/gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "Hi, How are you",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)

