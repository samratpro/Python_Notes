import asyncio
from playwright.async_api import async_playwright
from gologin import GoLogin

async def main():
    gl = GoLogin({
		"token": "yU0token",
		"profile_id": "yU0Pr0f1leiD",
	        # "extra_params":["--headless"]
		})

    debugger_address = gl.start()
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://"+debugger_address)
        default_context = browser.contexts[0]
        page = default_context.pages[0]
        await page.goto('https://gologin.com')
        await page.screenshot(path="gologin.png")
        await page.close()
    gl.stop()

asyncio.get_event_loop().run_until_complete(main())

# sync
from playwright.sync_api import sync_playwright
gl = GoLogin({"token": token,"profile_id": "66448d4d37d1dd0246ba4ec8"})
with sync_playwright() as p:
	debugger_address = gl.start()
	browser = p.chromium.connect_over_cdp("http://" + debugger_address)
	default_context = browser.contexts[0]
	page = default_context.pages[0]
	page.stop()
	gl.stop()
