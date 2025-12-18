import platform
from app.scraper.static_scraper import StaticScraper
from app.scraper.js_scraper import JSScraper

class ScrapingService:
    def __init__(self):
        self.errors = []
        self.interactions = {
            "clicks": [],
            "scrolls": 0,
            "pages": []
        }

    async def scrape(self, url: str):
        # ✅ ALWAYS try JS first
        scraper = JSScraper(url)

        scraper.errors = self.errors
        scraper.interactions = self.interactions

        return await scraper.scrape()
