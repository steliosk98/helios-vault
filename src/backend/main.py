from fastapi import FastAPI

app = FastAPI(title="Helios Vault Backend", version="0.1.0")


@app.get("/")
async def root():
    return {"status": "ok", "app": "Helios Vault", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"healthy": True}
