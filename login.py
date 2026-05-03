import asyncio
import random
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from playwright_stealth.stealth import Stealth

# Loading password and email from env
load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

async def login():
    async with async_playwright() as p:
        # Launching browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await Stealth().apply_stealth_async(page)

        # Going to login page
        await page.goto("https://login.pracuj.pl/")
        
        # Handling cookies
        try:
            await page.locator("[data-test=\"button-submitCookie\"]").click(timeout=1000)
            await page.get_by_role("button", name="Zamknij").click(timeout=1000)
        except Exception:
            pass

        # Probably will need to use type and some randomness to make it more human-like
        # Maybe also add some wait time between clicks
        # Filling email with random time between each charcater
        for char in email:
            await page.type("#email", char)
            await asyncio.sleep(random.uniform(0.03, 0.1))

        await page.get_by_role("button", name="Dalej").click()

        await page.wait_for_selector("#password")
        # Filling password with random time between each character
        for char in password:
            await page.type("#password", char)
            await asyncio.sleep(random.uniform(0.03, 0.1))

        await page.get_by_role("button", name="Zaloguj się").click()

        # await browser.close()

asyncio.run(login())