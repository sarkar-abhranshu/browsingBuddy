# Browsing Assistant MCP Firefox Extension

This is a minimal Firefox extension that lets you send the current page's content to your local MCP server and display its response.

## How it works
- Click the extension icon to open the popup.
- Click "Send Page to MCP" to send the current page's text and URL to your MCP server (assumed at http://localhost:8000/assist).
- The response from the server is shown in the popup.

## Setup
1. Go to `about:debugging#/runtime/this-firefox` in Firefox.
2. Click "Load Temporary Add-on" and select the `manifest.json` file in this folder.
3. Make sure your MCP server is running and listening for POST requests at `/assist`.

## Customization
- Replace `icon.png` with your own 48x48 icon.
- Update the MCP server endpoint in `popup.js` if needed.

---

This is a minimal scaffold. You can extend it to support more features, authentication, or a richer UI as needed.
