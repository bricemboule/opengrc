import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.hr.models import Certificate, Department, JobTitle, Staff, StaffSkill, Team, TeamMember, TrainingCourse, TrainingEvent, TrainingParticipant
from apps.org.models import Organization
from apps.people.models import Person
from apps.volunteers.models import Skill

User = get_user_model()


@pytest.mark.django_db
def test_create_staff_catalog_and_training_resources():
    organization = Organization.objects.create(name="HR Demo", code="HR-DEMO")
    person = Person.objects.create(organization=organization, first_name="Awa", last_name="Sarr", gender="female")
    user = User.objects.create_user(
        username="hr-admin",
        email="hr@test.com",
        password="Password123!",
        organization=organization,
    )
    user.is_superuser = True
    user.is_staff = True
    user.save(update_fields=["is_superuser", "is_staff"])

    client = APIClient()
    login_response = client.post("/api/auth/login/", {"email": "hr@test.com", "password": "Password123!"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")

    department_response = client.post("/api/hr/departments/", {"organization": organization.id, "code": "DEP001", "name": "Operations"}, format="json")
    job_title_response = client.post("/api/hr/job-titles/", {"organization": organization.id, "code": "JOB001", "name": "Coordinator"}, format="json")
    staff_response = client.post(
        "/api/hr/staffs/",
        {
            "organization": organization.id,
            "person": person.id,
            "department": department_response.data["id"],
            "job_title": job_title_response.data["id"],
            "code": "STF001",
            "name": "Awa Sarr",
            "status": "active",
            "contract_end_date": "2026-12-31",
        },
        format="json",
    )

    skill = Skill.objects.create(organization=organization, code="SKL001", name="First Aid")
    team_response = client.post("/api/hr/teams/", {"organization": organization.id, "code": "TEAM001", "name": "Rapid Response"}, format="json")
    team_member_response = client.post(
        "/api/hr/team-members/",
        {"organization": organization.id, "team": team_response.data["id"], "staff": staff_response.data["id"], "role": "Lead"},
        format="json",
    )
    staff_skill_response = client.post(
        "/api/hr/staff-skills/",
        {"organization": organization.id, "staff": staff_response.data["id"], "skill": skill.id, "proficiency": "advanced"},
        format="json",
    )
    training_course_response = client.post("/api/hr/training-courses/", {"organization": organization.id, "code": "TC001", "name": "Emergency Coordination"}, format="json")
    certificate_response = client.post("/api/hr/certificates/", {"organization": organization.id, "code": "CERT001", "name": "Emergency Certificate"}, format="json")
    training_event_response = client.post(
        "/api/hr/training-events/",
        {
            "organization": organization.id,
            "training_course": training_course_response.data["id"],
            "certificate": certificate_response.data["id"],
            "code": "TE001",
            "name": "Emergency Coordination Bootcamp",
            "start_date": "2026-05-01",
            "end_date": "2026-05-03",
        },
        format="json",
    )
    training_participant_response = client.post(
        "/api/hr/training-participants/",
        {
            "organization": organization.id,
            "training_event": training_event_response.data["id"],
            "staff": staff_response.data["id"],
            "completion_status": "registered",
            "certificate_awarded": False,
        },
        format="json",
    )

    assert department_response.status_code == 201
    assert job_title_response.status_code == 201
    assert staff_response.status_code == 201
    assert team_response.status_code == 201
    assert team_member_response.status_code == 201
    assert staff_skill_response.status_code == 201
    assert training_course_response.status_code == 201
    assert certificate_response.status_code == 201
    assert training_event_response.status_code == 201
    assert training_participant_response.status_code == 201
    assert Department.objects.count() == 1
    assert JobTitle.objects.count() == 1
    assert Staff.objects.count() == 1
    assert Team.objects.count() == 1
    assert TeamMember.objects.count() == 1
    assert StaffSkill.objects.count() == 1
    assert TrainingCourse.objects.count() == 1
    assert Certificate.objects.count() == 1
    assert TrainingEvent.objects.count() == 1
    assert TrainingParticipant.objects.count() == 1
