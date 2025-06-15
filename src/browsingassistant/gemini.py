# Gemini API integration for summarization
import os
import httpx
import dotenv

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"
# To use Gemini 2.5 Flash, use:
# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

def is_youtube_url(url: str) -> bool:
    return "youtube.com/watch" in url or "youtu.be/" in url

def build_gemini_prompt(text: str, url: str, question: str) -> str:
    if question.startswith("/notes"):
        return f"""Generate structured, student-friendly notes from the content below. Use this format:

## 📌 Short heading or topic name

✅ Summary in simple language.

🧠 Formulas, code snippets, or diagrams (if mentioned)

📊 Examples or real-life applications

⚠️ Tips or common mistakes

Use Markdown formatting, emojis, bullet points, and LaTeX for math if needed.

Text:
{text}
"""
    elif is_youtube_url(url):
        return f"Summarize the following YouTube video transcript or description.\n\n{question}\n\n{text}"
    else:
        return f"Summarize the following news article or web page.\n\n{question}\n\n{text}"

async def gemini_summarize(text: str, url: str, question: str) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key not set. Set GEMINI_API_KEY environment variable."
    prompt = build_gemini_prompt(text, url, question)
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Gemini API error: {e}"
