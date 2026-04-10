import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.org.models import Facility, Organization, Site

User = get_user_model()


@pytest.mark.django_db
def test_create_site_and_facility():
    organization = Organization.objects.create(name="Org Sites", code="ORG-SITES")
    user = User.objects.create_user(
        username="site-manager",
        email="sites@test.com",
        password="Password123!",
        organization=organization,
    )
    user.is_superuser = True
    user.is_staff = True
    user.save(update_fields=["is_superuser", "is_staff"])

    client = APIClient()
    login_response = client.post("/api/auth/login/", {"email": "sites@test.com", "password": "Password123!"}, format="json")
    access = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    site_response = client.post(
        "/api/org/sites/",
        {"name": "Douala Hub", "code": "SITE001", "city": "Douala", "address": "Bonanjo"},
        format="json",
    )
    site_id = site_response.data["id"]
    facility_response = client.post(
        "/api/org/facilities/",
        {"site": site_id, "name": "Main Clinic", "code": "FAC001", "facility_type": "clinic", "city": "Douala"},
        format="json",
    )

    assert site_response.status_code == 201
    assert facility_response.status_code == 201
    assert Site.objects.count() == 1
    assert Facility.objects.count() == 1
