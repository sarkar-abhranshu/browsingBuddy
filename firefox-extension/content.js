/*
content.js: Content script for keyboard shortcut handling.
- Listens for Ctrl+Q keyboard shortcut
- Creates a floating UI overlay when triggered
- Handles user input and sends requests to background script
*/

//Create and inject the floating UI
function createFloatingUI() {
  //Remove existing UI if present
  const existing = document.getElementById("browsing-assistant-overlay");
  if (existing) {
    existing.remove();
    return;
  }

  //Create overlay container
  const overlay = document.createElement("div");
  overlay.id = "browsing-assistant-overlay";
  overlay.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    width: 350px;
    background: #ffffff;
    border: 2px solid #4a90e2;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    z-index: 10000;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 14px;
    padding: 16px;
  `;

  //Create title
  const title = document.createElement("div");
  title.textContent = "Browsing Assistant";
  title.style.cssText = `
    font-weight: bold;
    margin-bottom: 12px;
    padding-right: 20px;
    color: #333;
  `;

  // Create input field
  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "Ask something about this page...";
  input.style.cssText = `
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 8px;
    box-sizing: border-box;
    outline: none;
  `;

  // Create result area
  const result = document.createElement("div");
  result.style.cssText = `
    max-height: 200px;
    overflow-y: auto;
    padding: 8px;
    background: #f8f9fa;
    border-radius: 4px;
    white-space: pre-wrap;
    font-size: 12px;
    display: none;
    border: 1px solid #e9ecef;
  `;

  // Handle Enter key and send requests
  input.addEventListener("keydown", async (event) => {
    if (event.key === "Enter") {
      const question = input.value.trim();
      if (!question) return;

      result.style.display = "block";
      result.textContent = "Processing...";

      try {
        // Send message to background script
        const response = await browser.runtime.sendMessage({
          action: "assist",
          text: document.body.innerText,
          url: window.location.href,
          question: question,
        });

        if (response.error) {
          result.textContent = "Error: " + response.error;
        } else {
          result.textContent = response.result;
        }
      } catch (error) {
        result.textContent = "Error: " + error.message;
      }
    } else if (event.key === "Escape") {
      overlay.remove();
    }
  });

  // Add close button
  const closeBtn = document.createElement("button");
  closeBtn.textContent = "x";
  closeBtn.style.cssText = `
    position: absolute;
    top: 8px;
    right: 12px;
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #666;
    line-height: 1;
    padding: 0;
    width: 20px;
    height: 20px;
  `;
  closeBtn.onclick = () => overlay.remove();

  // Add elements to overlay
  overlay.appendChild(closeBtn);
  overlay.appendChild(title);
  overlay.appendChild(input);
  overlay.appendChild(result);

  // Add to page and focus input
  document.body.appendChild(overlay);
  input.focus();
}

// Listen for Ctrl+Q keyboard shortcut
document.addEventListener("keydown", (event) => {
  if (event.ctrlKey && event.key.toLowerCase() === "q") {
    event.preventDefault();
    createFloatingUI();
  }
});
