from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Iterable
from pathlib import Path

from .model import get_model, get_model_status

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize model backend. Uses `MODEL_BACKEND` and `MODEL_PATH` env vars.
    model_path = None
    try:
        import os

        model_path = os.getenv("MODEL_PATH")
    except Exception:
        model_path = None

    app.state.model = get_model(model_path=model_path)
    yield


app = FastAPI(title="Helios Vault Backend", version="0.1.0", lifespan=lifespan)
FRONTEND_INDEX = Path(__file__).resolve().parents[1] / "frontend" / "index.html"


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.get("/")
async def root():
    if FRONTEND_INDEX.exists():
        return FileResponse(FRONTEND_INDEX)
    return {"status": "ok", "app": "Helios Vault", "version": "0.1.0"}


@app.get("/status")
async def status():
    return {"status": "ok", "app": "Helios Vault", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"healthy": True, "model": get_model_status(app.state.model)}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    model = app.state.model
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        reply = model.generate(req.message)
        return ChatResponse(reply=reply, model=model.name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    model = app.state.model
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    def iter_reply() -> Iterable[str]:
        try:
            if hasattr(model, "generate_stream"):
                for chunk in model.generate_stream(req.message):
                    yield chunk
            else:
                yield model.generate(req.message)
        except Exception as exc:
            yield f"[error] {exc}"

    return StreamingResponse(iter_reply(), media_type="text/plain")
