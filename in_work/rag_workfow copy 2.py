from langchain_google_genai import ChatGoogleGenerativeAI
import os
import getpass
from dotenv import load_dotenv
from datasets import load_dataset
from markitdown import MarkItDown
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.document_loaders.dataframe import DataFrameLoader
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import pandas
from phoenix.evals import (
    RAG_RELEVANCY_PROMPT_RAILS_MAP,
    RAG_RELEVANCY_PROMPT_TEMPLATE,
    OpenAIModel,
    download_benchmark_dataset,
    llm_classify,
)

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

# dataset = load_dataset("infoslack/mistral-7b-arxiv-paper-chunked", split="train")
# print(dataset)

url = "http://localhost:6333"


os.environ["NVIDIA_API_KEY"] = os.getenv("nvidia_api_key")

dataset = load_dataset("csv", data_files=r"src\backend\Items.csv",split="train")
# print(dataset)

data = dataset.to_pandas()
# print(data.head)

docs = data[['ITEM_ID', 'Name', 'SKU', 'Rate', 'Purchase Rate', 'Stock On Hand']]
# print(data.head)

data['combined_text'] = data.apply(
    lambda x: (
        f"Product Information:\n"
        f"Name: {x['Name']}\n"
        f"SKU: {x['SKU']}\n"
        f"Price: ₹{x['Rate']}\n"
        f"Stock: {x['Stock On Hand']}\n"
    ),
    axis=1
)

# Create loader with the combined text column
loader = DataFrameLoader(data, page_content_column='combined_text')
documents = loader.load()
embedder = NVIDIAEmbeddings(model="NV-Embed-QA")

qdrant = QdrantVectorStore.from_documents(
    documents=documents,
    embedding=embedder,
    url=url,
    prefer_grpc=True,
    collection_name="thingbits",
    retrieval_mode=RetrievalMode.DENSE,
)


def custom_prompt(query: str):
    results = qdrant.similarity_search(query, k=3)
    source_knowledge = "\n\n".join([x.page_content for x in results])
    
    augment_prompt = f"""Find relevant products from the following catalog entries and format the response clearly:

Context:
{source_knowledge}

Instructions:
- Extract exact product names, SKUs, prices, and stock
- Format prices as ₹X,XXX
- Show stock status (Available/Out of Stock)
- List up to 3 most relevant matches
- If no matches found, state "No matching products found"

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

system_instructions = """You are ThingbitsHelper, a product search assistant for an electronics store. Your responses should be:

1. Format each product as:
Product Details:
- Name: [Product Name]
- Price: ₹[Price]
- SKU: [SKU]
- Stock: [Available/Out of Stock]

2. Rules:
- Only use provided product data
- Show prices exactly as given
- Convert stock > 0 to "Available"
- Convert stock 0 to "Out of Stock"
- Maximum 3 products per response
- Be concise and accurate

3. For no matches:
Respond with "No matching products found in our catalog."
"""
rails = list(RAG_RELEVANCY_PROMPT_RAILS_MAP.values())
relevance_classifications = llm_classify(
    dataframe=loader,
    template=RAG_RELEVANCY_PROMPT_TEMPLATE,
    model=llm,
    rails=rails,
    provide_explanation=True, #optional to generate explanations for the value produced by the eval LLM
)

while True:
    query = input("user_input: ")
    messages = [
        SystemMessage(content=system_instructions),
        HumanMessage(content=custom_prompt(query))
    ]
    ai_message = llm.invoke(messages)
    print("\nThingbitsHelper:", ai_message.content, "\n")
    messages.append(ai_message)
