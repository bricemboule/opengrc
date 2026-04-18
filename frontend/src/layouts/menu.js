import { FiActivity, FiAlertCircle, FiClipboard, FiFileText, FiHome, FiMapPin, FiSend, FiShield, FiTarget } from "react-icons/fi";
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
        buildCrudSection(modulesByKey.asset_inventory_items, "Asset Inventory"),
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
        buildCrudSection(modulesByKey.threat_events, "Threat Events"),
        buildCrudSection(modulesByKey.vulnerability_records, "Vulnerability Records"),
        buildCrudSection(modulesByKey.risk_scenarios, "Risk Scenarios"),
        buildCrudSection(modulesByKey.risk_assessment_reviews, "Risk Assessment Reviews"),
        buildCrudSection(modulesByKey.capacity_assessments, "Capacity Assessments"),
        buildCrudSection(modulesByKey.training_programs, "Training Programs"),
      ].filter(Boolean),
    },
    {
      key: "threat-sharing-dropdown",
      label: "Threat & Sharing",
      icon: FiSend,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.threat_bulletins, "Threat Bulletins"),
        buildCrudSection(modulesByKey.indicators, "Indicators"),
        buildCrudSection(modulesByKey.distribution_groups, "Distribution Groups"),
        buildCrudSection(modulesByKey.information_shares, "Information Shares"),
        buildCrudSection(modulesByKey.acknowledgements, "Acknowledgements"),
      ].filter(Boolean),
    },
    {
      key: "documents-review-dropdown",
      label: "Documents & Review",
      icon: FiFileText,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.generated_documents, "Generated Documents"),
        buildCrudSection(modulesByKey.review_cycles, "Review Cycles"),
        buildCrudSection(modulesByKey.review_records, "Review Records"),
        buildCrudSection(modulesByKey.change_log_entries, "Change Log"),
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
      key: "incident-dropdown",
      label: "Incident Operations",
      icon: FiAlertCircle,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.incidents, "Incidents"),
        buildCrudSection(modulesByKey.sop_templates, "SOP Templates"),
        buildCrudSection(modulesByKey.sop_steps, "SOP Steps"),
        buildCrudSection(modulesByKey.sop_executions, "SOP Executions"),
        buildCrudSection(modulesByKey.asset_allocations, "Asset Allocations"),
        buildCrudSection(modulesByKey.incident_tasks, "Incident Tasks"),
        buildCrudSection(modulesByKey.incident_assignments, "Incident Assignments"),
        buildCrudSection(modulesByKey.incident_communications, "Incident Communications"),
        buildCrudSection(modulesByKey.incident_updates, "Incident Updates"),
        buildCrudSection(modulesByKey.incident_attachments, "Incident Attachments"),
      ].filter(Boolean),
    },
    {
      key: "standards-dropdown",
      label: "Standards & Audit",
      icon: FiShield,
      type: "dropdown",
      sections: [
        buildCrudSection(modulesByKey.cyber_standards, "Cyber Standards"),
        buildCrudSection(modulesByKey.standard_requirements, "Standard Requirements"),
        buildCrudSection(modulesByKey.standard_controls, "Standard Controls"),
        buildCrudSection(modulesByKey.conformity_assessments, "Conformity Assessments"),
        buildCrudSection(modulesByKey.control_evidence, "Control Evidence"),
        buildCrudSection(modulesByKey.audit_frameworks, "Audit Frameworks"),
        buildCrudSection(modulesByKey.audit_plans, "Audit Plans"),
        buildCrudSection(modulesByKey.audit_checklists, "Audit Checklists"),
        buildCrudSection(modulesByKey.audit_findings, "Audit Findings"),
        buildCrudSection(modulesByKey.non_conformities, "Non-Conformities"),
        buildCrudSection(modulesByKey.corrective_actions, "Corrective Actions"),
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
