from datetime import datetime

import pytest
from django.urls import reverse
from hhscarper.models import Request


@pytest.fixture
def initial():
    time = datetime.now().time()
    Request.objects.create(
        keyword='KEYWORD',
        status='pending',
        time=time,
    )


@pytest.mark.django_db
def test_request_list(client):
    url = reverse('hhscarper:request-list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_detail(client, initial):
    url = reverse(
        'hhscarper:request-detail',
        kwargs={'pk': Request.objects.get(keyword='KEYWORD').pk},
    )
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard(client):
    url = reverse('hhscarper:dashboard')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_vacancy_list(client):
    url = reverse('hhscarper:vacancy-list')
    response = client.get(url)
    assert response.status_code == 200
