import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.org.models import Facility, FacilityType, OfficeType, Organization, OrganizationType, Site

User = get_user_model()


@pytest.mark.django_db
def test_create_site_and_facility():
    organization = Organization.objects.create(name="Org Sites", code="ORG-SITES")
    organization_type = OrganizationType.objects.create(organization=organization, code="ORGTYPE1", name="National Society")
    office_type = OfficeType.objects.create(organization=organization, code="OFFTYPE1", name="Regional Office")
    facility_type = FacilityType.objects.create(organization=organization, code="FACTYPE1", name="Clinic")
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
        {
            "name": "Douala Hub",
            "code": "SITE001",
            "city": "Douala",
            "address": "Bonanjo",
            "office_type": office_type.id,
            "latitude": "4.051100",
            "longitude": "9.767900",
        },
        format="json",
    )
    site_id = site_response.data["id"]
    facility_response = client.post(
        "/api/org/facilities/",
        {
            "site": site_id,
            "name": "Main Clinic",
            "code": "FAC001",
            "facility_type": "clinic",
            "facility_type_ref": facility_type.id,
            "city": "Douala",
            "latitude": "4.048300",
            "longitude": "9.704300",
        },
        format="json",
    )
    organization_update = client.patch(f"/api/org/{organization.id}/", {"organization_type": organization_type.id}, format="json")

    assert site_response.status_code == 201
    assert facility_response.status_code == 201
    assert organization_update.status_code == 200
    assert Site.objects.count() == 1
    assert Facility.objects.count() == 1
