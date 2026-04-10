import pytest
from django.test import Client

@pytest.mark.django_db
def test_healthcheck():
    client = Client()
    response = client.get("/api/health/")
    assert response.status_code in [200, 503]
    data = response.json()
    assert "database" in data
    assert "redis" in data
