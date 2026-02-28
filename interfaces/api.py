from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from core.agent import chat, clear_history
import os

app - FastAPI()

class MessageRequest(BaseModel):
    message:str

@app.post("/chat")
async def chat_endpoint(request: MessageRequest):
    response =chat(request.message)
    return{"response": response}

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("interface/templates/index.html", "r") as f:
        return f.read()