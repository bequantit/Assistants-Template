import os
import sys
__import__("pysqlite3")
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv("ChromaDB/.env")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY")
embeddings = OpenAIEmbeddings()

