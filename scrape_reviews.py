import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
import config


def dismiss_overlays(driver):
    try:
        consent_button = driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
        consent_button.click()
        time.sleep(1)
    except:
        pass


def safe_click(driver, element, scroll_offset=150):
    driver.execute_script("""
        const rect = arguments[0].getBoundingClientRect();
        window.scrollBy({top: rect.top - arguments[1], left: 0, behavior: 'instant'});
    """, element, scroll_offset)
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def click_all_spoilers(driver):
    while True:
        spoiler_buttons = driver.find_elements(By.CSS_SELECTOR, "span.ipc-btn__text")
        found_spoiler = False

        for btn in spoiler_buttons:
            try:
                text_lower = btn.text.lower()
            except:
                continue

            if "spoiler" in text_lower:
                safe_click(driver, btn)
                found_spoiler = True
                break

        if not found_spoiler:
            break


def scrape_reviews(imdb_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/109.0.0.0 Safari/537.36"
    )

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(config.WEB_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.imdb.com/title/{imdb_id}/reviews"
    driver.get(url)
    time.sleep(2)

    dismiss_overlays(driver)

    def get_review_count():
        return len(driver.find_elements(By.CSS_SELECTOR, "div.ipc-html-content-inner-div"))

    last_count = get_review_count()
    start_same_count_time = None

    while True:
        all_buttons = driver.find_elements(By.CSS_SELECTOR, "span.ipc-see-more__text")
        for btn in all_buttons:
            if "all" in btn.text.lower():
                safe_click(driver, btn)
                time.sleep(1)
                break

        click_all_spoilers(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        new_count = get_review_count()
        if new_count == last_count:
            if start_same_count_time is None:
                start_same_count_time = time.time()
            else:
                elapsed = time.time() - start_same_count_time
                if elapsed >= 3.0:
                    break
        else:
            start_same_count_time = None
            last_count = new_count

    html_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_source, "html.parser")

    review_divs = soup.find_all("div", class_="ipc-html-content-inner-div")
    reviews = [div.get_text(strip=True) for div in review_divs]

    return reviews

