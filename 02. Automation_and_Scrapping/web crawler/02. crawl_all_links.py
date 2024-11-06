import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def extract_urls(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        absolute_url = urljoin(base_url, href)
        urls.append(absolute_url)
    return urls

async def crawl(url, visited):
    if url in visited:
        return
    print(f"Crawling: {url}")
    visited.add(url)
    html = await fetch(url)
    child_urls = await extract_urls(html, url)
    for child_url in child_urls:
        await crawl(child_url, visited)

async def main(start_url):
    visited = set()
    await crawl(start_url, visited)

start_url = 'https://www.momentummetropolitan.co.za'
asyncio.run(main(start_url))
