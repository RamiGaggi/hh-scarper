from datetime import datetime

import pytest
from django.urls import reverse
from hhscarper.models import Request


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
def test_detail(client, requests):
    url = reverse('hhscarper:request-detail', kwargs={'pk': 2})
    response = client.get(url)
    assert response.status_code == 200
    assert Request.objects.get(pk=2).keyword == 'Haskell'
