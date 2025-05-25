import requests
from unstructured.partition.html import partition_html

def scrape_and_structure(url: str, max_chars: int = 100_000) -> str:
    """
    Scrape a webpage and extract structured content using unstructured.
    """
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        # Extract semantic content using unstructured
        elements = partition_html(text=res.text)
        content = "\n".join(str(el) for el in elements)

        if len(content) > max_chars:
            print(f"[Warning] Truncating to {max_chars} characters.")
            content = content[:max_chars]

        return content

    except Exception as e:
        raise RuntimeError(f"Failed to scrape URL: {e}")
