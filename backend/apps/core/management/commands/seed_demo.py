from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.cybergrc.models import (
    AuditFramework,
    ContingencyPlan,
    CriticalInfrastructure,
    CyberStandard,
    DeliverableMilestone,
    EmergencyResponseAsset,
    GovernanceArtifact,
    RiskRegisterEntry,
    SimulationExercise,
    Stakeholder,
    TrainingProgram,
)
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

        ministry_stakeholder, _ = Stakeholder.objects.get_or_create(
            organization=organization,
            name="MOCDE Cybersecurity Directorate",
            defaults={
                "stakeholder_type": "government",
                "sector": "Public sector",
                "focal_point": "Director of Cybersecurity",
                "email": "cyber@mocde.local",
                "engagement_role": "National coordination",
            },
        )
        operator_stakeholder, _ = Stakeholder.objects.get_or_create(
            organization=organization,
            name="National Telecom Backbone Operator",
            defaults={
                "stakeholder_type": "cii_owner",
                "sector": "Telecommunications",
                "focal_point": "CII Operations Lead",
                "email": "ops@backbone.local",
                "engagement_role": "CII owner and reporting focal point",
            },
        )
        additional_stakeholders = [
            {
                "name": "National Banking Supervision Unit",
                "stakeholder_type": "regulator",
                "sector": "Financial services",
                "focal_point": "Chief Banking Risk Supervisor",
                "email": "banking.supervision@demo.local",
                "engagement_role": "Banking cyber oversight and escalation",
                "status": "in_review",
            },
            {
                "name": "National CERT / CSIRT",
                "stakeholder_type": "cert",
                "sector": "National cyber defense",
                "focal_point": "Head of Incident Coordination",
                "email": "coordination@cert.demo.local",
                "engagement_role": "Incident response coordination and advisories",
                "status": "active",
            },
            {
                "name": "Power Grid Control Operator",
                "stakeholder_type": "cni_operator",
                "sector": "Energy",
                "focal_point": "Grid Security Manager",
                "email": "grid.security@demo.local",
                "engagement_role": "Critical infrastructure resilience focal point",
                "status": "planned",
            },
            {
                "name": "National Water Utility Authority",
                "stakeholder_type": "operator",
                "sector": "Water",
                "focal_point": "Utility Operations Director",
                "email": "water.ops@demo.local",
                "engagement_role": "Essential service continuity coordination",
                "status": "draft",
            },
            {
                "name": "International Cyber Cooperation Partner",
                "stakeholder_type": "partner",
                "sector": "Development partner",
                "focal_point": "Regional Program Lead",
                "email": "partnerships@demo.local",
                "engagement_role": "Technical assistance and capability support",
                "status": "submitted",
            },
            {
                "name": "Metropolitan Internet Exchange Association",
                "stakeholder_type": "other",
                "sector": "Internet infrastructure",
                "focal_point": "Association Coordinator",
                "email": "ixp@demo.local",
                "engagement_role": "Traffic resilience and member coordination",
                "status": "validated",
            },
            {
                "name": "National Retail Bank Group",
                "stakeholder_type": "bank",
                "sector": "Banking",
                "focal_point": "Chief Information Security Officer",
                "email": "ciso@retailbank.demo.local",
                "engagement_role": "Sector reporting and contingency execution",
                "status": "completed",
            },
        ]
        for stakeholder_defaults in additional_stakeholders:
            Stakeholder.objects.get_or_create(
                organization=organization,
                name=stakeholder_defaults["name"],
                defaults=stakeholder_defaults,
            )

        demo_coordinate_points = [
            {"location": "Banjul", "latitude": 13.454876, "longitude": -16.579032},
            {"location": "Serekunda", "latitude": 13.438811, "longitude": -16.678577},
            {"location": "Bakau", "latitude": 13.478056, "longitude": -16.681944},
            {"location": "Brikama", "latitude": 13.271139, "longitude": -16.649444},
            {"location": "Farafenni", "latitude": 13.566667, "longitude": -15.600000},
            {"location": "Kerewan", "latitude": 13.489800, "longitude": -16.089100},
            {"location": "Soma", "latitude": 13.433333, "longitude": -15.533333},
            {"location": "Mansa Konko", "latitude": 13.443289, "longitude": -15.535972},
            {"location": "Janjanbureh", "latitude": 13.541667, "longitude": -14.766667},
            {"location": "Basse", "latitude": 13.309167, "longitude": -14.222778},
            {"location": "Essau", "latitude": 13.487222, "longitude": -16.534722},
            {"location": "Lamin", "latitude": 13.352778, "longitude": -16.433333},
        ]

        def coordinate_for(index):
            return demo_coordinate_points[(index - 1) % len(demo_coordinate_points)]

        critical_infrastructure, _ = CriticalInfrastructure.objects.get_or_create(
            organization=organization,
            code="CII-TEL-001",
            defaults={
                "owner_stakeholder": operator_stakeholder,
                "name": "National Telecom Backbone",
                "sector": "Telecommunications",
                "infrastructure_type": "cii",
                "owner_name": operator_stakeholder.name,
                "essential_service": "National internet backbone and core routing",
                "location": "Banjul",
                "designation_status": "designated",
                "criticality_level": "critical",
                "vulnerability_level": "high",
                "mapping_status": "mapped",
                "mission_assurance_status": "assessing",
                "critical_asset": True,
                "last_assessed_at": date(2026, 4, 1),
                "risk_summary": "Backbone concentration risk and third-party maintenance dependency identified.",
            },
        )
        primary_coordinate = coordinate_for(1)
        critical_infrastructure_updates = []
        if not critical_infrastructure.location or str(critical_infrastructure.location).startswith("Region "):
            critical_infrastructure.location = primary_coordinate["location"]
            critical_infrastructure_updates.append("location")
        if critical_infrastructure.latitude is None:
            critical_infrastructure.latitude = primary_coordinate["latitude"]
            critical_infrastructure_updates.append("latitude")
        if critical_infrastructure.longitude is None:
            critical_infrastructure.longitude = primary_coordinate["longitude"]
            critical_infrastructure_updates.append("longitude")
        if critical_infrastructure_updates:
            critical_infrastructure.save(update_fields=critical_infrastructure_updates)

        GovernanceArtifact.objects.get_or_create(
            organization=organization,
            title="National CII Protection Policy",
            artifact_type="policy",
            defaults={
                "phase": "governance",
                "status": "in_review",
                "version": "0.1",
                "owner_stakeholder": ministry_stakeholder,
                "summary": "Working baseline for policy statements, roles, obligations, and implementation framework.",
            },
        )
        GovernanceArtifact.objects.get_or_create(
            organization=organization,
            title="CII Mapping Tooling Pack",
            artifact_type="mapping_tool",
            defaults={
                "phase": "governance",
                "status": "draft",
                "owner_stakeholder": ministry_stakeholder,
                "related_infrastructure": critical_infrastructure,
                "summary": "Starter record for GIS mapping tools, mapping outputs, and designation evidence.",
            },
        )

        RiskRegisterEntry.objects.get_or_create(
            organization=organization,
            title="Core backbone outage during coordinated cyber incident",
            defaults={
                "infrastructure": critical_infrastructure,
                "category": "availability",
                "scenario": "Single national backbone outage affecting government and banking services.",
                "likelihood": 4,
                "impact": 5,
                "risk_score": 20,
                "risk_level": "critical",
                "treatment_status": "mitigating",
                "risk_owner": operator_stakeholder.name,
                "response_plan": "Implement diversified failover, update crisis escalation matrix, and run tabletop exercise.",
                "response_deadline": date(2026, 6, 15),
                "last_reviewed_at": date(2026, 4, 5),
            },
        )

        contingency_plan, _ = ContingencyPlan.objects.get_or_create(
            organization=organization,
            title="National Cyber Contingency Plan",
            defaults={
                "plan_type": "national",
                "scope": "Cross-sector cyber incidents impacting essential services",
                "status": "in_review",
                "communication_procedure": "Initial alert through CERT and national crisis coordination cell.",
                "coordination_mechanism": "Government-led coordination with sector focal points and CI owners.",
                "information_sharing_protocol": "Two-way threat and incident intelligence sharing across affected stakeholders.",
                "activation_trigger": "Critical or cross-sector cyber incident with national service disruption potential.",
                "review_cycle": "Quarterly review and post-exercise update",
                "next_review_date": date(2026, 7, 1),
            },
        )
        EmergencyResponseAsset.objects.get_or_create(
            organization=organization,
            contingency_plan=contingency_plan,
            name="National cyber incident coordination bridge",
            defaults={
                "infrastructure": critical_infrastructure,
                "asset_type": "platform",
                "priority": "critical",
                "owner_name": ministry_stakeholder.name,
                "availability_status": "ready",
                "location": "National CERT operations room",
                "activation_notes": "Used for coordinated incident triage and decision support.",
            },
        )
        SimulationExercise.objects.get_or_create(
            organization=organization,
            contingency_plan=contingency_plan,
            title="Telecom and banking ransomware tabletop",
            defaults={
                "exercise_type": "tabletop",
                "planned_date": date(2026, 8, 10),
                "status": "planned",
                "scenario": "Simulated ransomware spread across telecom and banking interdependencies.",
                "participating_sectors": "Telecommunications, banking, CERT, regulator",
            },
        )

        cyber_standard, _ = CyberStandard.objects.get_or_create(
            organization=organization,
            title="Minimum Security Standard for ISP and Banking Equipment",
            defaults={
                "standard_type": "isp_equipment",
                "target_sector": "ISPs and banking service providers",
                "status": "draft",
                "version": "0.1",
                "control_focus": "Firmware updates, strong authentication, encryption, privacy, backup, and DR readiness.",
                "review_cycle": "Annual",
                "owner_name": ministry_stakeholder.name,
            },
        )
        AuditFramework.objects.get_or_create(
            organization=organization,
            title="CNI Audit and Protection Framework",
            defaults={
                "related_standard": cyber_standard,
                "scope": "State-owned enterprises providing essential services",
                "status": "draft",
                "audit_frequency": "Semi-annual",
                "compliance_focus": "Protection controls, regular reviews, incident response, and recovery preparedness.",
            },
        )
        TrainingProgram.objects.get_or_create(
            organization=organization,
            title="Risk Assessment and Management Bootcamp",
            defaults={
                "program_type": "risk_management",
                "target_audience": "Government focal points and selected CII owners",
                "duration_days": 5,
                "delivery_mode": "in_person",
                "status": "planned",
                "certificate_required": True,
                "participant_target": 25,
                "summary": "Starter training record aligned to the ToR training deliverables.",
            },
        )
        DeliverableMilestone.objects.get_or_create(
            organization=organization,
            title="Initial design of national risk register",
            phase="risk",
            defaults={
                "deliverable_category": "risk_register",
                "status": "in_review",
                "planned_week": 1,
                "owner_name": ministry_stakeholder.name,
                "notes": "Foundational milestone for the centralized risk database and dashboard design.",
            },
        )

        # Extended Cyber GRC demo coverage for pagination testing.
        def pick(values, index):
            return values[(index - 1) % len(values)]

        workflow_statuses = ["draft", "planned", "in_progress", "active", "in_review", "submitted", "validated", "completed", "archived"]
        stakeholder_types = ["government", "regulator", "operator", "bank", "cii_owner", "cni_operator", "cert", "partner", "other"]
        sectors = [
            "Telecommunications",
            "Banking",
            "Energy",
            "Water",
            "Government",
            "Digital infrastructure",
            "Transport",
            "Health",
            "Emergency services",
        ]
        engagement_roles = [
            "Sector coordination",
            "Incident escalation",
            "Risk review participation",
            "Mapping focal point",
            "Operational continuity lead",
        ]
        risk_levels = ["low", "medium", "high", "critical"]
        treatment_statuses = ["identified", "assessing", "mitigating", "accepted", "closed"]
        artifact_types = ["policy", "regulation", "guideline", "framework", "mapping_tool", "report", "action_plan"]
        plan_types = ["national", "sectoral", "incident", "recovery", "communication"]
        emergency_asset_types = ["digital", "physical", "facility", "team", "platform", "other"]
        availability_statuses = ["planned", "ready", "constrained", "unavailable"]
        exercise_types = ["tabletop", "simulation", "live_drill"]
        standard_types = ["isp_equipment", "banking_equipment", "cni_protection", "privacy", "conformity"]
        program_types = ["risk_management", "contingency_response", "audit_awareness", "standards_compliance", "stakeholder_engagement"]
        delivery_modes = ["in_person", "virtual", "hybrid"]
        deliverable_categories = ["report", "workshop", "policy", "mapping", "risk_register", "contingency", "standard", "audit", "training"]
        phases = ["governance", "risk", "contingency", "standards", "audit"]
        extra_stakeholders = []
        for index in range(1, 121):
            stakeholder, _ = Stakeholder.objects.get_or_create(
                organization=organization,
                name=f"Cyber Stakeholder {index:03d}",
                defaults={
                    "stakeholder_type": pick(stakeholder_types, index),
                    "sector": pick(sectors, index),
                    "focal_point": f"Cyber Lead {index:03d}",
                    "email": f"stakeholder{index:03d}@demo.local",
                    "engagement_role": pick(engagement_roles, index),
                    "status": pick(workflow_statuses, index),
                },
            )
            extra_stakeholders.append(stakeholder)

        stakeholder_pool = [ministry_stakeholder, operator_stakeholder, *extra_stakeholders]

        infrastructure_pool = [critical_infrastructure]
        for index in range(2, 61):
            coordinate = coordinate_for(index)
            infrastructure, _ = CriticalInfrastructure.objects.get_or_create(
                organization=organization,
                code=f"CII-EXT-{index:03d}",
                defaults={
                    "owner_stakeholder": pick(stakeholder_pool, index),
                    "name": f"Critical Infrastructure Asset {index:03d}",
                    "sector": pick(sectors, index),
                    "infrastructure_type": "cii" if index % 3 else "cni",
                    "owner_name": pick(stakeholder_pool, index).name,
                    "essential_service": f"Essential digital service cluster {index:03d}",
                    "location": coordinate["location"],
                    "latitude": coordinate["latitude"],
                    "longitude": coordinate["longitude"],
                    "designation_status": ["identified", "designated", "validated", "monitored"][(index - 1) % 4],
                    "criticality_level": pick(risk_levels, index),
                    "vulnerability_level": pick(risk_levels[::-1], index),
                    "mapping_status": ["planned", "in_progress", "mapped", "reviewed"][(index - 1) % 4],
                    "mission_assurance_status": ["pending", "assessing", "mitigating", "completed"][(index - 1) % 4],
                    "requires_nda": index % 2 == 0,
                    "critical_asset": index % 5 == 0,
                    "last_assessed_at": date(2026, ((index - 1) % 12) + 1, ((index - 1) % 24) + 1),
                    "risk_summary": f"Extended infrastructure summary {index:03d} for mapping and assurance testing.",
                    "status": pick(workflow_statuses, index),
                },
            )
            infrastructure_updates = []
            if not infrastructure.location or str(infrastructure.location).startswith("Region "):
                infrastructure.location = coordinate["location"]
                infrastructure_updates.append("location")
            if infrastructure.latitude is None:
                infrastructure.latitude = coordinate["latitude"]
                infrastructure_updates.append("latitude")
            if infrastructure.longitude is None:
                infrastructure.longitude = coordinate["longitude"]
                infrastructure_updates.append("longitude")
            if infrastructure_updates:
                infrastructure.save(update_fields=infrastructure_updates)
            infrastructure_pool.append(infrastructure)

        for index in range(1, 81):
            GovernanceArtifact.objects.get_or_create(
                organization=organization,
                title=f"Governance Artifact {index:03d}",
                defaults={
                    "phase": pick(phases, index),
                    "artifact_type": pick(artifact_types, index),
                    "version": f"{1 + (index % 3)}.{index % 10}",
                    "status": pick(workflow_statuses, index),
                    "owner_stakeholder": pick(stakeholder_pool, index),
                    "related_infrastructure": pick(infrastructure_pool, index),
                    "summary": f"Extended governance artifact summary {index:03d} used for list pagination tests.",
                    "next_review_date": date(2026, ((index + 1) % 12) + 1, ((index - 1) % 24) + 1),
                },
            )

        for index in range(1, 141):
            likelihood = ((index - 1) % 5) + 1
            impact = ((index + 1) % 5) + 1
            RiskRegisterEntry.objects.get_or_create(
                organization=organization,
                title=f"National cyber risk scenario {index:03d}",
                defaults={
                    "infrastructure": pick(infrastructure_pool, index),
                    "category": pick(["availability", "integrity", "confidentiality", "supply_chain", "governance"], index),
                    "scenario": f"Extended risk scenario narrative {index:03d} for cross-sector cyber resilience planning.",
                    "likelihood": likelihood,
                    "impact": impact,
                    "risk_score": likelihood * impact,
                    "risk_level": risk_levels[min(3, ((likelihood * impact) - 1) // 6)],
                    "treatment_status": pick(treatment_statuses, index),
                    "risk_owner": pick(stakeholder_pool, index).name,
                    "response_plan": f"Mitigation plan {index:03d} covering controls, exercises, and review gates.",
                    "response_deadline": date(2026, ((index + 2) % 12) + 1, ((index - 1) % 24) + 1),
                    "last_reviewed_at": date(2026, ((index - 1) % 12) + 1, ((index - 1) % 24) + 1),
                    "update_notes": f"Extended update note {index:03d}.",
                },
            )

        contingency_plan_pool = [contingency_plan]
        for index in range(2, 31):
            plan, _ = ContingencyPlan.objects.get_or_create(
                organization=organization,
                title=f"Cyber Contingency Plan {index:03d}",
                defaults={
                    "plan_type": pick(plan_types, index),
                    "scope": f"Operational contingency scope {index:03d}",
                    "status": pick(workflow_statuses, index),
                    "communication_procedure": f"Communication procedure {index:03d}",
                    "coordination_mechanism": f"Coordination mechanism {index:03d}",
                    "information_sharing_protocol": f"Information sharing protocol {index:03d}",
                    "activation_trigger": f"Activation trigger {index:03d}",
                    "review_cycle": "Quarterly review",
                    "next_review_date": date(2026, ((index + 3) % 12) + 1, ((index - 1) % 24) + 1),
                    "notes": f"Extended contingency note {index:03d}",
                },
            )
            contingency_plan_pool.append(plan)

        for index in range(1, 61):
            EmergencyResponseAsset.objects.get_or_create(
                organization=organization,
                name=f"Emergency Response Asset {index:03d}",
                defaults={
                    "contingency_plan": pick(contingency_plan_pool, index),
                    "infrastructure": pick(infrastructure_pool, index),
                    "asset_type": pick(emergency_asset_types, index),
                    "priority": pick(risk_levels, index),
                    "owner_name": pick(stakeholder_pool, index).name,
                    "availability_status": pick(availability_statuses, index),
                    "location": f"Response node {index:03d}",
                    "activation_notes": f"Activation notes for emergency asset {index:03d}",
                },
            )

        for index in range(1, 41):
            SimulationExercise.objects.get_or_create(
                organization=organization,
                title=f"Simulation Exercise {index:03d}",
                defaults={
                    "contingency_plan": pick(contingency_plan_pool, index),
                    "exercise_type": pick(exercise_types, index),
                    "planned_date": date(2026, ((index + 4) % 12) + 1, ((index - 1) % 24) + 1),
                    "completed_date": None if index % 3 else date(2026, ((index + 4) % 12) + 1, ((index - 1) % 24) + 2),
                    "status": pick(workflow_statuses, index),
                    "scenario": f"Extended simulation scenario {index:03d}",
                    "participating_sectors": ", ".join({pick(sectors, index), pick(sectors, index + 1), pick(sectors, index + 2)}),
                    "findings": f"Key finding set {index:03d}",
                    "lessons_learned": f"Lesson learned note {index:03d}",
                },
            )

        standard_pool = [cyber_standard]
        for index in range(2, 31):
            standard, _ = CyberStandard.objects.get_or_create(
                organization=organization,
                title=f"Cyber Standard {index:03d}",
                defaults={
                    "standard_type": pick(standard_types, index),
                    "target_sector": pick(sectors, index),
                    "status": pick(workflow_statuses, index),
                    "version": f"{1 + (index % 4)}.{index % 10}",
                    "control_focus": f"Control focus narrative {index:03d}",
                    "review_cycle": "Annual",
                    "owner_name": pick(stakeholder_pool, index).name,
                    "summary": f"Extended standard summary {index:03d}",
                    "next_review_date": date(2026, ((index + 5) % 12) + 1, ((index - 1) % 24) + 1),
                },
            )
            standard_pool.append(standard)

        for index in range(1, 31):
            AuditFramework.objects.get_or_create(
                organization=organization,
                title=f"Audit Framework {index:03d}",
                defaults={
                    "related_standard": pick(standard_pool, index),
                    "scope": f"Audit scope {index:03d}",
                    "status": pick(workflow_statuses, index),
                    "audit_frequency": pick(["Monthly", "Quarterly", "Semi-annual", "Annual"], index),
                    "compliance_focus": f"Compliance focus {index:03d}",
                    "incident_response_procedure": f"Incident response procedure {index:03d}",
                    "recovery_procedure": f"Recovery procedure {index:03d}",
                    "next_review_date": date(2026, ((index + 6) % 12) + 1, ((index - 1) % 24) + 1),
                    "review_notes": f"Review notes {index:03d}",
                },
            )

        for index in range(1, 41):
            TrainingProgram.objects.get_or_create(
                organization=organization,
                title=f"Training Program {index:03d}",
                defaults={
                    "program_type": pick(program_types, index),
                    "target_audience": f"Target audience cluster {index:03d}",
                    "duration_days": 2 + (index % 5),
                    "delivery_mode": pick(delivery_modes, index),
                    "status": pick(workflow_statuses, index),
                    "certificate_required": index % 2 == 0,
                    "participant_target": 15 + index,
                    "summary": f"Extended training summary {index:03d}",
                },
            )

        for index in range(1, 41):
            DeliverableMilestone.objects.get_or_create(
                organization=organization,
                title=f"Deliverable Milestone {index:03d}",
                defaults={
                    "phase": pick(phases, index),
                    "deliverable_category": pick(deliverable_categories, index),
                    "status": pick(workflow_statuses, index),
                    "planned_week": index,
                    "due_date": date(2026, ((index + 7) % 12) + 1, ((index - 1) % 24) + 1),
                    "owner_name": pick(stakeholder_pool, index).name,
                    "notes": f"Extended milestone note {index:03d}",
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo data loaded."))
        self.stdout.write(self.style.SUCCESS("Login: admin@eden.local / Password123!"))
