import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.org.models import Organization

User = get_user_model()

@pytest.mark.django_db
def test_login_and_get_organizations():
    user = User.objects.create_user(username="admin", email="admin@test.com", password="Password123!")
    user.is_superuser = True
    user.is_staff = True
    user.save(update_fields=["is_superuser", "is_staff"])
    Organization.objects.create(name="Org Test", code="ORG001", is_active=True)

    client = APIClient()
    login_response = client.post("/api/auth/login/", {"email": "admin@test.com", "password": "Password123!"}, format="json")
    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    response = client.get("/api/org/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Org Test"
