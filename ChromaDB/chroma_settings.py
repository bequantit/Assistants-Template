import os
import sys
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

load_dotenv("ChromaDB/.env")

PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY")
embeddings = OpenAIEmbeddings()

