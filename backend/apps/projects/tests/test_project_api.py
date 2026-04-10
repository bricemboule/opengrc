import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.org.models import Organization
from apps.projects.models import Project

User = get_user_model()

@pytest.mark.django_db
def test_create_project():
    org = Organization.objects.create(name="Org A", code="ORGA")
    user = User.objects.create_user(username="manager", email="manager@test.com", password="Password123!", organization=org)
    user.is_superuser = True
    user.is_staff = True
    user.save(update_fields=["is_superuser", "is_staff"])
    client = APIClient()
    login_response = client.post("/api/auth/login/", {"email": "manager@test.com", "password": "Password123!"}, format="json")
    access = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = client.post("/api/projects/", {"name": "Project Alpha", "code": "PRJ001", "status": "draft"}, format="json")
    assert response.status_code == 201
    assert Project.objects.count() == 1
    assert Project.objects.first().name == "Project Alpha"
