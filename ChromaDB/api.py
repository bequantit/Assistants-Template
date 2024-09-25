import os
from dotenv import load_dotenv
from chroma_settings import PERSIST_DIRECTORY, embeddings
from langchain_chroma import Chroma
from flask import Flask, request, jsonify

load_dotenv("ChromaDB/.env")
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY")

if not os.path.exists(PERSIST_DIRECTORY):
    raise Exception(f"Persist directory {PERSIST_DIRECTORY} does not exist. Please create it first.")

db = Chroma(persist_directory=f"{PERSIST_DIRECTORY}", embedding_function=embeddings)

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    data = request.json

    query = data.get('query')
    k = data.get('k', 1)
    
    search_results = db.similarity_search(query, k=k)
    results = []
    for result in search_results:
        results.append({
            "metadata": result.metadata,
            "page_content": result.page_content,
        })
        
    return jsonify({"results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)
