from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from .model import ModelStub

app = FastAPI(title="Helios Vault Backend", version="0.1.0")


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.on_event("startup")
async def startup_event():
    # Initialize model stub (replace with real loader later)
    app.state.model = ModelStub()


@app.get("/")
async def root():
    return {"status": "ok", "app": "Helios Vault", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"healthy": True}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    model: ModelStub = app.state.model
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    reply = model.generate(req.message)
    return ChatResponse(reply=reply, model=model.name)
