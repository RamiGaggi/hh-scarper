import logging
from datetime import datetime

import requests
from hhscarper.models import Request, Vacancy
from hhscarper.preprocessor import clean_text, preprocess_text
from hhscarper.reports import REPORTS, make_report

logger = logging.getLogger(__name__)


def get_vacancy_info(  # noqa: WPS231, C901
    request_obj,
    vacancies,
    adress='https://api.hh.ru/vacancies',
    update=False,
):
    counter = 0
    for vacancy_id in vacancies:
        counter += 1
        logger.info(f'vacancy_id: {vacancy_id}')
        # It's awful, but it will do
        is_missing = False
        prefetch_vacancy = Vacancy.objects.filter(external_id=vacancy_id).first()
        if prefetch_vacancy:
            is_missing = prefetch_vacancy.is_missing
        # Check if vacancy exists in databse
        # Check for update if there is need to update existing vacancies
        # Check if vacancy info is missing, so we can proceed further
        if prefetch_vacancy and not (is_missing or update):
            logger.info('Get vacancy from databse ^')
            vacancy_instance = Vacancy.objects.get(external_id=vacancy_id)
            vacancy_instance.requests.add(request_obj)
            continue

        url = f'{adress}/{vacancy_id}'
        vacancy = requests.get(url)
        if vacancy.status_code == 200:
            vacancy_data = vacancy.json()
            description = clean_text(vacancy_data['description'])
            skills = [skill['name'] for skill in vacancy_data['key_skills']]
            lemmas = preprocess_text(description)
            vacancy_obj = Vacancy.objects.update_or_create(
                external_id=vacancy_data['id'],
                defaults={
                    'title': vacancy_data['name'],
                    'link': vacancy_data['alternate_url'],
                    'description': description,
                    'key_skills': skills,
                    'lemmas': lemmas,
                    'is_missing': False,
                },
            )
            # If vacancy were missed in other request, check for update
            if not update:
                vacancy_obj[0].requests.add(request_obj)
        else:
            vacancy_obj = Vacancy.objects.update_or_create(
                external_id=vacancy_id,
                defaults={
                    'title': '',
                    'link': '',
                    'description': '',
                    'key_skills': [],
                    'lemmas': [],
                    'is_missing': True,
                },
            )
            logger.warning(f"Can't reach {url}")
        if not update:
            vacancy_obj[0].requests.add(request_obj)
    return counter


def scrape(keyword, request_obj_id, adress='https://api.hh.ru/vacancies'):
    logger.info(f'Keyword is: {keyword}')
    request_obj = Request.objects.get(pk=request_obj_id)
    start = datetime.now()
    url = f'{adress}?per_page=100&text={keyword}'
    json_data = requests.get(url).json()

    num_pages = json_data['pages']
    logger.info(f'Pages: {num_pages}')
    logger.info(f"found: {json_data['found']}")

    base_url = '{0}?per_page=100&text={1}&page={2}'
    pages = (base_url.format(adress, keyword, num) for num in range(num_pages))

    counter = 0
    for page in pages:
        logger.info(f'Page is: {page}')
        page_items = requests.get(page).json()['items']
        vacancies = (int(vacancy['id']) for vacancy in page_items)

        counter += get_vacancy_info(
            request_obj,
            vacancies,
            adress=adress,
        )

    make_report(request_obj_id, *REPORTS)

    delta = datetime.now() - start
    time_delta = (datetime.min + delta).time()
    request_obj.time = time_delta
    request_obj.status = 'Resolved'
    request_obj.save()
    return counter
