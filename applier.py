import asyncio
from playwright_stealth.stealth import Stealth
from playwright.async_api import async_playwright

# Mockup (well real actually) job offers to see if it works
job_offers = {
    1004765163: {
        "title": "Supply Chain Consultant (SQL) k/m/*",
        "url": "https://www.pracuj.pl/praca/supply-chain-consultant-sql-k-m-warszawa,oferta,1004765163?s=e05d92f5&searchId=MTc3NzcyOTc3NDg5Mi40MDE="
    },
    1004801363: {
        "title": "Junior Java/Scala Developer",
        "url": "https://www.pracuj.pl/praca/junior-java-scala-developer-warszawa,oferta,1004801363?s=e05d92f5&searchId=MTc3NzcyOTc3NDg5Mi40MDE="
    },
    1004765111: {
        "title": "Microsoft Dynamics Specialist",
        "url": "https://www.pracuj.pl/praca/microsoft-dynamics-specialist-warszawa-domaniewska-42,oferta,1004765111?s=e05d92f5&searchId=MTc3NzcyOTc3NDg5Mi40MDE="
    },
    1004784292: {
        "title": "Backend Engineer",
        "url": "https://www.pracuj.pl/praca/backend-engineer-poznan,oferta,1004784292?s=e05d92f5&searchId=MTc3NzcyOTc3NDg5Mi40MDE="
    },
    1004751382: {
        "title": "Junior Software Tester (m/f)",
        "url": "https://www.pracuj.pl/praca/junior-software-tester-m-f-poznan-krysiewicza-9,oferta,1004751382?s=e05d92f5&searchId=MTc3NzcyOTc3NDg5Mi40MDE="
    },
    1004794584: {
        "title": "Administrator systemów IT (m/k)",
        "url": "https://www.pracuj.pl/praca/administrator-systemow-it-m-k-poznan-winogrady-70a,oferta,1004794584?s=e05d92f5&searchId=MTc3NzcyOTc3NDg5Mi40MDE="
    },
}

# Temporary place to store application success data
application_sent = []

# for key, value in job_offers.items():
#     print(value["url"])

async def applier():
    async with async_playwright() as playwright:
        applier_browser = await playwright.chromium.launch(headless=False)

        # Open every link and apply to job (not yet but in the future)
        for link in job_offers:
            offer_page = await applier_browser.new_page()
            await Stealth().apply_stealth_async(offer_page)

            key = job_offers[link]
            url = key["url"]
            print(url)
            await offer_page.goto(url)

            # Checking if apply button has link on himself
            href = await offer_page.get_attribute("a[data-test=\"anchor-apply\"]", "href", timeout=1000)

            # If link hides in button then we type False to note that application is not complete
            # There's actually major problem with on pracujpl site short forms thats gonna be hard to overcome
            if href:
                application_sent.append(False)
            # Else application is complete and we're good
            else:
                application_sent.append(True)

            await offer_page.close()

        print(application_sent)
asyncio.run(applier())

# https://login.pracuj.pl/
# await page.fill("#email", "bartekdemczak@atomicmail.io")
# await page.get_by_role("button", name="Dalej").click()
# await page.fill(name="password", "Bartek123!")
# await page.get_by_role("button", name-"Zaloguj się").click()