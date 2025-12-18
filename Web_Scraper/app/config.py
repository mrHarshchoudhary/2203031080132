from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    APP_NAME: str = "Web Scraper"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Scraping settings
    REQUEST_TIMEOUT: int = 30
    PLAYWRIGHT_TIMEOUT: int = 30000
    MAX_SECTIONS: int = 50
    MAX_RAW_HTML_LENGTH: int = 10000
    
    # JavaScript rendering settings
    USE_JS_THRESHOLD: int = 100  # Min characters to consider static content sufficient
    WAIT_FOR_NETWORK_IDLE: bool = True
    WAIT_FOR_SELECTOR_TIMEOUT: int = 5000
    
    # Interaction settings
    MAX_SCROLLS: int = 3
    MAX_PAGES: int = 3
    SCROLL_DELAY: int = 1000
    
    # Filtering settings
    NOISE_SELECTORS: list = [
        '[class*="cookie"]',
        '[class*="banner"]',
        '[class*="modal"]',
        '[class*="popup"]',
        '[class*="overlay"]',
        '[class*="newsletter"]',
        '[class*="subscribe"]',
        '[id*="cookie"]',
        '[id*="banner"]',
        '[id*="modal"]',
        '[id*="popup"]'
    ]
    
    class Config:
        env_file = ".env"

settings = Settings()