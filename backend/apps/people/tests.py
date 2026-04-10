import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.org.models import Organization
from apps.people.models import Contact, Identity, Person

User = get_user_model()


@pytest.mark.django_db
def test_create_contact_and_identity():
    organization = Organization.objects.create(name="Org People", code="ORG-PEOPLE")
    user = User.objects.create_user(
        username="people-manager",
        email="people@test.com",
        password="Password123!",
        organization=organization,
    )
    user.is_superuser = True
    user.is_staff = True
    user.save(update_fields=["is_superuser", "is_staff"])
    person = Person.objects.create(
        organization=organization,
        first_name="Jean",
        last_name="Dupont",
        gender="male",
    )

    client = APIClient()
    login_response = client.post("/api/auth/login/", {"email": "people@test.com", "password": "Password123!"}, format="json")
    access = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    contact_response = client.post(
        "/api/people/contacts/",
        {"person": person.id, "contact_type": "EMAIL", "value": "jean.dupont@example.com", "is_primary": True},
        format="json",
    )
    identity_response = client.post(
        "/api/people/identities/",
        {"person": person.id, "document_type": "passport", "document_number": "P123456", "issued_country": "CM"},
        format="json",
    )

    assert contact_response.status_code == 201
    assert identity_response.status_code == 201
    assert Contact.objects.count() == 1
    assert Identity.objects.count() == 1
