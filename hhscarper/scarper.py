import logging
import time
from datetime import datetime
from random import randint

import requests
from hhscarper.models import Request, Vacancy
from hhscarper.preprocessor import get_description_text, preprocess_text

logger = logging.getLogger(__name__)


def scrape(keyword, request_obj_id):
    request_obj = Request.objects.get(pk=request_obj_id)
    start = datetime.now()
    time.sleep(3)
    url = f'https://api.hh.ru/vacancies?text={keyword}'
    logger.debug(url)

    num_pages = requests.get(url).json()['pages']  # noqa: E501
    time.sleep(randint(4, 7))
    base_url = 'https://api.hh.ru/vacancies?per_page=100&text={0}&page={1}'
    pages = (base_url.format(keyword, num) for num in range(num_pages))

    for page in pages:
        page_items = requests.get(page).json()['items']
        time.sleep(randint(3, 6))
        vacancies = (vacancy['id'] for vacancy in page_items)

        for vacancy_id in vacancies:
            logger.debug(vacancy_id)
            vacancy = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
            time.sleep(randint(1, 3))
            vacancy_data = vacancy.json()

            description = get_description_text(vacancy_data['description'])
            skills = [skill['name'] for skill in vacancy_data['key_skills']]
            lemmas = list(preprocess_text(description))

            Vacancy.objects.get_or_create(
                external_id=vacancy_data['id'],
                title=vacancy_data['name'],
                link=vacancy_data['alternate_url'],
                description=description,
                key_skills=skills,
                lemmas=lemmas,
                request=request_obj,
            )
    delta = datetime.now() - start
    time_delta = (datetime.min + delta).time()
    request_obj.time = time_delta
    request_obj.status = 'Resolved'
    request_obj.save()
