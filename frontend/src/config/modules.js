const WORKFLOW_STATUS_CHOICES = [
  { value: "draft", display_name: "Draft" },
  { value: "planned", display_name: "Planned" },
  { value: "in_progress", display_name: "In progress" },
  { value: "active", display_name: "Active" },
  { value: "in_review", display_name: "In review" },
  { value: "submitted", display_name: "Submitted" },
  { value: "validated", display_name: "Validated" },
  { value: "completed", display_name: "Completed" },
  { value: "archived", display_name: "Archived" },
];

const PHASE_CHOICES = [
  { value: "governance", display_name: "Governance framework" },
  { value: "risk", display_name: "Risk register" },
  { value: "contingency", display_name: "Cyber contingency" },
  { value: "standards", display_name: "Minimum standards" },
  { value: "audit", display_name: "Audit and protection" },
];

const PRIORITY_CHOICES = [
  { value: "low", display_name: "Low" },
  { value: "medium", display_name: "Medium" },
  { value: "high", display_name: "High" },
  { value: "critical", display_name: "Critical" },
];

const ENGAGEMENT_CHANNEL_CHOICES = [
  { value: "in_person", display_name: "In person" },
  { value: "phone", display_name: "Phone" },
  { value: "video", display_name: "Video" },
  { value: "hybrid", display_name: "Hybrid" },
];

const CONSULTATION_STATUS_CHOICES = [
  { value: "draft", display_name: "Draft" },
  { value: "scheduled", display_name: "Scheduled" },
  { value: "confirmed", display_name: "Confirmed" },
  { value: "rescheduled", display_name: "Rescheduled" },
  { value: "completed", display_name: "Completed" },
  { value: "missed", display_name: "Missed" },
  { value: "archived", display_name: "Archived" },
];

const INCIDENT_SEVERITY_CHOICES = [
  { value: "low", display_name: "Low" },
  { value: "medium", display_name: "Medium" },
  { value: "high", display_name: "High" },
  { value: "critical", display_name: "Critical" },
  { value: "national", display_name: "National significance" },
];

const INCIDENT_STATUS_CHOICES = [
  { value: "reported", display_name: "Reported" },
  { value: "assessing", display_name: "Assessing" },
  { value: "active", display_name: "Active" },
  { value: "contained", display_name: "Contained" },
  { value: "recovering", display_name: "Recovering" },
  { value: "closed", display_name: "Closed" },
];

const INCIDENT_TYPE_CHOICES = [
  { value: "service_outage", display_name: "Service outage" },
  { value: "malware", display_name: "Malware" },
  { value: "data_breach", display_name: "Data breach" },
  { value: "phishing", display_name: "Phishing" },
  { value: "ddos", display_name: "DDoS" },
  { value: "unauthorized_access", display_name: "Unauthorized access" },
  { value: "fraud", display_name: "Fraud" },
  { value: "physical_intrusion", display_name: "Physical intrusion" },
  { value: "supply_chain", display_name: "Supply chain" },
  { value: "other", display_name: "Other" },
];

const INCIDENT_SOURCE_CHOICES = [
  { value: "internal_report", display_name: "Internal report" },
  { value: "external_report", display_name: "External report" },
  { value: "monitoring", display_name: "Monitoring alert" },
  { value: "threat_intelligence", display_name: "Threat intelligence" },
  { value: "exercise", display_name: "Exercise" },
  { value: "consultation", display_name: "Consultation" },
  { value: "other", display_name: "Other" },
];

const INCIDENT_UPDATE_TYPE_CHOICES = [
  { value: "situation", display_name: "Situation update" },
  { value: "decision", display_name: "Decision" },
  { value: "escalation", display_name: "Escalation" },
  { value: "containment", display_name: "Containment" },
  { value: "recovery", display_name: "Recovery" },
  { value: "lesson", display_name: "Lesson learned" },
];

const INCIDENT_TASK_STATUS_CHOICES = [
  { value: "planned", display_name: "Planned" },
  { value: "in_progress", display_name: "In progress" },
  { value: "blocked", display_name: "Blocked" },
  { value: "completed", display_name: "Completed" },
  { value: "cancelled", display_name: "Cancelled" },
];

const INCIDENT_ASSIGNMENT_STATUS_CHOICES = [
  { value: "assigned", display_name: "Assigned" },
  { value: "acknowledged", display_name: "Acknowledged" },
  { value: "active", display_name: "Active" },
  { value: "released", display_name: "Released" },
];

const INCIDENT_COMMUNICATION_DIRECTION_CHOICES = [
  { value: "outbound", display_name: "Outbound" },
  { value: "inbound", display_name: "Inbound" },
];

const INCIDENT_COMMUNICATION_CHANNEL_CHOICES = [
  { value: "email", display_name: "Email" },
  { value: "phone", display_name: "Phone" },
  { value: "video", display_name: "Video" },
  { value: "sms", display_name: "SMS" },
  { value: "briefing", display_name: "Briefing" },
  { value: "bulletin", display_name: "Bulletin" },
  { value: "other", display_name: "Other" },
];

const INCIDENT_ATTACHMENT_TYPE_CHOICES = [
  { value: "log", display_name: "Log" },
  { value: "report", display_name: "Report" },
  { value: "screenshot", display_name: "Screenshot" },
  { value: "evidence", display_name: "Evidence" },
  { value: "bulletin", display_name: "Bulletin" },
  { value: "other", display_name: "Other" },
];

const SOP_TEMPLATE_STATUS_CHOICES = [
  { value: "draft", display_name: "Draft" },
  { value: "ready", display_name: "Ready" },
  { value: "active", display_name: "Active" },
  { value: "archived", display_name: "Archived" },
];

const SOP_STEP_TYPE_CHOICES = [
  { value: "check", display_name: "Checklist" },
  { value: "decision", display_name: "Decision" },
  { value: "communication", display_name: "Communication" },
  { value: "escalation", display_name: "Escalation" },
  { value: "technical", display_name: "Technical" },
  { value: "evidence", display_name: "Evidence capture" },
];

const SOP_EXECUTION_STATUS_CHOICES = [
  { value: "planned", display_name: "Planned" },
  { value: "active", display_name: "Active" },
  { value: "blocked", display_name: "Blocked" },
  { value: "completed", display_name: "Completed" },
  { value: "cancelled", display_name: "Cancelled" },
];

const ALLOCATION_STATUS_CHOICES = [
  { value: "requested", display_name: "Requested" },
  { value: "approved", display_name: "Approved" },
  { value: "mobilizing", display_name: "Mobilizing" },
  { value: "deployed", display_name: "Deployed" },
  { value: "demobilizing", display_name: "Demobilizing" },
  { value: "released", display_name: "Released" },
  { value: "cancelled", display_name: "Cancelled" },
];

const DEPLOYMENT_STATUS_CHOICES = [
  { value: "idle", display_name: "Idle" },
  { value: "staged", display_name: "Staged" },
  { value: "deployed", display_name: "Deployed" },
  { value: "returning", display_name: "Returning" },
  { value: "maintenance", display_name: "Maintenance" },
];

const REQUIREMENT_TYPE_CHOICES = [
  { value: "governance", display_name: "Governance" },
  { value: "technical", display_name: "Technical" },
  { value: "operational", display_name: "Operational" },
  { value: "legal", display_name: "Legal" },
  { value: "reporting", display_name: "Reporting" },
];

const CONTROL_TYPE_CHOICES = [
  { value: "preventive", display_name: "Preventive" },
  { value: "detective", display_name: "Detective" },
  { value: "corrective", display_name: "Corrective" },
  { value: "directive", display_name: "Directive" },
];

const CONFORMITY_LEVEL_CHOICES = [
  { value: "conformant", display_name: "Conformant" },
  { value: "partial", display_name: "Partially conformant" },
  { value: "non_conformant", display_name: "Non-conformant" },
  { value: "not_applicable", display_name: "Not applicable" },
];

const EVIDENCE_STATUS_CHOICES = [
  { value: "pending", display_name: "Pending" },
  { value: "available", display_name: "Available" },
  { value: "reviewed", display_name: "Reviewed" },
  { value: "expired", display_name: "Expired" },
  { value: "rejected", display_name: "Rejected" },
];

const EVIDENCE_TYPE_CHOICES = [
  { value: "document", display_name: "Document" },
  { value: "screenshot", display_name: "Screenshot" },
  { value: "test_result", display_name: "Test result" },
  { value: "configuration", display_name: "Configuration" },
  { value: "interview", display_name: "Interview" },
  { value: "log", display_name: "Log" },
  { value: "report", display_name: "Report" },
  { value: "other", display_name: "Other" },
];

const CHECKLIST_STATUS_CHOICES = [
  { value: "planned", display_name: "Planned" },
  { value: "in_progress", display_name: "In progress" },
  { value: "blocked", display_name: "Blocked" },
  { value: "completed", display_name: "Completed" },
  { value: "skipped", display_name: "Skipped" },
];

const FINDING_STATUS_CHOICES = [
  { value: "identified", display_name: "Identified" },
  { value: "in_review", display_name: "In review" },
  { value: "validated", display_name: "Validated" },
  { value: "remediating", display_name: "Remediating" },
  { value: "resolved", display_name: "Resolved" },
  { value: "closed", display_name: "Closed" },
];

const NON_CONFORMITY_STATUS_CHOICES = [
  { value: "open", display_name: "Open" },
  { value: "in_review", display_name: "In review" },
  { value: "accepted", display_name: "Accepted" },
  { value: "remediating", display_name: "Remediating" },
  { value: "resolved", display_name: "Resolved" },
  { value: "closed", display_name: "Closed" },
];

const ASSET_INVENTORY_TYPE_CHOICES = [
  { value: "service", display_name: "Service" },
  { value: "application", display_name: "Application" },
  { value: "platform", display_name: "Platform" },
  { value: "network", display_name: "Network" },
  { value: "facility", display_name: "Facility" },
  { value: "data", display_name: "Data asset" },
  { value: "team", display_name: "Team" },
  { value: "process", display_name: "Process" },
  { value: "other", display_name: "Other" },
];

const THREAT_TYPE_CHOICES = [
  { value: "malware", display_name: "Malware" },
  { value: "phishing", display_name: "Phishing" },
  { value: "ddos", display_name: "DDoS" },
  { value: "ransomware", display_name: "Ransomware" },
  { value: "insider", display_name: "Insider threat" },
  { value: "supply_chain", display_name: "Supply chain" },
  { value: "fraud", display_name: "Fraud" },
  { value: "physical", display_name: "Physical threat" },
  { value: "other", display_name: "Other" },
];

const THREAT_SOURCE_TYPE_CHOICES = [
  { value: "monitoring", display_name: "Monitoring" },
  { value: "internal_report", display_name: "Internal report" },
  { value: "partner", display_name: "Partner notification" },
  { value: "vendor", display_name: "Vendor notification" },
  { value: "cert", display_name: "CERT / CSIRT" },
  { value: "public_source", display_name: "Public source" },
  { value: "exercise", display_name: "Exercise" },
  { value: "other", display_name: "Other" },
];

const THREAT_EVENT_STATUS_CHOICES = [
  { value: "identified", display_name: "Identified" },
  { value: "analyzing", display_name: "Analyzing" },
  { value: "monitored", display_name: "Monitored" },
  { value: "mitigated", display_name: "Mitigated" },
  { value: "closed", display_name: "Closed" },
];

const VULNERABILITY_STATUS_CHOICES = [
  { value: "identified", display_name: "Identified" },
  { value: "validating", display_name: "Validating" },
  { value: "remediating", display_name: "Remediating" },
  { value: "accepted", display_name: "Accepted" },
  { value: "resolved", display_name: "Resolved" },
  { value: "closed", display_name: "Closed" },
];

const BULLETIN_TYPE_CHOICES = [
  { value: "advisory", display_name: "Advisory" },
  { value: "alert", display_name: "Alert" },
  { value: "incident", display_name: "Incident bulletin" },
  { value: "coordination", display_name: "Coordination note" },
  { value: "watchlist", display_name: "Watchlist" },
];

const INDICATOR_TYPE_CHOICES = [
  { value: "ip", display_name: "IP address" },
  { value: "domain", display_name: "Domain" },
  { value: "url", display_name: "URL" },
  { value: "email", display_name: "Email address" },
  { value: "hash", display_name: "Hash" },
  { value: "yara", display_name: "YARA rule" },
  { value: "file_name", display_name: "File name" },
  { value: "other", display_name: "Other" },
];

const INDICATOR_STATUS_CHOICES = [
  { value: "new", display_name: "New" },
  { value: "active", display_name: "Active" },
  { value: "monitoring", display_name: "Monitoring" },
  { value: "expired", display_name: "Expired" },
  { value: "revoked", display_name: "Revoked" },
];

const DISTRIBUTION_GROUP_TYPE_CHOICES = [
  { value: "sector", display_name: "Sector" },
  { value: "institution", display_name: "Institution" },
  { value: "incident", display_name: "Incident" },
  { value: "national", display_name: "National" },
  { value: "partner", display_name: "Partner" },
];

const SHARE_CHANNEL_CHOICES = [
  { value: "platform", display_name: "Platform notification" },
  { value: "email", display_name: "Email" },
  { value: "briefing", display_name: "Briefing" },
  { value: "phone", display_name: "Phone" },
  { value: "sms", display_name: "SMS" },
  { value: "document", display_name: "Document" },
  { value: "meeting", display_name: "Meeting" },
];

const SHARE_STATUS_CHOICES = [
  { value: "draft", display_name: "Draft" },
  { value: "prepared", display_name: "Prepared" },
  { value: "shared", display_name: "Shared" },
  { value: "acknowledged", display_name: "Acknowledged" },
  { value: "closed", display_name: "Closed" },
];

const ACKNOWLEDGEMENT_STATUS_CHOICES = [
  { value: "pending", display_name: "Pending" },
  { value: "received", display_name: "Received" },
  { value: "actioned", display_name: "Actioned" },
  { value: "declined", display_name: "Declined" },
];

const DOCUMENT_TYPE_CHOICES = [
  { value: "report", display_name: "Operational report" },
  { value: "brief", display_name: "Briefing note" },
  { value: "minutes", display_name: "Meeting minutes" },
  { value: "plan", display_name: "Plan package" },
  { value: "standard_pack", display_name: "Standards pack" },
  { value: "dossier", display_name: "Final dossier" },
  { value: "template", display_name: "Template" },
];

const DOCUMENT_FORMAT_CHOICES = [
  { value: "markdown", display_name: "Markdown" },
  { value: "text", display_name: "Plain text" },
  { value: "json", display_name: "JSON snapshot" },
  { value: "pdf", display_name: "PDF" },
  { value: "docx", display_name: "DOCX" },
];

const DOCUMENT_STATUS_CHOICES = [
  { value: "generated", display_name: "Generated" },
  { value: "in_review", display_name: "In review" },
  { value: "approved", display_name: "Approved" },
  { value: "superseded", display_name: "Superseded" },
  { value: "archived", display_name: "Archived" },
];

const REVIEW_CYCLE_STATUS_CHOICES = [
  { value: "draft", display_name: "Draft" },
  { value: "active", display_name: "Active" },
  { value: "overdue", display_name: "Overdue" },
  { value: "completed", display_name: "Completed" },
  { value: "archived", display_name: "Archived" },
];

const REVIEW_DECISION_CHOICES = [
  { value: "approved", display_name: "Approved" },
  { value: "changes_requested", display_name: "Changes requested" },
  { value: "superseded", display_name: "Superseded" },
  { value: "rejected", display_name: "Rejected" },
];

const CHANGE_TYPE_CHOICES = [
  { value: "generated", display_name: "Generated" },
  { value: "review_started", display_name: "Review started" },
  { value: "review_recorded", display_name: "Review recorded" },
  { value: "approved", display_name: "Approved" },
  { value: "updated", display_name: "Updated" },
  { value: "superseded", display_name: "Superseded" },
  { value: "reminder", display_name: "Reminder" },
  { value: "archived", display_name: "Archived" },
];

const RISK_REVIEW_DECISION_CHOICES = [
  { value: "accept", display_name: "Accept" },
  { value: "mitigate", display_name: "Mitigate" },
  { value: "escalate", display_name: "Escalate" },
  { value: "monitor", display_name: "Monitor" },
  { value: "close", display_name: "Close" },
];

const cybergrcFieldDefinitions = {
  cybergrc_stakeholders: [
    { name: "name", required: true },
    {
      name: "stakeholder_type",
      type: "choice",
      choices: [
        { value: "government", display_name: "Government" },
        { value: "regulator", display_name: "Regulator" },
        { value: "operator", display_name: "Operator" },
        { value: "bank", display_name: "Bank" },
        { value: "cii_owner", display_name: "CII owner" },
        { value: "cni_operator", display_name: "CNI operator" },
        { value: "cert", display_name: "CERT / CSIRT" },
        { value: "partner", display_name: "Partner" },
        { value: "other", display_name: "Other" },
      ],
    },
    {
      name: "sector_ref",
      label: "Sector",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/sectors/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "email", type: "email" },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "notes", type: "textarea" },
  ],
  critical_infrastructure: [
    {
      name: "owner_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "code", required: true },
    { name: "name", required: true },
    {
      name: "sector_ref",
      label: "Sector",
      type: "relation",
      required: true,
      relation: {
        endpoint: "/cybergrc/sectors/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "infrastructure_type",
      type: "choice",
      choices: [
        { value: "cii", display_name: "Critical information infrastructure" },
        { value: "cni", display_name: "Critical national infrastructure" },
      ],
    },
    {
      name: "designation_status",
      type: "choice",
      choices: [
        { value: "identified", display_name: "Identified" },
        { value: "designated", display_name: "Designated" },
        { value: "validated", display_name: "Validated" },
        { value: "monitored", display_name: "Monitored" },
      ],
    },
    { name: "criticality_level", type: "choice", choices: PRIORITY_CHOICES },
    { name: "vulnerability_level", type: "choice", choices: PRIORITY_CHOICES },
    {
      name: "mapping_status",
      type: "choice",
      choices: [
        { value: "planned", display_name: "Planned" },
        { value: "in_progress", display_name: "In progress" },
        { value: "mapped", display_name: "Mapped" },
        { value: "reviewed", display_name: "Reviewed" },
      ],
    },
    {
      name: "mission_assurance_status",
      type: "choice",
      choices: [
        { value: "pending", display_name: "Pending" },
        { value: "assessing", display_name: "Assessing" },
        { value: "mitigating", display_name: "Mitigating" },
        { value: "completed", display_name: "Completed" },
      ],
    },
    { name: "requires_nda", type: "boolean" },
    { name: "critical_asset", type: "boolean" },
    { name: "last_assessed_at", type: "date" },
    { name: "risk_summary", type: "textarea" },
    { name: "notes", type: "textarea" },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
  ],
  governance_artifacts: [
    { name: "title", required: true },
    {
      name: "owner_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "phase", type: "choice", choices: PHASE_CHOICES },
    {
      name: "artifact_type",
      type: "choice",
      choices: [
        { value: "policy", display_name: "Policy" },
        { value: "regulation", display_name: "Regulation" },
        { value: "guideline", display_name: "Guideline" },
        { value: "framework", display_name: "Framework" },
        { value: "sop", display_name: "SOP" },
        { value: "template", display_name: "Template" },
        { value: "report", display_name: "Report" },
        { value: "sep", display_name: "Stakeholder engagement plan" },
        { value: "mapping_tool", display_name: "Mapping tool" },
        { value: "gis_map", display_name: "GIS map" },
        { value: "assessment", display_name: "Assessment" },
        { value: "action_plan", display_name: "Action plan" },
      ],
    },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "document_reference", type: "url" },
    { name: "summary", type: "textarea" },
    { name: "next_review_date", type: "date" },
  ],
  risk_register_entries: [
    {
      name: "infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "scenario", type: "textarea" },
    { name: "likelihood", type: "integer" },
    { name: "impact", type: "integer" },
    { name: "risk_score", type: "decimal" },
    { name: "risk_level", type: "choice", choices: PRIORITY_CHOICES },
    {
      name: "treatment_status",
      type: "choice",
      choices: [
        { value: "identified", display_name: "Identified" },
        { value: "assessing", display_name: "Assessing" },
        { value: "mitigating", display_name: "Mitigating" },
        { value: "accepted", display_name: "Accepted" },
        { value: "closed", display_name: "Closed" },
      ],
    },
    { name: "response_plan", type: "textarea" },
    { name: "response_deadline", type: "date" },
    { name: "last_reviewed_at", type: "date" },
    { name: "update_notes", type: "textarea" },
  ],
  asset_inventory_items: [
    {
      name: "owner_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "sector_ref",
      label: "Sector",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/sectors/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "code", required: true },
    { name: "name", required: true },
    { name: "asset_type", type: "choice", choices: ASSET_INVENTORY_TYPE_CHOICES },
    { name: "owner_name" },
    { name: "essential_function" },
    { name: "admin_area" },
    { name: "location" },
    { name: "latitude", type: "decimal" },
    { name: "longitude", type: "decimal" },
    { name: "criticality_level", type: "choice", choices: PRIORITY_CHOICES },
    { name: "dependency_summary", type: "textarea" },
    { name: "summary", type: "textarea" },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "notes", type: "textarea" },
  ],
  threat_events: [
    {
      name: "reporting_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "asset_item",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/asset-inventory/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "threat_type", type: "choice", choices: THREAT_TYPE_CHOICES },
    { name: "threat_source_type", type: "choice", choices: THREAT_SOURCE_TYPE_CHOICES },
    { name: "status", type: "choice", choices: THREAT_EVENT_STATUS_CHOICES },
    { name: "severity", type: "choice", choices: PRIORITY_CHOICES },
    { name: "confidence_level", type: "choice", choices: PRIORITY_CHOICES },
    { name: "first_seen_at", type: "datetime" },
    { name: "last_seen_at", type: "datetime" },
    { name: "admin_area" },
    { name: "location" },
    { name: "latitude", type: "decimal" },
    { name: "longitude", type: "decimal" },
    { name: "suspected_actor" },
    { name: "summary", type: "textarea" },
    { name: "recommended_action", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  vulnerability_records: [
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "asset_item",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/asset-inventory/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_threat_event",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/threat-events/",
        labelField: "title",
        ordering: "title",
      },
    },
    { name: "title", required: true },
    { name: "vulnerability_type" },
    { name: "severity", type: "choice", choices: PRIORITY_CHOICES },
    { name: "status", type: "choice", choices: VULNERABILITY_STATUS_CHOICES },
    { name: "exploitability_level", type: "choice", choices: PRIORITY_CHOICES },
    { name: "discovered_on", type: "date" },
    { name: "remediation_due_date", type: "date" },
    { name: "owner_name" },
    { name: "summary", type: "textarea" },
    { name: "remediation_guidance", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  risk_scenarios: [
    {
      name: "risk_register_entry",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/risk-register/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "asset_item",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/asset-inventory/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_threat_event",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/threat-events/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "vulnerability_record",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/vulnerability-records/",
        labelField: "title",
        ordering: "title",
      },
    },
    { name: "title", required: true },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "risk_level", type: "choice", choices: PRIORITY_CHOICES },
    {
      name: "treatment_status",
      type: "choice",
      choices: [
        { value: "identified", display_name: "Identified" },
        { value: "assessing", display_name: "Assessing" },
        { value: "mitigating", display_name: "Mitigating" },
        { value: "accepted", display_name: "Accepted" },
        { value: "closed", display_name: "Closed" },
      ],
    },
    { name: "scenario_owner" },
    { name: "likelihood", type: "integer" },
    { name: "impact", type: "integer" },
    { name: "risk_score", type: "decimal" },
    { name: "scenario_summary", type: "textarea" },
    { name: "business_impact", type: "textarea" },
    { name: "response_plan", type: "textarea" },
    { name: "review_due_date", type: "date" },
    { name: "notes", type: "textarea" },
  ],
  risk_assessment_reviews: [
    {
      name: "risk_scenario",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/risk-scenarios/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "risk_register_entry",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/risk-register/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "reviewer_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "review_date", type: "date" },
    { name: "decision", type: "choice", choices: RISK_REVIEW_DECISION_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "residual_risk_level", type: "choice", choices: PRIORITY_CHOICES },
    { name: "summary", type: "textarea" },
    { name: "recommendations", type: "textarea" },
    { name: "follow_up_date", type: "date" },
    { name: "notes", type: "textarea" },
  ],
  threat_bulletins: [
    {
      name: "related_threat_event",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/threat-events/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "target_sector_ref",
      label: "Target sector",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/sectors/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "bulletin_type", type: "choice", choices: BULLETIN_TYPE_CHOICES },
    { name: "severity", type: "choice", choices: PRIORITY_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "issued_on", type: "date" },
    { name: "valid_until", type: "date" },
    { name: "summary", type: "textarea" },
    { name: "recommended_actions", type: "textarea" },
    { name: "source_reference", type: "url" },
    { name: "notes", type: "textarea" },
  ],
  indicators: [
    {
      name: "related_bulletin",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/threat-bulletins/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_threat_event",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/threat-events/",
        labelField: "title",
        ordering: "title",
      },
    },
    { name: "title", required: true },
    { name: "indicator_type", type: "choice", choices: INDICATOR_TYPE_CHOICES },
    { name: "value", required: true },
    { name: "status", type: "choice", choices: INDICATOR_STATUS_CHOICES },
    { name: "confidence_level", type: "choice", choices: PRIORITY_CHOICES },
    { name: "first_seen_at", type: "datetime" },
    { name: "last_seen_at", type: "datetime" },
    { name: "notes", type: "textarea" },
  ],
  distribution_groups: [
    { name: "title", required: true },
    { name: "group_type", type: "choice", choices: DISTRIBUTION_GROUP_TYPE_CHOICES },
    {
      name: "target_sector_ref",
      label: "Target sector",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/sectors/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    {
      name: "stakeholders",
      type: "multirelation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "distribution_notes", type: "textarea" },
  ],
  information_shares: [
    {
      name: "related_bulletin",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/threat-bulletins/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_threat_event",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/threat-events/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "distribution_group",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/distribution-groups/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "target_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "share_channel", type: "choice", choices: SHARE_CHANNEL_CHOICES },
    { name: "status", type: "choice", choices: SHARE_STATUS_CHOICES },
    { name: "shared_at", type: "datetime" },
    { name: "acknowledgement_due_date", type: "date" },
    { name: "action_requested", type: "textarea" },
    { name: "access_link", type: "url" },
    { name: "message_summary", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  acknowledgements: [
    {
      name: "information_share",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/information-shares/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "status", type: "choice", choices: ACKNOWLEDGEMENT_STATUS_CHOICES },
    { name: "responded_at", type: "datetime" },
    { name: "action_note", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  generated_documents: [
    { name: "title", required: true },
    { name: "module_key", required: true },
    { name: "module_label" },
    { name: "record_id", type: "integer" },
    { name: "record_title" },
    { name: "document_type", type: "choice", choices: DOCUMENT_TYPE_CHOICES },
    { name: "output_format", type: "choice", choices: DOCUMENT_FORMAT_CHOICES },
    { name: "status", type: "choice", choices: DOCUMENT_STATUS_CHOICES },
    { name: "version_number", type: "integer" },
    { name: "version_label" },
    { name: "generated_on", type: "datetime" },
    { name: "published_on", type: "datetime" },
    { name: "generated_by_name" },
    { name: "approved_by_name" },
    { name: "summary", type: "textarea" },
    { name: "content_text", type: "textarea" },
    { name: "mime_type" },
    { name: "file_size_bytes", type: "integer" },
    { name: "notes", type: "textarea" },
  ],
  review_cycles: [
    {
      name: "generated_document",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/generated-documents/",
        labelField: "title",
        ordering: "-generated_on",
      },
    },
    { name: "title", required: true },
    { name: "module_key" },
    { name: "module_label" },
    { name: "record_id", type: "integer" },
    { name: "record_title" },
    { name: "owner_name" },
    { name: "cadence_days", type: "integer" },
    { name: "status", type: "choice", choices: REVIEW_CYCLE_STATUS_CHOICES },
    { name: "current_version_label" },
    { name: "last_review_date", type: "date" },
    { name: "next_review_date", type: "date" },
    { name: "scope_summary", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  review_records: [
    {
      name: "review_cycle",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/review-cycles/",
        labelField: "title",
        ordering: "next_review_date",
      },
    },
    {
      name: "generated_document",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/generated-documents/",
        labelField: "title",
        ordering: "-generated_on",
      },
    },
    { name: "title", required: true },
    { name: "review_date", type: "date" },
    { name: "decision", type: "choice", choices: REVIEW_DECISION_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "reviewer_name" },
    { name: "summary", type: "textarea" },
    { name: "recommendations", type: "textarea" },
    { name: "next_review_date", type: "date" },
    { name: "version_label" },
    { name: "notes", type: "textarea" },
  ],
  change_log_entries: [
    {
      name: "generated_document",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/generated-documents/",
        labelField: "title",
        ordering: "-generated_on",
      },
    },
    {
      name: "review_cycle",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/review-cycles/",
        labelField: "title",
        ordering: "next_review_date",
      },
    },
    {
      name: "review_record",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/review-records/",
        labelField: "title",
        ordering: "-review_date",
      },
    },
    { name: "title", required: true },
    { name: "module_key" },
    { name: "module_label" },
    { name: "record_id", type: "integer" },
    { name: "record_title" },
    { name: "change_type", type: "choice", choices: CHANGE_TYPE_CHOICES },
    { name: "version_label" },
    { name: "summary", type: "textarea" },
    { name: "changed_on", type: "datetime" },
    { name: "changed_by_name" },
  ],
  contingency_plans: [
    { name: "title", required: true },
    {
      name: "plan_type",
      type: "choice",
      choices: [
        { value: "national", display_name: "National" },
        { value: "sectoral", display_name: "Sectoral" },
        { value: "incident", display_name: "Incident response" },
        { value: "recovery", display_name: "Recovery" },
        { value: "communication", display_name: "Communication" },
      ],
    },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "communication_procedure", type: "textarea" },
    { name: "coordination_mechanism", type: "textarea" },
    { name: "information_sharing_protocol", type: "textarea" },
    { name: "activation_trigger", type: "textarea" },
    { name: "next_review_date", type: "date" },
    { name: "notes", type: "textarea" },
  ],
  emergency_response_assets: [
    {
      name: "contingency_plan",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/contingency-plans/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "owner_stakeholder",
      label: "Owner stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "name", required: true },
    {
      name: "asset_type",
      type: "choice",
      choices: [
        { value: "digital", display_name: "Digital tool" },
        { value: "physical", display_name: "Physical asset" },
        { value: "facility", display_name: "Facility" },
        { value: "team", display_name: "Team" },
        { value: "platform", display_name: "Platform" },
        { value: "other", display_name: "Other" },
      ],
    },
    { name: "priority", type: "choice", choices: PRIORITY_CHOICES },
    {
      name: "availability_status",
      type: "choice",
      choices: [
        { value: "planned", display_name: "Planned" },
        { value: "ready", display_name: "Ready" },
        { value: "constrained", display_name: "Constrained" },
        { value: "unavailable", display_name: "Unavailable" },
      ],
    },
    { name: "deployment_status", type: "choice", choices: DEPLOYMENT_STATUS_CHOICES },
    { name: "mobilization_eta_minutes", type: "integer" },
    { name: "capacity_units", type: "integer" },
    { name: "last_readiness_check", type: "date" },
    { name: "location" },
    { name: "latitude", type: "number" },
    { name: "longitude", type: "number" },
    { name: "activation_notes", type: "textarea" },
  ],
  simulation_exercises: [
    {
      name: "contingency_plan",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/contingency-plans/",
        labelField: "title",
        ordering: "title",
      },
    },
    { name: "title", required: true },
    {
      name: "exercise_type",
      type: "choice",
      choices: [
        { value: "tabletop", display_name: "Tabletop" },
        { value: "simulation", display_name: "Simulation" },
        { value: "live_drill", display_name: "Live drill" },
      ],
    },
    { name: "planned_date", type: "date" },
    { name: "completed_date", type: "date" },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "scenario", type: "textarea" },
    { name: "participating_sectors", type: "textarea" },
    { name: "findings", type: "textarea" },
    { name: "lessons_learned", type: "textarea" },
  ],
  cyber_standards: [
    { name: "title", required: true },
    {
      name: "target_sector_ref",
      label: "Target sector",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/sectors/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "standard_type",
      type: "choice",
      choices: [
        { value: "isp_equipment", display_name: "ISP equipment" },
        { value: "banking_equipment", display_name: "Banking equipment" },
        { value: "cni_protection", display_name: "CNI protection" },
        { value: "privacy", display_name: "Data protection and privacy" },
        { value: "conformity", display_name: "Conformity assessment" },
      ],
    },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "control_focus", type: "textarea" },
    { name: "summary", type: "textarea" },
    { name: "next_review_date", type: "date" },
  ],
  audit_frameworks: [
    { name: "title", required: true },
    {
      name: "related_standard",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/cyber-standards/",
        labelField: "title",
        ordering: "title",
      },
    },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "compliance_focus", type: "textarea" },
    { name: "incident_response_procedure", type: "textarea" },
    { name: "recovery_procedure", type: "textarea" },
    { name: "next_review_date", type: "date" },
    { name: "review_notes", type: "textarea" },
  ],
  standard_requirements: [
    {
      name: "related_standard",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/cyber-standards/",
        labelField: "title",
        ordering: "title",
      },
    },
    { name: "code", required: true },
    { name: "title", required: true },
    { name: "chapter" },
    { name: "requirement_type", type: "choice", choices: REQUIREMENT_TYPE_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "priority", type: "choice", choices: PRIORITY_CHOICES },
    { name: "owner_name" },
    { name: "sort_order", type: "integer" },
    { name: "summary", type: "textarea" },
    { name: "implementation_guidance", type: "textarea" },
    { name: "verification_method", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  standard_controls: [
    {
      name: "related_standard",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/cyber-standards/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_requirement",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-requirements/",
        labelField: "title",
        ordering: "code",
      },
    },
    { name: "code", required: true },
    { name: "title", required: true },
    { name: "domain" },
    { name: "control_type", type: "choice", choices: CONTROL_TYPE_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "priority", type: "choice", choices: PRIORITY_CHOICES },
    { name: "owner_name" },
    { name: "sort_order", type: "integer" },
    { name: "control_objective", type: "textarea" },
    { name: "control_procedure", type: "textarea" },
    { name: "measurement_criteria", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  conformity_assessments: [
    {
      name: "related_standard",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/cyber-standards/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_requirement",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-requirements/",
        labelField: "title",
        ordering: "code",
      },
    },
    {
      name: "related_control",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-controls/",
        labelField: "title",
        ordering: "code",
      },
    },
    {
      name: "related_framework",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/audit-frameworks/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "target_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "conformity_level", type: "choice", choices: CONFORMITY_LEVEL_CHOICES },
    { name: "assessed_on", type: "date" },
    { name: "next_review_date", type: "date" },
    { name: "assessor_name" },
    { name: "score", type: "integer" },
    { name: "evidence_summary", type: "textarea" },
    { name: "gap_summary", type: "textarea" },
    { name: "recommendation_summary", type: "textarea" },
    { name: "follow_up_action", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  control_evidence: [
    {
      name: "related_assessment",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/conformity-assessments/",
        labelField: "title",
        ordering: "-assessed_on",
      },
    },
    {
      name: "related_standard",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/cyber-standards/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_requirement",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-requirements/",
        labelField: "title",
        ordering: "code",
      },
    },
    {
      name: "related_control",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-controls/",
        labelField: "title",
        ordering: "code",
      },
    },
    { name: "title", required: true },
    { name: "evidence_type", type: "choice", choices: EVIDENCE_TYPE_CHOICES },
    { name: "status", type: "choice", choices: EVIDENCE_STATUS_CHOICES },
    { name: "reference_url", type: "url" },
    { name: "reference_label" },
    { name: "captured_on", type: "date" },
    { name: "validity_until", type: "date" },
    { name: "owner_name" },
    { name: "notes", type: "textarea" },
  ],
  audit_plans: [
    {
      name: "related_framework",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/audit-frameworks/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_standard",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/cyber-standards/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "target_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "scope" },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "planned_start_date", type: "date" },
    { name: "planned_end_date", type: "date" },
    { name: "actual_end_date", type: "date" },
    { name: "lead_auditor" },
    { name: "objectives", type: "textarea" },
    { name: "sampling_strategy", type: "textarea" },
    { name: "summary", type: "textarea" },
    { name: "next_step" },
    { name: "notes", type: "textarea" },
  ],
  audit_checklists: [
    {
      name: "audit_plan",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/audit-plans/",
        labelField: "title",
        ordering: "-planned_start_date",
      },
    },
    {
      name: "related_requirement",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-requirements/",
        labelField: "title",
        ordering: "code",
      },
    },
    {
      name: "related_control",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-controls/",
        labelField: "title",
        ordering: "code",
      },
    },
    { name: "item_order", type: "integer" },
    { name: "title", required: true },
    { name: "verification_procedure", type: "textarea" },
    { name: "expected_evidence", type: "textarea" },
    { name: "status", type: "choice", choices: CHECKLIST_STATUS_CHOICES },
    { name: "result", type: "choice", choices: CONFORMITY_LEVEL_CHOICES },
    { name: "finding_summary", type: "textarea" },
    { name: "evidence_reference", type: "url" },
    { name: "notes", type: "textarea" },
  ],
  audit_findings: [
    {
      name: "audit_plan",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/audit-plans/",
        labelField: "title",
        ordering: "-planned_start_date",
      },
    },
    {
      name: "checklist_item",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/audit-checklists/",
        labelField: "title",
        ordering: "item_order",
      },
    },
    {
      name: "related_assessment",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/conformity-assessments/",
        labelField: "title",
        ordering: "-assessed_on",
      },
    },
    {
      name: "related_requirement",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-requirements/",
        labelField: "title",
        ordering: "code",
      },
    },
    {
      name: "related_control",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-controls/",
        labelField: "title",
        ordering: "code",
      },
    },
    { name: "title", required: true },
    { name: "severity", type: "choice", choices: PRIORITY_CHOICES },
    { name: "status", type: "choice", choices: FINDING_STATUS_CHOICES },
    { name: "due_date", type: "date" },
    { name: "owner_name" },
    { name: "impact_summary", type: "textarea" },
    { name: "recommendation", type: "textarea" },
    { name: "evidence_reference", type: "url" },
    { name: "notes", type: "textarea" },
  ],
  non_conformities: [
    {
      name: "audit_finding",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/audit-findings/",
        labelField: "title",
        ordering: "-due_date",
      },
    },
    {
      name: "related_assessment",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/conformity-assessments/",
        labelField: "title",
        ordering: "-assessed_on",
      },
    },
    {
      name: "related_requirement",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-requirements/",
        labelField: "title",
        ordering: "code",
      },
    },
    {
      name: "related_control",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-controls/",
        labelField: "title",
        ordering: "code",
      },
    },
    { name: "title", required: true },
    { name: "severity", type: "choice", choices: PRIORITY_CHOICES },
    { name: "status", type: "choice", choices: NON_CONFORMITY_STATUS_CHOICES },
    { name: "due_date", type: "date" },
    { name: "owner_name" },
    { name: "root_cause", type: "textarea" },
    { name: "containment_action", type: "textarea" },
    { name: "remediation_expectation", type: "textarea" },
    { name: "verification_notes", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  corrective_actions: [
    {
      name: "related_finding",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/audit-findings/",
        labelField: "title",
        ordering: "-due_date",
      },
    },
    {
      name: "related_non_conformity",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/non-conformities/",
        labelField: "title",
        ordering: "-due_date",
      },
    },
    {
      name: "related_assessment",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/conformity-assessments/",
        labelField: "title",
        ordering: "-assessed_on",
      },
    },
    {
      name: "related_control",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/standard-controls/",
        labelField: "title",
        ordering: "code",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "owner_name" },
    { name: "priority", type: "choice", choices: PRIORITY_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "start_date", type: "date" },
    { name: "due_date", type: "date" },
    { name: "completed_date", type: "date" },
    { name: "action_summary", type: "textarea" },
    { name: "success_metric" },
    { name: "blocker_summary", type: "textarea" },
    { name: "evidence_reference", type: "url" },
    { name: "verification_notes", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  training_programs: [
    { name: "title", required: true },
    {
      name: "program_type",
      type: "choice",
      choices: [
        { value: "risk_management", display_name: "Risk management" },
        { value: "contingency_response", display_name: "Contingency response" },
        { value: "audit_awareness", display_name: "Audit and awareness" },
        { value: "standards_compliance", display_name: "Standards compliance" },
        { value: "stakeholder_engagement", display_name: "Stakeholder engagement" },
      ],
    },
    { name: "duration_days", type: "integer" },
    {
      name: "delivery_mode",
      type: "choice",
      choices: [
        { value: "in_person", display_name: "In person" },
        { value: "virtual", display_name: "Virtual" },
        { value: "hybrid", display_name: "Hybrid" },
      ],
    },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "certificate_required", type: "boolean" },
    { name: "participant_target", type: "integer" },
    { name: "summary", type: "textarea" },
  ],
  deliverable_milestones: [
    { name: "title", required: true },
    { name: "phase", type: "choice", choices: PHASE_CHOICES },
    {
      name: "deliverable_category",
      type: "choice",
      choices: [
        { value: "report", display_name: "Report" },
        { value: "workshop", display_name: "Workshop" },
        { value: "policy", display_name: "Policy" },
        { value: "regulation", display_name: "Regulation" },
        { value: "mapping", display_name: "Mapping" },
        { value: "risk_register", display_name: "Risk register" },
        { value: "contingency", display_name: "Contingency" },
        { value: "standard", display_name: "Standard" },
        { value: "audit", display_name: "Audit" },
        { value: "training", display_name: "Training" },
        { value: "template", display_name: "Template" },
      ],
    },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "planned_week", type: "integer" },
    { name: "due_date", type: "date" },
    { name: "notes", type: "textarea" },
  ],
  desk_study_reviews: [
    {
      name: "related_stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    {
      name: "source_type",
      type: "choice",
      choices: [
        { value: "policy", display_name: "Policy" },
        { value: "regulation", display_name: "Regulation" },
        { value: "standard", display_name: "Standard" },
        { value: "incident", display_name: "Incident material" },
        { value: "report", display_name: "Report" },
        { value: "legal", display_name: "Legal text" },
        { value: "other", display_name: "Other" },
      ],
    },
    { name: "document_owner" },
    { name: "scope" },
    { name: "summary", type: "textarea" },
    { name: "gap_summary", type: "textarea" },
    { name: "recommendation_summary", type: "textarea" },
    { name: "priority", type: "choice", choices: PRIORITY_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "due_date", type: "date" },
    { name: "completed_date", type: "date" },
    { name: "next_action" },
    { name: "notes", type: "textarea" },
  ],
  stakeholder_consultations: [
    {
      name: "stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    {
      name: "consultation_type",
      type: "choice",
      choices: [
        { value: "briefing", display_name: "Briefing" },
        { value: "interview", display_name: "Interview" },
        { value: "workshop", display_name: "Workshop" },
        { value: "validation", display_name: "Validation session" },
        { value: "field_visit", display_name: "Field visit" },
        { value: "exercise", display_name: "Exercise coordination" },
      ],
    },
    { name: "engagement_channel", type: "choice", choices: ENGAGEMENT_CHANNEL_CHOICES },
    { name: "status", type: "choice", choices: CONSULTATION_STATUS_CHOICES },
    { name: "start_datetime", type: "datetime" },
    { name: "end_datetime", type: "datetime" },
    { name: "meeting_location" },
    { name: "meeting_link", type: "url" },
    { name: "dial_in_details", type: "textarea" },
    { name: "focal_person" },
    { name: "objective", type: "textarea" },
    { name: "agenda", type: "textarea" },
    { name: "attendees", type: "textarea", helperText: "Add one attendee or contact per line." },
    { name: "minutes", type: "textarea" },
    { name: "outcome_summary", type: "textarea" },
    { name: "follow_up_actions", type: "textarea" },
    { name: "next_follow_up_date", type: "date" },
    { name: "notes", type: "textarea" },
  ],
  capacity_assessments: [
    {
      name: "infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "scope" },
    { name: "assessment_area" },
    { name: "current_maturity", type: "integer" },
    { name: "target_maturity", type: "integer" },
    { name: "gap_level", type: "choice", choices: PRIORITY_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "lead_assessor" },
    { name: "due_date", type: "date" },
    { name: "completed_date", type: "date" },
    { name: "baseline_summary", type: "textarea" },
    { name: "gap_summary", type: "textarea" },
    { name: "priority_actions", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  action_plan_tasks: [
    {
      name: "related_risk",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/risk-register/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_milestone",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/deliverable-milestones/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "title", required: true },
    { name: "workstream" },
    { name: "owner_name" },
    { name: "priority", type: "choice", choices: PRIORITY_CHOICES },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "start_date", type: "date" },
    { name: "due_date", type: "date" },
    { name: "completed_date", type: "date" },
    { name: "success_metric" },
    { name: "blocker_summary", type: "textarea" },
    { name: "progress_note", type: "textarea" },
    { name: "next_step" },
    { name: "notes", type: "textarea" },
  ],
};

const settingsFieldDefinitions = {
  users: [
    { name: "email", type: "email", required: true },
    { name: "full_name", required: true },
    { name: "phone" },
    {
      name: "organization",
      label: "Workspace organization",
      type: "relation",
      relation: {
        endpoint: "/org/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "role_ids",
      label: "Roles",
      type: "multirelation",
      relation: {
        endpoint: "/rbac/roles/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "password", type: "password", placeholder: "Temporary password" },
    { name: "is_staff", type: "boolean" },
    { name: "is_active", type: "boolean" },
    { name: "is_verified", type: "boolean" },
  ],
  roles: [
    { name: "name", required: true },
    { name: "code", required: true },
    { name: "description", type: "textarea" },
    {
      name: "permission_ids",
      label: "Permissions",
      type: "multirelation",
      relation: {
        endpoint: "/rbac/permissions/",
        labelField: "name",
        ordering: "name",
      },
      span: 2,
    },
  ],
  sectors: [
    { name: "code", required: true },
    { name: "name", required: true },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "description", type: "textarea" },
  ],
  organizations: [
    {
      name: "organization_type",
      label: "Organization type",
      type: "relation",
      relation: {
        endpoint: "/org/organization-types/",
        labelField: "name",
        ordering: "name",
      },
    },
  ],
  organization_types: [
    {
      name: "organization",
      label: "Workspace organization",
      type: "relation",
      relation: {
        endpoint: "/org/",
        labelField: "name",
        ordering: "name",
      },
    },
  ],
  asset_types: [
    {
      name: "organization",
      label: "Workspace organization",
      type: "relation",
      relation: {
        endpoint: "/org/",
        labelField: "name",
        ordering: "name",
      },
    },
  ],
  assets: [
    {
      name: "organization",
      label: "Workspace organization",
      type: "relation",
      relation: {
        endpoint: "/org/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "asset_type",
      label: "Resource type",
      type: "relation",
      relation: {
        endpoint: "/assets/asset-types/",
        labelField: "name",
        ordering: "name",
      },
    },
  ],
  incidents: [
    { name: "title", required: true },
    { name: "incident_type", type: "choice", choices: INCIDENT_TYPE_CHOICES },
    { name: "severity", type: "choice", choices: INCIDENT_SEVERITY_CHOICES },
    { name: "status", type: "choice", choices: INCIDENT_STATUS_CHOICES },
    { name: "source", type: "choice", choices: INCIDENT_SOURCE_CHOICES },
    { name: "detected_at", type: "datetime" },
    { name: "reported_at", type: "datetime" },
    {
      name: "incident_coordinator",
      label: "Incident Coordinator",
      type: "relation",
      relation: {
        endpoint: "/auth/users/",
        labelField: "email",
        ordering: "email",
      },
    },
    {
      name: "lead_stakeholder",
      label: "Lead Stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "linked_plan",
      label: "Linked Plan",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/contingency-plans/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "affected_sectors",
      label: "Affected Sectors",
      type: "multirelation",
      relation: {
        endpoint: "/cybergrc/sectors/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "affected_infrastructure",
      label: "Affected Infrastructure",
      type: "multirelation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "national_significance", type: "boolean" },
    { name: "next_update_due", type: "datetime" },
    { name: "containment_target_at", type: "datetime" },
    { name: "recovery_target_at", type: "datetime" },
    { name: "external_reference" },
    { name: "summary", type: "textarea" },
    { name: "operational_objective", type: "textarea" },
    { name: "cross_sector_impact", type: "textarea" },
    { name: "decision_log", type: "textarea" },
    { name: "lessons_learned", type: "textarea" },
  ],
  incident_updates: [
    {
      name: "incident",
      type: "relation",
      relation: {
        endpoint: "/incident-management/incidents/",
        labelField: "title",
        ordering: "reported_at",
      },
    },
    { name: "title", required: true },
    { name: "update_type", type: "choice", choices: INCIDENT_UPDATE_TYPE_CHOICES },
    { name: "message", type: "textarea" },
    { name: "status_snapshot", type: "choice", choices: INCIDENT_STATUS_CHOICES },
    { name: "severity_snapshot", type: "choice", choices: INCIDENT_SEVERITY_CHOICES },
    { name: "recorded_at", type: "datetime" },
    { name: "next_step" },
  ],
  incident_tasks: [
    {
      name: "incident",
      type: "relation",
      relation: {
        endpoint: "/incident-management/incidents/",
        labelField: "title",
        ordering: "reported_at",
      },
    },
    { name: "title", required: true },
    { name: "description", type: "textarea" },
    { name: "status", type: "choice", choices: INCIDENT_TASK_STATUS_CHOICES },
    { name: "priority", type: "choice", choices: PRIORITY_CHOICES },
    {
      name: "assigned_to",
      label: "Assigned To",
      type: "relation",
      relation: {
        endpoint: "/auth/users/",
        labelField: "email",
        ordering: "email",
      },
    },
    { name: "due_at", type: "datetime" },
    { name: "completed_at", type: "datetime" },
    { name: "blocker_summary" },
    { name: "next_step" },
  ],
  incident_assignments: [
    {
      name: "incident",
      type: "relation",
      relation: {
        endpoint: "/incident-management/incidents/",
        labelField: "title",
        ordering: "reported_at",
      },
    },
    {
      name: "assignee",
      type: "relation",
      relation: {
        endpoint: "/auth/users/",
        labelField: "email",
        ordering: "email",
      },
    },
    {
      name: "stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "role_in_response", required: true },
    { name: "status", type: "choice", choices: INCIDENT_ASSIGNMENT_STATUS_CHOICES },
    { name: "assigned_at", type: "datetime" },
    { name: "acknowledged_at", type: "datetime" },
    { name: "released_at", type: "datetime" },
    { name: "notes", type: "textarea" },
  ],
  incident_communications: [
    {
      name: "incident",
      type: "relation",
      relation: {
        endpoint: "/incident-management/incidents/",
        labelField: "title",
        ordering: "reported_at",
      },
    },
    { name: "subject", required: true },
    { name: "direction", type: "choice", choices: INCIDENT_COMMUNICATION_DIRECTION_CHOICES },
    { name: "channel", type: "choice", choices: INCIDENT_COMMUNICATION_CHANNEL_CHOICES },
    { name: "audience" },
    { name: "message", type: "textarea" },
    { name: "sent_at", type: "datetime" },
    { name: "external_reference" },
    { name: "requires_acknowledgement", type: "boolean" },
  ],
  incident_attachments: [
    {
      name: "incident",
      type: "relation",
      relation: {
        endpoint: "/incident-management/incidents/",
        labelField: "title",
        ordering: "reported_at",
      },
    },
    { name: "title", required: true },
    { name: "attachment_type", type: "choice", choices: INCIDENT_ATTACHMENT_TYPE_CHOICES },
    { name: "reference_url", type: "url" },
    { name: "reference_label" },
    { name: "notes", type: "textarea" },
  ],
  sop_templates: [
    { name: "code", required: true },
    { name: "title", required: true },
    { name: "version" },
    { name: "status", type: "choice", choices: SOP_TEMPLATE_STATUS_CHOICES },
    {
      name: "contingency_plan",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/contingency-plans/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_artifact",
      label: "Related artifact",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/governance-artifacts/",
        labelField: "title",
        ordering: "title",
      },
    },
    {
      name: "related_infrastructure",
      label: "Related infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "owner_stakeholder",
      label: "Owner stakeholder",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/stakeholders/",
        labelField: "name",
        ordering: "name",
      },
    },
    { name: "objective", type: "textarea" },
    { name: "activation_trigger", type: "textarea" },
    { name: "last_reviewed_at", type: "date" },
    { name: "review_notes", type: "textarea" },
    { name: "notes", type: "textarea" },
  ],
  sop_steps: [
    {
      name: "template",
      type: "relation",
      relation: {
        endpoint: "/incident-management/sop-templates/",
        labelField: "title",
        ordering: "title",
      },
    },
    { name: "step_order", type: "integer", required: true },
    { name: "title", required: true },
    { name: "step_type", type: "choice", choices: SOP_STEP_TYPE_CHOICES },
    { name: "is_required", type: "boolean" },
    { name: "responsible_role" },
    {
      name: "default_assignee",
      label: "Default assignee",
      type: "relation",
      relation: {
        endpoint: "/auth/users/",
        labelField: "email",
        ordering: "email",
      },
    },
    { name: "estimated_duration_minutes", type: "integer" },
    { name: "instruction", type: "textarea" },
    { name: "evidence_hint" },
    { name: "escalation_hint" },
  ],
  sop_executions: [
    {
      name: "incident",
      type: "relation",
      relation: {
        endpoint: "/incident-management/incidents/",
        labelField: "title",
        ordering: "reported_at",
      },
    },
    {
      name: "template",
      type: "relation",
      relation: {
        endpoint: "/incident-management/sop-templates/",
        labelField: "title",
        ordering: "title",
      },
    },
    { name: "title", required: true },
    { name: "status", type: "choice", choices: SOP_EXECUTION_STATUS_CHOICES },
    {
      name: "execution_commander",
      label: "Execution commander",
      type: "relation",
      relation: {
        endpoint: "/auth/users/",
        labelField: "email",
        ordering: "email",
      },
    },
    { name: "started_at", type: "datetime" },
    { name: "target_completion_at", type: "datetime" },
    { name: "completed_at", type: "datetime" },
    { name: "summary", type: "textarea" },
    { name: "outcome_summary", type: "textarea" },
    { name: "blocker_summary", type: "textarea" },
    { name: "next_action" },
  ],
  asset_allocations: [
    {
      name: "incident",
      type: "relation",
      relation: {
        endpoint: "/incident-management/incidents/",
        labelField: "title",
        ordering: "reported_at",
      },
    },
    {
      name: "emergency_asset",
      label: "Emergency asset",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/emergency-response-assets/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "destination_infrastructure",
      label: "Destination infrastructure",
      type: "relation",
      relation: {
        endpoint: "/cybergrc/critical-infrastructure/",
        labelField: "name",
        ordering: "name",
      },
    },
    {
      name: "related_task",
      label: "Related incident task",
      type: "relation",
      relation: {
        endpoint: "/incident-management/incident-tasks/",
        labelField: "title",
        ordering: "due_at",
      },
    },
    { name: "title", required: true },
    { name: "status", type: "choice", choices: ALLOCATION_STATUS_CHOICES },
    { name: "priority", type: "choice", choices: INCIDENT_SEVERITY_CHOICES },
    {
      name: "requested_by",
      label: "Requested by",
      type: "relation",
      relation: {
        endpoint: "/auth/users/",
        labelField: "email",
        ordering: "email",
      },
    },
    {
      name: "approved_by",
      label: "Approved by",
      type: "relation",
      relation: {
        endpoint: "/auth/users/",
        labelField: "email",
        ordering: "email",
      },
    },
    { name: "quantity_requested", type: "integer" },
    { name: "quantity_allocated", type: "integer" },
    { name: "requested_at", type: "datetime" },
    { name: "approved_at", type: "datetime" },
    { name: "mobilized_at", type: "datetime" },
    { name: "deployed_at", type: "datetime" },
    { name: "released_at", type: "datetime" },
    { name: "destination" },
    { name: "deployment_notes", type: "textarea" },
    { name: "release_notes", type: "textarea" },
  ],
};

export const moduleConfigs = [
  {
    "key": "users",
    "label": "Users",
    "route": "users",
    "endpoint": "/auth/users/",
    "permission": "accounts.view_user",
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "email",
      "full_name",
      "phone",
      "organization",
      "role_ids",
      "password",
      "is_staff",
      "is_active",
      "is_verified"
    ],
    "fieldDefinitions": settingsFieldDefinitions.users,
    "columns": [
      "full_name",
      "email",
      "organization_name",
      "is_staff",
      "is_active"
    ]
  },
  {
    "key": "roles",
    "label": "Roles",
    "route": "roles",
    "endpoint": "/rbac/roles/",
    "permission": "rbac.view_role",
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "name",
      "code",
      "description",
      "permission_ids"
    ],
    "fieldDefinitions": settingsFieldDefinitions.roles,
    "columns": [
      "name",
      "code",
      "description"
    ]
  },
  {
    "key": "permissions_catalog",
    "label": "Permissions",
    "route": "permissions",
    "endpoint": "/rbac/permissions/",
    "permission": "auth.view_permission",
    "views": [
      "list"
    ],
    "columns": [
      "app_label",
      "codename",
      "name"
    ]
  },
  {
    "key": "sectors",
    "label": "Sectors",
    "route": "sectors",
    "endpoint": "/cybergrc/sectors/",
    "permission": "cybergrc.view_sector",
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "code",
      "name",
      "status",
      "description"
    ],
    "fieldDefinitions": settingsFieldDefinitions.sectors,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "organizations",
    "label": "Organizations",
    "route": "organizations",
    "endpoint": "/org/",
    "permission": "org.view_organization",
    "views": [
      "list",
      "create",
      "import"
    ],
    "formFields": [
      "name",
      "code",
      "organization_type",
      "description",
      "email",
      "phone",
      "is_active"
    ],
    "fieldDefinitions": settingsFieldDefinitions.organizations,
    "columns": [
      "name",
      "code",
      "email",
      "is_active"
    ]
  },
  {
    "key": "sites",
    "label": "Offices",
    "route": "sites",
    "endpoint": "/org/sites/",
    "permission": "org.view_site",
    "views": [
      "list",
      "create",
      "import",
      "map"
    ],
    "formFields": [
      "organization",
      "office_type",
      "name",
      "code",
      "site_type",
      "city",
      "address",
      "phone",
      "alternate_phone",
      "email",
      "fax",
      "status",
      "latitude",
      "longitude"
    ],
    "columns": [
      "name",
      "office_type_name",
      "city",
      "address"
    ]
  },
  {
    "key": "facilities",
    "label": "Facilities",
    "route": "facilities",
    "endpoint": "/org/facilities/",
    "permission": "org.view_facility",
    "views": [
      "list",
      "create",
      "import"
    ],
    "formFields": [
      "organization",
      "site",
      "name",
      "code",
      "facility_type_ref",
      "facility_type",
      "status",
      "city",
      "address",
      "contact_person",
      "phone",
      "email",
      "opening_times",
      "description",
      "latitude",
      "longitude"
    ],
    "columns": [
      "name",
      "facility_type_name",
      "status"
    ]
  },
  {
    "key": "organization_types",
    "label": "Organization Types",
    "route": "organization-types",
    "endpoint": "/org/organization-types/",
    "permission": "org.view_organizationtype",
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "description",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "office_types",
    "label": "Office Types",
    "route": "office-types",
    "endpoint": "/org/office-types/",
    "permission": "org.view_officetype",
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "description",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "facility_types",
    "label": "Facility Types",
    "route": "facility-types",
    "endpoint": "/org/facility-types/",
    "permission": "org.view_facilitytype",
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "description",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "people",
    "label": "People",
    "route": "people",
    "endpoint": "/people/",
    "permission": "people.view_person",
    "formFields": [
      "organization",
      "first_name",
      "last_name",
      "gender",
      "date_of_birth"
    ],
    "columns": [
      "first_name",
      "last_name",
      "gender",
      "date_of_birth"
    ]
  },
  {
    "key": "contacts",
    "label": "Contacts",
    "route": "contacts",
    "endpoint": "/people/contacts/",
    "permission": "people.view_contact",
    "formFields": [
      "organization",
      "person",
      "contact_type",
      "value",
      "label",
      "priority",
      "is_primary",
      "access_level",
      "comments"
    ],
    "columns": [
      "person_name",
      "contact_type",
      "value",
      "is_primary"
    ]
  },
  {
    "key": "identities",
    "label": "Identities",
    "route": "identities",
    "endpoint": "/people/identities/",
    "permission": "people.view_identity",
    "formFields": [
      "organization",
      "person",
      "document_type",
      "document_number",
      "description",
      "issued_country",
      "issued_place",
      "issuing_authority",
      "valid_from",
      "valid_until",
      "comments"
    ],
    "columns": [
      "person_name",
      "document_type",
      "document_number",
      "issued_country"
    ]
  },
  {
    "key": "projects",
    "label": "Projects",
    "route": "projects",
    "endpoint": "/projects/",
    "permission": "projects.view_project",
    "formFields": [
      "organization",
      "name",
      "code",
      "status",
      "start_date",
      "end_date"
    ],
    "columns": [
      "name",
      "code",
      "status",
      "start_date"
    ]
  },
  {
    "key": "activities",
    "label": "Activities",
    "route": "activities",
    "endpoint": "/projects/activities/",
    "permission": "projects.view_activity",
    "formFields": [
      "organization",
      "project",
      "name",
      "description",
      "status",
      "start_date",
      "end_date",
      "contact_person",
      "estimated_hours",
      "actual_hours"
    ],
    "columns": [
      "project_name",
      "name",
      "status",
      "start_date"
    ]
  },
  {
    "key": "tasks",
    "label": "Tasks",
    "route": "tasks",
    "endpoint": "/projects/tasks/",
    "permission": "projects.view_task",
    "formFields": [
      "organization",
      "project",
      "activity",
      "title",
      "description",
      "status",
      "priority",
      "assigned_to",
      "due_date",
      "estimated_hours",
      "actual_hours",
      "source",
      "source_url"
    ],
    "columns": [
      "activity_name",
      "title",
      "status",
      "priority"
    ]
  },
  {
    "key": "messages",
    "label": "Messages",
    "route": "messages",
    "endpoint": "/communications/messages/",
    "permission": null,
    "columns": [
      "recipient",
      "channel",
      "subject",
      "status"
    ]
  },
  {
    "key": "departments",
    "label": "Department Catalog",
    "route": "departments",
    "endpoint": "/hr/departments/",
    "permission": null,
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "job_titles",
    "label": "Job Title Catalog",
    "route": "job-titles",
    "endpoint": "/hr/job-titles/",
    "permission": null,
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "staffs",
    "label": "Staff",
    "route": "staffs",
    "endpoint": "/hr/staffs/",
    "permission": null,
    "views": [
      "list",
      "create",
      "import",
      "report-staff",
      "report-contracts"
    ],
    "formFields": [
      "organization",
      "person",
      "department",
      "job_title",
      "code",
      "name",
      "status",
      "contract_end_date"
    ],
    "columns": [
      "person_name",
      "name",
      "department_name",
      "job_title_name",
      "contract_end_date",
      "status"
    ]
  },
  {
    "key": "volunteers",
    "label": "Volunteers",
    "route": "volunteers",
    "endpoint": "/volunteers/volunteers/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "skills",
    "label": "Skill Catalog",
    "route": "skills",
    "endpoint": "/volunteers/skills/",
    "permission": null,
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "teams",
    "label": "Teams",
    "route": "teams",
    "endpoint": "/hr/teams/",
    "permission": null,
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "team_members",
    "label": "Team Members",
    "route": "team-members",
    "endpoint": "/hr/team-members/",
    "permission": null,
    "views": [
      "list",
      "create",
      "import",
      "search"
    ],
    "formFields": [
      "organization",
      "team",
      "staff",
      "role",
      "status"
    ],
    "columns": [
      "team_name",
      "staff_name",
      "role",
      "status"
    ]
  },
  {
    "key": "staff_skills",
    "label": "Staff Skills",
    "route": "staff-skills",
    "endpoint": "/hr/staff-skills/",
    "permission": null,
    "views": [
      "list",
      "create",
      "search"
    ],
    "formFields": [
      "organization",
      "staff",
      "skill",
      "proficiency",
      "status"
    ],
    "columns": [
      "staff_name",
      "skill_name",
      "proficiency",
      "status"
    ]
  },
  {
    "key": "training_courses",
    "label": "Training Course Catalog",
    "route": "training-courses",
    "endpoint": "/hr/training-courses/",
    "permission": null,
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "certificates",
    "label": "Certificate Catalog",
    "route": "certificates",
    "endpoint": "/hr/certificates/",
    "permission": null,
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "status"
    ],
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "training_events",
    "label": "Training Events",
    "route": "training-events",
    "endpoint": "/hr/training-events/",
    "permission": null,
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "training_course",
      "certificate",
      "code",
      "name",
      "start_date",
      "end_date",
      "status"
    ],
    "columns": [
      "name",
      "training_course_name",
      "start_date",
      "end_date",
      "status"
    ]
  },
  {
    "key": "training_participants",
    "label": "Training Participants",
    "route": "training-participants",
    "endpoint": "/hr/training-participants/",
    "permission": null,
    "views": [
      "list",
      "create",
      "import",
      "search",
      "report-training"
    ],
    "formFields": [
      "organization",
      "training_event",
      "staff",
      "completion_status",
      "score",
      "certificate_awarded"
    ],
    "columns": [
      "training_event_name",
      "staff_name",
      "completion_status",
      "score",
      "certificate_awarded"
    ]
  },
  {
    "key": "availabilitys",
    "label": "Availabilitys",
    "route": "availabilitys",
    "endpoint": "/volunteers/availabilitys/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "requests",
    "label": "Requests",
    "route": "requests",
    "endpoint": "/requests/requests/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "request_items",
    "label": "Request Items",
    "route": "request-items",
    "endpoint": "/requests/request-items/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "quantity"
    ]
  },
  {
    "key": "request_assignments",
    "label": "Request Assignments",
    "route": "request-assignments",
    "endpoint": "/requests/request-assignments/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "warehouses",
    "label": "Warehouses",
    "route": "warehouses",
    "endpoint": "/inventory/warehouses/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "stocks",
    "label": "Stocks",
    "route": "stocks",
    "endpoint": "/inventory/stocks/",
    "permission": null,
    "columns": [
      "sku",
      "name",
      "quantity"
    ]
  },
  {
    "key": "shipments",
    "label": "Shipments",
    "route": "shipments",
    "endpoint": "/inventory/shipments/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "adjustments",
    "label": "Adjustments",
    "route": "adjustments",
    "endpoint": "/inventory/adjustments/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "asset_types",
    "label": "Resource Types",
    "route": "asset-types",
    "endpoint": "/assets/asset-types/",
    "permission": null,
    "views": [
      "list",
      "create"
    ],
    "formFields": [
      "organization",
      "code",
      "name",
      "status"
    ],
    "fieldDefinitions": settingsFieldDefinitions.asset_types,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "assets",
    "label": "Resources",
    "route": "assets",
    "endpoint": "/assets/assets/",
    "permission": null,
    "views": [
      "list",
      "create",
      "import"
    ],
    "formFields": [
      "organization",
      "asset_type",
      "code",
      "name",
      "status"
    ],
    "fieldDefinitions": settingsFieldDefinitions.assets,
    "columns": [
      "code",
      "name",
      "asset_type_name",
      "status"
    ]
  },
  {
    "key": "assignments",
    "label": "Assignments",
    "route": "assignments",
    "endpoint": "/assets/assignments/",
    "permission": null,
    "columns": [
      "assigned_to_name",
      "status"
    ]
  },
  {
    "key": "vehicles",
    "label": "Vehicles",
    "route": "vehicles",
    "endpoint": "/fleet/vehicles/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "trips",
    "label": "Trips",
    "route": "trips",
    "endpoint": "/fleet/trips/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "maintenances",
    "label": "Maintenances",
    "route": "maintenances",
    "endpoint": "/fleet/maintenances/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "vendors",
    "label": "Vendors",
    "route": "vendors",
    "endpoint": "/procurement/vendors/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "purchase_requests",
    "label": "Purchase Requests",
    "route": "purchase-requests",
    "endpoint": "/procurement/purchase-requests/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "purchase_orders",
    "label": "Purchase Orders",
    "route": "purchase-orders",
    "endpoint": "/procurement/purchase-orders/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "documents",
    "label": "Documents",
    "route": "documents",
    "endpoint": "/documents/documents/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "file_attachments",
    "label": "File Attachments",
    "route": "file-attachments",
    "endpoint": "/documents/file-attachments/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "reports",
    "label": "Reports",
    "route": "reports",
    "endpoint": "/reporting/reports/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "dashboards",
    "label": "Dashboards",
    "route": "dashboards",
    "endpoint": "/reporting/dashboards/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "metrics",
    "label": "Metrics",
    "route": "metrics",
    "endpoint": "/reporting/metrics/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "amount"
    ]
  },
  {
    "key": "budgets",
    "label": "Budgets",
    "route": "budgets",
    "endpoint": "/finance/budgets/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "amount",
      "status"
    ]
  },
  {
    "key": "transactions",
    "label": "Transactions",
    "route": "transactions",
    "endpoint": "/finance/transactions/",
    "permission": null,
    "columns": [
      "reference",
      "amount",
      "status"
    ]
  },
  {
    "key": "budget_plans",
    "label": "Budget Plans",
    "route": "budget-plans",
    "endpoint": "/budgets/budget-plans/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "budget_lines",
    "label": "Budget Lines",
    "route": "budget-lines",
    "endpoint": "/budgets/budget-lines/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "amount"
    ]
  },
  {
    "key": "members",
    "label": "Members",
    "route": "members",
    "endpoint": "/memberships/members/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "subscriptions",
    "label": "Subscriptions",
    "route": "subscriptions",
    "endpoint": "/memberships/subscriptions/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "alerts",
    "label": "Alerts",
    "route": "alerts",
    "endpoint": "/alerts/alerts/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "cap_messages",
    "label": "Cap Messages",
    "route": "cap-messages",
    "endpoint": "/alerts/cap-messages/",
    "permission": null,
    "columns": [
      "identifier",
      "headline",
      "scope"
    ]
  },
  {
    "key": "shelters",
    "label": "Shelters",
    "route": "shelters",
    "endpoint": "/shelters/shelters/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "occupancys",
    "label": "Occupancys",
    "route": "occupancys",
    "endpoint": "/shelters/occupancys/",
    "permission": null,
    "columns": [
      "name",
      "quantity"
    ]
  },
  {
    "key": "checkins",
    "label": "Checkins",
    "route": "checkins",
    "endpoint": "/shelters/checkins/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "clients",
    "label": "Clients",
    "route": "clients",
    "endpoint": "/case-management/clients/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "case_filess",
    "label": "Case Filess",
    "route": "case-filess",
    "endpoint": "/case-management/case-filess/",
    "permission": null,
    "columns": [
      "case_number",
      "name",
      "status"
    ]
  },
  {
    "key": "case_events",
    "label": "Case Events",
    "route": "case-events",
    "endpoint": "/case-management/case-events/",
    "permission": null,
    "columns": [
      "event_type",
      "status"
    ]
  },
  {
    "key": "hospitals",
    "label": "Hospitals",
    "route": "hospitals",
    "endpoint": "/health-facilities/hospitals/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "facility_statuss",
    "label": "Facility Statuss",
    "route": "facility-statuss",
    "endpoint": "/health-facilities/facility-statuss/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "patients",
    "label": "Patients",
    "route": "patients",
    "endpoint": "/patients/patients/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "referrals",
    "label": "Referrals",
    "route": "referrals",
    "endpoint": "/patients/referrals/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "medical_records",
    "label": "Medical Records",
    "route": "medical-records",
    "endpoint": "/medical/medical-records/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "consultations",
    "label": "Consultations",
    "route": "consultations",
    "endpoint": "/medical/consultations/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "epidemiology_cases",
    "label": "Epidemiology Cases",
    "route": "epidemiology-cases",
    "endpoint": "/epidemiology/epidemiology-cases/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "contact_traces",
    "label": "Contact Traces",
    "route": "contact-traces",
    "endpoint": "/epidemiology/contact-traces/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "outbreaks",
    "label": "Outbreaks",
    "route": "outbreaks",
    "endpoint": "/epidemiology/outbreaks/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "events",
    "label": "Events",
    "route": "events",
    "endpoint": "/events/events/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "scenarios",
    "label": "Scenarios",
    "route": "scenarios",
    "endpoint": "/events/scenarios/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "event_resources",
    "label": "Event Resources",
    "route": "event-resources",
    "endpoint": "/events/event-resources/",
    "permission": null,
    "columns": [
      "name",
      "status"
    ]
  },
  {
    "key": "missing_persons",
    "label": "Missing Persons",
    "route": "missing-persons",
    "endpoint": "/missing-persons/missing-persons/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "missing_person_reports",
    "label": "Missing Person Reports",
    "route": "missing-person-reports",
    "endpoint": "/missing-persons/missing-person-reports/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "victims",
    "label": "Victims",
    "route": "victims",
    "endpoint": "/victim-identification/victims/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "identifications",
    "label": "Identifications",
    "route": "identifications",
    "endpoint": "/victim-identification/identifications/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "locations",
    "label": "Locations",
    "route": "locations",
    "endpoint": "/locations/locations/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "geo_json_layers",
    "label": "Geo Json Layers",
    "route": "geo-json-layers",
    "endpoint": "/locations/geo-json-layers/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "map_layers",
    "label": "Map Layers",
    "route": "map-layers",
    "endpoint": "/locations/map-layers/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "pages",
    "label": "Pages",
    "route": "pages",
    "endpoint": "/content/pages/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "posts",
    "label": "Posts",
    "route": "posts",
    "endpoint": "/content/posts/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "news_items",
    "label": "News Items",
    "route": "news-items",
    "endpoint": "/content/news-items/",
    "permission": null,
    "columns": [
      "code",
      "title",
      "status"
    ]
  },
  {
    "key": "cybergrc_stakeholders",
    "label": "Cyber Stakeholders",
    "route": "cyber-stakeholders",
    "endpoint": "/cybergrc/stakeholders/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "name",
      "stakeholder_type",
      "sector_ref",
      "focal_point",
      "email",
      "phone",
      "engagement_role",
      "status",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.cybergrc_stakeholders,
    "columns": [
      "name",
      "stakeholder_type",
      "sector",
      "status"
    ]
  },
  {
    "key": "critical_infrastructure",
    "label": "Critical Infrastructure",
    "route": "critical-infrastructure",
    "endpoint": "/cybergrc/critical-infrastructure/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "owner_stakeholder",
      "code",
      "name",
      "sector_ref",
      "infrastructure_type",
      "owner_name",
      "essential_service",
      "location",
      "latitude",
      "longitude",
      "designation_status",
      "criticality_level",
      "vulnerability_level",
      "mapping_status",
      "mission_assurance_status",
      "requires_nda",
      "critical_asset",
      "last_assessed_at",
      "risk_summary",
      "notes",
      "status"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.critical_infrastructure,
    "columns": [
      "code",
      "name",
      "sector",
      "designation_status",
      "criticality_level",
      "mapping_status"
    ]
  },
  {
    "key": "governance_artifacts",
    "label": "Governance Artifacts",
    "route": "governance-artifacts",
    "endpoint": "/cybergrc/governance-artifacts/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "title",
      "phase",
      "artifact_type",
      "status",
      "version",
      "owner_stakeholder",
      "related_infrastructure",
      "document_reference",
      "summary",
      "next_review_date"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.governance_artifacts,
    "columns": [
      "title",
      "phase",
      "artifact_type",
      "status",
      "version"
    ]
  },
  {
    "key": "risk_register_entries",
    "label": "Risk Register",
    "route": "risk-register",
    "endpoint": "/cybergrc/risk-register/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "infrastructure",
      "title",
      "category",
      "scenario",
      "likelihood",
      "impact",
      "risk_score",
      "risk_level",
      "treatment_status",
      "risk_owner",
      "response_plan",
      "response_deadline",
      "last_reviewed_at",
      "update_notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.risk_register_entries,
    "columns": [
      "title",
      "category",
      "risk_level",
      "treatment_status",
      "response_deadline"
    ]
  },
  {
    "key": "asset_inventory_items",
    "label": "Asset Inventory",
    "route": "asset-inventory",
    "endpoint": "/cybergrc/asset-inventory/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "owner_stakeholder",
      "related_infrastructure",
      "sector_ref",
      "code",
      "name",
      "asset_type",
      "owner_name",
      "essential_function",
      "admin_area",
      "location",
      "latitude",
      "longitude",
      "criticality_level",
      "dependency_summary",
      "summary",
      "status",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.asset_inventory_items,
    "columns": [
      "code",
      "name",
      "asset_type",
      "criticality_level",
      "status"
    ]
  },
  {
    "key": "threat_events",
    "label": "Threat Events",
    "route": "threat-events",
    "endpoint": "/cybergrc/threat-events/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "reporting_stakeholder",
      "related_infrastructure",
      "asset_item",
      "title",
      "threat_type",
      "threat_source_type",
      "status",
      "severity",
      "confidence_level",
      "first_seen_at",
      "last_seen_at",
      "admin_area",
      "location",
      "latitude",
      "longitude",
      "suspected_actor",
      "summary",
      "recommended_action",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.threat_events,
    "columns": [
      "title",
      "threat_type",
      "severity",
      "status",
      "first_seen_at"
    ]
  },
  {
    "key": "vulnerability_records",
    "label": "Vulnerability Records",
    "route": "vulnerability-records",
    "endpoint": "/cybergrc/vulnerability-records/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_infrastructure",
      "asset_item",
      "related_threat_event",
      "title",
      "vulnerability_type",
      "severity",
      "status",
      "exploitability_level",
      "discovered_on",
      "remediation_due_date",
      "owner_name",
      "summary",
      "remediation_guidance",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.vulnerability_records,
    "columns": [
      "title",
      "vulnerability_type",
      "severity",
      "status",
      "remediation_due_date"
    ]
  },
  {
    "key": "risk_scenarios",
    "label": "Risk Scenarios",
    "route": "risk-scenarios",
    "endpoint": "/cybergrc/risk-scenarios/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "risk_register_entry",
      "related_infrastructure",
      "asset_item",
      "related_threat_event",
      "vulnerability_record",
      "title",
      "status",
      "risk_level",
      "treatment_status",
      "scenario_owner",
      "likelihood",
      "impact",
      "risk_score",
      "scenario_summary",
      "business_impact",
      "response_plan",
      "review_due_date",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.risk_scenarios,
    "columns": [
      "title",
      "risk_level",
      "treatment_status",
      "status",
      "review_due_date"
    ]
  },
  {
    "key": "risk_assessment_reviews",
    "label": "Risk Assessment Reviews",
    "route": "risk-assessment-reviews",
    "endpoint": "/cybergrc/risk-assessment-reviews/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "risk_scenario",
      "risk_register_entry",
      "reviewer_stakeholder",
      "title",
      "review_date",
      "decision",
      "status",
      "residual_risk_level",
      "summary",
      "recommendations",
      "follow_up_date",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.risk_assessment_reviews,
    "columns": [
      "title",
      "decision",
      "residual_risk_level",
      "status",
      "follow_up_date"
    ]
  },
  {
    "key": "threat_bulletins",
    "label": "Threat Bulletins",
    "route": "threat-bulletins",
    "endpoint": "/cybergrc/threat-bulletins/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_threat_event",
      "related_infrastructure",
      "target_sector_ref",
      "title",
      "bulletin_type",
      "severity",
      "status",
      "issued_on",
      "valid_until",
      "summary",
      "recommended_actions",
      "source_reference",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.threat_bulletins,
    "columns": [
      "title",
      "bulletin_type",
      "severity",
      "status",
      "valid_until"
    ]
  },
  {
    "key": "indicators",
    "label": "Indicators",
    "route": "indicators",
    "endpoint": "/cybergrc/indicators/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_bulletin",
      "related_threat_event",
      "title",
      "indicator_type",
      "value",
      "status",
      "confidence_level",
      "first_seen_at",
      "last_seen_at",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.indicators,
    "columns": [
      "title",
      "indicator_type",
      "status",
      "value",
      "last_seen_at"
    ]
  },
  {
    "key": "distribution_groups",
    "label": "Distribution Groups",
    "route": "distribution-groups",
    "endpoint": "/cybergrc/distribution-groups/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "title",
      "group_type",
      "target_sector_ref",
      "status",
      "stakeholders",
      "distribution_notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.distribution_groups,
    "columns": [
      "title",
      "group_type",
      "target_sector",
      "status"
    ]
  },
  {
    "key": "information_shares",
    "label": "Information Shares",
    "route": "information-shares",
    "endpoint": "/cybergrc/information-shares/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_bulletin",
      "related_threat_event",
      "distribution_group",
      "target_stakeholder",
      "title",
      "share_channel",
      "status",
      "shared_at",
      "acknowledgement_due_date",
      "action_requested",
      "access_link",
      "message_summary",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.information_shares,
    "columns": [
      "title",
      "share_channel",
      "status",
      "shared_at",
      "acknowledgement_due_date"
    ]
  },
  {
    "key": "acknowledgements",
    "label": "Acknowledgements",
    "route": "acknowledgements",
    "endpoint": "/cybergrc/acknowledgements/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "information_share",
      "stakeholder",
      "status",
      "responded_at",
      "action_note",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.acknowledgements,
    "columns": [
      "information_share_title",
      "stakeholder_name",
      "status",
      "responded_at"
    ]
  },
  {
    "key": "generated_documents",
    "label": "Generated Documents",
    "route": "generated-documents",
    "endpoint": "/cybergrc/generated-documents/",
    "permission": "cybergrc.view_generateddocument",
    "views": ["list"],
    "formFields": [
      "title",
      "module_key",
      "module_label",
      "record_id",
      "record_title",
      "document_type",
      "output_format",
      "status",
      "version_number",
      "version_label",
      "generated_on",
      "published_on",
      "generated_by_name",
      "approved_by_name",
      "summary",
      "content_text",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.generated_documents,
    "columns": [
      "title",
      "module_label",
      "document_type",
      "output_format",
      "status",
      "version_label",
      "file_size_bytes",
      "generated_on"
    ]
  },
  {
    "key": "review_cycles",
    "label": "Review Cycles",
    "route": "review-cycles",
    "endpoint": "/cybergrc/review-cycles/",
    "permission": "cybergrc.view_reviewcycle",
    "views": ["list", "create"],
    "formFields": [
      "generated_document",
      "title",
      "module_key",
      "module_label",
      "record_id",
      "record_title",
      "owner_name",
      "cadence_days",
      "status",
      "current_version_label",
      "last_review_date",
      "next_review_date",
      "scope_summary",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.review_cycles,
    "columns": [
      "title",
      "module_label",
      "status",
      "current_version_label",
      "next_review_date"
    ]
  },
  {
    "key": "review_records",
    "label": "Review Records",
    "route": "review-records",
    "endpoint": "/cybergrc/review-records/",
    "permission": "cybergrc.view_reviewrecord",
    "views": ["list", "create"],
    "formFields": [
      "review_cycle",
      "generated_document",
      "title",
      "review_date",
      "decision",
      "status",
      "reviewer_name",
      "summary",
      "recommendations",
      "next_review_date",
      "version_label",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.review_records,
    "columns": [
      "title",
      "decision",
      "status",
      "reviewer_name",
      "review_date",
      "next_review_date"
    ]
  },
  {
    "key": "change_log_entries",
    "label": "Change Log",
    "route": "change-log",
    "endpoint": "/cybergrc/change-log-entries/",
    "permission": "cybergrc.view_changelogentry",
    "views": ["list"],
    "formFields": [],
    "columns": [
      "title",
      "change_type",
      "version_label",
      "changed_on",
      "changed_by_name"
    ]
  },
  {
    "key": "contingency_plans",
    "label": "Contingency Plans",
    "route": "contingency-plans",
    "endpoint": "/cybergrc/contingency-plans/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "title",
      "plan_type",
      "scope",
      "status",
      "communication_procedure",
      "coordination_mechanism",
      "information_sharing_protocol",
      "activation_trigger",
      "review_cycle",
      "next_review_date",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.contingency_plans,
    "columns": [
      "title",
      "plan_type",
      "status",
      "next_review_date"
    ]
  },
  {
    "key": "emergency_response_assets",
    "label": "Emergency Response Assets",
    "route": "emergency-response-assets",
    "endpoint": "/cybergrc/emergency-response-assets/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "contingency_plan",
      "infrastructure",
      "name",
      "asset_type",
      "priority",
      "owner_stakeholder",
      "owner_name",
      "availability_status",
      "deployment_status",
      "mobilization_eta_minutes",
      "capacity_units",
      "last_readiness_check",
      "location",
      "latitude",
      "longitude",
      "activation_notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.emergency_response_assets,
    "columns": [
      "name",
      "asset_type",
      "priority",
      "availability_status",
      "deployment_status",
      "location"
    ]
  },
  {
    "key": "simulation_exercises",
    "label": "Simulation Exercises",
    "route": "simulation-exercises",
    "endpoint": "/cybergrc/simulation-exercises/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "contingency_plan",
      "title",
      "exercise_type",
      "planned_date",
      "completed_date",
      "status",
      "scenario",
      "participating_sectors",
      "findings",
      "lessons_learned"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.simulation_exercises,
    "columns": [
      "title",
      "exercise_type",
      "planned_date",
      "status"
    ]
  },
  {
    "key": "cyber_standards",
    "label": "Cyber Standards",
    "route": "cyber-standards",
    "endpoint": "/cybergrc/cyber-standards/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "title",
      "standard_type",
      "target_sector_ref",
      "status",
      "version",
      "control_focus",
      "review_cycle",
      "owner_name",
      "summary",
      "next_review_date"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.cyber_standards,
    "columns": [
      "title",
      "standard_type",
      "target_sector",
      "status",
      "version"
    ]
  },
  {
    "key": "audit_frameworks",
    "label": "Audit Frameworks",
    "route": "audit-frameworks",
    "endpoint": "/cybergrc/audit-frameworks/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "title",
      "scope",
      "related_standard",
      "status",
      "audit_frequency",
      "compliance_focus",
      "incident_response_procedure",
      "recovery_procedure",
      "next_review_date",
      "review_notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.audit_frameworks,
    "columns": [
      "title",
      "scope",
      "status",
      "audit_frequency"
    ]
  },
  {
    "key": "standard_requirements",
    "label": "Standard Requirements",
    "route": "standard-requirements",
    "endpoint": "/cybergrc/standard-requirements/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_standard",
      "code",
      "title",
      "chapter",
      "requirement_type",
      "status",
      "priority",
      "owner_name",
      "sort_order",
      "summary",
      "implementation_guidance",
      "verification_method",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.standard_requirements,
    "columns": [
      "code",
      "title",
      "related_standard_title",
      "status",
      "priority"
    ]
  },
  {
    "key": "standard_controls",
    "label": "Standard Controls",
    "route": "standard-controls",
    "endpoint": "/cybergrc/standard-controls/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_standard",
      "related_requirement",
      "code",
      "title",
      "domain",
      "control_type",
      "status",
      "priority",
      "owner_name",
      "sort_order",
      "control_objective",
      "control_procedure",
      "measurement_criteria",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.standard_controls,
    "columns": [
      "code",
      "title",
      "related_standard_title",
      "status",
      "priority"
    ]
  },
  {
    "key": "conformity_assessments",
    "label": "Conformity Assessments",
    "route": "conformity-assessments",
    "endpoint": "/cybergrc/conformity-assessments/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_standard",
      "related_requirement",
      "related_control",
      "related_framework",
      "target_stakeholder",
      "related_infrastructure",
      "title",
      "status",
      "conformity_level",
      "assessed_on",
      "next_review_date",
      "assessor_name",
      "score",
      "evidence_summary",
      "gap_summary",
      "recommendation_summary",
      "follow_up_action",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.conformity_assessments,
    "columns": [
      "title",
      "related_standard_title",
      "conformity_level",
      "status",
      "next_review_date"
    ]
  },
  {
    "key": "control_evidence",
    "label": "Control Evidence",
    "route": "control-evidence",
    "endpoint": "/cybergrc/control-evidence/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_assessment",
      "related_standard",
      "related_requirement",
      "related_control",
      "title",
      "evidence_type",
      "status",
      "reference_url",
      "reference_label",
      "captured_on",
      "validity_until",
      "owner_name",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.control_evidence,
    "columns": [
      "title",
      "evidence_type",
      "status",
      "captured_on",
      "validity_until"
    ]
  },
  {
    "key": "audit_plans",
    "label": "Audit Plans",
    "route": "audit-plans",
    "endpoint": "/cybergrc/audit-plans/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_framework",
      "related_standard",
      "target_stakeholder",
      "related_infrastructure",
      "title",
      "scope",
      "status",
      "planned_start_date",
      "planned_end_date",
      "actual_end_date",
      "lead_auditor",
      "objectives",
      "sampling_strategy",
      "summary",
      "next_step",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.audit_plans,
    "columns": [
      "title",
      "related_framework_title",
      "status",
      "planned_start_date",
      "planned_end_date"
    ]
  },
  {
    "key": "audit_checklists",
    "label": "Audit Checklists",
    "route": "audit-checklists",
    "endpoint": "/cybergrc/audit-checklists/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "audit_plan",
      "related_requirement",
      "related_control",
      "item_order",
      "title",
      "verification_procedure",
      "expected_evidence",
      "status",
      "result",
      "finding_summary",
      "evidence_reference",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.audit_checklists,
    "columns": [
      "audit_plan_title",
      "title",
      "status",
      "result",
      "item_order"
    ]
  },
  {
    "key": "audit_findings",
    "label": "Audit Findings",
    "route": "audit-findings",
    "endpoint": "/cybergrc/audit-findings/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "audit_plan",
      "checklist_item",
      "related_assessment",
      "related_requirement",
      "related_control",
      "title",
      "severity",
      "status",
      "due_date",
      "owner_name",
      "impact_summary",
      "recommendation",
      "evidence_reference",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.audit_findings,
    "columns": [
      "title",
      "audit_plan_title",
      "severity",
      "status",
      "due_date"
    ]
  },
  {
    "key": "non_conformities",
    "label": "Non-Conformities",
    "route": "non-conformities",
    "endpoint": "/cybergrc/non-conformities/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "audit_finding",
      "related_assessment",
      "related_requirement",
      "related_control",
      "title",
      "severity",
      "status",
      "due_date",
      "owner_name",
      "root_cause",
      "containment_action",
      "remediation_expectation",
      "verification_notes",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.non_conformities,
    "columns": [
      "title",
      "audit_finding_title",
      "severity",
      "status",
      "due_date"
    ]
  },
  {
    "key": "corrective_actions",
    "label": "Corrective Actions",
    "route": "corrective-actions",
    "endpoint": "/cybergrc/corrective-actions/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_finding",
      "related_non_conformity",
      "related_assessment",
      "related_control",
      "related_infrastructure",
      "title",
      "owner_name",
      "priority",
      "status",
      "start_date",
      "due_date",
      "completed_date",
      "action_summary",
      "success_metric",
      "blocker_summary",
      "evidence_reference",
      "verification_notes",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.corrective_actions,
    "columns": [
      "title",
      "related_finding_title",
      "priority",
      "status",
      "due_date"
    ]
  },
  {
    "key": "training_programs",
    "label": "Training Programs",
    "route": "training-programs",
    "endpoint": "/cybergrc/training-programs/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "title",
      "program_type",
      "target_audience",
      "duration_days",
      "delivery_mode",
      "status",
      "certificate_required",
      "participant_target",
      "summary"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.training_programs,
    "columns": [
      "title",
      "program_type",
      "delivery_mode",
      "status",
      "duration_days"
    ]
  },
  {
    "key": "deliverable_milestones",
    "label": "Deliverable Milestones",
    "route": "deliverable-milestones",
    "endpoint": "/cybergrc/deliverable-milestones/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "title",
      "phase",
      "deliverable_category",
      "status",
      "planned_week",
      "due_date",
      "owner_name",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.deliverable_milestones,
    "columns": [
      "title",
      "phase",
      "deliverable_category",
      "status",
      "planned_week"
    ]
  },
  {
    "key": "desk_study_reviews",
    "label": "Desk Study Reviews",
    "route": "desk-study-reviews",
    "endpoint": "/cybergrc/desk-study-reviews/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_stakeholder",
      "related_infrastructure",
      "title",
      "source_type",
      "document_owner",
      "scope",
      "summary",
      "gap_summary",
      "recommendation_summary",
      "priority",
      "status",
      "due_date",
      "completed_date",
      "next_action",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.desk_study_reviews,
    "columns": [
      "title",
      "source_type",
      "priority",
      "status",
      "due_date"
    ]
  },
  {
    "key": "stakeholder_consultations",
    "label": "Stakeholder Consultations",
    "route": "stakeholder-consultations",
    "endpoint": "/cybergrc/stakeholder-consultations/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "stakeholder",
      "related_infrastructure",
      "title",
      "consultation_type",
      "engagement_channel",
      "status",
      "start_datetime",
      "end_datetime",
      "meeting_location",
      "meeting_link",
      "dial_in_details",
      "focal_person",
      "objective",
      "agenda",
      "attendees",
      "minutes",
      "outcome_summary",
      "follow_up_actions",
      "next_follow_up_date",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.stakeholder_consultations,
    "columns": [
      "title",
      "consultation_type",
      "engagement_channel",
      "start_datetime",
      "status",
      "next_follow_up_date"
    ]
  },
  {
    "key": "capacity_assessments",
    "label": "Capacity Assessments",
    "route": "capacity-assessments",
    "endpoint": "/cybergrc/capacity-assessments/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "infrastructure",
      "stakeholder",
      "title",
      "scope",
      "assessment_area",
      "current_maturity",
      "target_maturity",
      "gap_level",
      "status",
      "lead_assessor",
      "due_date",
      "completed_date",
      "baseline_summary",
      "gap_summary",
      "priority_actions",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.capacity_assessments,
    "columns": [
      "title",
      "assessment_area",
      "gap_level",
      "status",
      "due_date"
    ]
  },
  {
    "key": "action_plan_tasks",
    "label": "Action Plan Tasks",
    "route": "action-plan-tasks",
    "endpoint": "/cybergrc/action-plan-tasks/",
    "permission": null,
    "views": ["list", "create"],
    "formFields": [
      "related_risk",
      "related_milestone",
      "related_infrastructure",
      "title",
      "workstream",
      "owner_name",
      "priority",
      "status",
      "start_date",
      "due_date",
      "completed_date",
      "success_metric",
      "blocker_summary",
      "progress_note",
      "next_step",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.action_plan_tasks,
    "columns": [
      "title",
      "workstream",
      "priority",
      "status",
      "due_date"
    ]
  },
  {
    "key": "incidents",
    "label": "Incidents",
    "route": "incidents",
    "endpoint": "/incident-management/incidents/",
    "permission": "incident_management.view_incident",
    "views": ["list", "create"],
    "formFields": [
      "title",
      "incident_type",
      "severity",
      "status",
      "source",
      "detected_at",
      "reported_at",
      "incident_coordinator",
      "lead_stakeholder",
      "linked_plan",
      "affected_sectors",
      "affected_infrastructure",
      "national_significance",
      "next_update_due",
      "containment_target_at",
      "recovery_target_at",
      "external_reference",
      "summary",
      "operational_objective",
      "cross_sector_impact",
      "decision_log",
      "lessons_learned"
    ],
    "fieldDefinitions": settingsFieldDefinitions.incidents,
    "columns": [
      "title",
      "incident_type",
      "severity",
      "status",
      "incident_coordinator_name",
      "next_update_due"
    ]
  },
  {
    "key": "incident_updates",
    "label": "Incident Updates",
    "route": "incident-updates",
    "endpoint": "/incident-management/incident-updates/",
    "permission": "incident_management.view_incidentupdate",
    "views": ["list", "create"],
    "formFields": [
      "incident",
      "title",
      "update_type",
      "message",
      "status_snapshot",
      "severity_snapshot",
      "recorded_at",
      "next_step"
    ],
    "fieldDefinitions": settingsFieldDefinitions.incident_updates,
    "columns": [
      "incident_title",
      "title",
      "update_type",
      "recorded_at"
    ]
  },
  {
    "key": "incident_tasks",
    "label": "Incident Tasks",
    "route": "incident-tasks",
    "endpoint": "/incident-management/incident-tasks/",
    "permission": "incident_management.view_incidenttask",
    "views": ["list", "create"],
    "formFields": [
      "incident",
      "title",
      "description",
      "status",
      "priority",
      "assigned_to",
      "due_at",
      "completed_at",
      "blocker_summary",
      "next_step"
    ],
    "fieldDefinitions": settingsFieldDefinitions.incident_tasks,
    "columns": [
      "incident_title",
      "title",
      "priority",
      "status",
      "due_at"
    ]
  },
  {
    "key": "incident_assignments",
    "label": "Incident Assignments",
    "route": "incident-assignments",
    "endpoint": "/incident-management/incident-assignments/",
    "permission": "incident_management.view_incidentassignment",
    "views": ["list", "create"],
    "formFields": [
      "incident",
      "assignee",
      "stakeholder",
      "role_in_response",
      "status",
      "assigned_at",
      "acknowledged_at",
      "released_at",
      "notes"
    ],
    "fieldDefinitions": settingsFieldDefinitions.incident_assignments,
    "columns": [
      "incident_title",
      "role_in_response",
      "assignee_name",
      "status",
      "assigned_at"
    ]
  },
  {
    "key": "incident_communications",
    "label": "Incident Communications",
    "route": "incident-communications",
    "endpoint": "/incident-management/incident-communications/",
    "permission": "incident_management.view_incidentcommunication",
    "views": ["list", "create"],
    "formFields": [
      "incident",
      "subject",
      "direction",
      "channel",
      "audience",
      "message",
      "sent_at",
      "external_reference",
      "requires_acknowledgement"
    ],
    "fieldDefinitions": settingsFieldDefinitions.incident_communications,
    "columns": [
      "incident_title",
      "subject",
      "direction",
      "channel",
      "sent_at"
    ]
  },
  {
    "key": "incident_attachments",
    "label": "Incident Attachments",
    "route": "incident-attachments",
    "endpoint": "/incident-management/incident-attachments/",
    "permission": "incident_management.view_incidentattachment",
    "views": ["list", "create"],
    "formFields": [
      "incident",
      "title",
      "attachment_type",
      "reference_url",
      "reference_label",
      "notes"
    ],
    "fieldDefinitions": settingsFieldDefinitions.incident_attachments,
    "columns": [
      "incident_title",
      "title",
      "attachment_type",
      "reference_label"
    ]
  },
  {
    "key": "sop_templates",
    "label": "SOP Templates",
    "route": "sop-templates",
    "endpoint": "/incident-management/sop-templates/",
    "permission": "incident_management.view_soptemplate",
    "views": ["list", "create"],
    "formFields": [
      "code",
      "title",
      "version",
      "status",
      "contingency_plan",
      "related_artifact",
      "related_infrastructure",
      "owner_stakeholder",
      "objective",
      "activation_trigger",
      "last_reviewed_at",
      "review_notes",
      "notes"
    ],
    "fieldDefinitions": settingsFieldDefinitions.sop_templates,
    "columns": [
      "code",
      "title",
      "status",
      "contingency_plan_title",
      "last_reviewed_at"
    ]
  },
  {
    "key": "sop_steps",
    "label": "SOP Steps",
    "route": "sop-steps",
    "endpoint": "/incident-management/sop-steps/",
    "permission": "incident_management.view_sopstep",
    "views": ["list", "create"],
    "formFields": [
      "template",
      "step_order",
      "title",
      "step_type",
      "is_required",
      "responsible_role",
      "default_assignee",
      "estimated_duration_minutes",
      "instruction",
      "evidence_hint",
      "escalation_hint"
    ],
    "fieldDefinitions": settingsFieldDefinitions.sop_steps,
    "columns": [
      "template_title",
      "step_order",
      "title",
      "step_type",
      "is_required"
    ]
  },
  {
    "key": "sop_executions",
    "label": "SOP Executions",
    "route": "sop-executions",
    "endpoint": "/incident-management/sop-executions/",
    "permission": "incident_management.view_sopexecution",
    "views": ["list", "create"],
    "formFields": [
      "incident",
      "template",
      "title",
      "status",
      "execution_commander",
      "started_at",
      "target_completion_at",
      "completed_at",
      "summary",
      "outcome_summary",
      "blocker_summary",
      "next_action"
    ],
    "fieldDefinitions": settingsFieldDefinitions.sop_executions,
    "columns": [
      "incident_title",
      "title",
      "template_title",
      "status",
      "execution_commander_name",
      "target_completion_at",
      "completion_ratio"
    ]
  },
  {
    "key": "asset_allocations",
    "label": "Asset Allocations",
    "route": "asset-allocations",
    "endpoint": "/incident-management/asset-allocations/",
    "permission": "incident_management.view_assetallocation",
    "views": ["list", "create"],
    "formFields": [
      "incident",
      "emergency_asset",
      "destination_infrastructure",
      "related_task",
      "title",
      "status",
      "priority",
      "requested_by",
      "approved_by",
      "quantity_requested",
      "quantity_allocated",
      "requested_at",
      "approved_at",
      "mobilized_at",
      "deployed_at",
      "released_at",
      "destination",
      "deployment_notes",
      "release_notes"
    ],
    "fieldDefinitions": settingsFieldDefinitions.asset_allocations,
    "columns": [
      "title",
      "incident_title",
      "emergency_asset_name",
      "status",
      "priority",
      "quantity_allocated",
      "deployed_at"
    ]
  }
];
