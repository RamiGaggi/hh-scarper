import logging
import time
from datetime import datetime
from random import randint

import requests
from django.forms import model_to_dict
from hhscarper.models import Request, Vacancy
from hhscarper.preprocessor import clean_text, preprocess_text

logger = logging.getLogger(__name__)


def scrape(keyword, request_obj_id, adress='https://api.hh.ru/vacancies'):
    request_obj = Request.objects.get(pk=request_obj_id)

    start = datetime.now()

    time.sleep(3)
    url = f'{adress}?text={keyword}'
    logger.debug(url)

    num_pages = requests.get(url).json()['pages']  # noqa: E501
    time.sleep(randint(4, 7))
    base_url = '{0}?per_page=100&text={1}&page={2}'
    pages = (base_url.format(adress, keyword, num) for num in range(num_pages))

    for page in pages:
        page_items = requests.get(page).json()['items']
        time.sleep(randint(3, 6))  # Sleep
        vacancies = (vacancy['id'] for vacancy in page_items)
        db_vacancies = set(Vacancy.objects.values_list('external_id', flat=True))  # noqa: E501

        for vacancy_id in vacancies:
            logger.debug(vacancy_id)
            if vacancy_id in db_vacancies:
                vacancy_instance = Vacancy.objects.filter(external_id=vacancy_id).first()  # noqa: E501
                kwargs = model_to_dict(
                    vacancy_instance,
                    exclude=['id', 'request'],
                )
                vacancy_obj = Vacancy.objects.create(**kwargs)
                vacancy_obj.request.add(request_obj)
                continue

            vacancy = requests.get(f'{adress}/{vacancy_id}')
            time.sleep(randint(1, 3))  # Sleep
            vacancy_data = vacancy.json()

            description = clean_text(vacancy_data['description'])
            skills = [skill['name'] for skill in vacancy_data['key_skills']]
            lemmas = list(preprocess_text(description))

            vacancy_obj = Vacancy.objects.create(
                external_id=vacancy_data['id'],
                title=vacancy_data['name'],
                link=vacancy_data['alternate_url'],
                description=description,
                key_skills=skills,
                lemmas=lemmas,
            )
            vacancy_obj.request.add(request_obj)

    delta = datetime.now() - start
    time_delta = (datetime.min + delta).time()
    request_obj.time = time_delta
    request_obj.status = 'Resolved'
    request_obj.save()
