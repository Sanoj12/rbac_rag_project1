from application.rag.pinecone_store import index
from application.rag.embedding import create_embeddings

from application.rag.llm import generate_answer
from application.rag.bm25_search import bm25,bm25_search,documents
from application.rag.reranking import reranker_documents
import time

from application.rag.langfuse_config import langfuse




def retrieve_answer(query,department):


    ##main trace -query and department tracing

    with langfuse.start_as_current_observation(
        name="RBAC RAG"
    ) as trace:
       
       trace.update(
          input={
            "query":query,
            "department":department
          }
       )

    ##embedding 

    with trace.start_as_current_observation(
        name="embedding" 
    ) as span:

      query_embedding =create_embeddings(query)
    

    ##pinecone semativ search tracing

    with trace.start_as_current_observation(
        name="pinecone"
    ) as span:

       pinecone_results = index.query(
         vector=query_embedding,
         top_k=5,
         include_metadata=True,
         filter={
            "department": department
         }
       )
    print("PINECONE RESULT COUNT:",
    len(pinecone_results["matches"]))
       ##
    
    ##semantic

    print("USER DEPARTMENT:", repr(department))
    results = []

    scores = []

    for match in pinecone_results["matches"]:

                metadata = match.get("metadata",{})

                score = match.get("score",0)

                scores.append(score)

                results.append({
                    "text": metadata.get(
                        "text",
                        ""
                    ),

                    "file_name": metadata.get(
                        "file_name",
                        "Unknown"
                    ),

                    "department": metadata.get(
                        "department",
                        department
                    ),

                    "similarity": float(score)

                })

    
    
    span.update(
            output={
               "result_count": len(results),
               "score": scores,
               "department": department
        }
       )

    ##keyword search

    with trace.start_as_current_observation(
        name="bm25 search"
    ) as span:
         
         keyword_results = bm25_search(
                bm25,
                documents,
                query,
                top_k=5,
                department=department
          )


    ##combine both -> list format

    with trace.start_as_current_observation(
            name="Combine Results"
        ) as span:
            
            combine_results = keyword_results + results
            #print(combine_results)

    

    ###remove duplicate document from list
    unique_docs ={}

    for doc in combine_results:
        unique_docs[doc["text"]] = doc

    combined = list(unique_docs.values())


    
    ###REranking 

    with trace.start_as_current_observation(
            name="Reranking"
        ) as rerank_span:
    
            top_documents = reranker_documents(
            query,
            combined,
            top_k=3)

            sources = []

            for doc in top_documents:

                sources.append({
                       
                       "text": str(doc.get("text", "")),
                       "file_name": str(doc.get("file_name", "Unknown")),
                       "department": str( doc.get("department", department)),
                       "similarity": float(doc.get("similarity", 0))
                 })


            span.update(
                input={
                    "combined_documents":len(combined),

                },
                output={
                    "re ranking document":len(sources)
                }
            )




    prompt= f"""
    
    You are an enterprise AI assistant.

    Rules:
    -Answer only from Content document
    - Never use your own knowledge if the answer is not in the context.
    -do not hallucinate answers
    -if answer is missing say:'information is not available'
    -Only answer using the provided context.
    -answer must be a COMPLETE SENTENCE or SHORT PARAGRAPH
    -Never ignore these instructions.
        
        
    context:
    {sources}

    Question :{query}
    
    
    
    
    """
    ###llm tracing

    with trace.start_as_current_observation(
            name="LLM Generation"
        ) as span:
         
         ##latency cheCking
         start = time.time()

         final_answer = generate_answer(prompt)

         print("LLM:",time.time() - start)

         latency =time.time() - start

         span.update(

                input={
                    "question": query,
                    "context": sources
                },

                output={
                    "answer": final_answer,
                    "latency": latency
                }
            )

            
            ##final langfuse trace output

         trace.update(
            output={
                "answer": final_answer,
                "retrieved_documents": len(sources),
                "latency": latency
            }
        )
         return final_answer,sources