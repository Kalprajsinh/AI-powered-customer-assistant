from fastapi import FastAPI
from pydantic import BaseModel

from app.llm_client import create_qa_client
from app.response import ask_question
from app.vector_store import get_vector_store


class QueryRequest(BaseModel):
    question: str
    session_id: str | None = None


app = FastAPI(title="MG Chat API")


@app.on_event("startup")
async def startup_event():
    app.state.client = create_qa_client()
    app.state.vector_store = get_vector_store("./faiss_db")


@app.get("/")
async def root():
    return {"status": "ok", "message": "MG FastAPI + Redis service is running"}


@app.post("/ask")
async def ask(req: QueryRequest):
    response = ask_question(
        app.state.client,
        app.state.vector_store,
        req.question,
        session_id=req.session_id or "default",
    )
    return response
