"""FastAPI backend exposing /assist endpoint for the browser extension.

Receives JSON payload ({text, url, question}), stores a snippet in state,
delegates to Gemini summarization, and returns a JSON response.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from pydantic import BaseModel, Field, ValidationError

from .state import notes
from .gemini import gemini_summarize

app = FastAPI()

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Add CORS middleware to allow browser extension requests to the FastAPI server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class AssistRequest(BaseModel):
    text: str = Field(..., max_length=20000)
    url: str = Field("", max_length=2000)
    question: str = Field("Summarize this page", max_length=500)

@app.post("/assist")
async def assist(request: Request):
    """Handle the /assist endpoint: parse JSON payload, store a snippet in state, call Gemini summarization, and return the result."""
    try:
        payload = await request.json()
        req = AssistRequest(**payload)
    except ValidationError as e:
        logger.warning("Invalid assist request payload: %s", e)
        return JSONResponse(status_code=400, content={"error": "Invalid request payload."})
    except Exception as e:
        logger.exception("Unexpected error parsing request JSON")
        return JSONResponse(status_code=400, content={"error": "Malformed JSON."})
    text, url, question = req.text, req.url, req.question
    # Store the note
    note_name = url or "page"
    # Sanitize note name length
    note_name = note_name[:100]
    notes[note_name] = text[:200]  # Store first 200 chars as a note
    # Simple logic: echo the question and a preview of the page
    if not text:
        summary = "No content received."
    else:
        try:
            summary = await gemini_summarize(text, url, question)
        except Exception:
            logger.exception("Error during summarization")
            return JSONResponse(status_code=500, content={"error": "Internal server error."})
    return JSONResponse({"result": summary})

# Note: Application entry point removed to prevent accidental public exposure
# Run using uvicorn CLI: uvicorn src.browsingassistant.api:app --host 127.0.0.1 --port 8000