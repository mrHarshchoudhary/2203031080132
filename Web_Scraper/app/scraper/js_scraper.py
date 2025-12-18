import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Page

from app.scraper.base import BaseScraper
from app.scraper.static_scraper import StaticScraper
from app.config import settings
from datetime import datetime

class JSScraper(BaseScraper):
    """
    JavaScript-rendered scraper using Playwright
    """

    def __init__(self, url: str):
        # ✅ Call parent __init__ to properly set up interactions
        super().__init__(url)
        self.page: Optional[Page] = None
        self.browser = None

    async def scrape(self) -> Dict[str, Any]:
        try:
            async with async_playwright() as p:
                self.browser = await p.chromium.launch(
                    headless=True,
                    args=["--disable-blink-features=AutomationControlled"],
                )

                context = await self.browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120 Safari/537.36"
                    ),
                )

                self.page = await context.new_page()

                # ✅ Log that we're starting
                print(f"Starting JS scraper for: {self.url}")
                print(f"Initial interactions state: {self.interactions}")

                await self.page.goto(self.url, wait_until="domcontentloaded", timeout=30000)
                await self._wait_for_page_ready()
                await self._remove_noise()

                # ✅ Perform interactions
                await self._perform_interactions()

                # ✅ Log after interactions
                print(f"After interactions - clicks: {len(self.interactions['clicks'])}, scrolls: {self.interactions['scrolls']}")

                # Get final HTML
                html = await self.page.content()

                # Parse HTML using StaticScraper - but preserve our interactions
             
                static_scraper = StaticScraper(self.url)
                
                # ✅ Get the static scraping result
               
                result = static_scraper.scrape_from_html(html)
                
                # ✅ PRESERVE OUR INTERACTIONS
                result["interactions"] = self.interactions  # This should have clicks and scrolls
                result["strategy"] = "js"
                
                # ✅ Also preserve errors
                if self.errors:
                    result["errors"] = self.errors + result.get("errors", [])
                
                print(f"Final result interactions: {result.get('interactions')}")
                return result

        except Exception as e:
            self.errors.append({"message": str(e), "phase": "render"})
            # Fall back to static but preserve what we have
            static_result = await StaticScraper(self.url).scrape()
            static_result["interactions"] = self.interactions
            static_result["errors"] = self.errors + static_result.get("errors", [])
            return static_result

        finally:
            if self.browser:
                await self.browser.close()
    # ------------------------------------------------------------------
    # PAGE WAIT
    # ------------------------------------------------------------------

    async def _wait_for_page_ready(self):
        try:
            await self.page.wait_for_function(
                "() => document.readyState === 'complete'", timeout=15000
            )
            await self.page.wait_for_selector("body", timeout=10000)
            await self.page.wait_for_selector("button, a", timeout=5000)
            await asyncio.sleep(1)
        except:
            pass

    # ------------------------------------------------------------------
    # REMOVE NOISE
    # ------------------------------------------------------------------

    async def _remove_noise(self):
        selectors = [
            '[id*="cookie"]',
            '[class*="cookie"]',
            '[aria-label*="cookie"]',
            '[class*="consent"]',
        ]
        for sel in selectors:
            try:
                for el in await self.page.query_selector_all(sel):
                    await el.evaluate("el => el.remove()")
            except:
                pass

    # ------------------------------------------------------------------
    # INTERACTIONS
    # ------------------------------------------------------------------

    async def _perform_interactions(self):
        """Perform all interactions"""
        print("Starting interactions...")
        await self._scroll_page()
        await self._click_buttons()
        await self._handle_pagination()
        print(f"Completed interactions: {self.interactions}")

    async def _scroll_page(self):
        """Scroll the page and count scrolls"""
        try:
            print("Starting to scroll...")
            for i in range(settings.MAX_SCROLLS):
                # Scroll to bottom
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                
                # ✅ INCREMENT SCROLLS
                self.interactions["scrolls"] += 1
                print(f"Scroll #{i+1} completed. Total scrolls: {self.interactions['scrolls']}")
                
                await asyncio.sleep(2)
                
                # Check if we're at the bottom
                current_position = await self.page.evaluate("window.pageYOffset + window.innerHeight")
                total_height = await self.page.evaluate("document.body.scrollHeight")
                
                if current_position >= total_height:
                    print("Reached bottom of page")
                    break
                    
        except Exception as e:
            error_msg = f"Scroll error: {str(e)}"
            self.errors.append({"message": error_msg, "phase": "scroll"})
            print(error_msg)

    async def _click_buttons(self):
        """Click interactive elements"""
        selectors = [
            'button',
            'a',
            '[role="button"]',
            '[aria-expanded]',
            'button:has-text("More")',
            'button:has-text("Load")',
            'button:has-text("Show")',
            'button:has-text("View")',
            'button:has-text("Next")',
        ]

        clicked = set()
        click_count = 0

        for sel in selectors:
            try:
                elements = await self.page.query_selector_all(sel)
                print(f"Found {len(elements)} elements for selector: {sel}")
                
                for el in elements[:5]:  # Limit to first 5 per selector
                    try:
                        if not await el.is_visible():
                            continue

                        text = (await el.text_content() or "").strip()
                        if len(text) < 2:
                            continue

                        # Create a unique key
                        element_id = await el.evaluate("el => el.id || ''")
                        key = f"{sel}-{text[:30]}-{element_id}"
                        
                        if key in clicked:
                            continue

                        # Scroll into view and click
                        await el.scroll_into_view_if_needed()
                        await el.click(force=True, timeout=3000)

                        # ✅ ADD CLICK RECORD
                        click_record = {
                            "text": text[:50],
                            "selector": sel,
                            "element_id": element_id,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        self.interactions["clicks"].append(click_record)
                        clicked.add(key)
                        click_count += 1
                        
                        print(f"Clicked: {text[:50]}")

                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        print(f"Failed to click element: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error with selector {sel}: {str(e)}")
                continue
        
        print(f"Total clicks performed: {click_count}")