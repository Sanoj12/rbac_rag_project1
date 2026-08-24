import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = BASE_DIR / ".env"




load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)



API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        f"GROQ_API_KEY not found in {ENV_FILE}"
    )

print("Groq API key loaded:", True)
print("Key prefix:", API_KEY[:8])


#groq client

client = Groq(
    api_key=API_KEY
)


##generate qestion and answer

def generate_sample_answer(chunk):

    prompt = f"""
You are creating an evaluation dataset for a RAG system.

Create ONE meaningful question and its ground-truth answer
based ONLY on the provided document chunk.

source file:
{chunk["text"]}

rule:

1. the question must be answerable from the source chunk.
2. the ground-truth answer must come only from the source chunk.
3. do not use outside knowledge.
4. do not hallucinate.
5. the question should be useful for RAG evaluation.
6. Return only valid JSON.
7. The ground-truth answer must be a COMPLETE SENTENCE or SHORT PARAGRAPH


Return exactly this format:

{{
    "question": "",
    "ground_truth": ""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    output = response.choices[0].message.content.strip()
    #print(output)

    data = json.loads(output)
    
    return data



#load chunk file


CHUNK_FILE = BASE_DIR / "chunking_data.json"

with open(CHUNK_FILE,"r",encoding="utf-8") as f:
 
       chunks = json.load(f)

#print(chunks[0].keys())




# Ground truth generation

ground_truth = []

OUTPUT_FILE = BASE_DIR / "ground_truth.json"

for i, chunk in enumerate(chunks, start=1):

    try:

        print(f"Processing chunk {i}/{len(chunks)}")

        response = generate_sample_answer(chunk)

        record = {
            "chunk_id": chunk["chunk_id"],
            "department": chunk["department"],
            "file_name": chunk["file_name"],
            "question": response["question"],
            "ground_truth": response["ground_truth"]
        }

        print("Generated record:")
        print(record)

        # Add record to list
        ground_truth.append(record)

        # Save
        with open(OUTPUT_FILE,"w",encoding="utf-8") as f:

            json.dump(ground_truth,f,indent=4)

        print(f"Saved record {i}")

    except Exception as e:

        print(  f"Error processing chunk {i}: {e}",)
       
        print(f"Error message: {e}")
            