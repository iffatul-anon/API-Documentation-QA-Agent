"""
This module handles the chunking of documentation text into smaller segments
for efficient processing and embedding.

The module uses LangChain's RecursiveCharacterTextSplitter to split text
into chunks while preserving semantic meaning where possible.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    """
    Split a large text into smaller, semantically meaningful chunks.

    This function uses RecursiveCharacterTextSplitter to break down text into
    smaller pieces while trying to preserve semantic meaning. It attempts to split
    at natural boundaries like newlines and periods before falling back to
    splitting on spaces or characters.

    Args:
        text (str): The input text to be chunked. Should be non-empty.
        chunk_size (int, optional): Maximum size of each chunk in characters.
            Defaults to 500. Should be positive.
        chunk_overlap (int, optional): Number of characters of overlap between
            chunks. Defaults to 100. Should be less than chunk_size.

    Returns:
        List[str]: A list of text chunks, where each chunk is a string of
            maximum length chunk_size.

    Example:
        >>> text = "This is a long document. It needs to be split into chunks."
        >>> chunks = chunk_text(text, chunk_size=20, chunk_overlap=5)
        >>> print(chunks)
        ['This is a long', 'long document.', 'document. It needs', 'needs to be split']
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)