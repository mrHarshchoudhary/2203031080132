from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class SectionType(str, Enum):
    HERO = "hero"
    SECTION = "section"
    NAV = "nav"
    FOOTER = "footer"
    LIST = "list"
    GRID = "grid"
    FAQ = "faq"
    PRICING = "pricing"
    UNKNOWN = "unknown"
class Click(BaseModel):
    text: str
    selector: str
    element_id: Optional[str] = None
    timestamp: str


class Link(BaseModel):
    text: str
    href: str


class Image(BaseModel):
    src: str
    alt: str


class Content(BaseModel):
    headings: List[str] = []
    text: str = ""
    links: List[Link] = []
    images: List[Image] = []
    lists: List[List[str]] = []
    tables: List[Dict[str, Any]] = []


class Section(BaseModel):
    id: str
    type: SectionType
    label: str
    sourceUrl: str
    content: Content
    rawHtml: str
    truncated: bool = False


class Error(BaseModel):
    message: str
    phase: str


class Interactions(BaseModel):
    clicks: List[Click] = []
    scrolls: int = 0
    pages: List[str] = []


class Meta(BaseModel):
    title: str = ""
    description: str = ""
    language: str = ""
    canonical: Optional[str] = None


class ScrapeResult(BaseModel):
    url: str
    scrapedAt: str            # ✅ FIXED
    meta: Meta
    sections: List[Section]
    interactions: Interactions
    errors: List[Error] = []


class ScrapeRequest(BaseModel):
    url: str


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())  # ✅ FIXED


class ScrapeResponse(BaseModel):
    result: ScrapeResult
    strategy: Optional[str] = None
    processing_time: Optional[float] = None
