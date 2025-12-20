from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from .model import get_model

app = FastAPI(title="Helios Vault Backend", version="0.1.0")


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.on_event("startup")
async def startup_event():
    # Initialize model backend. Uses `MODEL_BACKEND` and `MODEL_PATH` env vars.
    model_path = None
    try:
        import os

        model_path = os.getenv("MODEL_PATH")
    except Exception:
        model_path = None

    app.state.model = get_model(model_path=model_path)


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
