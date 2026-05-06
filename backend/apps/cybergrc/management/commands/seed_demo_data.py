from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.cybergrc.models import (
    Acknowledgement,
    AssetInventoryItem,
    AssetInventoryType,
    AvailabilityStatus,
    BulletinType,
    ContingencyPlan,
    CriticalInfrastructure,
    CyberStandard,
    DesignationStatus,
    DistributionGroup,
    DistributionGroupType,
    EmergencyAssetType,
    EmergencyResponseAsset,
    GovernanceArtifact,
    Indicator,
    IndicatorStatus,
    IndicatorType,
    InformationShare,
    InfrastructureType,
    MappingStatus,
    Phase,
    PlanType,
    PriorityLevel,
    RiskRegisterEntry,
    RiskScenario,
    RiskTreatmentStatus,
    Sector,
    ShareChannel,
    ShareStatus,
    SimulationExercise,
    Stakeholder,
    StakeholderConsultation,
    StakeholderType,
    StandardControl,
    StandardRequirement,
    StandardType,
    ThreatBulletin,
    ThreatEvent,
    ThreatEventStatus,
    ThreatSourceType,
    ThreatType,
    VulnerabilityRecord,
    WorkflowStatus,
)
from apps.incident_management.models import (
    AssetAllocation,
    Incident,
    IncidentAssignment,
    IncidentCommunication,
    IncidentSeverity,
    IncidentSource,
    IncidentStatus,
    IncidentTask,
    IncidentTaskStatus,
    IncidentType,
    IncidentUpdate,
    SOPExecution,
    SOPExecutionStatus,
    SOPExecutionStep,
    SOPExecutionStepStatus,
    SOPStep,
    SOPStepType,
    SOPTemplate,
    SOPTemplateStatus,
)
from apps.org.models import (
    Facility,
    FacilityType,
    OfficeType,
    Organization,
    OrganizationType,
    Site,
)
from apps.people.models import Contact, Identity, Person


class Command(BaseCommand):
    help = "Seed additive National-3CPERS demo data without deleting existing rows."

    def add_arguments(self, parser):
        parser.add_argument(
            "--prefix",
            default="N3C-DEMO",
            help="Stable prefix used for generated codes and usernames.",
        )

    def handle(self, *args, **options):
        self.prefix = options["prefix"].strip() or "N3C-DEMO"
        self.now = timezone.now()
        self.today = timezone.localdate()
        self.created = 0
        self.updated = 0

        with transaction.atomic():
            organization = self.seed_organization()
            user = self.seed_user(organization)
            sectors = self.seed_sectors(organization)
            stakeholders = self.seed_stakeholders(organization, sectors)
            infrastructure = self.seed_infrastructure(
                organization, sectors, stakeholders
            )
            self.seed_sites_and_people(organization)
            plan = self.seed_contingency(organization)
            asset = self.seed_response_assets(
                organization, plan, infrastructure, stakeholders
            )
            self.seed_governance_and_standards(
                organization, sectors, infrastructure, stakeholders
            )
            risk = self.seed_risk_and_threats(
                organization, sectors, stakeholders, infrastructure
            )
            self.seed_incident_response(
                organization, user, stakeholders, infrastructure, plan, asset, risk
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. created={self.created}, updated={self.updated}"
            )
        )

    def upsert(self, model, lookup, defaults=None):
        obj, created = model.objects.update_or_create(**lookup, defaults=defaults or {})
        self.created += int(created)
        self.updated += int(not created)
        return obj

    def seed_organization(self):
        org_type = self.upsert(
            OrganizationType,
            {"code": f"{self.prefix}-GOV"},
            {
                "name": "Government cyber coordination authority",
                "description": "Demo organization type for national cyber coordination.",
                "status": "active",
            },
        )
        return self.upsert(
            Organization,
            {"code": f"{self.prefix}-ORG"},
            {
                "name": "National-3CPERS Coordination Unit",
                "organization_type": org_type,
                "description": "Demo tenant for the National Cyber Coordination and Communication Platform.",
                "email": "coordination@national-3cpers.example",
                "phone": "+220 000 1000",
                "is_active": True,
            },
        )

    def seed_user(self, organization):
        User = get_user_model()
        user = self.upsert(
            User,
            {"email": "demo.responder@national-3cpers.example"},
            {
                "username": f"{self.prefix.lower()}-responder",
                "full_name": "Demo National-3CPERS Responder",
                "phone": "+220 000 1100",
                "organization": organization,
                "is_active": True,
                "is_staff": True,
                "is_verified": True,
            },
        )
        if not user.has_usable_password():
            user.set_password("DemoPass123!")
            user.save(update_fields=["password"])
        return user

    def seed_sectors(self, organization):
        rows = [
            ("BANKING", "Banking and financial services"),
            ("TELECOM", "Telecommunications"),
            ("GOV", "Government digital services"),
            ("ENERGY", "Energy and utilities"),
        ]
        return {
            code: self.upsert(
                Sector,
                {"code": f"{self.prefix}-{code}"},
                {
                    "organization": organization,
                    "name": name,
                    "description": f"Demo sector for {name.lower()} coordination.",
                    "status": WorkflowStatus.ACTIVE,
                },
            )
            for code, name in rows
        }

    def seed_stakeholders(self, organization, sectors):
        rows = [
            (
                "MOCDE",
                "Ministry of Communications and Digital Economy",
                StakeholderType.GOVERNMENT,
                "GOV",
            ),
            ("CERT", "National CERT", StakeholderType.CERT, "GOV"),
            (
                "CBG",
                "Central Bank Cyber Resilience Desk",
                StakeholderType.REGULATOR,
                "BANKING",
            ),
            (
                "TELCO",
                "National Telecom Operator NOC",
                StakeholderType.OPERATOR,
                "TELECOM",
            ),
            (
                "ENERGY",
                "National Utility Security Office",
                StakeholderType.CNI_OPERATOR,
                "ENERGY",
            ),
        ]
        stakeholders = {}
        for code, name, stakeholder_type, sector_code in rows:
            sector = sectors[sector_code]
            stakeholders[code] = self.upsert(
                Stakeholder,
                {"organization": organization, "name": name},
                {
                    "stakeholder_type": stakeholder_type,
                    "sector_ref": sector,
                    "sector": sector.name,
                    "focal_point": f"{name} focal point",
                    "email": f"{code.lower()}@national-3cpers.example",
                    "phone": "+220 000 1200",
                    "engagement_role": "Cyber emergency coordination and information sharing",
                    "status": WorkflowStatus.ACTIVE,
                    "notes": "Generated demo stakeholder. Existing records are updated, not deleted.",
                },
            )
        return stakeholders

    def seed_infrastructure(self, organization, sectors, stakeholders):
        rows = [
            (
                "PAYMENT-SWITCH",
                "National payment switch",
                "BANKING",
                "CBG",
                PriorityLevel.CRITICAL,
                13.4521,
                -16.5780,
            ),
            (
                "IXP-GATEWAY",
                "National internet exchange gateway",
                "TELECOM",
                "TELCO",
                PriorityLevel.HIGH,
                13.4548,
                -16.5796,
            ),
            (
                "EGOV-PORTAL",
                "Government digital services portal",
                "GOV",
                "MOCDE",
                PriorityLevel.HIGH,
                13.4563,
                -16.5812,
            ),
        ]
        items = {}
        for code, name, sector_code, owner_code, criticality, lat, lon in rows:
            sector = sectors[sector_code]
            stakeholder = stakeholders[owner_code]
            items[code] = self.upsert(
                CriticalInfrastructure,
                {"code": f"{self.prefix}-{code}"},
                {
                    "organization": organization,
                    "owner_stakeholder": stakeholder,
                    "name": name,
                    "sector_ref": sector,
                    "sector": sector.name,
                    "infrastructure_type": InfrastructureType.CII,
                    "owner_name": stakeholder.name,
                    "essential_service": f"{name} continuity",
                    "location": "Greater Banjul Area",
                    "latitude": lat,
                    "longitude": lon,
                    "designation_status": DesignationStatus.DESIGNATED,
                    "criticality_level": criticality,
                    "vulnerability_level": PriorityLevel.MEDIUM,
                    "mapping_status": MappingStatus.MAPPED,
                    "critical_asset": True,
                    "last_assessed_at": self.today - timedelta(days=12),
                    "risk_summary": "Demo infrastructure requiring coordinated cyber resilience monitoring.",
                    "status": WorkflowStatus.ACTIVE,
                },
            )
        return items

    def seed_sites_and_people(self, organization):
        office_type = self.upsert(
            OfficeType,
            {"code": f"{self.prefix}-NOC"},
            {
                "organization": organization,
                "name": "National operations centre",
                "status": "active",
            },
        )
        facility_type = self.upsert(
            FacilityType,
            {"code": f"{self.prefix}-SOC"},
            {
                "organization": organization,
                "name": "Security operations centre",
                "status": "active",
            },
        )
        site = self.upsert(
            Site,
            {"code": f"{self.prefix}-HQ"},
            {
                "organization": organization,
                "office_type": office_type,
                "name": "National-3CPERS Coordination Centre",
                "site_type": "coordination_center",
                "city": "Banjul",
                "address": "Demo national coordination compound",
                "email": "hq@national-3cpers.example",
                "status": "active",
                "latitude": 13.4540,
                "longitude": -16.5790,
            },
        )
        self.upsert(
            Facility,
            {"code": f"{self.prefix}-SOC-FACILITY"},
            {
                "organization": organization,
                "site": site,
                "facility_type_ref": facility_type,
                "name": "National-3CPERS SOC Room",
                "facility_type": "soc",
                "status": "active",
                "city": "Banjul",
                "contact_person": "Demo SOC Lead",
                "phone": "+220 000 1300",
                "email": "soc@national-3cpers.example",
            },
        )
        person = self.upsert(
            Person,
            {"organization": organization, "first_name": "Awa", "last_name": "Jallow"},
            {
                "gender": "female",
                "date_of_birth": self.today.replace(year=self.today.year - 34),
            },
        )
        self.upsert(
            Contact,
            {
                "organization": organization,
                "person": person,
                "contact_type": "EMAIL",
                "value": "awa.jallow@national-3cpers.example",
            },
            {
                "label": "Work email",
                "priority": 1,
                "is_primary": True,
                "access_level": "official",
            },
        )
        self.upsert(
            Identity,
            {
                "organization": organization,
                "person": person,
                "document_type": "staff_id",
                "document_number": f"{self.prefix}-STAFF-001",
            },
            {
                "description": "Demo staff identity",
                "issued_country": "GM",
                "issued_place": "Banjul",
                "is_system_generated": True,
            },
        )

    def seed_contingency(self, organization):
        plan = self.upsert(
            ContingencyPlan,
            {
                "organization": organization,
                "title": "National cyber emergency coordination plan",
            },
            {
                "plan_type": PlanType.NATIONAL,
                "scope": "Banking, telecom, government services and utility cyber incidents",
                "status": WorkflowStatus.ACTIVE,
                "communication_procedure": "Activate platform room, notify sector focal points, publish verified updates.",
                "coordination_mechanism": "National-3CPERS coordinates incident command, resource allocation and stakeholder briefings.",
                "information_sharing_protocol": "Share TLP:AMBER indicators with verified responders and sector groups.",
                "activation_trigger": "Critical cyber incident affecting essential national services.",
                "review_cycle": "Quarterly",
                "next_review_date": self.today + timedelta(days=90),
            },
        )
        self.upsert(
            SimulationExercise,
            {
                "organization": organization,
                "title": "Payment switch ransomware tabletop",
            },
            {
                "contingency_plan": plan,
                "planned_date": self.today + timedelta(days=21),
                "status": WorkflowStatus.PLANNED,
                "scenario": "Coordinated ransomware exercise involving banking, telecom and CERT responders.",
                "participating_sectors": "Banking, Telecommunications, Government",
            },
        )
        return plan

    def seed_response_assets(self, organization, plan, infrastructure, stakeholders):
        return self.upsert(
            EmergencyResponseAsset,
            {
                "organization": organization,
                "name": "National incident bridge and evidence vault",
            },
            {
                "contingency_plan": plan,
                "infrastructure": infrastructure["PAYMENT-SWITCH"],
                "asset_type": EmergencyAssetType.PLATFORM,
                "priority": PriorityLevel.CRITICAL,
                "owner_stakeholder": stakeholders["CERT"],
                "owner_name": stakeholders["CERT"].name,
                "availability_status": AvailabilityStatus.READY,
                "mobilization_eta_minutes": 15,
                "capacity_units": 50,
                "last_readiness_check": self.today - timedelta(days=2),
                "location": "National-3CPERS SOC",
                "activation_notes": "Demo asset for secure bridge, evidence capture and responder coordination.",
            },
        )

    def seed_governance_and_standards(
        self, organization, sectors, infrastructure, stakeholders
    ):
        artifact = self.upsert(
            GovernanceArtifact,
            {
                "organization": organization,
                "title": "National CII cyber coordination framework",
            },
            {
                "owner_stakeholder": stakeholders["MOCDE"],
                "related_infrastructure": infrastructure["EGOV-PORTAL"],
                "phase": Phase.GOVERNANCE,
                "artifact_type": "framework",
                "version": "1.0-demo",
                "status": WorkflowStatus.IN_REVIEW,
                "summary": "Demo governance framework for CII/CNI mapping, risk review and incident coordination.",
                "next_review_date": self.today + timedelta(days=60),
            },
        )
        standard = self.upsert(
            CyberStandard,
            {
                "organization": organization,
                "title": "Minimum cyber resilience standard for payment services",
            },
            {
                "standard_type": StandardType.BANKING_EQUIPMENT,
                "target_sector_ref": sectors["BANKING"],
                "target_sector": sectors["BANKING"].name,
                "status": WorkflowStatus.ACTIVE,
                "version": "2026-demo",
                "control_focus": "Incident detection, MFA, backup restoration and secure communication.",
                "review_cycle": "Annual",
                "owner_name": stakeholders["CBG"].name,
                "summary": "Demo standard used for conformity assessment and audit planning.",
                "next_review_date": self.today + timedelta(days=180),
            },
        )
        requirement = self.upsert(
            StandardRequirement,
            {
                "organization": organization,
                "related_standard": standard,
                "code": "REQ-IR-001",
            },
            {
                "title": "Incident reporting within defined timelines",
                "chapter": "Incident response",
                "requirement_type": "operational",
                "status": WorkflowStatus.ACTIVE,
                "priority": PriorityLevel.HIGH,
                "implementation_guidance": "Report high-severity incidents to National-3CPERS within one hour.",
                "verification_method": "Review incident logs, notifications and acknowledgement timestamps.",
                "owner_name": stakeholders["CBG"].name,
                "sort_order": 1,
                "summary": "Demo reporting requirement for sector responders.",
            },
        )
        self.upsert(
            StandardControl,
            {
                "organization": organization,
                "related_standard": standard,
                "code": "CTRL-IR-001",
            },
            {
                "related_requirement": requirement,
                "title": "24/7 cyber incident notification channel",
                "domain": "Incident Response",
                "control_type": "detective",
                "status": WorkflowStatus.ACTIVE,
                "priority": PriorityLevel.HIGH,
                "control_objective": "Ensure incidents are visible to national coordination stakeholders quickly.",
                "control_procedure": "Maintain monitored mailbox, hotline and platform notification workflow.",
                "measurement_criteria": "Notification route tested every quarter.",
                "owner_name": stakeholders["CERT"].name,
                "sort_order": 1,
            },
        )
        return artifact, standard

    def seed_risk_and_threats(
        self, organization, sectors, stakeholders, infrastructure
    ):
        asset = self.upsert(
            AssetInventoryItem,
            {"organization": organization, "code": f"{self.prefix}-ASSET-PAY-API"},
            {
                "owner_stakeholder": stakeholders["CBG"],
                "related_infrastructure": infrastructure["PAYMENT-SWITCH"],
                "sector_ref": sectors["BANKING"],
                "name": "Payment switch API gateway",
                "asset_type": AssetInventoryType.APPLICATION,
                "sector": sectors["BANKING"].name,
                "owner_name": stakeholders["CBG"].name,
                "essential_function": "Interbank payment routing",
                "admin_area": "Greater Banjul",
                "location": "Primary data centre",
                "latitude": 13.4521,
                "longitude": -16.5780,
                "criticality_level": PriorityLevel.CRITICAL,
                "summary": "Demo asset for risk, threat and vulnerability workflows.",
                "status": WorkflowStatus.ACTIVE,
            },
        )
        risk = self.upsert(
            RiskRegisterEntry,
            {
                "organization": organization,
                "title": "Ransomware disruption of payment switching",
            },
            {
                "infrastructure": infrastructure["PAYMENT-SWITCH"],
                "category": "Cyber resilience",
                "scenario": "Ransomware limits payment switch availability and delays interbank settlement.",
                "likelihood": 3,
                "impact": 5,
                "risk_score": 15,
                "risk_level": PriorityLevel.HIGH,
                "treatment_status": RiskTreatmentStatus.MITIGATING,
                "risk_owner": stakeholders["CBG"].name,
                "response_plan": "Activate national coordination plan, isolate affected systems and validate clean backup restoration.",
                "response_deadline": self.today + timedelta(days=30),
                "last_reviewed_at": self.today - timedelta(days=5),
            },
        )
        threat = self.upsert(
            ThreatEvent,
            {
                "organization": organization,
                "title": "Phishing campaign targeting payment operations",
            },
            {
                "reporting_stakeholder": stakeholders["CERT"],
                "related_infrastructure": infrastructure["PAYMENT-SWITCH"],
                "asset_item": asset,
                "threat_type": ThreatType.PHISHING,
                "threat_source_type": ThreatSourceType.CERT,
                "status": ThreatEventStatus.ANALYZING,
                "severity": PriorityLevel.HIGH,
                "confidence_level": PriorityLevel.MEDIUM,
                "first_seen_at": self.now - timedelta(days=2),
                "last_seen_at": self.now - timedelta(hours=6),
                "admin_area": "Greater Banjul",
                "location": "Banking sector",
                "summary": "Demo threat event with malicious links sent to payment operations staff.",
                "recommended_action": "Block indicators, notify sector group and verify MFA coverage.",
            },
        )
        vuln = self.upsert(
            VulnerabilityRecord,
            {
                "organization": organization,
                "title": "Legacy VPN appliance pending patch",
            },
            {
                "related_infrastructure": infrastructure["PAYMENT-SWITCH"],
                "asset_item": asset,
                "related_threat_event": threat,
                "vulnerability_type": "Remote access exposure",
                "severity": PriorityLevel.HIGH,
                "status": "remediating",
                "exploitability_level": PriorityLevel.HIGH,
                "discovered_on": self.today - timedelta(days=10),
                "remediation_due_date": self.today + timedelta(days=7),
                "owner_name": stakeholders["CBG"].name,
                "summary": "Demo vulnerability record for pending VPN hardening.",
                "remediation_guidance": "Apply vendor patch, rotate credentials and restrict administrative source ranges.",
            },
        )
        self.upsert(
            RiskScenario,
            {
                "organization": organization,
                "title": "Credential theft leading to payment API misuse",
            },
            {
                "risk_register_entry": risk,
                "related_infrastructure": infrastructure["PAYMENT-SWITCH"],
                "asset_item": asset,
                "related_threat_event": threat,
                "vulnerability_record": vuln,
                "status": WorkflowStatus.IN_PROGRESS,
                "risk_level": PriorityLevel.HIGH,
                "treatment_status": RiskTreatmentStatus.MITIGATING,
                "scenario_owner": stakeholders["CBG"].name,
                "likelihood": 3,
                "impact": 4,
                "risk_score": 12,
                "scenario_summary": "Demo risk scenario linking phishing, vulnerable remote access and payment service disruption.",
                "business_impact": "Potential delayed settlements and public confidence impact.",
                "response_plan": "Contain account compromise, enforce MFA reset and activate sector communications.",
                "review_due_date": self.today + timedelta(days=14),
            },
        )
        bulletin = self.upsert(
            ThreatBulletin,
            {"organization": organization, "title": "Banking sector phishing advisory"},
            {
                "related_threat_event": threat,
                "related_infrastructure": infrastructure["PAYMENT-SWITCH"],
                "target_sector_ref": sectors["BANKING"],
                "bulletin_type": BulletinType.ADVISORY,
                "severity": PriorityLevel.HIGH,
                "status": WorkflowStatus.ACTIVE,
                "issued_on": self.today,
                "valid_until": self.today + timedelta(days=14),
                "target_sector": sectors["BANKING"].name,
                "summary": "Demo bulletin warning of payment operations phishing attempts.",
                "recommended_actions": "Block indicators, brief payment staff, review suspicious logins.",
            },
        )
        self.upsert(
            Indicator,
            {"organization": organization, "value": "payments-support-demo.example"},
            {
                "related_bulletin": bulletin,
                "related_threat_event": threat,
                "title": "Demo phishing domain",
                "indicator_type": IndicatorType.DOMAIN,
                "status": IndicatorStatus.ACTIVE,
                "confidence_level": PriorityLevel.MEDIUM,
                "first_seen_at": self.now - timedelta(days=2),
                "last_seen_at": self.now - timedelta(hours=6),
                "notes": "Non-real demo indicator.",
            },
        )
        group = self.upsert(
            DistributionGroup,
            {"organization": organization, "title": "Banking sector cyber alert group"},
            {
                "group_type": DistributionGroupType.SECTOR,
                "target_sector_ref": sectors["BANKING"],
                "target_sector": sectors["BANKING"].name,
                "status": WorkflowStatus.ACTIVE,
                "distribution_notes": "Demo sector group for banking threat bulletins.",
            },
        )
        group.stakeholders.add(
            stakeholders["CBG"], stakeholders["CERT"], stakeholders["MOCDE"]
        )
        share = self.upsert(
            InformationShare,
            {"organization": organization, "title": "Share banking phishing advisory"},
            {
                "related_bulletin": bulletin,
                "related_threat_event": threat,
                "distribution_group": group,
                "target_stakeholder": stakeholders["CBG"],
                "share_channel": ShareChannel.PLATFORM,
                "status": ShareStatus.SHARED,
                "shared_at": self.now,
                "acknowledgement_due_date": self.today + timedelta(days=2),
                "action_requested": "Acknowledge receipt and confirm indicator blocking.",
                "message_summary": "Demo information share for banking phishing advisory.",
            },
        )
        self.upsert(
            Acknowledgement,
            {
                "organization": organization,
                "information_share": share,
                "stakeholder": stakeholders["CBG"],
            },
            {
                "status": "received",
                "responded_at": self.now,
                "action_note": "Demo acknowledgement received.",
            },
        )
        return risk

    def seed_incident_response(
        self, organization, user, stakeholders, infrastructure, plan, asset, risk
    ):
        incident = self.upsert(
            Incident,
            {
                "organization": organization,
                "title": "Demo payment switch service degradation",
            },
            {
                "incident_type": IncidentType.SERVICE_OUTAGE,
                "severity": IncidentSeverity.HIGH,
                "status": IncidentStatus.ACTIVE,
                "source": IncidentSource.MONITORING,
                "detected_at": self.now - timedelta(hours=4),
                "reported_at": self.now - timedelta(hours=3, minutes=40),
                "summary": "Demo incident showing service degradation in national payment switching.",
                "operational_objective": "Restore stable payment routing and maintain coordinated public messaging.",
                "cross_sector_impact": "Banking customers may experience delayed transfers; telecom links remain stable.",
                "decision_log": "National-3CPERS bridge opened; banking and CERT focal points engaged.",
                "next_update_due": self.now + timedelta(hours=1),
                "containment_target_at": self.now + timedelta(hours=2),
                "recovery_target_at": self.now + timedelta(hours=8),
                "national_significance": True,
                "incident_coordinator": user,
                "lead_stakeholder": stakeholders["CERT"],
                "linked_plan": plan,
            },
        )
        incident.affected_infrastructure.add(infrastructure["PAYMENT-SWITCH"])
        self.upsert(
            IncidentUpdate,
            {
                "organization": organization,
                "incident": incident,
                "title": "Initial national coordination update",
            },
            {
                "message": "Demo update: responders are validating service health and checking for malicious activity.",
                "status_snapshot": IncidentStatus.ACTIVE,
                "severity_snapshot": IncidentSeverity.HIGH,
                "recorded_at": self.now - timedelta(hours=3),
                "next_step": "Publish verified status update to banking sector group.",
            },
        )
        task = self.upsert(
            IncidentTask,
            {
                "organization": organization,
                "incident": incident,
                "title": "Validate payment switch transaction backlog",
            },
            {
                "description": "Demo task to review queues, failed transactions and recovery priorities.",
                "status": IncidentTaskStatus.IN_PROGRESS,
                "priority": IncidentSeverity.HIGH,
                "assigned_to": user,
                "due_at": self.now + timedelta(hours=2),
                "next_step": "Share backlog summary with incident bridge.",
            },
        )
        self.upsert(
            IncidentAssignment,
            {
                "organization": organization,
                "incident": incident,
                "role_in_response": "Incident commander",
            },
            {
                "assignee": user,
                "stakeholder": stakeholders["CERT"],
                "status": "active",
                "assigned_at": self.now - timedelta(hours=3),
                "acknowledged_at": self.now - timedelta(hours=2, minutes=50),
                "notes": "Demo assignment for incident command.",
            },
        )
        self.upsert(
            IncidentCommunication,
            {
                "organization": organization,
                "incident": incident,
                "subject": "Banking sector situation brief",
            },
            {
                "direction": "outbound",
                "channel": "briefing",
                "audience": stakeholders["CBG"].name,
                "sent_at": self.now - timedelta(hours=2),
                "message": "Demo brief: payment services degraded; responders coordinating restoration.",
                "external_reference": f"{self.prefix}-COMMS-001",
                "requires_acknowledgement": True,
            },
        )
        template = self.upsert(
            SOPTemplate,
            {"organization": organization, "code": f"{self.prefix}-SOP-RANSOMWARE"},
            {
                "contingency_plan": plan,
                "related_infrastructure": infrastructure["PAYMENT-SWITCH"],
                "owner_stakeholder": stakeholders["CERT"],
                "title": "Ransomware triage and coordination SOP",
                "version": "1.0-demo",
                "status": SOPTemplateStatus.READY,
                "objective": "Coordinate containment, evidence capture and stakeholder communications.",
                "activation_trigger": "Suspected ransomware affecting essential payment or government services.",
                "last_reviewed_at": self.today - timedelta(days=15),
            },
        )
        steps = [
            (
                1,
                "Open coordination bridge",
                SOPStepType.COMMUNICATION,
                "Create incident bridge and invite verified responders.",
            ),
            (
                2,
                "Freeze evidence",
                SOPStepType.EVIDENCE,
                "Capture logs, hashes and timeline before restoration actions.",
            ),
            (
                3,
                "Confirm containment",
                SOPStepType.TECHNICAL,
                "Validate network isolation and endpoint containment.",
            ),
        ]
        for order, title, step_type, instruction in steps:
            self.upsert(
                SOPStep,
                {
                    "organization": organization,
                    "template": template,
                    "step_order": order,
                },
                {
                    "title": title,
                    "instruction": instruction,
                    "step_type": step_type,
                    "responsible_role": "Incident response lead",
                    "default_assignee": user,
                    "estimated_duration_minutes": 30,
                    "evidence_hint": "Attach screenshots or log extracts where applicable.",
                },
            )
        execution = self.upsert(
            SOPExecution,
            {
                "organization": organization,
                "incident": incident,
                "template": template,
                "title": "Execute ransomware triage SOP",
            },
            {
                "status": SOPExecutionStatus.ACTIVE,
                "execution_commander": user,
                "started_at": self.now - timedelta(hours=2, minutes=30),
                "target_completion_at": self.now + timedelta(hours=4),
                "summary": "Demo SOP execution linked to the payment switch incident.",
                "next_action": "Complete containment confirmation.",
            },
        )
        for order, title, step_type, instruction in steps:
            self.upsert(
                SOPExecutionStep,
                {
                    "organization": organization,
                    "execution": execution,
                    "step_order": order,
                },
                {
                    "template_step": SOPStep.objects.get(
                        template=template, step_order=order
                    ),
                    "title": title,
                    "instruction": instruction,
                    "step_type": step_type,
                    "status": (
                        SOPExecutionStepStatus.COMPLETED
                        if order < 3
                        else SOPExecutionStepStatus.IN_PROGRESS
                    ),
                    "assigned_to": user,
                    "started_at": self.now - timedelta(hours=2),
                    "completed_at": (
                        self.now - timedelta(hours=1) if order < 3 else None
                    ),
                    "notes": "Demo SOP execution step.",
                },
            )
        self.upsert(
            AssetAllocation,
            {
                "organization": organization,
                "incident": incident,
                "emergency_asset": asset,
            },
            {
                "destination_infrastructure": infrastructure["PAYMENT-SWITCH"],
                "related_task": task,
                "title": "Deploy national incident bridge and evidence vault",
                "status": "deployed",
                "priority": IncidentSeverity.HIGH,
                "requested_by": user,
                "approved_by": user,
                "requested_at": self.now - timedelta(hours=3),
                "approved_at": self.now - timedelta(hours=2, minutes=45),
                "mobilized_at": self.now - timedelta(hours=2, minutes=30),
                "deployed_at": self.now - timedelta(hours=2),
                "quantity_requested": 1,
                "quantity_allocated": 1,
                "destination": "National-3CPERS SOC",
                "deployment_notes": f"Support mitigation for risk: {risk.title}",
            },
        )
        self.upsert(
            StakeholderConsultation,
            {
                "organization": organization,
                "title": "Post-incident banking coordination review",
            },
            {
                "stakeholder": stakeholders["CBG"],
                "related_infrastructure": infrastructure["PAYMENT-SWITCH"],
                "consultation_type": "validation",
                "engagement_channel": "hybrid",
                "meeting_location": "National-3CPERS SOC",
                "start_datetime": self.now + timedelta(days=3),
                "end_datetime": self.now + timedelta(days=3, hours=2),
                "objective": "Review incident decisions, communications and residual controls.",
                "agenda": "Timeline review; sector impact; control gaps; corrective actions.",
                "status": "scheduled",
                "focal_person": "Demo National-3CPERS Responder",
            },
        )
