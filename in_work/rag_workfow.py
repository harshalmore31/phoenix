from langchain_google_genai import ChatGoogleGenerativeAI
import os
import getpass
from dotenv import load_dotenv
from datasets import load_dataset
from markitdown import MarkItDown
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.document_loaders.dataframe import DataFrameLoader
from langchain_qdrant import QdrantVectorStore
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import pandas

load_dotenv()

# md = MarkItDown()
# content = md.convert_url("https://arxiv.org/html/1706.03762v7")
# result = content.text_content


# data_set = load_dataset("text", data_files=result)

# client = OpenAI(
#   api_key= os.getenv("nvidia_api_key"),
#   base_url="https://integrate.api.nvidia.com/v1"
# )
# response = client.embeddings.create(
#     input=["What is the capital of France?"],
#     model="nvidia/llama-3.2-nv-embedqa-1b-v2",
#     encoding_format="float",
#     extra_body={"input_type": "query", "truncate": "NONE"}
# )


# url = os.getenv("QDRANT_URL")
# api_key = os.getenv("QDRANT_KEY")

url = "http://localhost:6333"


dataset = load_dataset("infoslack/mistral-7b-arxiv-paper-chunked", split="train")
# print(dataset)


os.environ["NVIDIA_API_KEY"] = os.getenv("nvidia_api_key")

data = dataset.to_pandas()
# print(data.head)

docs = data[['chunk','source']]

loader = DataFrameLoader(docs, page_content_column="chunk")
documents = loader.load()
embedder = NVIDIAEmbeddings(model="NV-Embed-QA")

qdrant = QdrantVectorStore.from_documents(
    documents=documents,
    embedding=embedder,
    url=url
)

query = "What do you know about Mistral AI"

def custom_prompt(query: str):
    results = qdrant.similarity_search(query,k=3) 
    source_knowledge = "\n".join([x.page_content for x in results])
    augment_prompt = f"""Using the context below, answer the query:

    Contexts:
    {source_knowledge}

    Query: {query}"""
    return augment_prompt

# print(custom_prompt(ui))

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
)

messages = [
    SystemMessage(content="You are an helpful assistant"),
    HumanMessage(content=custom_prompt(query))
]

ai_message = llm.invoke(messages)
print(ai_message.content)
