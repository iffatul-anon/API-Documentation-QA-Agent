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


def chunk_text(text: str, chunk_size: int = 500):
    """Split text into chunks of given size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

