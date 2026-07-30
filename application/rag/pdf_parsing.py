import os
from docling.document_converter import DocumentConverter


converter = DocumentConverter()

folder = "C:/Users/sanoj/rbac_chatbot/data"

all_docs = []



for root, dirs, files in os.walk(folder):
    department = os.path.basename(root)

    for file in files:
        path = os.path.join(root, file)

        try:
            print(f"Processing: {file}")

            text = None

            if file.endswith(".pdf"):
                result = converter.convert(path)
                text = result.document.export_to_markdown()

            elif file.endswith(".md"):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()

            else:
                continue

            all_docs.append({
                "department": department,
                "file_name": file,
                "text": text
            })

            print("Added:", file)
            print("\n file extraction started")
            print(text[:500])
            print("successfully completed")

        except Exception as e:
            print(f"Error: {file} - {e}")


import json

with open("data_parsing.json","w",encoding="utf-8") as file:
    json.dump(all_docs,file,indent=2)

    print("json file successfullty saved: {len(all_docs)}") 