import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document

load_dotenv("ChromaDB/.env")

documents = []
for file in os.listdir("ChromaDB/data"):
    with open(f"ChromaDB/data/{file}") as f:
        raw_document = f.read()
        Document(page_content=raw_document, metadata={"filename": file})
        
embedding = OpenAIEmbeddings()