# Universal Website Scraper (MVP)

A universal, section-aware website scraper built using **FastAPI** and **Playwright**.  
The system supports both **static** and **JavaScript-rendered** websites, performs
basic interaction flows (scrolling and clicking), and returns structured JSON output.

This project was developed as part of a **Full-Stack Assignment**.

---

## 🚀 Features

- Static website scraping using BeautifulSoup and lxml
- JavaScript-rendered website scraping using Playwright (Chromium)
- Automatic page scrolling (depth ≥ 3)
- Interactive element detection and clicking (buttons, links, expandable menus)
- Section-aware structured JSON output
- Interaction analytics (clicks, scrolls)
- FastAPI backend with a minimal frontend (Jinja2)
- Error handling and fallback to static scraping

---

## 🧱 Tech Stack

**Backend**
- Python 3.10+
- FastAPI
- Uvicorn

**Scraping**
- Playwright (Chromium)
- BeautifulSoup4
- lxml
- httpx
- aiohttp

**Frontend**
- Jinja2 (minimal UI)

**Data Validation**
- Pydantic v2

---

## 📦 Dependencies

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.1
beautifulsoup4==4.12.2
playwright==1.40.0
jinja2==3.1.2
pydantic==2.5.0
python-multipart==0.0.6
python-dateutil==2.8.2
aiohttp
lxml==4.9.3
validators==0.22.0
