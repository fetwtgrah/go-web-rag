import ollama
import spliter
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class ChatRequest(BaseModel):
    content: str

@app.post("/chat")
def post_chat(req: ChatRequest):
    question=req.content
    response=ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role":"user",
                "content":question
            }
        ]
    )
    ans=response["message"]["content"]
    return{
        "msg":"请求成功",
        "ans":ans,
    }

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client=QdrantClient(url="http://localhost:6333")
client.recreate_collection(
        collection_name="my_chunk",
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE)

    )

@app.post("/chunk/{path}")
def before_question(path: str):
   spliter.split_md(path)
   return{
       "msg":"成功存入"
   }

import reter
@app.post("/ques")
def after_question(req: ChatRequest):
    result=reter.retrieve(req.content,6)
