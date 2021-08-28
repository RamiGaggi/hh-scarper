from datetime import datetime

import pytest
from django.urls import reverse
from hhscarper.models import Request, SkillReport, WordReport


@pytest.fixture
def initial():
    time = datetime.now().time()
    Request.objects.create(
        keyword='KEYWORD_PENDING',
        status='Pending',
        time=time,
    )
    Request.objects.create(
        keyword='KEYWORD_RESOLVED',
        status='Resolved',
        time=time,
    )
    SkillReport.objects.create(
        data={'skill': 14, 'bar': 1, 'zax': 4},
        request=Request.objects.get(keyword='KEYWORD_RESOLVED'),
    )
    WordReport.objects.create(
        data={'word': 12, 'bar': 2, 'vax': 5},
        request=Request.objects.get(keyword='KEYWORD_RESOLVED'),
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
        kwargs={'pk': Request.objects.get(keyword='KEYWORD_PENDING').pk},
    )
    response_pending = client.get(url)
    assert response_pending.status_code == 302
    url = reverse(
        'hhscarper:request-detail',
        kwargs={'pk': Request.objects.get(keyword='KEYWORD_RESOLVED').pk},
    )
    response_resolved = client.get(url)
    assert response_resolved.status_code == 200


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
