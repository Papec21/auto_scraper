import json
import asyncio
import os
from playwright.async_api import async_playwright

# Function to save cookies click 
async def cookie_clicker():
    async with async_playwright() as p:
        # Launching browser
        # Will need to check later how you can run pracujpl in headless mode
        cookie_browser = await p.chromium.launch(headless=False)
        cookie_context = await cookie_browser.new_context()
        cookie_page = await cookie_context.new_page()

        # If "cookies.json" file exists we just read it and add load saved cookies
        if os.path.exists("cookies.json"):
            with open("cookies.json", "r") as f:
                cookies = json.loads(f.read())
                await cookie_context.add_cookies(cookies)

        # Else we go to website, click cookies and save them
        else:
            await cookie_page.goto("https://www.pracuj.pl/")
            await cookie_page.locator("[data-test=\"button-submitCookie\"]").click()
            await cookie_page.get_by_role("button", name="OK, zamknij").click()

            with open("cookies.json", "w") as f:
                f.write(json.dumps(await cookie_context.cookies()))

        await cookie_browser.close()

asyncio.run(cookie_clicker())