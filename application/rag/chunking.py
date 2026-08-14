import json
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Load data
with open("data_parsing.json", "r", encoding="utf-8") as file:
    all_docs = json.load(file)


# Setup splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


def chunk_documents(all_docs, text_splitter):
    all_chunks = []

    for doc in all_docs:
        try:
            text = doc.get("text", "")
            department = doc.get("department", "")
            file_name = doc.get("file_name", "unknown")

            if not text:
                print(f"No text found: {file_name}")
                continue

            chunks = text_splitter.split_text(text)

            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "department": department,
                    "file_name": file_name,
                    "chunk_id": i,
                    "text": chunk
                })

            print(f"{file_name} - {len(chunks)} chunks")

        except Exception as e:
            print(f"Error processing document: {e}")

    return all_chunks



all_chunks = chunk_documents(all_docs, text_splitter)


# Save chunks
with open("chunking_data.json", "w", encoding="utf-8") as file:
    json.dump(all_chunks, file, indent=2, ensure_ascii=False)

print(f"✅ Chunking completed: {len(all_chunks)} chunks saved")
