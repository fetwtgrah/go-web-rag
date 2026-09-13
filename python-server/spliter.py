import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
def split_md(path: str):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks=[]
        current_chunks=[]
        for line in text.split("\n"):
                if line.startswith("#"):
                        if current_chunks:
                                chunks.append(
                                        "\n".join(current_chunks)
                                )
                        current_chunks=[]

                current_chunks.append(line)
        if current_chunks:
               chunks.append(
                      "\n".join(current_chunks)
               )
        result=[]
        for i,chunk in enumerate(chunks,start=1):
               item={
                      "id":i,
                      "chunk":chunk
               }
               result.append(item)

        # embedding
    
        points=[]
        for item in result:
            response=ollama.embed(
                          model="bge-m3",
                          input=item["chunk"]
                )
            vector=(response["embeddings"][0])

            points.append(
                   PointStruct(
                          id=item["id"],
                          vector=vector,
                          payload={"chunk":item["chunk"]}
                   )
            )

        client=QdrantClient(url="http://localhost:6333")
        client.upsert(
               collection_name="my_chunk",
               points=points
        )
