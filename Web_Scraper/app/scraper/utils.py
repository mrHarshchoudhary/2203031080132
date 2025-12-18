from urllib.parse import urlparse
import validators
from typing import Optional

class URLUtils:
    """URL utility functions"""
    
    @staticmethod
    def validate_url(url: str) -> tuple[bool, Optional[str]]:
        """Validate URL format"""
        if not url:
            return False, "URL is required"
        
        # Check if it's a valid URL
        if not validators.url(url):
            return False, "Invalid URL format"
        
        # Check scheme
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return False, "Only http and https URLs are supported"
        
        return True, None
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL"""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

class ContentUtils:
    """Content utility functions"""
    
    @staticmethod
    def estimate_text_completeness(text: str, threshold: int = 100) -> bool:
        """Estimate if text content is complete enough"""
        return len(text.strip()) >= threshold
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common noise patterns
        noise_patterns = [
            r'\s*\.{3,}\s*',  # Multiple dots
            r'\s*-\s*-\s*',   # Multiple dashes
        ]
        
        for pattern in noise_patterns:
            text = text.replace(pattern, ' ')
        
        return text.strip()