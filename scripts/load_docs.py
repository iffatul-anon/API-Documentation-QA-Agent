"""
This module handles the loading and scraping of API documentation from web URLs.

It uses the requests library for fetching web content and the unstructured
library for extracting meaningful content from HTML pages while removing
navigation elements, footers, and other non-documentation content.
"""

import requests
from unstructured.partition.html import partition_html
from typing import Optional

def scrape_and_structure_data(url: str) -> str:
    """
    Scrape a webpage and extract structured content using unstructured library.

    This function fetches the content of a given URL and processes it to extract
    meaningful text content while removing boilerplate elements like navigation,
    footers, etc. It's specifically designed for API documentation pages but
    works with any HTML content.

    Args:
        url (str): The URL of the webpage to scrape. Must be a valid HTTP/HTTPS URL
            that returns HTML content.

    Returns:
        str: The extracted and processed text content from the webpage, with
            structural elements preserved through newlines.

    Raises:
        RuntimeError: If the URL cannot be accessed, returns non-200 status,
            or if content processing fails.
        
    Example:
        >>> url = "https://api.example.com/docs"
        >>> content = scrape_and_structure_data(url)
        >>> print(content[:100])  # Print first 100 chars of documentation
    """
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        # Extract semantic content using unstructured
        elements = partition_html(text=res.text)
        content = "\n".join(str(el) for el in elements)

        return content

    except Exception as e:
        raise RuntimeError(f"Failed to scrape URL: {e}")