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
    "label": "Departments",
    "route": "departments",
    "endpoint": "/hr/departments/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "job_titles",
    "label": "Job Titles",
    "route": "job-titles",
    "endpoint": "/hr/job-titles/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
    ]
  },
  {
    "key": "staffs",
    "label": "Staffs",
    "route": "staffs",
    "endpoint": "/hr/staffs/",
    "permission": null,
    "columns": [
      "code",
      "name",
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
    "label": "Skills",
    "route": "skills",
    "endpoint": "/volunteers/skills/",
    "permission": null,
    "columns": [
      "code",
      "name",
      "status"
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
  }
];
