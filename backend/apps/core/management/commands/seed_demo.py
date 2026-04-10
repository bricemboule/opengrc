from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.org.models import Facility, FacilityType, OfficeType, Organization, OrganizationType, Site
from apps.people.models import Contact, Identity, Person
from apps.projects.models import Activity, Project, Task


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
