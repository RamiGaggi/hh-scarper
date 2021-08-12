import logging

from selenium import webdriver

CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument('--headless')
CHROME_OPTIONS.add_argument('--incognito')
CHROME_OPTIONS.add_argument('--disable-dev-shm-usage')
CHROME_OPTIONS.add_argument('--no-sandbox')
TIMEOUT = 15

logger = logging.getLogger(__name__)


def construct_hh_page(keyword, num_page=0):
    return f'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&st=sear)chVacancy&text={keyword}&page={num_page}'  # noqa:E501


def get_num_pages(url):
    driver = webdriver.Chrome(options=CHROME_OPTIONS)

    with driver as browser:
        browser.get(url)
        num_pages = int(browser.find_element())

    return num_pages


def get_vacancy_urls(url):
    browser = webdriver.Chrome(options=CHROME_OPTIONS)
    browser.get(url)

    vacancies = browser.find_elements_by_xpath(
        "//span[@class='g-user-content']/a[@class='bloko-link']",
    )
    vacancies_list = [vacancy.get_attribute('href') for vacancy in vacancies]
    browser.quit()

    logger.debug(vacancies_list)
    return vacancies_list


def vacancy_scrape(browser, url):
    browser.get(url)
    return browser.find_element_by_class_name('vacancy-description').text


def scrape(keyword):
    url = construct_hh_page(keyword)
    num_pages = get_num_pages(url)  # Browser out

    for num in range(num_pages):
        page = construct_hh_page(keyword, num_page=num)
        logger.debug(page)
