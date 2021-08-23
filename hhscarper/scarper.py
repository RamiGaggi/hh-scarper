import logging
import time
from datetime import datetime
from random import randint

import requests
from hhscarper.models import Request, Vacancy
from hhscarper.preprocessor import clean_text, preprocess_text
from hhscarper.reports import REPORTS, make_report

logger = logging.getLogger(__name__)


def scrape(keyword, request_obj_id, adress='https://api.hh.ru/vacancies'):
    request_obj = Request.objects.get(pk=request_obj_id)
    start = datetime.now()
    url = f'{adress}?per_page=100&text={keyword}'
    json_data = requests.get(url).json()
    num_pages = json_data['pages']  # noqa: E501
    logger.info(f"found: {json_data['found']}")

    time.sleep(randint(4, 7))
    base_url = '{0}?per_page=100&text={1}&page={2}'
    pages = (base_url.format(adress, keyword, num) for num in range(num_pages))
    db_vacancies = set(Vacancy.objects.all().values_list('external_id', flat=True))  # noqa: E501

    for page in pages:
        page_items = requests.get(page).json()['items']
        time.sleep(randint(3, 6))  # Sleep
        vacancies = (int(vacancy['id']) for vacancy in page_items)
        counter = 0
        for vacancy_id in vacancies:
            logger.info(f'vacancy_id: {vacancy_id}')
            counter += 1
            if vacancy_id in db_vacancies:
                vacancy_instance = Vacancy.objects.get(external_id=vacancy_id)  # noqa: E501
                vacancy_instance.requests.add(request_obj)
                continue

            vacancy = requests.get(f'{adress}/{vacancy_id}')
            time.sleep(randint(1, 3))  # Sleep
            vacancy_data = vacancy.json()

            description = clean_text(vacancy_data['description'])
            skills = [skill['name'] for skill in vacancy_data['key_skills']]
            lemmas = preprocess_text(description)

            vacancy_obj = Vacancy.objects.create(
                external_id=vacancy_data['id'],
                title=vacancy_data['name'],
                link=vacancy_data['alternate_url'],
                description=description,
                key_skills=skills,
                lemmas=lemmas,
            )
            vacancy_obj.requests.add(request_obj)

    make_report(request_obj_id, *REPORTS)

    delta = datetime.now() - start
    time_delta = (datetime.min + delta).time()
    request_obj.time = time_delta
    request_obj.status = 'Resolved'
    request_obj.save()
    return counter
