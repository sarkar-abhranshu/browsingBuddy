"""FastAPI backend exposing /assist endpoint for the browser extension.

Receives JSON payload ({text, url, question}), stores a snippet in state,
delegates to Gemini summarization, and returns a JSON response.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .state import notes
from .gemini import gemini_summarize

app = FastAPI()

# Add CORS middleware to allow browser extension requests to the FastAPI server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/assist")
async def assist(request: Request):
    """Handle the /assist endpoint: parse JSON payload, store a snippet in state, call Gemini summarization, and return the result."""
    data = await request.json()
    text = data.get("text", "")
    url = data.get("url", "")
    question = data.get("question", "Summarize this page")
    # Store the note
    note_name = url or "page"
    notes[note_name] = text[:200]  # Store first 200 chars as a note
    # Simple logic: echo the question and a preview of the page
    if not text:
        summary = "No content received."
    else:
        summary = await gemini_summarize(text, url, question)
    return JSONResponse({"result": summary})

if __name__ == "__main__":
    """Run the FastAPI app with Uvicorn server on localhost:8000."""
    uvicorn.run(app, host="0.0.0.0", port=8000)