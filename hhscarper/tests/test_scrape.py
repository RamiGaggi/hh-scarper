import logging
from datetime import datetime

import pytest
import requests_mock
from dotenv import load_dotenv
from hhscarper.models import Request, Vacancy, VacancyRequest
from hhscarper.scarper import get_vacancy_info, scrape

load_dotenv()

logger = logging.getLogger(__name__)

KEYWORD = 'test_keyword'
URL = 'https://api-test.hhscarpertest.ru/vacancies'
URL_KEYWWORD = f'{URL}?per_page=100&text={KEYWORD}'
PAGE_URL = f'{URL}?per_page=100&text={KEYWORD}&page=0'

vacancies = {
    'vacancy_id1': 111,
    'vacancy_id2': 222,
    'vacancy_id3': 333,
    'vacancy_id4': 000,
}

VACANCY_URL1 = f'{URL}/{vacancies["vacancy_id1"]}'
VACANCY_URL2 = f'{URL}/{vacancies["vacancy_id2"]}'
VACANCY_URL3 = f'{URL}/{vacancies["vacancy_id3"]}'
VACANCY_URL4 = f'{URL}/{vacancies["vacancy_id4"]}'


@pytest.fixture
def initial():
    time = datetime.now().time()
    Request.objects.create(
        keyword=KEYWORD,
        status='pending',
        time=time,
    )
    Vacancy.objects.create(
        external_id=333,
        title='Existed vacancy',
        link='https://xa.com',
        description='Existed vacancy',
        key_skills=['1', '2', '3'],
        lemmas=['4', '5', '6'],
    )


@pytest.mark.django_db
def test_scrape(client, initial):
    assert Request.objects.count() == 1
    assert Vacancy.objects.count() == 1

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
                'items': [
                    {'id': vacancy_id} for vacancy_id in vacancies.values()
                ],
            },
        )
        mock.get(VACANCY_URL1, json={
            'id': vacancies['vacancy_id1'],
            'name': 'Some title1',
            'description': 'Magic test1',
            'key_skills': [{'name': 'Postgres'}],
            'alternate_url': 'https://test1.test',
        })
        mock.get(VACANCY_URL2, json={
            'id': vacancies['vacancy_id2'],
            'name': 'Another title2',
            'description': 'Magic test2',
            'key_skills': [],
            'alternate_url': 'https://tes2.test',
        })
        mock.get(VACANCY_URL3, json={
            'id': vacancies['vacancy_id3'],
            'name': 'Another title3',
            'description': 'Magic test3',
            'key_skills': [],
            'alternate_url': 'https://tes2.test',
        })
        mock.get(VACANCY_URL4, status_code=404, json={
            'id': vacancies['vacancy_id4'],
            'name': 'Another title4',
            'description': 'Magic test4',
            'key_skills': [],
            'alternate_url': 'https://tes2.test',
        })
    # Actual testing
        req_obj = Request.objects.get(keyword=KEYWORD)
        scrape_result = scrape(
            keyword=KEYWORD,
            request_obj_id=req_obj.pk,
            adress='https://api-test.hhscarpertest.ru/vacancies',
        )

        vacancy_object = req_obj.vacancy_set.get(external_id=111)
        missing_vacancy_object = req_obj.vacancy_set.get(external_id=000)

        assert VacancyRequest.objects.count() == 4
        assert req_obj.vacancy_set.count() == 4
        assert Request.objects.count() == 1
        assert Vacancy.objects.count() == 4
        assert scrape_result == 4

        assert vacancy_object.title == 'Some title1'
        assert vacancy_object.link == 'https://test1.test'
        assert vacancy_object.description == 'Magic test1'
        assert 'Postgres' in vacancy_object.key_skills
        assert 'MAGIC' in vacancy_object.lemmas
        assert 'TEST1' in vacancy_object.lemmas

        assert missing_vacancy_object.is_missing
        # Test for updateing
        mock.get(VACANCY_URL1, json={
            'id': vacancies['vacancy_id1'],
            'name': 'Update Some title1',
            'description': 'Update Magic test1',
            'key_skills': [{'name': 'Postgres'}],
            'alternate_url': 'https://test1.test',
        })
        mock.get(VACANCY_URL4, status_code=200, json={
            'id': vacancies['vacancy_id4'],
            'name': 'Update',
            'description': 'Update desc',
            'key_skills': [{'name': 'Update'}],
            'alternate_url': 'https://update.test',
        })

        vacancy_info_result = get_vacancy_info(
            Request.objects.get(keyword=KEYWORD),
            (vac.external_id for vac in Vacancy.objects.all()),
            adress='https://api-test.hhscarpertest.ru/vacancies',
            update=True,
        )

        assert VacancyRequest.objects.count() == 4
        update_missing_vacancy_obj = req_obj.vacancy_set.get(external_id=000)
        update_existing_vacancy_obj = req_obj.vacancy_set.get(external_id=111)
        assert update_missing_vacancy_obj.title == 'Update'
        assert update_existing_vacancy_obj.description == 'Update Magic test1'
        assert vacancy_info_result == 4
