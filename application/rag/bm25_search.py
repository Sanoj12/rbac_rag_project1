import json

from rank_bm25 import BM25Okapi


with open("chunking_data.json", "r", encoding="utf-8") as f:
    documents = json.load(f)


def bm25_index(documents):
    """create bm index"""
    texts = [doc["text"].lower().split() for doc in documents]

    bm25 = BM25Okapi(texts)

    return bm25

def bm25_search(bm25,documents,query,top_k=3,department=None):
    """search document"""
   

    try:

        ##tokenize user query
       tokenize_query= query.lower().split()


       ##get bm25 sscore

       scores = bm25.get_scores(tokenize_query)


       results = []

       for doc ,score in zip(documents,scores):

        ##role filtering
          if department and doc.get("department") != department:
              continue

          results.append({
            "text":doc["text"],
            "department":doc.get("department"),
            "score":score
          })

          
          ##sorted by score high -> low

       results.sort(key=lambda x:x["score"],reverse=True)
        
       return results[:top_k]
    

    except Exception as e:
        print(f"bm25 search err:{e}")
    


bm25 = bm25_index(documents)