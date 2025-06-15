# BrowsingAssistant MCP server

MCP-powered assistant for day-to-day browsing tasks

## Features
- Summarize web pages
- Extract information from web content
- Automate simple browsing actions
- Modular and extensible for future features

## Project Structure
- MCP server powered by Python and the Model Context Protocol
- Virtual environment managed in `.venv`
- Main entry: `browsingassistant` module

## Setup
1. Ensure Python 3.11+ is installed
2. Install dependencies:
   ```powershell
   uv sync --dev --all-extras
   ```
3. To run the server:
   ```powershell
   .venv\Scripts\python.exe -m browsingassistant
   ```

## VS Code Integration
- The `.vscode/mcp.json` file is preconfigured for debugging and running the MCP server in VS Code.

## SDK and Documentation
- SDK: https://github.com/modelcontextprotocol/create-python-server
- More info: https://modelcontextprotocol.io/llms-full.txt

---

## Components

### Resources

The server implements a simple note storage system with:
- Custom note:// URI scheme for accessing individual notes
- Each note resource has a name, description and text/plain mimetype

### Prompts

The server provides a single prompt:
- summarize-notes: Creates summaries of all stored notes
  - Optional "style" argument to control detail level (brief/detailed)
  - Generates prompt combining all current notes with style preference

### Tools

The server implements one tool:
- add-note: Adds a new note to the server
  - Takes "name" and "content" as required string arguments
  - Updates server state and notifies clients of resource changes

## Configuration

[TODO: Add configuration details specific to your implementation]

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "BrowsingAssistant": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\Users\abhra\OneDrive\Desktop\Code\mcpBrowsingAssistant",
        "run",
        "BrowsingAssistant"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "BrowsingAssistant": {
      "command": "uvx",
      "args": [
        "BrowsingAssistant"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory C:\Users\abhra\OneDrive\Desktop\Code\mcpBrowsingAssistant run browsingassistant
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.