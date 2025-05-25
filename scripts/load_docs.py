import requests
from bs4 import BeautifulSoup

def scrape_url(url: str) -> str:
    """Scrape text content from a URL."""
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        elements = soup.find_all(["p", "li", "code"])
        return "\n".join(e.get_text(strip=True) for e in elements)
    except Exception as e:
        raise RuntimeError(f"Failed to scrape URL: {e}")
