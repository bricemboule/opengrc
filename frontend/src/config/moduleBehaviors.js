const DEFAULT_VIEW_LABELS = {
  list: "List",
  create: "Create",
  import: "Import",
  map: "Map",
  search: "Search",
  workflow: "Workflow",
  report: "Report",
};

const STAKEHOLDER_FORM_PRESENTATION = {
  variant: "editorial",
  eyebrow: "Governance & Mapping",
  sectionLabel: "Stakeholder coordination file",
  createTitle: "Create a cyber stakeholder",
  editTitle: "Update the cyber stakeholder",
  createDescription: "Fill in the identity, focal point, and engagement role used for cyber coordination.",
  editDescription: "Update the profile, primary contact, and engagement level for this cyber stakeholder.",
  footerNote: "A clear record supports coordination, consultations, and action tracking across institutions.",
  sections: [
    {
      title: "Stakeholder identity",
      description: "Define the institution and its place in the cyber governance and coordination setup.",
      fields: ["name", "stakeholder_type", "sector", "status"],
    },
    {
      title: "Primary coordination contact",
      description: "Fill in the person and the channels the team should use first for operational exchanges.",
      fields: ["focal_point", "email", "phone", "engagement_role"],
    },
    {
      title: "Engagement notes",
      description: "Keep the context needed here to prepare reviews, workshops, and follow-up actions.",
      fields: ["notes"],
    },
  ],
  sidePanel: {
    title: "Build a usable stakeholder file",
    description: "This record should make it easy to understand who the stakeholder is, how to reach them, and what role they play in the cyber program.",
    keyFields: ["name", "stakeholder_type", "focal_point", "status"],
    highlights: [
      "Use the stakeholder's official name rather than an internal alias.",
      "Prioritize a named focal point and direct contact details.",
      "Write the engagement role with concrete verbs: coordinate, supervise, support, or escalate.",
    ],
  },
};

function createWorkflowBlueprint(config) {
  return config;
}

const WORKFLOW_BLUEPRINTS = {
  cybergrc_stakeholders: createWorkflowBlueprint({
    objective: "Move stakeholder files from basic identification to an active coordination posture.",
    contextFields: ["stakeholder_type", "sector", "engagement_role"],
    ownerFields: ["focal_point", "email"],
    blockerRules: [
      { when: (row) => !row.focal_point, label: "Primary focal point missing" },
      { when: (row) => !row.email && !row.phone, label: "No direct contact channel" },
    ],
    stageNotes: {
      draft: "Profile not yet usable for coordination.",
      planned: "Engagement is scheduled but not active yet.",
      in_progress: "Stakeholder file is being completed for active use.",
      active: "Stakeholder is participating in coordination.",
      in_review: "Mandate or contact details are being validated.",
      submitted: "Profile has been routed for validation or approval.",
      validated: "Ready for programme use.",
      completed: "Engagement objective closed.",
      archived: "Record is kept for reference and is no longer in active use.",
    },
    nextActionLabels: {
      draft: "Complete the stakeholder profile and contact details.",
      planned: "Confirm the focal point and first engagement step.",
      active: "Keep coordination notes and responsibilities current.",
      in_review: "Validate the mandate and institutional role.",
      validated: "Use this record as the reference contact file.",
      completed: "Archive or reopen only if the engagement scope changes.",
    },
  }),
  critical_infrastructure: createWorkflowBlueprint({
    objective: "Progress infrastructure from identification to reviewed mapping with criticality and assurance context.",
    contextFields: ["sector", "essential_service", "criticality_level"],
    ownerFields: ["owner_stakeholder_name", "owner_name"],
    dueFields: ["last_assessed_at"],
    blockerRules: [
      { when: (row) => row.requires_nda && ["planned", "in_progress"].includes(row.mapping_status), label: "NDA prerequisite still open" },
      { when: (row) => ["mapped", "reviewed"].includes(row.mapping_status) && (!row.latitude || !row.longitude), label: "Coordinates missing for mapped site" },
      { when: (row) => ["high", "critical"].includes(row.criticality_level) && !row.risk_summary, label: "Risk summary missing for high criticality asset" },
    ],
    stageNotes: {
      planned: "Candidate site is queued for scoping.",
      in_progress: "Assessment and mapping are underway.",
      mapped: "Core data has been captured.",
      reviewed: "Mapping has been reviewed and can be used operationally.",
    },
    nextActionLabels: {
      planned: "Confirm scope, owner, and field assessment prerequisites.",
      in_progress: "Complete mapping data, coordinates, and assurance notes.",
      mapped: "Run the validation review with the relevant parties.",
      reviewed: "Keep coordinates and last assessment date current.",
    },
  }),
  governance_artifacts: createWorkflowBlueprint({
    objective: "Take policies, regulations, templates, and SOPs through drafting, consultation, validation, and publication.",
    contextFields: ["phase", "artifact_type", "version"],
    ownerFields: ["owner_stakeholder_name"],
    dueFields: ["next_review_date"],
    blockerRules: [
      { when: (row) => !row.summary, label: "Summary not filled in" },
      { when: (row) => ["submitted", "validated", "completed"].includes(row.status) && !row.document_reference, label: "Published reference missing" },
    ],
    nextActionLabels: {
      draft: "Finalize the core text and scope.",
      planned: "Prepare the consultation and validation path.",
      in_review: "Collect comments and consolidate revisions.",
      submitted: "Route the artifact for formal decision.",
      validated: "Publish, circulate, and schedule the review loop.",
      completed: "Maintain the current version and review cycle.",
    },
  }),
  desk_study_reviews: createWorkflowBlueprint({
    objective: "Track document analysis from intake through gap extraction and decision-ready recommendations.",
    contextFields: ["source_type", "scope", "priority"],
    ownerFields: ["document_owner", "related_stakeholder_name"],
    dueFields: ["due_date", "completed_date"],
    blockerRules: [
      { when: (row) => ["in_review", "submitted", "validated", "completed"].includes(row.status) && !row.gap_summary, label: "Gap analysis still missing" },
      { when: (row) => ["submitted", "validated", "completed"].includes(row.status) && !row.recommendation_summary, label: "Recommendations not captured" },
    ],
    nextActionLabels: {
      draft: "Capture the document source and review scope.",
      planned: "Schedule the desk review and assign the analyst.",
      in_progress: "Extract findings and critical gaps from the material.",
      in_review: "Validate the findings with the delivery lead.",
      submitted: "Convert findings into decision-ready recommendations.",
      validated: "Feed approved gaps and actions into delivery tracking.",
      completed: "Keep the review linked to action plans and updates.",
    },
  }),
  stakeholder_consultations: createWorkflowBlueprint({
    objective: "Coordinate interviews, workshops, and validation sessions with clear follow-up and accountability.",
    contextFields: ["consultation_type", "stakeholder_name", "focal_person"],
    ownerFields: ["focal_person", "stakeholder_name"],
    dueFields: ["planned_date", "next_follow_up_date"],
    blockerRules: [
      { when: (row) => !row.stakeholder && !row.focal_person, label: "No accountable stakeholder or focal person" },
      { when: (row) => ["planned", "in_progress", "active"].includes(row.status) && !row.planned_date, label: "Consultation date not scheduled" },
      { when: (row) => row.status === "completed" && !row.outcome_summary, label: "Outcome summary still missing" },
    ],
    nextActionLabels: {
      draft: "Clarify the consultation goal and the target stakeholders.",
      planned: "Confirm the date, invitees, and facilitation owner.",
      in_progress: "Capture decisions, commitments, and unresolved issues live.",
      active: "Keep the engagement loop moving and document updates.",
      in_review: "Validate the outputs before closing the session.",
      completed: "Track follow-up actions and next contact date.",
    },
  }),
  risk_register_entries: createWorkflowBlueprint({
    objective: "Take risks from identification to treatment, acceptance, or closure with a named owner and due response.",
    contextFields: ["risk_level", "category", "infrastructure_name"],
    ownerFields: ["risk_owner"],
    dueFields: ["response_deadline", "last_reviewed_at"],
    blockerRules: [
      { when: (row) => ["high", "critical"].includes(row.risk_level) && !row.response_plan, label: "Response plan missing for a priority risk" },
      { when: (row) => !row.risk_owner, label: "Risk owner not assigned" },
    ],
    stageNotes: {
      identified: "Risk has been registered but not assessed.",
      assessing: "The scenario and score are being reviewed.",
      mitigating: "Treatment actions are underway.",
      accepted: "Residual exposure was formally accepted.",
      closed: "Treatment is complete and the record can be monitored.",
    },
    nextActionLabels: {
      identified: "Confirm the owner, score, and immediate response path.",
      assessing: "Validate likelihood, impact, and treatment options.",
      mitigating: "Track delivery of the mitigation actions.",
      accepted: "Document acceptance rationale and review trigger.",
      closed: "Retain the evidence and schedule re-evaluation if needed.",
    },
  }),
  capacity_assessments: createWorkflowBlueprint({
    objective: "Measure preparedness, document gaps, and convert them into targeted strengthening actions.",
    contextFields: ["assessment_area", "gap_level", "scope"],
    ownerFields: ["lead_assessor", "stakeholder_name"],
    dueFields: ["due_date", "completed_date"],
    blockerRules: [
      { when: (row) => row.current_maturity === null || row.current_maturity === undefined, label: "Current maturity score missing" },
      { when: (row) => row.target_maturity === null || row.target_maturity === undefined, label: "Target maturity score missing" },
      { when: (row) => ["high", "critical"].includes(row.gap_level) && !row.priority_actions, label: "Priority actions not defined for a major gap" },
    ],
    nextActionLabels: {
      draft: "Define the assessment scope and method.",
      planned: "Confirm the assessors, dates, and evidence sources.",
      in_progress: "Capture baseline findings and gap levels.",
      in_review: "Validate the gap narrative and action priorities.",
      validated: "Turn approved actions into monitored tasks.",
      completed: "Use the baseline for the next readiness review.",
    },
  }),
  contingency_plans: createWorkflowBlueprint({
    objective: "Develop, validate, and operationalize contingency procedures and coordination steps.",
    contextFields: ["plan_type", "scope", "review_cycle"],
    dueFields: ["next_review_date"],
    blockerRules: [
      { when: (row) => !row.communication_procedure, label: "Communication procedure missing" },
      { when: (row) => !row.coordination_mechanism, label: "Coordination mechanism missing" },
    ],
    nextActionLabels: {
      draft: "Complete the plan structure and activation logic.",
      planned: "Prepare internal review and stakeholder walkthroughs.",
      in_review: "Resolve comments on activation, comms, and coordination.",
      validated: "Publish the plan and communicate the operating model.",
      active: "Keep the review cycle and supporting assets current.",
      completed: "Archive only after a replacement plan is in place.",
    },
  }),
  emergency_response_assets: createWorkflowBlueprint({
    objective: "Keep emergency assets visible, assigned, and ready for activation.",
    contextFields: ["asset_type", "priority", "location"],
    ownerFields: ["owner_name"],
    blockerRules: [
      { when: (row) => row.availability_status === "constrained", label: "Asset is constrained" },
      { when: (row) => row.availability_status === "unavailable", label: "Asset is unavailable" },
    ],
    stageNotes: {
      planned: "Asset is expected but not yet ready.",
      ready: "Asset can be activated.",
      constrained: "Asset is only partly usable.",
      unavailable: "Asset needs recovery or replacement.",
    },
    nextActionLabels: {
      planned: "Confirm ownership, location, and activation notes.",
      ready: "Keep the readiness assumptions current.",
      constrained: "Log the constraint and define a workaround.",
      unavailable: "Escalate the gap and assign restoration actions.",
    },
  }),
  simulation_exercises: createWorkflowBlueprint({
    objective: "Plan, run, and close simulations with findings and lessons learned that feed back into the programme.",
    contextFields: ["exercise_type", "contingency_plan_title", "participating_sectors"],
    dueFields: ["planned_date", "completed_date"],
    blockerRules: [
      { when: (row) => !row.scenario, label: "Exercise scenario missing" },
      { when: (row) => row.status === "completed" && !row.lessons_learned, label: "Lessons learned not captured" },
    ],
    nextActionLabels: {
      planned: "Confirm the scenario, participants, and exercise date.",
      in_progress: "Capture findings and coordination issues during execution.",
      completed: "Turn findings into actions and update related plans.",
    },
  }),
  cyber_standards: createWorkflowBlueprint({
    objective: "Move standards from drafting to validated adoption and recurring review.",
    contextFields: ["standard_type", "target_sector", "version"],
    ownerFields: ["owner_name"],
    dueFields: ["next_review_date"],
    blockerRules: [
      { when: (row) => !row.control_focus, label: "Control focus missing" },
      { when: (row) => !row.summary, label: "Standard summary missing" },
    ],
    nextActionLabels: {
      draft: "Complete the control baseline and target scope.",
      planned: "Prepare consultation and pilot adoption steps.",
      in_review: "Incorporate technical and regulatory feedback.",
      validated: "Publish the validated version and adoption notes.",
      active: "Track implementation and keep the review cycle current.",
    },
  }),
  audit_frameworks: createWorkflowBlueprint({
    objective: "Establish audit methods, response checks, and review cycles that can be run consistently.",
    contextFields: ["scope", "audit_frequency", "related_standard_title"],
    dueFields: ["next_review_date"],
    blockerRules: [
      { when: (row) => !row.incident_response_procedure, label: "Incident response procedure missing" },
      { when: (row) => !row.recovery_procedure, label: "Recovery procedure missing" },
    ],
    nextActionLabels: {
      draft: "Define the audit scope and method.",
      planned: "Confirm review cadence and required evidence.",
      submitted: "Route the framework for validation.",
      validated: "Publish the approved framework and rollout plan.",
      active: "Use the framework and keep review notes current.",
    },
  }),
  training_programs: createWorkflowBlueprint({
    objective: "Take training programmes from design to completed delivery with clear target audience and participation goals.",
    contextFields: ["program_type", "delivery_mode", "target_audience"],
    dueFields: [],
    blockerRules: [
      { when: (row) => !row.participant_target, label: "Participant target missing" },
      { when: (row) => !row.summary, label: "Training summary missing" },
    ],
    nextActionLabels: {
      planned: "Confirm the delivery format, audience, and logistics.",
      in_progress: "Track attendance and the active delivery status.",
      completed: "Capture completion evidence and outputs.",
    },
  }),
  deliverable_milestones: createWorkflowBlueprint({
    objective: "Monitor programme outputs against phase, due date, and validation status.",
    contextFields: ["phase", "deliverable_category", "planned_week"],
    ownerFields: ["owner_name"],
    dueFields: ["due_date"],
    blockerRules: [
      { when: (row) => !row.owner_name, label: "Owner missing" },
      { when: (row) => !row.due_date, label: "Due date missing" },
    ],
    nextActionLabels: {
      draft: "Define the deliverable scope and accountable owner.",
      planned: "Confirm the production window and due date.",
      in_progress: "Track delivery effort and dependencies.",
      validated: "Retain sign-off and handover details.",
      completed: "Keep this milestone as completed evidence.",
    },
  }),
  action_plan_tasks: createWorkflowBlueprint({
    objective: "Turn gaps and decisions into accountable action items with blockers and next steps made visible.",
    contextFields: ["workstream", "priority", "related_infrastructure_name"],
    ownerFields: ["owner_name"],
    dueFields: ["due_date", "completed_date"],
    blockerRules: [
      { when: (row) => !row.owner_name, label: "Owner missing" },
      { when: (row) => Boolean(row.blocker_summary), label: (row) => row.blocker_summary || "Task is blocked" },
      { when: (row) => !row.next_step && row.status !== "completed", label: "Next step not defined" },
    ],
    nextActionLabels: {
      draft: "Clarify the task scope and success metric.",
      planned: "Confirm the owner, start date, and first step.",
      in_progress: "Update progress and escalate blockers early.",
      in_review: "Validate completion evidence before closing.",
      completed: "Keep this task linked to the related gap or deliverable.",
    },
  }),
};

const MODULE_BEHAVIORS = {
  cybergrc_stakeholders: {
    extraViews: ["workflow"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.cybergrc_stakeholders,
    viewLabels: { workflow: "Engagement workflow" },
    formPresentation: STAKEHOLDER_FORM_PRESENTATION,
  },
  critical_infrastructure: {
    extraViews: ["workflow", "map", "report"],
    workflowField: "mapping_status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.critical_infrastructure,
    reportPreset: "mapping",
    viewLabels: { workflow: "Mapping workflow", map: "GIS map", report: "Coverage report" },
  },
  governance_artifacts: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.governance_artifacts,
    reportPreset: "review",
    viewLabels: { workflow: "Validation workflow", report: "Review report" },
  },
  desk_study_reviews: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.desk_study_reviews,
    reportPreset: "desk-study",
    viewLabels: { workflow: "Desk study workflow", report: "Desk study report" },
  },
  stakeholder_consultations: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.stakeholder_consultations,
    reportPreset: "consultation",
    viewLabels: { workflow: "Consultation workflow", report: "Consultation report" },
  },
  risk_register_entries: {
    extraViews: ["workflow", "report"],
    workflowField: "treatment_status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.risk_register_entries,
    reportPreset: "risk",
    viewLabels: { workflow: "Treatment workflow", report: "Risk report" },
  },
  capacity_assessments: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.capacity_assessments,
    reportPreset: "capacity",
    viewLabels: { workflow: "Capacity workflow", report: "Capacity report" },
  },
  contingency_plans: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.contingency_plans,
    reportPreset: "review",
    viewLabels: { workflow: "Activation workflow", report: "Review report" },
  },
  emergency_response_assets: {
    extraViews: ["workflow"],
    workflowField: "availability_status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.emergency_response_assets,
    viewLabels: { workflow: "Readiness board" },
  },
  simulation_exercises: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.simulation_exercises,
    reportPreset: "exercise",
    viewLabels: { workflow: "Exercise workflow", report: "Exercise report" },
  },
  cyber_standards: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.cyber_standards,
    reportPreset: "review",
    viewLabels: { workflow: "Adoption workflow", report: "Review report" },
  },
  audit_frameworks: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.audit_frameworks,
    reportPreset: "review",
    viewLabels: { workflow: "Audit workflow", report: "Review report" },
  },
  training_programs: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.training_programs,
    reportPreset: "training",
    viewLabels: { workflow: "Delivery workflow", report: "Training report" },
  },
  deliverable_milestones: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.deliverable_milestones,
    reportPreset: "delivery",
    viewLabels: { workflow: "Delivery workflow", report: "Delivery report" },
  },
  action_plan_tasks: {
    extraViews: ["workflow", "report"],
    workflowField: "status",
    workflowBlueprint: WORKFLOW_BLUEPRINTS.action_plan_tasks,
    reportPreset: "action-plan",
    viewLabels: { workflow: "Action plan workflow", report: "Action plan report" },
  },
};

export function getModuleBehavior(moduleConfigOrKey) {
  const key = typeof moduleConfigOrKey === "string" ? moduleConfigOrKey : moduleConfigOrKey?.key;
  return MODULE_BEHAVIORS[key] || {};
}

export function getSupportedViews(moduleConfig) {
  if (!moduleConfig) return ["list"];

  const behavior = getModuleBehavior(moduleConfig);
  return ["list", ...(moduleConfig.views || []), ...(behavior.extraViews || [])]
    .filter((view, index, values) => values.indexOf(view) === index)
    .filter((view) => view !== "create" || (moduleConfig.formFields || []).length > 0);
}

export function getViewLabel(moduleConfig, view) {
  const behavior = getModuleBehavior(moduleConfig);
  return behavior.viewLabels?.[view] || DEFAULT_VIEW_LABELS[view] || view;
}

export function getFormPresentation(moduleConfig) {
  const behavior = getModuleBehavior(moduleConfig);
  return behavior.formPresentation || null;
}

export function getWorkflowBlueprint(moduleConfig) {
  const behavior = getModuleBehavior(moduleConfig);
  return behavior.workflowBlueprint || null;
}
