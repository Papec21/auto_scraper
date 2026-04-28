import asyncio
from playwright_stealth.stealth import Stealth
from playwright.async_api import async_playwright
import csv

# Temporary place to store job offers
job_offers = {}

async def main():
    async with async_playwright() as p:
        # Launching browser
        browser = await p.chromium.launch(headless=False)

        # Waiting for our desired page to load
        page = await browser.new_page()
        await Stealth().apply_stealth_async(page)
        await page.goto("https://it.pracuj.pl/praca/poznan;wp/ostatnich%2024h;p,1?rd=30&et=1%2C17%2C3")

        # Recorded sequence to pass cookies popup
        await page.locator("[data-test=\"button-submitCookie\"]").click()
        await page.get_by_role("button", name="Zamknij").click()

        # Taking all default offers from page
        # Waiting for page to fully load
        await page.locator("[data-test=\"default-offer\"]").first.wait_for(state="visible")
        await page.wait_for_load_state("networkidle")
        
        # Got problem with too long waiting time for title
        count = await page.locator("[data-test=\"default-offer\"]").count()

        # Getting id and title of every job offer
        for i in range(count):
            offer = page.locator("[data-test=\"default-offer\"]").nth(i)
            # Scroll down to prevent offers from not loading
            await offer.scroll_into_view_if_needed()
            offer_id = await offer.get_attribute("data-test-offerid")
            title = await offer.locator("[data-test=\"link-offer-title\"]").inner_text()
            
            # If id not in the dict, it will update it
            if offer_id not in job_offers:
                job_offers[offer_id] = title

            # for offer_id, title in job_offers.items():
            #    print({"ID": offer_id, "title": title})

        # Printing our dictionary
        for key, value in job_offers.items():
            print(f"{key} | {value}")

        await browser.close()


asyncio.run(main())

#if __name__ == "__main__":
#    asyncio.run(main())