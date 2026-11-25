import json
import re
import httpx
from app.config import settings

SYSTEM_PROMPT = """
You are a Senior Full-Stack Software Architect.
Analyze the provided website screenshot, simplified HTML DOM, and network requests.
Reverse-engineer the website into a step-by-step prompt blueprint so a developer can rebuild it from scratch using an AI coding assistant.

RULES:
1. Be concise, clear, and actionable. No filler text.
2. Deduce the required Backend (Database schema, Auth, API routes, business logic) based on the UI features (forms, login, dashboards, pricing, data lists) and network calls.
3. Return ONLY valid JSON matching this exact structure (no markdown code blocks around it):

{
  "techStack": "Recommended stack (e.g., React, Tailwind CSS, FastAPI, PostgreSQL)",
  "frontendPrompts": [
    {
      "step": 1,
      "title": "Design System & Global Layout",
      "prompt": "Detailed copy-pasteable prompt specifying colors, fonts, navbar, and layout..."
    }
  ],
  "backendPrompts": [
    {
      "step": 1,
      "title": "Database Schema & Models",
      "prompt": "Detailed copy-pasteable prompt specifying tables, fields, and relationships..."
    }
  ]
}
"""

async def generate_prompts_from_site(
    url: str,
    cleaned_html: str,
    screenshot_b64: str,
    detected_apis: list[str]
) -> dict:
    """
    Sends the scraped website data to OpenRouter's free Vision LLM.
    """
    user_message = (
        f"Target URL: {url}\n\n"
        f"Detected XHR/API Calls:\n{json.dumps(detected_apis, indent=2)}\n\n"
        f"Simplified HTML Structure:\n{cleaned_html}"
    )

    payload = {
        "models": settings.FREE_VISION_MODELS,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_message},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{screenshot_b64}"
                        },
                    },
                ],
            },
        ],
        "temperature": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": settings.FRONTEND_URL,
        "X-Title": "SiteToPrompts",
    }

    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

    raw_content = result["choices"][0]["message"]["content"]

    # Clean markdown fences if the LLM wrapped the JSON in ```json ... ```
    cleaned_json_str = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_content.strip())

    return json.loads(cleaned_json_str)