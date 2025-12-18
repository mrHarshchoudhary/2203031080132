import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.routes import router as api_router
from app.frontend.routes import router as frontend_router
from app.config import settings

app = FastAPI(
    title="Web Scraper API",
    description="Advanced web scraping with JS rendering and interaction capabilities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(frontend_router)

@app.on_event("startup")
async def startup_event():
    print("Web Scraper API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Web Scraper API shutting down...")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
