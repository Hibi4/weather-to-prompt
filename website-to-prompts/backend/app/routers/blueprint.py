import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from app.models.schemas import BlueprintRequest, BlueprintResponse
from app.services.scraper import scrape_website
from app.utils.html_cleaner import clean_html
from app.services.ai_pipeline import generate_prompts_from_site

router = APIRouter(prefix="/blueprint", tags=["Blueprint"])

# Temporary in-memory storage until Step 4 (Supabase)
TEMP_BLUEPRINTS: dict[str, BlueprintResponse] = {}

@router.post("/generate", response_model=BlueprintResponse)
async def create_blueprint(payload: BlueprintRequest):
    target_url = str(payload.url)
    try:
        # Step 1: Scrape website with Playwright
        scraped_data = await scrape_website(target_url)

        # Step 2: Clean HTML with BeautifulSoup
        cleaned_dom = clean_html(scraped_data["raw_html"])

        # Step 3: Generate Prompts via OpenRouter Vision LLM
        ai_output = await generate_prompts_from_site(
            url=target_url,
            cleaned_html=cleaned_dom,
            screenshot_b64=scraped_data["screenshot_b64"],
            detected_apis=scraped_data["detected_apis"],
        )

        # Build response object
        blueprint_id = str(uuid.uuid4())
        blueprint = BlueprintResponse(
            id=blueprint_id,
            url=target_url,
            techStack=ai_output.get("techStack", "React, Tailwind, FastAPI, PostgreSQL"),
            frontendPrompts=ai_output.get("frontendPrompts", []),
            backendPrompts=ai_output.get("backendPrompts", []),
            createdAt=datetime.now(timezone.utc).isoformat(),
        )

        # Save in memory temporarily
        TEMP_BLUEPRINTS[blueprint_id] = blueprint
        return blueprint

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

@router.get("/list", response_model=list[BlueprintResponse])
async def list_blueprints():
    return list(TEMP_BLUEPRINTS.values())

@router.get("/{blueprint_id}", response_model=BlueprintResponse)
async def get_blueprint(blueprint_id: str):
    if blueprint_id not in TEMP_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return TEMP_BLUEPRINTS[blueprint_id]