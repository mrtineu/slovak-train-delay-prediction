from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def scrape_timetable(train_number: str) -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()
        page.goto("https://mapa.zsr.sk/", wait_until="networkidle")

        url = f"https://mapa.zsr.sk/Start/TrainDetail?cisloVlaku={train_number}"
        page.goto(url, wait_until="networkidle")

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    stops = []

    for row in soup.select(".timeline__list .row"):
        name_div = row.select_one(".bold")
        if not name_div:
            continue
        name = name_div.get_text(strip=True)
        if not name:
            continue

        has_time = bool(
            row.select_one(
                "span[lang-title-key='arrival'], span[lang-title-key='depart']"
            )
        )

        if has_time and name not in stops:
            stops.append(name)

    return stops