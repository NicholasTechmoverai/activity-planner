# Install: pip install google-generativeai
import google.generativeai as genai

# Get your free key from https://aistudio.google.com/app/apikey
genai.configure(api_key="AIzaSyAzfdjtwMMNpQ5qRF34vPvLWehsDPLGvM8")
model = genai.GenerativeModel('gemini-2.0-flash')

def query_model(prompt):
    response = model.generate_content(prompt)
    return response.text

# Test it
result = query_model("What is the capital of France? Explain briefly.")
print(result)