import logging

from hhscarper.models import Vacancy
from selenium import webdriver

CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument('--headless')
CHROME_OPTIONS.add_argument('--incognito')
CHROME_OPTIONS.add_argument('--disable-dev-shm-usage')
CHROME_OPTIONS.add_argument('--no-sandbox')
TIMEOUT = 15

logger = logging.getLogger(__name__)


def _construct_hh_page(keyword, num_page=0):
    return f'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&st=sear)chVacancy&text={keyword}&page={num_page}'  # noqa:E501


def _get_num_pages(url):  # noqa: WPS210
    driver = webdriver.Chrome(options=CHROME_OPTIONS)

    with driver as browser:
        browser.get(url)
        elements = browser.find_elements_by_xpath("//a[@class='bloko-button']/span")  # noqa:E501

        max_num = 0
        number_of_pages = 0
        for elem in elements:
            try:
                number_of_pages = int(elem.text)
            except ValueError:
                logger.debug(f'ValueError: {elem.text}')

            if number_of_pages > max_num:
                max_num = number_of_pages

    return max_num


def _get_vacancy_urls(url):
    browser = webdriver.Chrome(options=CHROME_OPTIONS)
    browser.get(url)

    vacancies = browser.find_elements_by_xpath(
        "//span[@class='g-user-content']/a[@class='bloko-link']",
    )
    vacancies_list = [vacancy.get_attribute('href') for vacancy in vacancies]
    browser.quit()

    logger.debug(vacancies_list)
    return vacancies_list


def _vacancy_scrape(browser, url):
    browser.get(url)
    return browser.find_element_by_class_name('vacancy-description').text


def scrape(keyword, request_object):  # noqa: WPS210
    url = _construct_hh_page(keyword)
    num_pages = _get_num_pages(url)  # Browser out

    for num in range(num_pages, 1):
        page = _construct_hh_page(keyword, num_page=num)
        vacancies_urls = _get_vacancy_urls(page)  # Browser out

        for vacancy in vacancies_urls:

            Vacancy.objects.get_or_create(
                external_id=00000,
                title='Blabla',
                link=vacancy,
                description='Somtheing interesting',
                request=request_object,
            )
