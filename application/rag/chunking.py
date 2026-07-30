#setup and load data from json file 
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

with open("data_parsing.json" , "r",encoding="utf-8") as file:
    all_docs = json.load(file)

##splitter setup


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap=100
)

def chunk_documents(all_docs, text_splitter):
    all_chunks = []

    for doc in all_docs:
        try:
            text = doc["text"]
            department = doc["department"]
            file_name = doc["file_name"]

            chunks = text_splitter.split_text(text) if text else []

            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "department": department,
                    "file_name": file_name,
                    "chunk_id": i,
                    "text": chunk
                })

            print(f"{file_name} - {len(chunks)} chunks")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    return all_chunks


    ##save to json file

import json 

with open("chunking_data.json" ,"w", encoding="utf-8") as file:
    json.dump(all_chunks,file,indent=2)

    print("chunking document successfully save to json file")