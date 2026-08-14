
from pathlib import Path
from dotenv import load_dotenv
import os

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Exact .env file
ENV_FILE = BASE_DIR / ".env"

print("Loading .env from:")
print(ENV_FILE)

# Force .env to override existing environment variables
load_dotenv(
    ENV_FILE,
    override=True
)

api_key = os.getenv("GROQ_API_KEY")

print("Key loaded:", api_key is not None)

if api_key:
    print("Key prefix:", api_key[:8])
    print("Key length:", len(api_key))
else:
    print("GROQ_API_KEY not found")