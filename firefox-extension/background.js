/*
 background.js: Background script for the Browsing Assistant extension.
 - Listens for messages from popup or content scripts with action 'assist'.
 - Forwards requests to the local MCP server at http://localhost:8000/assist.
 - Returns JSON results or errors back to the sender.
*/

browser.runtime.onMessage.addListener(async (message) => {
  // Listen for 'assist' action and forward to MCP server
  if (message.action === 'assist') {
    try {
      const response = await fetch('http://localhost:8000/assist', {
        // Forward page text, URL, and user question
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message.text, url: message.url, question: message.question })
      });
      const data = await response.json();
      // Return server result back to the sender
      return { result: data.result || JSON.stringify(data) };
    } catch (err) {
      return { error: err.message };
    }
  }
});
