from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
import time
logger = logging.getLogger(__name__)

# Crucial function that returns the data of every train currently running in Slovakia
def get_train_state():
    start = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        train_data = []
        #This function is called when we get a response, and we extract the json from that, so we do not need to do a second request to the API
        def handle_intercept(intercept):
            if "api/action" in intercept.url:
                try:
                    train_data.append(intercept.json())
                except Exception as e :
                    logger.error(f"Something went wrong with parsing API response: {e}")
                    
        
        page.on('response', handle_intercept)
        try:
            page.goto('https://mapa.zsr.sk/index.aspx')
        except PlaywrightTimeoutError:
            logger.error("Timeout: response did not come in under 30s")
        except Exception as e:
            logger.error(f"Exception happend while loading the site: {e}")
            return train_data
        page.wait_for_load_state('networkidle')
        logger.info("Recieved data from the API")
        logger.debug(f"Getting train data took {round(time.time()-start,2)} seconds")
        return train_data


if __name__ == "__main__":
    print(get_train_state())