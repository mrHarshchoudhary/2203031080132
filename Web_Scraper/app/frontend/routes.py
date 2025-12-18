from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import time

from app.models import (
    ScrapeRequest,
    ScrapeResponse,
    ScrapeResult,
    Interactions,
)
from app.services.scraping_service import ScrapingService
from app.scraper.utils import URLUtils

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Web Scraper",
            "url": "",
            "result": None,
            "pretty_json": {},
            "has_error": False,
            "error": None,
        },
    )


# -------------------------------------------------
# FORM SUBMIT HANDLER
# -------------------------------------------------
@router.post("/scrape-web", response_class=HTMLResponse)
async def scrape_web(request: Request, url: str = Form(...)):
    start_time = time.time()

    try:
        # Validate URL
        is_valid, error_message = URLUtils.validate_url(url)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)

        normalized_url = URLUtils.normalize_url(url)

        service = ScrapingService()
        raw_result = await service.scrape(normalized_url)

        processing_time = time.time() - start_time

        response = ScrapeResponse(
            result=ScrapeResult(
                url=normalized_url,
                scrapedAt=datetime.utcnow().isoformat(),
                meta=raw_result.get("meta"),
                sections=raw_result.get("sections", []),
                interactions=Interactions(
                    clicks=raw_result.get("interactions", {}).get("clicks", []),
                    scrolls=raw_result.get("interactions", {}).get("scrolls", 0),
                    pages=raw_result.get("interactions", {}).get(
                        "pages", [normalized_url]
                    ),
                ),
                errors=raw_result.get("errors", []),
            ),
            strategy=raw_result.get("strategy", "static"),
            processing_time=processing_time,
        )

        result_dict = response.model_dump()

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Web Scraper",
                "url": url,
                "result": result_dict,
                "pretty_json": result_dict,
                "has_error": False,
                "error": None,
            },
        )

    except Exception as e:
        error_msg = str(e.detail) if hasattr(e, "detail") else str(e)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Web Scraper",
                "url": url,
                "result": None,
                "pretty_json": {},
                "has_error": True,
                "error": error_msg,
            },
        )
