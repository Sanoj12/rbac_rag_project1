from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


if api_key:
    print("API key:", api_key[:8])
else:
    print("GROQ_API_KEY not found")

client = Groq(api_key=api_key)


def generate_answer(prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


print(generate_answer("What is RAG?"))