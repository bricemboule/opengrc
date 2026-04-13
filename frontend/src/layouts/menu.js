import { FiActivity, FiClipboard, FiHome, FiMapPin, FiShield, FiTarget } from "react-icons/fi";
import { getSupportedViews, getViewLabel } from "../config/moduleBehaviors";

function buildModuleLookup(moduleConfigs) {
  return Object.fromEntries(moduleConfigs.map((item) => [item.key, item]));
}

function buildRoute(moduleConfig, mode = null) {
  if (!moduleConfig) return "/";
  return mode ? `/modules/${moduleConfig.route}?mode=${mode}` : `/modules/${moduleConfig.route}`;
}

function buildCrudSection(moduleConfig, title = null) {
  if (!moduleConfig) return null;

  return {
    title: title || moduleConfig.label,
    permission: moduleConfig.permission,
    items: getSupportedViews(moduleConfig).map((view) => ({
      label: getViewLabel(moduleConfig, view),
      to: buildRoute(moduleConfig, view === "list" ? null : view),
    })),
  };
}

export function buildMenu(moduleConfigs) {
  const modulesByKey = buildModuleLookup(moduleConfigs);

  return [
    {
      label: "Overview",
      to: "/dashboard",
      icon: FiHome,
      permission: null,
    },
    {
      key: "governance-dropdown",
      label: "Governance & Mapping",
      icon: FiMapPin,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.cybergrc_stakeholders, "Stakeholders"),
        buildCrudSection(modulesByKey.desk_study_reviews, "Desk Study Reviews"),
        buildCrudSection(modulesByKey.stakeholder_consultations, "Stakeholder Consultations"),
        buildCrudSection(modulesByKey.critical_infrastructure, "Critical Infrastructure"),
        buildCrudSection(modulesByKey.governance_artifacts, "Governance Artifacts"),
      ].filter(Boolean),
    },
    {
      key: "risk-dropdown",
      label: "Risk & Capacity",
      icon: FiActivity,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.risk_register_entries, "Risk Register"),
        buildCrudSection(modulesByKey.capacity_assessments, "Capacity Assessments"),
        buildCrudSection(modulesByKey.training_programs, "Training Programs"),
      ].filter(Boolean),
    },
    {
      key: "contingency-dropdown",
      label: "Contingency Planning",
      icon: FiTarget,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.contingency_plans, "Contingency Plans"),
        buildCrudSection(modulesByKey.emergency_response_assets, "Emergency Response Assets"),
        buildCrudSection(modulesByKey.simulation_exercises, "Simulation Exercises"),
      ].filter(Boolean),
    },
    {
      key: "standards-dropdown",
      label: "Standards & Audit",
      icon: FiShield,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.cyber_standards, "Cyber Standards"),
        buildCrudSection(modulesByKey.audit_frameworks, "Audit Frameworks"),
      ].filter(Boolean),
    },
    {
      key: "delivery-dropdown",
      label: "Delivery Tracking",
      icon: FiClipboard,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.deliverable_milestones, "Deliverable Milestones"),
        buildCrudSection(modulesByKey.action_plan_tasks, "Action Plan Tasks"),
      ].filter(Boolean),
    },
  ];
}