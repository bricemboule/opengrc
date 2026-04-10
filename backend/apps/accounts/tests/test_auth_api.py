import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_login_success():
    User.objects.create_user(username="user1", email="user1@test.com", password="Password123!")
    client = APIClient()
    response = client.post("/api/auth/login/", {"email": "user1@test.com", "password": "Password123!"}, format="json")
    assert response.status_code == 200
    assert "access" in response.data
    assert response.data["user"]["email"] == "user1@test.com"
