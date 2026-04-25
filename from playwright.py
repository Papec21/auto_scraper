from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto("https://it.pracuj.pl/praca/poznan;wp?rd=30&et=1%2C17%2C3")

        title = page.title()

        print(f"Page title: {title}")

        browser.close()