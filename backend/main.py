from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .rag import ask_question


# -------------------------
# Create FastAPI application
# -------------------------

app = FastAPI(
    title="AWS Documentation Assistant API",
    description="Backend API for the AWS RAG Assistant",
    version="1.0.0",
)


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Request model
# -------------------------

class QuestionRequest(BaseModel):
    query: str = Field(..., min_length=1)


# -------------------------
# Response model
# -------------------------

class QuestionResponse(BaseModel):
    answer: str
    sources: List[str]


# -------------------------
# Health check
# -------------------------

@app.get("/")
def root():
    return {
        "message": "AWS Documentation Assistant API is running"
    }


# -------------------------
# Ask question
# -------------------------

@app.post("/api/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest):

    answer, sources = ask_question(request.query)

    return {
        "answer": answer,
        "sources": sources,
    }