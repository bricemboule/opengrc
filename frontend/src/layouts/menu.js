import { Box, LayoutDashboard, Users } from "lucide-react";

const organizationManagedKeys = new Set([
  "organizations",
  "sites",
  "facilities",
  "organization_types",
  "office_types",
  "facility_types",
  "assets",
  "asset_types",
]);

const staffManagedKeys = new Set([
  "departments",
  "job_titles",
  "staffs",
  "skills",
  "teams",
  "team_members",
  "staff_skills",
  "training_courses",
  "training_events",
  "training_participants",
  "certificates",
]);

function buildModuleLookup(moduleConfigs) {
  return Object.fromEntries(moduleConfigs.map((item) => [item.key, item]));
}

function buildRoute(moduleConfig, mode = null) {
  if (!moduleConfig) return "/";
  return mode ? `/modules/${moduleConfig.route}?mode=${mode}` : `/modules/${moduleConfig.route}`;
}

export function buildMenu(moduleConfigs) {
  const modulesByKey = buildModuleLookup(moduleConfigs);

  const organizationMenu = {
    key: "organization-dropdown",
    label: "Organizations",
    icon: Box,
    type: "dropdown",
    sections: [
      {
        title: "Organizations",
        permission: modulesByKey.organizations?.permission,
        items: [
          { label: "List", to: buildRoute(modulesByKey.organizations) },
          { label: "Create", to: buildRoute(modulesByKey.organizations, "create") },
          { label: "Import", to: buildRoute(modulesByKey.organizations, "import") },
        ],
      },
      {
        title: "Offices",
        permission: modulesByKey.sites?.permission,
        items: [
          { label: "List", to: buildRoute(modulesByKey.sites) },
          { label: "Create", to: buildRoute(modulesByKey.sites, "create") },
          { label: "Map", to: buildRoute(modulesByKey.sites, "map") },
          { label: "Import", to: buildRoute(modulesByKey.sites, "import") },
        ],
      },
      {
        title: "Facilities",
        permission: modulesByKey.facilities?.permission,
        items: [
          { label: "List", to: buildRoute(modulesByKey.facilities) },
          { label: "Create", to: buildRoute(modulesByKey.facilities, "create") },
          { label: "Import", to: buildRoute(modulesByKey.facilities, "import") },
        ],
      },
      {
        title: "Resources",
        permission: modulesByKey.assets?.permission,
        items: [
          { label: "List", to: buildRoute(modulesByKey.assets) },
          { label: "Create", to: buildRoute(modulesByKey.assets, "create") },
          { label: "Import", to: buildRoute(modulesByKey.assets, "import") },
        ],
      },
      {
        title: "Organization Types",
        permission: modulesByKey.organization_types?.permission,
        items: [
          { label: "List", to: buildRoute(modulesByKey.organization_types) },
          { label: "Create", to: buildRoute(modulesByKey.organization_types, "create") },
        ],
      },
      {
        title: "Office Types",
        permission: modulesByKey.office_types?.permission,
        items: [
          { label: "List", to: buildRoute(modulesByKey.office_types) },
          { label: "Create", to: buildRoute(modulesByKey.office_types, "create") },
        ],
      },
      {
        title: "Facility Types",
        permission: modulesByKey.facility_types?.permission,
        items: [
          { label: "List", to: buildRoute(modulesByKey.facility_types) },
          { label: "Create", to: buildRoute(modulesByKey.facility_types, "create") },
        ],
      },
      {
        title: "Resource Types",
        permission: modulesByKey.asset_types?.permission,
        items: [
          { label: "List", to: buildRoute(modulesByKey.asset_types) },
          { label: "Create", to: buildRoute(modulesByKey.asset_types, "create") },
        ],
      },
    ],
  };

  const staffMenu = {
    key: "staff-dropdown",
    label: "Staff",
    icon: Users,
    type: "dropdown",
    sections: [
      {
        title: "Staff",
        permission: modulesByKey.staffs?.permission,
        items: [
          { label: "Create", to: buildRoute(modulesByKey.staffs, "create") },
          { label: "Search by Skills", to: buildRoute(modulesByKey.staff_skills, "search") },
          { label: "Import", to: buildRoute(modulesByKey.staffs, "import") },
        ],
      },
      {
        title: "Staff & Volunteers (Combined)",
        permission: null,
        items: [],
      },
      {
        title: "Teams",
        permission: modulesByKey.teams?.permission,
        items: [
          { label: "Create", to: buildRoute(modulesByKey.teams, "create") },
          { label: "Search Members", to: buildRoute(modulesByKey.team_members, "search") },
          { label: "Import", to: buildRoute(modulesByKey.team_members, "import") },
        ],
      },
      {
        title: "Department Catalog",
        permission: modulesByKey.departments?.permission,
        items: [{ label: "Create", to: buildRoute(modulesByKey.departments, "create") }],
      },
      {
        title: "Job Title Catalog",
        permission: modulesByKey.job_titles?.permission,
        items: [{ label: "Create", to: buildRoute(modulesByKey.job_titles, "create") }],
      },
      {
        title: "Skill Catalog",
        permission: modulesByKey.skills?.permission,
        items: [{ label: "Create", to: buildRoute(modulesByKey.skills, "create") }],
      },
      {
        title: "Training Events",
        permission: modulesByKey.training_events?.permission,
        items: [
          { label: "Create", to: buildRoute(modulesByKey.training_events, "create") },
          { label: "Search Training Participants", to: buildRoute(modulesByKey.training_participants, "search") },
          { label: "Import Participant List", to: buildRoute(modulesByKey.training_participants, "import") },
        ],
      },
      {
        title: "Training Course Catalog",
        permission: modulesByKey.training_courses?.permission,
        items: [{ label: "Create", to: buildRoute(modulesByKey.training_courses, "create") }],
      },
      {
        title: "Certificate Catalog",
        permission: modulesByKey.certificates?.permission,
        items: [{ label: "Create", to: buildRoute(modulesByKey.certificates, "create") }],
      },
      {
        title: "Reports",
        permission: null,
        items: [
          { label: "Staff Report", to: buildRoute(modulesByKey.staffs, "report-staff") },
          { label: "Expiring Staff Contracts Report", to: buildRoute(modulesByKey.staffs, "report-contracts") },
          { label: "Training Report", to: buildRoute(modulesByKey.training_participants, "report-training") },
        ],
      },
    ],
  };

  const flatItems = moduleConfigs
    .filter((item) => !organizationManagedKeys.has(item.key) && !staffManagedKeys.has(item.key))
    .map((item) => ({
      type: "link",
      label: item.label,
      to: buildRoute(item),
      icon: Box,
      permission: item.permission,
    }));

  return [
    { type: "link", label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
    organizationMenu,
    staffMenu,
    ...flatItems,
  ];
}

export { organizationManagedKeys, staffManagedKeys };
