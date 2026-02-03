# url_loader.py

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

class URLLoader:
    """
    Simple URL Loader for RAG.
    Fetches HTML pages, cleans content, and returns text.
    """

    def __init__(self, timeout: int = 15, user_agent: Optional[str] = None):
        self.timeout = timeout
        self.headers = {
            "User-Agent": user_agent
            or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[URLLoader] Error fetching {url}: {e}")
            return None

    def parse_html(self, html: str, remove_scripts: bool = True) -> str:
        soup = BeautifulSoup(html, "html.parser")
        if remove_scripts:
            for tag in soup(["script", "style", "noscript"]):
                tag.extract()
        text = soup.get_text(separator=" ")
        cleaned = " ".join(text.split())
        return cleaned

    def load(self, url: str) -> Dict[str, Any]:
        html = self.fetch(url)
        if not html:
            return {"url": url, "success": False, "content": ""}

        text = self.parse_html(html)
        return {
            "url": url,
            "success": True,
            "content": text,
            "length": len(text),
        }


if __name__ == "__main__":
    loader = URLLoader()
    result = loader.load("https://example.com")
    print(result)
