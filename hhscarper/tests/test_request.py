import logging
from datetime import datetime

import pytest
from django.urls import reverse
from dotenv import load_dotenv
from hhscarper.models import Request

load_dotenv()

logger = logging.getLogger(__name__)


@pytest.fixture
def requests():
    time = datetime.now().time()
    Request.objects.create(
        keyword='Python',
        status='pending',
        time=time,
    )
    Request.objects.create(
        keyword='Haskell',
        status='resolved',
        time=time,
    )
    Request.objects.create(
        keyword='Celery',
        status='pending',
        time=time,
    )


@pytest.mark.django_db
def test_list(client, requests):
    url = reverse('hhscarper:request-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(Request.objects.all()) == 3


@pytest.mark.django_db
def test_detail(client, requests, db):
    req_obj = Request.objects.get(keyword='Haskell')
    url = reverse('hhscarper:request-detail', kwargs={'pk': req_obj.pk})
    response = client.get(url)
    assert response.status_code == 200
