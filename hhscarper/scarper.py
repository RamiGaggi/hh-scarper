import logging

from selenium import webdriver

CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument('--headless')
CHROME_OPTIONS.add_argument('--incognito')
CHROME_OPTIONS.add_argument('--disable-dev-shm-usage')
CHROME_OPTIONS.add_argument('--no-sandbox')
TIMEOUT = 15

logger = logging.getLogger(__name__)


def get_vacancy_urls(page):
    browser = webdriver.Chrome(options=CHROME_OPTIONS)
    browser.get(page)

    vacancies = browser.find_elements_by_xpath(
        "//span[@class='g-user-content']/a[@class='bloko-link']",
    )
    vacancies_list = [vacancy.get_attribute('href') for vacancy in vacancies]
    browser.quit()

    return vacancies_list
