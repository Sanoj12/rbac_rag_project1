from pathlib import Path
import os

from dotenv import load_dotenv
from groq import Groq




BASE_DIR = Path(__file__).resolve().parents[1]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    ENV_FILE,
    override=True
)

# GET GROQ API KEY


API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        f"GROQ_API_KEY not found in {ENV_FILE}"
    )


print("Groq API key loaded:", True)
print("Key prefix:", API_KEY[:8])


# GROQ CLIENT

client = Groq(
    api_key=API_KEY.strip()
)

# GENERATE ANSWER

def generate_answer(prompt):

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

    )

    return response.choices[0].message.content