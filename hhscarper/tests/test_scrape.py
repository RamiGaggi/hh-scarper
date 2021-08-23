import logging
from datetime import datetime

import pytest
import requests_mock
from dotenv import load_dotenv
from hhscarper.models import Request, VacancyRequest
from hhscarper.scarper import scrape

load_dotenv()

logger = logging.getLogger(__name__)

KEYWORD = 'test_keyword'
URL = 'https://api-test.hhscarpertest.ru/vacancies'
URL_KEYWWORD = f'{URL}?per_page=100&text={KEYWORD}'
PAGE_URL = f'{URL}?per_page=100&text={KEYWORD}&page=0'
VACANCY_ID1 = 000
VACANCY_ID2 = 777
VACANCY_URL1 = f'{URL}/{VACANCY_ID1}'
VACANCY_URL2 = f'{URL}/{VACANCY_ID2}'


@pytest.fixture
def requests():
    time = datetime.now().time()
    Request.objects.create(
        keyword=KEYWORD,
        status='pending',
        time=time,
    )


@pytest.mark.django_db
def test_scrape(client, requests):
    req_obj = Request.objects.get(keyword=KEYWORD)
    with requests_mock.Mocker() as mock:
        mock.get(
            URL_KEYWWORD,
            json={
                'pages': 1,
                'found': 234,
            },
        )
        mock.get(
            PAGE_URL,
            json={
                'items': [{'id': 000}, {'id': 777}],
            },
        )
        mock.get(VACANCY_URL1, json={
            'id': 000,
            'name': 'Some title',
            'description': 'Magic test',
            'key_skills': [{'name': 'Postgres'}],
            'alternate_url': 'https://test1.test',
        })
        mock.get(VACANCY_URL2, json={
            'id': 777,
            'name': 'Another title',
            'description': 'Magic test2',
            'key_skills': [],
            'alternate_url': 'https://tes2.test',
        })
        scrape_result = scrape(
            keyword=KEYWORD,
            request_obj_id=req_obj.pk,
            adress='https://api-test.hhscarpertest.ru/vacancies',
        )

    vacancy_object = req_obj.vacancy_set.get(external_id=000)

    assert Request.objects.all().count() == 1
    assert VacancyRequest.objects.all().count() == 2
    assert req_obj.vacancy_set

    assert vacancy_object.title == 'Some title'
    assert vacancy_object.link == 'https://test1.test'
    assert vacancy_object.description == 'Magic test'
    assert vacancy_object.key_skills == ['Postgres']
    assert scrape_result == 2
