from fastapi import APIRouter, HTTPException
from datetime import datetime
import time

from app.models import (
    HealthResponse,
    ScrapeRequest,
    ScrapeResponse,
    ScrapeResult,
    Interactions
)
from app.services.scraping_service import ScrapingService
from app.scraper.utils import URLUtils

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
async def health_check():
    return HealthResponse()


@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_url(request: ScrapeRequest):
    start_time = time.time()

    # ✅ Validate URL
    is_valid, error_message = URLUtils.validate_url(request.url)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    try:
    
        normalized_url = URLUtils.normalize_url(request.url)

      
        service = ScrapingService()

       
        result = await service.scrape(normalized_url)

        processing_time = time.time() - start_time

        return ScrapeResponse(
    result=ScrapeResult(
        url=normalized_url,
        scrapedAt=datetime.utcnow().isoformat(),  
        meta=result.get("meta"),
        sections=result.get("sections", []),
       interactions=Interactions(
    clicks=result.get("interactions", {}).get("clicks", []),
    scrolls=result.get("interactions", {}).get("scrolls", 0),
    pages=result.get("interactions", {}).get("pages", [])
),

        errors=service.errors
    ),
    strategy=result.get("strategy", "static"),
    processing_time=processing_time
)


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scraping failed: {str(e)}"
        )
