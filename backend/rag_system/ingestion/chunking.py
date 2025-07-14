import re
from typing import List

def chunk_by_length(text: str, chunk_size: int, chunk_overlap: int = 0) -> List[str]:
    """Chunks text into segments of a specified size with optional overlap."""
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")
    if chunk_overlap < 0:
        raise ValueError("Chunk overlap cannot be negative.")
    if chunk_overlap >= chunk_size:
        raise ValueError("Chunk overlap must be smaller than chunk size.")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def chunk_by_headings(text: str) -> List[str]:
    """Chunks Markdown text by headings (levels 1-3)."""
    # Regex to find markdown headings (levels 1-3)
    heading_pattern = re.compile(r'(^#{1,3} .*)', re.MULTILINE)
    # Split the text by headings, keeping the headings
    sections = heading_pattern.split(text)

    # The first element might be content before the first heading
    chunks = []
    if sections[0].strip():
        chunks.append(sections[0].strip())

    # Combine each heading with its content
    for i in range(1, len(sections), 2):
        heading = sections[i]
        content = sections[i+1] if (i+1) < len(sections) else ""
        chunks.append((heading + content).strip())

    return [chunk for chunk in chunks if chunk] # Filter out empty chunks

def clean_code_blocks(text: str) -> str:
    """Cleans Markdown code blocks to improve processing by language models."""
    # This pattern finds fenced code blocks (```) and removes the fences
    # while keeping the content, optionally adding a marker.
    code_block_pattern = re.compile(r'```(?:\w+)?\n(.*?)\n```', re.DOTALL)
    
    def replacer(match):
        # We can add a marker to indicate this was a code block
        # For now, we just return the code itself, cleaned up.
        code_content = match.group(1).strip()
        return f"\n--- CODE BLOCK ---\n{code_content}\n--- END CODE BLOCK ---\n"

    return code_block_pattern.sub(replacer, text)
