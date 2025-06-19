# Browsing Assistant

This repository contains two integrated components:

1. **Python MCP Server** (`src/browsingassistant`): Implements a Model Context Protocol server that summarizes and extracts information from web content using Gemini.
2. **Browser Extension** (`firefox-extension`): A Firefox popup extension that captures page text, sends it to the local MCP server, and displays formatted responses (including structured `/notes` output) using Markdown.

---

## Features

- **Summarize any webpage** with a single click
- **Structured `/notes` command**: Generate student-friendly notes in Markdown with headings, emojis, bullet points, and LaTeX support
- **YouTube transcript support**: Detects YouTube URLs and summarizes transcripts or descriptions
- **CORS-ready API**: FastAPI backend with CORS middleware for seamless extension requests

---

## Project Structure

```
.
├── firefox-extension/
│   ├── manifest.json      Browser extension manifest (manifest v2)
│   ├── popup.html         Extension UI (includes marked.js for Markdown)
│   ├── popup.js           JS logic to query page, send `/assist` requests, and render Markdown
│   └── icon.png           Extension icon
├── src/browsingassistant/
│   ├── api.py             FastAPI app exposing `/assist` endpoint
│   ├── gemini.py          Gemini integration and prompt builder (handles `/notes` format)
│   ├── server.py          MCP stdio server entry point (for MCP clients)
│   └── state.py           In-memory note storage for MCP resources and prompts
├── requirements.txt       Python dependencies (FastAPI, httpx, mcp)
├── pyproject.toml         Project metadata and dependencies
├── uv.lock                Lockfile for `uv` environment tool
└── README.md              This file
```

---

## Quickstart

### 1. Setup Python environment

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the MCP server

Use the VS Code task or run directly:

```powershell
# VS Code task: "Run BrowsingAssistant MCP Server"
.venv\Scripts\python.exe -m browsingassistant

# Or with uvicorn:
uvicorn src.browsingassistant.api:app --reload --host 0.0.0.0 --port 8000
```

### 3. Load the Firefox extension

1. Open `about:debugging#/runtime/this-firefox` in Firefox.
2. Click **"Load Temporary Add-on"** and select `firefox-extension/manifest.json`.
3. The **Browsing Assistant** icon should appear in your toolbar.

### 4. Use the Extension

- Click the extension icon on any webpage.
- Type a question (e.g., `Summarize this page`).
- For structured notes, start with `/notes` and hit **Enter**.
- Responses render in Markdown with headings, emojis, and more.

---