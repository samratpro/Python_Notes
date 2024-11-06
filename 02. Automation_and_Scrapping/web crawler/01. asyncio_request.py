# Multiple Request at a time
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main(urls):
    tasks = [fetch(url) for url in urls]  # Create fetch tasks for each URL dynamically
    results = await asyncio.gather(*tasks)  # Execute tasks concurrently
    return results

async def fetch_multiple(urls):
    return await main(urls)

async def example():
    urls = [
        'https://example.com',
        'https://example.com/another',
        'https://example.com/yet-another'
    ]
    results = await fetch_multiple(urls)
    print(results)

asyncio.run(example())
