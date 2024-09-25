import requests

schema = {
    "name": "query_database",
    "description": "Query the internal database containing information about lectures.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The question the user is asking"},
        },
        "required": [
            "query",
        ],
    },
}


def executable(query):
    search_results = requests.post("http://localhost:5000/query", json={"query": query, "k": 1}).json()["results"]
        
    res = "This results where found:\n"    
    for result in search_results:
        res += result["page_content"]
        res += "\n"
        
    return res

query_database_definition = {
    "name": schema["name"],
    "schema": schema,
    "executable": executable,
}