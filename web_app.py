"""
Web app entry point: FastAPI + single-page form.

Flow: browser shows a form -> user types a situation -> POST / runs the
same rag pipeline as the CLI (retrieve + Gemini generate) -> the answer
renders back on the same page.

Run locally:  python web_app.py       (or  uvicorn web_app:app --reload)
On Render:    uvicorn web_app:app --host 0.0.0.0 --port $PORT
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from rag.retrieve import LawRetriever
from rag.generate import generate_answer

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

retriever = LawRetriever()

app = FastAPI(title="Legal Section Finder")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"query": "", "answer": None, "matches": []},
    )


@app.get("/health", response_class=HTMLResponse)
def health():
    return "ok"


@app.post("/", response_class=HTMLResponse)
def answer_form(request: Request, query: str = Form(...)):
    if not query.strip():
        return templates.TemplateResponse(
            request,
            "index.html",
            {"query": query, "answer": None, "matches": []},
        )

    try:
        matches = retriever.retrieve(query)
        answer = generate_answer(query, matches)
    except Exception as exc:
        answer = (
            "Something went wrong while talking to the AI service. "
            f"Error: {exc}"
        )
        matches = []

    return templates.TemplateResponse(
        request,
        "index.html",
        {"query": query, "answer": answer, "matches": matches},
    )


if __name__ == "__main__":
    import uvicorn

    reload = os.environ.get("APP_RELOAD", "0") == "1"
    uvicorn.run(
        "web_app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        reload=reload,
    )