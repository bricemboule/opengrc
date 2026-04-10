import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.org.models import Organization
from apps.people.models import Person
from apps.projects.models import Activity, Project, Task

User = get_user_model()


@pytest.mark.django_db
def test_create_activity_and_task():
    organization = Organization.objects.create(name="Org Projects", code="ORG-PROJECTS")
    user = User.objects.create_user(
        username="project-manager",
        email="project-manager@test.com",
        password="Password123!",
        organization=organization,
    )
    user.is_superuser = True
    user.is_staff = True
    user.save(update_fields=["is_superuser", "is_staff"])
    project = Project.objects.create(organization=organization, name="Response", code="PRJ-001")
    person = Person.objects.create(organization=organization, first_name="Alice", last_name="Manager")

    client = APIClient()
    login_response = client.post("/api/auth/login/", {"email": "project-manager@test.com", "password": "Password123!"}, format="json")
    access = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    activity_response = client.post(
        "/api/projects/activities/",
        {"project": project.id, "name": "Field Assessment", "status": "planned", "contact_person": person.id},
        format="json",
    )
    activity_id = activity_response.data["id"]
    task_response = client.post(
        "/api/projects/tasks/",
        {"project": project.id, "activity": activity_id, "title": "Prepare checklist", "status": "new", "priority": "high"},
        format="json",
    )

    assert activity_response.status_code == 201
    assert task_response.status_code == 201
    assert Activity.objects.count() == 1
    assert Task.objects.count() == 1
