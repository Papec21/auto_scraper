import asyncio
from playwright_stealth.stealth import Stealth
from playwright.async_api import async_playwright

async def applier():
    async with async_playwright() as playwright:
        applier_browser = await playwright.chromium.launch(headless=False)

        offer_page = await applier_browser.new_page()
        await Stealth().apply_stealth_async(offer_page)
        await offer_page.goto(f"{job_offers[1]}")
