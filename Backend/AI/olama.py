# # Install Ollama (one command)
# curl -fsSL https://ollama.com/install.sh | sh

# # Run a model
# ollama run llama3.2

# # Use as API (OpenAI-compatible)
# curl http://localhost:11434/v1/chat/completions \
#   -d '{"model":"llama3.2","messages":[{"role":"user","content":"Hello"}]}'



# pip install ollama
import ollama

response = ollama.chat(
    model='phi',  # or 'llama3.2', 'mistral', 'gemma2'
    messages=[{'role': 'user', 'content': 'What is the capital of France?'}]
)
print(response['message']['content'])