# from langchain_google_genai import ChatGoogleGenerativeAI
import os
# import getpass
from dotenv import load_dotenv
from datasets import load_dataset
# from markitdown import MarkItDown
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.document_loaders.dataframe import DataFrameLoader
from langchain_qdrant import QdrantVectorStore
from langchain.schema import SystemMessage, HumanMessage, AIMessage
# import pandas
import cohere

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
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(input_files=[r'in_work/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf'], file_extractor=file_extractor).load_data()

# for doc in documents:
#     print(doc.text)
#     print("-" * 50) 

# context = "\n\n".join([doc.text for doc in documents])

# data_set = load_dataset("text", data_files=context)


url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_KEY")

# url = "http://localhost:6333"


# dataset = load_dataset("pdf", data_files=r"in_work/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf",split="train")
# print(dataset)


os.environ["NVIDIA_API_KEY"] = os.getenv("nvidia_api_key")

# data = dataset.to_pandas()
# # print(data.head)

# docs = data[['chunk','source']]
texts = [doc.text for doc in documents]

# loader = DataFrameLoader(context, page_content_column="chunk")
# documents = loader.load()
embedder = NVIDIAEmbeddings(model="NV-Embed-QA")

from langchain.text_splitter import TokenTextSplitter

# Create a text splitter that respects the 512 token limit
text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=0)

# Extract text from documents
texts = [doc.text for doc in documents]

# Split texts into chunks that fit within token limit
split_texts = []
for text in texts:
    splits = text_splitter.split_text(text)
    split_texts.extend(splits)


# Modified to check if collection exists and reuse
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseException

client = QdrantClient(url=url, api_key=api_key)
collection_name = "my_rag_collection"  # Replace with your desired collection name

try:
    client.get_collection(collection_name=collection_name)
    print(f"Collection '{collection_name}' already exists, using it.")
    qdrant = QdrantVectorStore(client=client, collection_name=collection_name, embedding=embedder)
except ResponseException as e:
    if e.status_code == 404:
        print(f"Collection '{collection_name}' does not exist, creating a new one.")
        qdrant = QdrantVectorStore.from_texts(
            texts=split_texts,
            embedding=embedder,
            url=url,
            api_key=api_key,
            timeout=300,
            collection_name=collection_name
        )
    else:
      raise
# query = "What do you know about Mistral AI"

def custom_prompt(query: str):
    results = qdrant.similarity_search(query,k=5) 
    source_knowledge = "\n".join([x.page_content for x in results])
    augment_prompt = f"""Using the context below, answer the query:

    Contexts:
    {source_knowledge}

    Query: {query}"""
    return augment_prompt


api_key = os.getenv("cohere_api_key")

co = cohere.ClientV2(api_key)

while 1:
    user_query = input("Query : ")
    # Send query to Cohere model
    augmented_query = custom_prompt(user_query)
    system_instruct = f"You are an helpful assistant, if you don't know an answer, you check the retrevial results {augmented_query}"
    # fq = system_instruct + augmented_query

    response = co.chat(
        model="command-r-plus",
        messages=[{"role": 'system', "content": system_instruct},
                  {"role": 'user', "content": user_query}],
    )
    print(response.message.content[0].text)