from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import hashlib
import re

from app.models import Section, Content, Link, Image, SectionType
from app.config import settings

class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self, url: str):
        self.url = url
        self.base_url = self._get_base_url(url)
        self.errors = []
        self.sections = []
        self.interactions = {
            "clicks": [],
            "scrolls": 0,
            "pages": [url]
        }
    
    def _get_base_url(self, url: str) -> str:
        """Extract base URL from full URL"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URL to absolute"""
        if not url:
            return ""
        
        if url.startswith(('http://', 'https://')):
            return url
        
        if url.startswith('//'):
            return f"{urlparse(self.url).scheme}:{url}"
        
        if url.startswith('/'):
            return urljoin(self.base_url, url)
        
        return urljoin(self.url, url)
    
    def _generate_section_id(self, element_text: str) -> str:
        """Generate a stable section ID"""
        text_hash = hashlib.md5(element_text.encode()).hexdigest()[:8]
        return f"section-{text_hash}"
    
    def _extract_text_content(self, html: str) -> str:
        """Extract clean text content from HTML"""
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        
        # Remove HTML tags but keep text
        text = re.sub(r'<[^>]+>', ' ', html)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _truncate_html(self, html: str, max_length: int = settings.MAX_RAW_HTML_LENGTH) -> tuple[str, bool]:
        """Truncate HTML content"""
        if len(html) <= max_length:
            return html, False
        
        # Try to truncate at a tag boundary
        truncated = html[:max_length]
        last_tag = truncated.rfind('>')
        
        if last_tag != -1:
            truncated = truncated[:last_tag + 1]
        
        return truncated + "...", True
    
    @abstractmethod
    async def scrape(self) -> Dict[str, Any]:
        """Main scraping method to be implemented by subclasses"""
        pass