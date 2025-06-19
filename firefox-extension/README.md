# Browsing Assistant Firefox Extension

A minimal Firefox add-on that captures page text, sends it to a local MCP server, and displays formatted responses.

## Files

- **manifest.json**: Extension manifest (v2) declaring permissions (`activeTab`, `storage`, `http://localhost:8000/*`) and default popup.
- **popup.html**: UI markup for the popup. Includes:
  - `<input id="question">` for user queries.
  - `<button id="send">` to trigger requests.
  - `<pre id="result">` to display Markdown-formatted replies.
  - Loads `marked.min.js` (CDN) for Markdown parsing.
- **popup.js**: Logic to:
  1. Query the active tab's `document.body.innerText`.
  2. Send POST to `http://localhost:8000/assist` with `text`, `url`, and `question`.
  3. Render JSON response using `marked.parse()` into the result area.
  4. Supports `/notes` prefix: backend will generate structured student-friendly notes.
- **icon.png**: 48×48 icon used in toolbar and popup.

## Features

- One-click summary of any page.
- `/notes` command: Generates Markdown notes with headings, emojis, bullet points, and LaTeX support.
- YouTube detection: Server handles YouTube URLs separately.
- Markdown rendering powered by [marked.js](https://github.com/markedjs/marked).

## Setup

1. Ensure your MCP server is running at `http://localhost:8000`.
2. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`.
3. Click **Load Temporary Add-on** and select `manifest.json` in this folder.
4. Click the Browsing Assistant icon in the toolbar.
5. Type a query or `/notes` and press Enter or click **Send**.

---

*Note: Requires `marked.min.js` to parse Markdown; CSP in `manifest.json` allows loading from jsDelivr.*
