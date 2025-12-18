from unittest import result
import httpx
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin

from app.scraper.base import BaseScraper
from app.models import Section, Content, Link, Image, SectionType, Meta
from app.config import settings


class StaticScraper(BaseScraper):
    """Static HTML scraper using httpx + BeautifulSoup"""

    async def scrape(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.get(self.url, follow_redirects=True)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "lxml")

                meta = self._extract_metadata(soup)
                sections = self._extract_sections(soup)

                result = {
                    "meta": meta,
                    "sections": sections,
                    "interactions": self.interactions,
                    "strategy": "static"
}
                return result


        except Exception as e:
            self.errors.append({"message": str(e), "phase": "fetch"})
            return {"meta": Meta(), "sections": [], "strategy": "static"}

    # ---------------- METADATA ---------------- #
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Meta:
        meta = Meta()

        title = soup.select_one("title")
        if title:
            meta.title = title.get_text(strip=True)

        desc = soup.select_one('meta[name="description"]')
        if desc:
            meta.description = desc.get("content", "")

        html = soup.select_one("html")
        if html:
            meta.language = html.get("lang", "")

        canonical = soup.select_one('link[rel="canonical"]')
        if canonical:
            meta.canonical = self._make_absolute_url(canonical.get("href"))

        return meta

    # ---------------- SECTIONS ---------------- #

    def _extract_sections(self, soup: BeautifulSoup) -> List[Section]:
        sections: List[Section] = []

        semantic_tags = ["header", "nav", "main", "section", "article", "footer"]

    # 1️⃣ Semantic sections
        for tag in semantic_tags:
            for elem in soup.find_all(tag):
                section = self._create_section_from_element(elem)
                if section and section.content.text.strip():
                    sections.append(section)
    # 2️⃣ Fallback for modern websites (div-based layouts)
        if not sections:
            for div in soup.find_all("div", recursive=False):
                section = self._create_section_from_element(div)
                if section and section.content.text.strip():
                    sections.append(section)
    # 3️⃣ Last fallback: body
        if not sections and soup.body:
            section = self._create_section_from_element(soup.body)
            if section and section.content.text.strip():
                sections.append(section)

        return sections[: settings.MAX_SECTIONS]

    def _create_section_from_element(self, elem: Tag) -> Optional[Section]:
        try:
            section_type = self._determine_section_type(elem)
            content = self._extract_content(elem)
            label = self._generate_section_label(content.text, elem)

            raw_html = str(elem)
            truncated_html, truncated = self._truncate_html(raw_html)
            section_id = self._generate_section_id(label)

            return Section(
                id=section_id,
                type=section_type,
                label=label,
                sourceUrl=self.url,
                content=content,
                rawHtml=truncated_html,
                truncated=truncated
            )

        except Exception as e:
            self.errors.append({"message": str(e), "phase": "parse"})
            return None

    # ---------------- CONTENT ---------------- #

    def _extract_content(self, elem: Tag) -> Content:
        content = Content()

        content.text = elem.get_text(" ", strip=True)

        for h in elem.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            content.headings.append(h.get_text(strip=True))

        for a in elem.find_all("a", href=True):
            content.links.append(
                Link(
                    text=a.get_text(strip=True),
                    href=self._make_absolute_url(a["href"])
                )
            )

        for img in elem.find_all("img", src=True):
            content.images.append(
                Image(
                    src=self._make_absolute_url(img["src"]),
                    alt=img.get("alt", "")
                )
            )

        return content

    # ---------------- HELPERS ---------------- #

    def _determine_section_type(self, elem: Tag) -> SectionType:
        tag = elem.name or ""

        if tag == "nav":
            return SectionType.NAV
        if tag == "footer":
            return SectionType.FOOTER
        if tag == "header":
            return SectionType.HERO
        if tag == "section":
            return SectionType.SECTION

        return SectionType.UNKNOWN

    def _generate_section_label(self, text: str, elem: Tag) -> str:
        heading = elem.find(["h1", "h2", "h3"])
        if heading:
            return heading.get_text(strip=True)

        if text:
            return " ".join(text.split()[:6])

        return elem.name.capitalize() if elem.name else "Content"
    def scrape_from_html(self, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "lxml")
        meta = self._extract_metadata(soup)
        sections = self._extract_sections(soup)

        return {
        "meta": meta,
        "sections": sections,
        "interactions": self.interactions,
        "strategy": "js"
    }
