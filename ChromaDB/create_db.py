import os
from chroma_settings import PERSIST_DIRECTORY, embeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

documents = []
for file in os.listdir("ChromaDB/data"):
    with open(f"ChromaDB/data/{file}") as f:
        raw_document = f.read()
        documents.append(Document(page_content=raw_document, metadata={"filename": file}))


if os.path.exists(PERSIST_DIRECTORY):
    raise Exception(f"Persist directory {PERSIST_DIRECTORY} already exists. Please delete it first.")    

db = Chroma.from_documents(
    documents=documents,
    persist_directory=f"{PERSIST_DIRECTORY}",
    embedding=embeddings,
)
