# url_loader.py
from bs4 import BeautifulSoup
import requests

class URLLoader:
    def load(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ")

# pdf_loader.py
import pdfplumber

class PDFLoader:
    def load(self, path: str) -> str:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

# json_loader.py
import json

class JSONLoader:
    def load(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)

# markdown_loader.py
class MarkdownLoader:
    def load(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

# html_loader.py
from bs4 import BeautifulSoup

class HTMLLoader:
    def load(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        return soup.get_text(separator=" ")

# directory_loader.py
import os

class DirectoryLoader:
    def load(self, directory: str) -> dict:
        contents = {}
        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        contents[full_path] = f.read()
                except Exception:
                    continue
        return contents

# sitemap_loader.py
import requests
from bs4 import BeautifulSoup

class SitemapLoader:
    def load(self, sitemap_url: str) -> list:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        return urls

# rss_loader.py
import feedparser

class RSSLoader:
    def load(self, rss_url: str) -> list:
        feed = feedparser.parse(rss_url)
        entries = []
        for entry in feed.entries:
            entries.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", "")
            })
        return entries

# universal_loader_registry.py
class LoaderRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, name: str, loader):
        self.registry[name] = loader

    def get(self, name: str):
        return self.registry.get(name)

loader_registry = LoaderRegistry()
loader_registry.register("url", URLLoader())
loader_registry.register("pdf", PDFLoader())
loader_registry.register("json", JSONLoader())
loader_registry.register("md", MarkdownLoader())
loader_registry.register("html", HTMLLoader())
loader_registry.register("directory", DirectoryLoader())
loader_registry.register("sitemap", SitemapLoader())
loader_registry.register("rss", RSSLoader())
