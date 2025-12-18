# 🕷️ Universal Website Scraper (MVP)

A powerful, section-aware website scraper built with **FastAPI** and **Playwright**. The system intelligently handles both **static** and **JavaScript-rendered** websites, performs automated interaction flows (scrolling and clicking), and returns clean, structured JSON output.

> **Developed as part of a Full-Stack Assignment**

---

## ✨ Features

- 🔍 **Dual Scraping Modes**: Static (BeautifulSoup + lxml) and Dynamic (Playwright + Chromium)
- 🖱️ **Smart Interactions**: Automatic scrolling (depth ≥ 3) and intelligent element clicking
- 🧩 **Section-Aware Parsing**: Structured JSON output with hierarchical content organization
- 📊 **Interaction Analytics**: Detailed logs of clicks, scrolls, and user interactions
- 🚀 **FastAPI Backend**: High-performance async API with minimal Jinja2 frontend
- 🛡️ **Robust Error Handling**: Automatic fallback from dynamic to static scraping
- ⚡ **Interactive Element Detection**: Identifies and interacts with buttons, links, and expandable menus

---

## 🏗️ Tech Stack

### Backend
- **Python** 3.10+
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server

### Scraping Engine
- **Playwright** (Chromium) - JavaScript rendering
- **BeautifulSoup4** - HTML parsing
- **lxml** - Fast XML/HTML processing
- **httpx** - Async HTTP client
- **aiohttp** - Async HTTP requests

### Frontend
- **Jinja2** - Minimal templating UI

### Data Validation
- **Pydantic v2** - Data validation and serialization

---

## 📋 Prerequisites

- **Python** 3.10 or higher
- **Chrome/Chromium** browser (automatically installed via Playwright)
- **Git** (for cloning the repository)

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mrHarshchoudhary/universal-web-scraper-lyftr.git
cd universal-web-scraper-lyftr
```

### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Playwright Browsers

```bash
playwright install chromium
```

### 5️⃣ Run the Application

**Option A: Using the run script (Linux/macOS)**
```bash
chmod +x run.sh
./run.sh
```

**Option B: Manual start (All platforms)**
```bash
python -m uvicorn app.main:app --reload
```

### 6️⃣ Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

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
```

---

## 🧪 Testing URLs

The scraper has been tested and validated on the following websites:

| Website | URL | Type |
|---------|-----|------|
| Wikipedia - AI | https://en.wikipedia.org/wiki/Artificial_intelligence | Static + Dynamic |
| Vercel | https://vercel.com | JavaScript-heavy |
| Hacker News | https://news.ycombinator.com | Static |

---

## 📁 Project Structure

```
universal-web-scraper-lyftr/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── scraper.py           # Core scraping logic
│   ├── models.py            # Pydantic models
│   └── templates/           # Jinja2 templates
├── requirements.txt         # Python dependencies
├── run.sh                   # Quick start script
└── README.md               # This file
```

---

## 🔧 API Endpoints

### `POST /scrape`

Scrapes a website and returns structured JSON data.

**Request Body:**
```json
{
  "url": "https://example.com",
  "mode": "dynamic",
  "scroll_depth": 3
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "sections": [...],
  "interactions": {
    "clicks": 5,
    "scrolls": 3
  },
  "timestamp": "2024-12-18T10:30:00Z"
}
```

---

## 🎯 Usage Example

### Web Interface
1. Navigate to `http://127.0.0.1:8000`
2. Enter the target URL
3. Select scraping mode (Static/Dynamic)
4. Click "Scrape"
5. View structured JSON output

### API Call (cURL)
```bash
curl -X POST "http://127.0.0.1:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "mode": "dynamic",
    "scroll_depth": 3
  }'
```

---

## 🛠️ Configuration

You can customize scraping behavior by modifying parameters:

- **`scroll_depth`**: Number of scroll iterations (default: 3)
- **`mode`**: `static` or `dynamic` (default: `dynamic`)
- **`timeout`**: Request timeout in seconds (default: 30)

---

## 🐛 Troubleshooting

### Issue: Playwright browser not found
**Solution:**
```bash
playwright install chromium
```

### Issue: Port 8000 already in use
**Solution:**
```bash
python -m uvicorn app.main:app --reload --port 8080
```

### Issue: Module not found errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Harsh Choudhary**

- GitHub: [@mrHarshchoudhary](https://github.com/mrHarshchoudhary)
- Repository: [universal-web-scraper-lyftr](https://github.com/mrHarshchoudhary/universal-web-scraper)

---

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **Playwright** for browser automation capabilities
- **BeautifulSoup** for HTML parsing simplicity
- All open-source contributors

---



**⭐ If you find this project useful, please consider giving it a star on GitHub!**