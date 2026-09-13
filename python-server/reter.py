from qdrant_client import QdrantClient
import ollama
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")
def retrieve(ques: str,top_n:int,top_k:int):
    client=QdrantClient(url="http://localhost:6333")
    response=ollama.embed(model="bge-m3",input=ques)
    vector=response["embeddings"][0]
    
    result=client.query_points(
            collection_name="my_chunk",
            query=vector,
            limit=top_n #可使用可变参数
        )
        
    candidates = []
    for item in result.points:
        candidates.append({
            "id": item.id,
            "chunk": item.payload["chunk"],  
            "score": item.score  
        })

    pairs = [[ques, c["chunk"]] for c in candidates]
    scores = reranker.predict(pairs)

    for c, s in zip(candidates, scores):
        c["rerank_score"] = float(s)

    ranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    return ranked[:top_k] 


    