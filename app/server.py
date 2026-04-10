from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.llm_client import create_qa_client
from app.response import ask_question
from app.vector_store import get_vector_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryRequest(BaseModel):
    question: str
    session_id: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        logger.info("Initializing LLM client...")
        app.state.client = create_qa_client()
        logger.info("LLM client ready.")

        logger.info("Loading vector store...")
        app.state.vector_store = get_vector_store("./faiss_db")
        logger.info("Vector store ready.")
    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)
        # Still allow app to start so the port binds; /ask will return 503
        app.state.client = None
        app.state.vector_store = None

    yield  # app runs here

    # Shutdown (nothing to clean up)


app = FastAPI(title="MG Chat API", lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "ok", "message": "MG FastAPI + Redis service is running"}


@app.get("/health")
async def health():
    ready = app.state.client is not None and app.state.vector_store is not None
    return {"status": "ready" if ready else "initializing", "ready": ready}


@app.post("/ask")
async def ask(req: QueryRequest):
    if app.state.client is None or app.state.vector_store is None:
        raise HTTPException(status_code=503, detail="Service is still initializing. Try again shortly.")

    response = ask_question(
        app.state.client,
        app.state.vector_store,
        req.question,
        session_id=req.session_id or "default",
    )
    return response