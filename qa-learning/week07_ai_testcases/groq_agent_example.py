import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables (from .env file)
from pathlib import Path
env_path = Path(r"D:\Shafeeque\AI skilled QA\qa-learning-journey\qa-learning\.env")
load_dotenv(dotenv_path=env_path)

# Initialize the Groq client
# Make sure you have GROQ_API_KEY set in your .env file
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise SystemExit("Error: Please set your GROQ_API_KEY in the .env file.")

client = Groq(api_key=api_key)

print("Groq Client Initialized! Sending a test prompt to LLaMA 3...\n")

# A simple AI Agent call using the ultra-fast LLaMA 3 model
completion = client.chat.completions.create(
    model="llama-3.1-8b-instant", # The latest LLaMA 3.1 8B model hosted by Groq
    messages=[
        {
            "role": "system",
            "content": "You are a highly intelligent and lightning-fast AI QA Engineer."
        },
        {
            "role": "user", 
            "content": "Write exactly two sentences explaining what an AI Agent is."}
    ],
    temperature=0.5,
)

print("--- AI Response ---")
print(completion.choices[0].message.content)
print("-------------------")
