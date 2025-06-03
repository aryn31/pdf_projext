import requests

def query_local_llm(prompt: str, model_name="llama3.2"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]
