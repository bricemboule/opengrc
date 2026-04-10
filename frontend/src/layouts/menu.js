import { Box, LayoutDashboard } from "lucide-react";

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

  const flatItems = moduleConfigs
    .filter((item) => !organizationManagedKeys.has(item.key))
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
    ...flatItems,
  ];
}

export { organizationManagedKeys };
