# Web Scraper with JavaScript Rendering

An advanced web scraping application built with FastAPI, Playwright, and modern web technologies. This tool can scrape both static and JavaScript-rendered websites, handle interactions like clicks and scrolls, and provide structured data output.

## Features

- **Static HTML scraping** using httpx and selectolax
- **JavaScript rendering** with Playwright for dynamic content
- **Smart fallback strategy** - uses JS only when needed
- **Interactive scraping** - clicks tabs, "Load more" buttons, and handles pagination
- **Content sectioning** - groups content into semantic sections
- **Noise filtering** - removes cookie banners, modals, and overlays
- **Structured JSON output** - consistent schema with metadata, sections, and interactions
- **Web UI** - user-friendly interface to test and visualize results
- **REST API** - programmatic access to scraping functionality

## Technology Stack

- **Backend**: FastAPI (Python 3.10+)
- **HTML Parsing**: selectolax, BeautifulSoup4
- **HTTP Client**: httpx
- **JavaScript Rendering**: Playwright
- **Frontend**: Jinja2 templates with Bootstrap
- **Server**: Uvicorn

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Chrome/Chromium browser (for Playwright)

### Installation & Running

1. **Clone and set up**:
```bash
# Make run.sh executable
chmod +x run.sh

# Run the application
./run.sh