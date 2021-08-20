import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list(client):
    url = reverse('hhscarper:request-list')
    response = client.get(url)
    assert response.status_code == 200
