# agentic-home-energy/backend/test_llm_router.py

from llm_router import llm_router
from dotenv import load_dotenv
load_dotenv()  # reads .env into os.environ

if __name__ == "__main__":
    prompt = "Hello, what's the weather like today?"
    print(">>> Prompt:\n", prompt)
    reply = llm_router(prompt, max_tokens=50)
    print("\n>>> Response:\n", reply)
