// popup.js: Handles UI interactions in the browser extension popup.
// - Queries active tab text
// - Sends data to MCP server at /assist
// - Renders Markdown responses via marked.js

document.getElementById('send').addEventListener('click', async () => {
  const question = document.getElementById('question').value.trim();
  // const isNotes = question.startsWith("/notes");  // not needed: backend handles `/notes`

  document.getElementById('result').textContent = 'Processing...';

  const [tab] = await browser.tabs.query({active: true, currentWindow: true});
  browser.tabs.executeScript(tab.id, {code: 'document.body.innerText'}).then(async (results) => {
    const pageText = results[0];
    // Send to MCP server (assumes running at localhost:8000)
    const response = await fetch('http://localhost:8000/assist', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: pageText, url: tab.url, question})
    });

    const data = await response.json();
    const output = data.result || JSON.stringify(data);

    // Preserve Markdown formatting
    document.getElementById('result').innerHTML = marked.parse(output);
  }).catch(e => {
    document.getElementById('result').textContent = 'Error: ' + e;
  });
});

// Trigger assistant on Enter key in the input box
const questionInput = document.getElementById('question');
questionInput.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    document.getElementById('send').click();
  }
});
