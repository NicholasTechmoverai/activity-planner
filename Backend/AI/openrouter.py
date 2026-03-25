import requests

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [{"role": "user", "content": "Hello"}]
    }
)