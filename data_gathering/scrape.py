from playwright.sync_api import sync_playwright

def get_train_state():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        train_data = []

        def handle_intercept(intercept):
            if "api/action" in intercept.url:
                try:
                    train_data.append(intercept.json())
                except:
                    print("Something went wrong with parsing API response")
        
        page.on('response', handle_intercept)

        page.goto('https://mapa.zsr.sk/index.aspx')
        page.wait_for_load_state('networkidle')

        return train_data
