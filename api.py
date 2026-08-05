"""FastAPI wrapper exposing the RAG pipeline (for Azure Container Apps / any container host).

Run locally:  uvicorn api:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from rag.generate.answer import answer

app = FastAPI(title="prod-rag", version="1.0.0")


class AskRequest(BaseModel):
    question: str


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest) -> dict:
    """Retrieve → rerank → generate → enforce citations. Returns answer + citations."""
    return answer(req.question)
