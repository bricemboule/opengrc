from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.hr.models import Certificate, Department, JobTitle, Staff, StaffSkill, Team, TeamMember, TrainingCourse, TrainingEvent, TrainingParticipant
from apps.org.models import Facility, FacilityType, OfficeType, Organization, OrganizationType, Site
from apps.people.models import Contact, Identity, Person
from apps.projects.models import Activity, Project, Task
from apps.volunteers.models import Skill


class Command(BaseCommand):
    help = "Charge un jeu de donnees de demonstration minimal aligne sur les modules EDEN principaux."

    def handle(self, *args, **options):
        user_model = get_user_model()

        organization, _ = Organization.objects.get_or_create(
            code="EDEN-DEMO",
            defaults={
                "name": "EDEN Demo Organization",
                "email": "demo@eden.local",
                "phone": "+237600000000",
                "is_active": True,
            },
        )

        user, created = user_model.objects.get_or_create(
            email="admin@eden.local",
            defaults={
                "username": "admin-eden",
                "organization": organization,
                "is_staff": True,
                "is_superuser": True,
                "full_name": "EDEN Administrator",
            },
        )
        if created:
            user.set_password("Password123!")
            user.save()

        organization_type, _ = OrganizationType.objects.get_or_create(
            organization=organization,
            code="NGO",
            defaults={"name": "NGO", "description": "Organisation non gouvernementale"},
        )
        office_type, _ = OfficeType.objects.get_or_create(
            organization=organization,
            code="COORD",
            defaults={"name": "Coordination Office", "description": "Bureau de coordination"},
        )
        facility_type, _ = FacilityType.objects.get_or_create(
            organization=organization,
            code="CLINIC",
            defaults={"name": "Clinic", "description": "Centre de soins"},
        )
        if organization.organization_type_id != organization_type.id:
            organization.organization_type = organization_type
            organization.save(update_fields=["organization_type"])

        person, _ = Person.objects.get_or_create(
            organization=organization,
            first_name="Marie",
            last_name="Operatrice",
            defaults={"gender": "female"},
        )
        Contact.objects.get_or_create(
            organization=organization,
            person=person,
            contact_type="EMAIL",
            value="marie.operatrice@example.com",
            defaults={"is_primary": True},
        )
        Identity.objects.get_or_create(
            organization=organization,
            person=person,
            document_type="passport",
            document_number="CM-0001",
            defaults={"issued_country": "CM"},
        )

        department, _ = Department.objects.get_or_create(
            organization=organization,
            code="OPS",
            defaults={"name": "Operations", "status": "active"},
        )
        job_title, _ = JobTitle.objects.get_or_create(
            organization=organization,
            code="COORD",
            defaults={"name": "Coordinator", "status": "active"},
        )
        staff, _ = Staff.objects.get_or_create(
            organization=organization,
            code="STF-DEMO",
            defaults={
                "person": person,
                "department": department,
                "job_title": job_title,
                "name": "Marie Operatrice",
                "status": "active",
                "contract_end_date": date(2026, 12, 31),
            },
        )
        skill, _ = Skill.objects.get_or_create(
            organization=organization,
            code="SKILL-COORD",
            defaults={"name": "Coordination", "status": "active"},
        )
        StaffSkill.objects.get_or_create(
            organization=organization,
            staff=staff,
            skill=skill,
            defaults={"proficiency": "advanced", "status": "active"},
        )
        team, _ = Team.objects.get_or_create(
            organization=organization,
            code="TEAM-RESP",
            defaults={"name": "Rapid Response Team", "status": "active"},
        )
        TeamMember.objects.get_or_create(
            organization=organization,
            team=team,
            staff=staff,
            defaults={"role": "Lead", "status": "active"},
        )
        training_course, _ = TrainingCourse.objects.get_or_create(
            organization=organization,
            code="COURSE-EMERG",
            defaults={"name": "Emergency Coordination", "status": "active"},
        )
        certificate, _ = Certificate.objects.get_or_create(
            organization=organization,
            code="CERT-EMERG",
            defaults={"name": "Emergency Coordination Certificate", "status": "active"},
        )
        training_event, _ = TrainingEvent.objects.get_or_create(
            organization=organization,
            code="TRAIN-BOOTCAMP",
            defaults={
                "training_course": training_course,
                "certificate": certificate,
                "name": "Emergency Coordination Bootcamp",
                "start_date": date(2026, 5, 1),
                "end_date": date(2026, 5, 3),
                "status": "planned",
            },
        )
        TrainingParticipant.objects.get_or_create(
            organization=organization,
            training_event=training_event,
            staff=staff,
            defaults={"completion_status": "registered", "certificate_awarded": False},
        )

        site, _ = Site.objects.get_or_create(
            organization=organization,
            code="SITE-DEMO",
            defaults={
                "name": "Douala Coordination Office",
                "office_type": office_type,
                "city": "Douala",
                "address": "Bonanjo",
                "status": "active",
                "latitude": 4.051100,
                "longitude": 9.767900,
            },
        )
        Facility.objects.get_or_create(
            organization=organization,
            code="FAC-DEMO",
            defaults={
                "site": site,
                "facility_type_ref": facility_type,
                "name": "Douala Health Post",
                "facility_type": "clinic",
                "city": "Douala",
                "latitude": 4.048300,
                "longitude": 9.704300,
            },
        )

        project, _ = Project.objects.get_or_create(
            organization=organization,
            code="PRJ-DEMO",
            defaults={"name": "EDEN Response Pilot", "status": "active"},
        )
        activity, _ = Activity.objects.get_or_create(
            organization=organization,
            project=project,
            name="Baseline Assessment",
            defaults={"status": "planned", "contact_person": person},
        )
        Task.objects.get_or_create(
            organization=organization,
            project=project,
            activity=activity,
            title="Prepare field checklist",
            defaults={"status": "new", "priority": "high", "assigned_to": person},
        )

        self.stdout.write(self.style.SUCCESS("Demo data loaded."))
        self.stdout.write(self.style.SUCCESS("Login: admin@eden.local / Password123!"))
