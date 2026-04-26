from playwright.sync_api import sync_playwright

# Temporary place to store job offers
job_offers = {}

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto("https://it.pracuj.pl/praca/poznan;wp/ostatnich%2024h;p,1?rd=30&et=1%2C17%2C3")

        # Recorded sequene to pass cookies popup
        page.locator("[data-test=\"button-submitCookie\"]").click()
        page.get_by_role("button", name="Zamknij").click()

        # Taking all default offers from page
        offers = page.locator('[data-test="default-offer"]').all()
        
        # Getting id and title of every job offer
        for offer in offers:
            offer_id = offer.get_attribute("data-test-offerid")
            title = offer.locator("[data-test=\"link-offer-title\"]").inner_text()
            
            # If id is already exists in our dictionary, the code will pass it
            # If not then it will update the dictionary
            if job_offers.get(offer_id):
                pass
            else:
                job_offers.update({offer_id: title})

        # Printing what we got in our dictionary just to see if it works correctly
        for key, value in job_offers.items():
            print(f"{key} | {value}")

        # browser.close()

if __name__ == "__main__":
    main()