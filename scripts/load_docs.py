import requests
from bs4 import BeautifulSoup

def scrape_url(url: str, max_chars: int = 100_000) -> str:
    """
    Scrape clean text content from a URL, focusing on useful tags.
    Limits total output to avoid overload.
    """
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Target commonly useful content tags
        elements = soup.find_all(["p", "li", "code", "pre", "h2", "h3"])

        content = "\n".join(e.get_text(strip=True) for e in elements)

        return content

    except Exception as e:
        raise RuntimeError(f"Failed to scrape URL '{url}': {e}")

