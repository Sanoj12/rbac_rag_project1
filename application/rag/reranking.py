#from FlagEmbedding import FlagReranker
from sentence_transformers import CrossEncoder
import traceback

# reranker = FlagReranker(
#     "BAAI/bge-reranker-base",
#      use_fp16=False  #gpu support false
#)


reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    device="cpu"
)

def reranker_documents(query,documents,top_k=3):
    """ re rank retrieved documents based on relevance"""

    try:

        if not documents:
            return []

        ##create query-documents

        query_doc = [
            [query,doc["text"]]
            for doc in documents
        ]

        ##caclualte score
        scores = reranker.predict(query_doc)

        scores_doc = []

        for doc, score in zip(documents, scores):
             scores_doc.append({
                "text": doc,
                "score": score
        })



        scores_doc.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scores_doc[:top_k]

    except Exception as e:
        print(f"re ranking err:{e}")
        traceback.print_exc()
        return []

