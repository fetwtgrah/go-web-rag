import ollama
from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
profile={
    "name":"fresh",
    "content":"a passionate worker",
}

class ChatRequest(BaseModel):
    content: str

@app.get("/chat")
def get_profile():
    return profile
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
