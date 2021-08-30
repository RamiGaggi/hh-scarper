import logging
from datetime import datetime

import pytest
from django.urls import reverse
from hhscarper.models import Request, SkillReport, User, WordReport

logger = logging.getLogger(__name__)


@pytest.fixture
def data():
    credentials = {
        'username': 'RamilGG',
        'password': 'asd_asAFS34',
    }
    User.objects.create_user(**credentials)
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

    data = {
        'request_pending': Request.objects.get(keyword='KEYWORD_PENDING'),
        'request_resolved': Request.objects.get(keyword='KEYWORD_RESOLVED'),
        'credentials': credentials,
    }
    data.update(
        {
            'skillreport': SkillReport.objects.get(request=data['request_resolved']),
            'wordreport': WordReport.objects.get(request=data['request_resolved']),
        },
    )
    return data


@pytest.mark.django_db
def test_request_list(client):
    url = reverse('hhscarper:request-list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_detail(client, data):
    url = reverse(
        'hhscarper:request-detail',
        kwargs={'pk': data['request_pending'].pk},
    )
    response_pending = client.get(url)
    assert response_pending.status_code == 302
    url = reverse(
        'hhscarper:request-detail',
        kwargs={'pk': data['request_resolved'].pk},
    )
    response_resolved = client.get(url)
    assert response_resolved.status_code == 200


@pytest.mark.django_db
def test_request_delete(client, data):
    url_login = reverse('hhscarper:user-login')
    response_login = client.post(url_login, data['credentials'])
    assert response_login.status_code == 302

    url = reverse(
        'hhscarper:request-delete',
        kwargs={'pk': data['request_resolved'].pk},
    )
    response_resolved = client.post(url)
    with pytest.raises(Request.DoesNotExist):
        Request.objects.get(pk=data['request_resolved'].pk)
    assert response_resolved.status_code == 302


@pytest.mark.django_db
def test_dashboard(client):
    url = reverse('hhscarper:dashboard')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_skillreport_detail(client, data):
    url = reverse(
        'hhscarper:skill-report-detail',
        kwargs={'pk': data['skillreport'].pk},
    )
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_wordreport_detail(client, data):
    url = reverse(
        'hhscarper:word-report-detail',
        kwargs={'pk': data['wordreport'].pk},
    )
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_export_data(client, data):
    req_name = data['request_resolved'].keyword
    url = f"{reverse('hhscarper:export-data')}?report=skill&request={req_name}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.get('Content-Disposition') == f'attachment; filename="{req_name}_skill.csv"'
