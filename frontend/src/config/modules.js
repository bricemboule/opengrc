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
    { name: "email", type: "email" },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "notes", type: "textarea" },
  ],
  critical_infrastructure: [
    { name: "code", required: true },
    { name: "name", required: true },
    { name: "sector", required: true },
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
    { name: "activation_notes", type: "textarea" },
  ],
  simulation_exercises: [
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
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "compliance_focus", type: "textarea" },
    { name: "incident_response_procedure", type: "textarea" },
    { name: "recovery_procedure", type: "textarea" },
    { name: "next_review_date", type: "date" },
    { name: "review_notes", type: "textarea" },
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
    { name: "objective", type: "textarea" },
    { name: "planned_date", type: "date" },
    { name: "completed_date", type: "date" },
    { name: "status", type: "choice", choices: WORKFLOW_STATUS_CHOICES },
    { name: "focal_person" },
    { name: "outcome_summary", type: "textarea" },
    { name: "follow_up_actions", type: "textarea" },
    { name: "next_follow_up_date", type: "date" },
    { name: "notes", type: "textarea" },
  ],
  capacity_assessments: [
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

export const moduleConfigs = [
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
      "sector",
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
      "sector",
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
      "owner_name",
      "availability_status",
      "location",
      "activation_notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.emergency_response_assets,
    "columns": [
      "name",
      "asset_type",
      "priority",
      "availability_status"
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
      "target_sector",
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
      "objective",
      "planned_date",
      "completed_date",
      "status",
      "focal_person",
      "outcome_summary",
      "follow_up_actions",
      "next_follow_up_date",
      "notes"
    ],
    "fieldDefinitions": cybergrcFieldDefinitions.stakeholder_consultations,
    "columns": [
      "title",
      "consultation_type",
      "planned_date",
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
  }
];
