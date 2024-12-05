import requests

QWEN_API_URL = "http://qwen_api_server:11434/api/generate"

def generate_recipe(ingredients):
    payload = {
        "model": "qwen",
        "prompt": f"Create a recipe using these ingredients: {ingredients}",
        "max_tokens": 150,
        "stream": False
    }
    try:
        response = requests.post(QWEN_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("text", "No recipe generated.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
