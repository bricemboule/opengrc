import json

import pytest
from django.test import Client

from apps.accounts.models import User
from apps.cybergrc.models import ContingencyPlan, CriticalInfrastructure, Sector, Stakeholder
from apps.incident_management.models import Incident, IncidentCommunication, IncidentTask, IncidentUpdate
from apps.org.models import Organization


@pytest.fixture
def organization():
    return Organization.objects.create(name="Incident Org", code="INC-ORG")


@pytest.fixture
def other_organization():
    return Organization.objects.create(name="Other Org", code="INC-ORG-2")


@pytest.fixture
def user(organization):
    return User.objects.create_user(
        username="incident-admin",
        email="incident-admin@test.local",
        password="Password123!",
        organization=organization,
        is_staff=True,
    )


@pytest.fixture
def api_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def stakeholder(organization):
    return Stakeholder.objects.create(organization=organization, name="National CERT")


@pytest.fixture
def sector(organization):
    return Sector.objects.create(organization=organization, code="energy", name="Energy")


@pytest.fixture
def infrastructure(organization, stakeholder, sector):
    return CriticalInfrastructure.objects.create(
        organization=organization,
        owner_stakeholder=stakeholder,
        code="cii-001",
        name="National Power Control",
        sector_ref=sector,
        sector=sector.name,
    )


@pytest.fixture
def plan(organization):
    return ContingencyPlan.objects.create(organization=organization, title="National Cyber Contingency")


@pytest.mark.django_db
def test_create_incident_with_related_records(api_client, organization, user, stakeholder, sector, infrastructure, plan):
    response = api_client.post(
        "/api/incident-management/incidents/",
        data=json.dumps(
            {
                "title": "Power control malware outbreak",
                "incident_type": "malware",
                "severity": "critical",
                "status": "reported",
                "source": "monitoring",
                "reported_at": "2026-04-17T09:00:00Z",
                "incident_coordinator": user.id,
                "lead_stakeholder": stakeholder.id,
                "linked_plan": plan.id,
                "affected_sectors": [sector.id],
                "affected_infrastructure": [infrastructure.id],
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 201
    incident = Incident.objects.get()
    assert incident.organization == organization
    assert incident.affected_sectors.count() == 1
    assert incident.affected_infrastructure.count() == 1


@pytest.mark.django_db
def test_incident_rejects_cross_organization_links(api_client, user, stakeholder, other_organization):
    foreign_sector = Sector.objects.create(organization=other_organization, code="telecom", name="Telecom")

    response = api_client.post(
        "/api/incident-management/incidents/",
        data=json.dumps(
            {
                "title": "Foreign link test",
                "incident_type": "service_outage",
                "severity": "medium",
                "status": "reported",
                "source": "internal_report",
                "reported_at": "2026-04-17T09:00:00Z",
                "incident_coordinator": user.id,
                "lead_stakeholder": stakeholder.id,
                "affected_sectors": [foreign_sector.id],
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = json.loads(response.content)
    assert "affected_sectors" in payload


@pytest.mark.django_db
def test_incident_timeline_endpoint_returns_nested_operational_objects(api_client, organization, user):
    incident = Incident.objects.create(
        organization=organization,
        title="National DDoS wave",
        incident_type="ddos",
        severity="high",
        status="active",
        source="external_report",
        reported_at="2026-04-17T09:00:00Z",
        incident_coordinator=user,
    )
    IncidentUpdate.objects.create(
        organization=organization,
        incident=incident,
        title="Initial triage",
        update_type="situation",
        message="Traffic is being filtered.",
        recorded_at="2026-04-17T09:30:00Z",
    )
    IncidentTask.objects.create(
        organization=organization,
        incident=incident,
        title="Activate upstream mitigation",
        status="in_progress",
        priority="high",
        assigned_to=user,
    )
    IncidentCommunication.objects.create(
        organization=organization,
        incident=incident,
        subject="Operator briefing",
        direction="outbound",
        channel="briefing",
        message="Operators have been briefed.",
        sent_at="2026-04-17T10:00:00Z",
    )

    response = api_client.get(f"/api/incident-management/incidents/{incident.id}/timeline/")

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["incident"]["title"] == incident.title
    assert len(payload["updates"]) == 1
    assert len(payload["tasks"]) == 1
    assert len(payload["communications"]) == 1
