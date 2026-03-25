import os
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Reusable "async" function by wrapping sync call
async def get_groq_response(prompt: str, model: str = "openai/gpt-oss-20b") -> str:
    """
    Sends a prompt to the Groq/OpenAI endpoint asynchronously
    by running the sync call in a thread pool.
    """
    client = OpenAI(
        api_key=os.environ.get("GROQ_API_KEY", ""),
        base_url="https://api.groq.com/openai/v1"
    )

    # Run the synchronous .create() in a thread pool
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,  # None = default ThreadPoolExecutor
        lambda: client.responses.create(
            input=prompt,
            model=model
        )
    )

    return response.output_text

# # Example usage
# if __name__ == "__main__":
#     async def main():
#         prompt = "If the weather is 53% rainy and 23 degrees sunny, suggest clothing and best 3 activities"
#         result = await get_groq_response(prompt)
#         print(result)

#     asyncio.run(main())