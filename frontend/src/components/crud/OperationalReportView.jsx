import DataTable from "./DataTable";
import EmptyState from "./EmptyState";
import MenuSelect from "../ui/MenuSelect";

function daysUntil(dateValue) {
  const target = new Date(dateValue);
  if (Number.isNaN(target.getTime())) return null;

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  target.setHours(0, 0, 0, 0);
  return Math.round((target.getTime() - today.getTime()) / 86400000);
}

function countStatuses(rows, statuses) {
  return rows.filter((row) => statuses.includes(row.status)).length;
}

function formatReadableValue(value) {
  if (value === null || value === undefined || value === "") return "";
  if (typeof value === "boolean") return value ? "Yes" : "No";

  const normalized = String(value).trim();
  if (!normalized) return "";

  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(normalized)) {
    const parsed = new Date(normalized);
    if (!Number.isNaN(parsed.getTime())) {
      return parsed.toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
    }
  }

  if (/^\d{4}-\d{2}-\d{2}/.test(normalized)) {
    const parsed = new Date(normalized);
    if (!Number.isNaN(parsed.getTime())) {
      return parsed.toLocaleDateString();
    }
  }

  if (normalized.includes("_") || normalized.includes("-") || normalized === normalized.toLowerCase()) {
    return normalized.replaceAll("_", " ").replaceAll("-", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase());
  }

  return normalized;
}

function joinMeta(parts) {
  return parts.map(formatReadableValue).filter(Boolean).join(" • ");
}

function buildSummary(config, rows) {
  switch (config.reportPreset) {
    case "mapping": {
      const mapped = rows.filter((row) => ["mapped", "reviewed"].includes(row.mapping_status)).length;
      const critical = rows.filter((row) => row.criticality_level === "critical").length;
      const vulnerable = rows.filter((row) => ["high", "critical"].includes(row.vulnerability_level)).length;
      return [
        { label: "Coverage", value: `${rows.length ? Math.round((mapped / rows.length) * 100) : 0}%`, helper: `${mapped} of ${rows.length} mapped` },
        { label: "Critical assets", value: critical, helper: "High mission impact records" },
        { label: "High vulnerability", value: vulnerable, helper: "Items needing hardening" },
      ];
    }
    case "risk": {
      const urgent = rows.filter((row) => ["high", "critical"].includes(row.risk_level)).length;
      const dueSoon = rows.filter((row) => row.response_deadline && (daysUntil(row.response_deadline) ?? 999) <= 30).length;
      const closed = rows.filter((row) => row.treatment_status === "closed").length;
      return [
        { label: "High priority", value: urgent, helper: "High and critical risks" },
        { label: "Due in 30 days", value: dueSoon, helper: "Response deadlines approaching" },
        { label: "Closed", value: closed, helper: "Risks already treated" },
      ];
    }
    case "asset-inventory": {
      const geolocated = rows.filter((row) => row.latitude && row.longitude).length;
      const critical = rows.filter((row) => ["high", "critical"].includes(row.criticality_level)).length;
      const active = countStatuses(rows, ["active", "validated", "completed"]);
      return [
        { label: "Geolocated", value: geolocated, helper: "Inventory items with usable coordinates" },
        { label: "High criticality", value: critical, helper: "Items that need stronger operational oversight" },
        { label: "Active", value: active, helper: "Inventory records ready for mapping and response use" },
      ];
    }
    case "threat": {
      const severe = rows.filter((row) => ["high", "critical"].includes(row.severity)).length;
      const open = rows.filter((row) => !["mitigated", "closed"].includes(row.status)).length;
      const geolocated = rows.filter((row) => row.latitude && row.longitude).length;
      return [
        { label: "High severity", value: severe, helper: "Threats needing rapid coordination" },
        { label: "Open", value: open, helper: "Threats still under analysis or monitoring" },
        { label: "Mapped", value: geolocated, helper: "Threat events carrying usable location data" },
      ];
    }
    case "vulnerability": {
      const severe = rows.filter((row) => ["high", "critical"].includes(row.severity)).length;
      const dueSoon = rows.filter((row) => row.remediation_due_date && (daysUntil(row.remediation_due_date) ?? 999) >= 0 && (daysUntil(row.remediation_due_date) ?? 999) <= 14).length;
      const resolved = countStatuses(rows, ["resolved", "closed"]);
      return [
        { label: "High severity", value: severe, helper: "Vulnerabilities requiring urgent action" },
        { label: "Due in 14 days", value: dueSoon, helper: "Remediation dates approaching quickly" },
        { label: "Resolved", value: resolved, helper: "Records already fixed or formally closed" },
      ];
    }
    case "risk-scenario": {
      const urgent = rows.filter((row) => ["high", "critical"].includes(row.risk_level)).length;
      const dueSoon = rows.filter((row) => row.review_due_date && (daysUntil(row.review_due_date) ?? 999) >= 0 && (daysUntil(row.review_due_date) ?? 999) <= 30).length;
      const mitigating = countStatuses(rows, ["mitigating"]);
      const closed = countStatuses(rows, ["closed"]);
      return [
        { label: "High priority", value: urgent, helper: "Scenarios with major national or sector impact" },
        { label: "Review due", value: dueSoon, helper: "Scenario reviews needed in the next 30 days" },
        { label: "Mitigating", value: mitigating, helper: "Scenarios currently under treatment" },
        { label: "Closed", value: closed, helper: "Scenarios formally closed out" },
      ];
    }
    case "risk-review": {
      const dueSoon = rows.filter((row) => row.follow_up_date && (daysUntil(row.follow_up_date) ?? 999) >= 0 && (daysUntil(row.follow_up_date) ?? 999) <= 30).length;
      const highResidual = rows.filter((row) => ["high", "critical"].includes(row.residual_risk_level)).length;
      const completed = countStatuses(rows, ["validated", "completed"]);
      return [
        { label: "Follow-up due", value: dueSoon, helper: "Reviews requiring an action in the next 30 days" },
        { label: "High residual", value: highResidual, helper: "Reviews that still carry major residual exposure" },
        { label: "Completed", value: completed, helper: "Reviews already validated or closed out" },
      ];
    }
    case "bulletin": {
      const active = countStatuses(rows, ["validated", "active"]);
      const expiring = rows.filter((row) => row.valid_until && (daysUntil(row.valid_until) ?? 999) >= 0 && (daysUntil(row.valid_until) ?? 999) <= 7).length;
      const severe = rows.filter((row) => ["high", "critical"].includes(row.severity)).length;
      return [
        { label: "Active", value: active, helper: "Bulletins ready for operational use" },
        { label: "Expiring in 7 days", value: expiring, helper: "Bulletins that need refresh or closure soon" },
        { label: "High severity", value: severe, helper: "Bulletins carrying elevated urgency" },
      ];
    }
    case "indicator": {
      const active = countStatuses(rows, ["new", "active"]);
      const monitoring = countStatuses(rows, ["monitoring"]);
      const expired = countStatuses(rows, ["expired", "revoked"]);
      return [
        { label: "Active", value: active, helper: "Indicators ready for operational use" },
        { label: "Monitoring", value: monitoring, helper: "Indicators still under live watch" },
        { label: "Expired or revoked", value: expired, helper: "Indicators needing refresh or retirement" },
      ];
    }
    case "distribution-group": {
      const active = countStatuses(rows, ["active", "validated"]);
      const sectorGroups = rows.filter((row) => row.group_type === "sector").length;
      const populated = rows.filter((row) => Array.isArray(row.stakeholder_names) && row.stakeholder_names.length > 0).length;
      return [
        { label: "Active", value: active, helper: "Groups currently ready for distribution use" },
        { label: "Sector groups", value: sectorGroups, helper: "Groups centered on sector coordination" },
        { label: "Populated", value: populated, helper: "Groups already carrying stakeholder members" },
      ];
    }
    case "information-share": {
      const shared = countStatuses(rows, ["shared", "acknowledged"]);
      const dueSoon = rows.filter((row) => row.acknowledgement_due_date && (daysUntil(row.acknowledgement_due_date) ?? 999) >= 0 && (daysUntil(row.acknowledgement_due_date) ?? 999) <= 7).length;
      const closed = countStatuses(rows, ["closed"]);
      return [
        { label: "Shared", value: shared, helper: "Messages already distributed to the target audience" },
        { label: "Ack due in 7 days", value: dueSoon, helper: "Shares needing acknowledgement soon" },
        { label: "Closed", value: closed, helper: "Sharing cycles already completed" },
      ];
    }
    case "acknowledgement": {
      const pending = countStatuses(rows, ["pending"]);
      const received = countStatuses(rows, ["received"]);
      const actioned = countStatuses(rows, ["actioned"]);
      const declined = countStatuses(rows, ["declined"]);
      return [
        { label: "Pending", value: pending, helper: "Acknowledgements still waiting for response" },
        { label: "Received", value: received, helper: "Recipients confirmed receipt" },
        { label: "Actioned", value: actioned, helper: "Recipients confirmed action" },
        { label: "Declined", value: declined, helper: "Recipients declined or could not act" },
      ];
    }
    case "generated-document": {
      const awaitingReview = countStatuses(rows, ["generated", "in_review"]);
      const approved = countStatuses(rows, ["approved"]);
      const superseded = countStatuses(rows, ["superseded"]);
      const published = rows.filter((row) => row.published_on).length;
      return [
        { label: "Awaiting review", value: awaitingReview, helper: "Documents still waiting for a final decision" },
        { label: "Approved", value: approved, helper: "Documents approved for controlled use" },
        { label: "Published", value: published, helper: "Documents already carrying a publication time" },
        { label: "Superseded", value: superseded, helper: "Older versions retained for traceability" },
      ];
    }
    case "review-cycle": {
      const overdue = countStatuses(rows, ["overdue"]);
      const active = countStatuses(rows, ["active"]);
      const dueSoon = rows.filter((row) => row.next_review_date && (daysUntil(row.next_review_date) ?? 999) >= 0 && (daysUntil(row.next_review_date) ?? 999) <= 30).length;
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Overdue", value: overdue, helper: "Review cycles that already need attention" },
        { label: "Due in 30 days", value: dueSoon, helper: "Scheduled reviews approaching soon" },
        { label: "Active", value: active, helper: "Review cycles currently in force" },
        { label: "Completed", value: completed, helper: "Review rounds formally closed" },
      ];
    }
    case "review-record": {
      const approved = rows.filter((row) => row.decision === "approved").length;
      const changesRequested = rows.filter((row) => row.decision === "changes_requested").length;
      const superseded = rows.filter((row) => row.decision === "superseded").length;
      const followUpDue = rows.filter((row) => row.next_review_date && (daysUntil(row.next_review_date) ?? 999) >= 0 && (daysUntil(row.next_review_date) ?? 999) <= 30).length;
      return [
        { label: "Approved", value: approved, helper: "Review outcomes that approved the current version" },
        { label: "Changes requested", value: changesRequested, helper: "Reviews still asking for updates" },
        { label: "Superseded", value: superseded, helper: "Reviews that replaced an earlier version" },
        { label: "Follow-up due", value: followUpDue, helper: "Reviews that already set a next review date" },
      ];
    }
    case "change-log": {
      const generated = rows.filter((row) => row.change_type === "generated").length;
      const approved = rows.filter((row) => row.change_type === "approved").length;
      const reviewed = rows.filter((row) => row.change_type === "review_recorded").length;
      const recent = rows.filter((row) => row.changed_on && (daysUntil(String(row.changed_on).slice(0, 10)) ?? 999) >= -7).length;
      return [
        { label: "Generated", value: generated, helper: "New document versions created from live data" },
        { label: "Reviewed", value: reviewed, helper: "Formal review decisions captured in the audit trail" },
        { label: "Approved", value: approved, helper: "Changes that marked a version as approved" },
        { label: "Recent changes", value: recent, helper: "Entries recorded in the last 7 days" },
      ];
    }
    case "desk-study": {
      const dueSoon = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? 999) >= 0 && (daysUntil(row.due_date) ?? 999) <= 14).length;
      const overdue = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? -999) < 0 && !["completed", "archived"].includes(row.status)).length;
      const completed = countStatuses(rows, ["completed", "validated"]);
      return [
        { label: "Due in 14 days", value: dueSoon, helper: "Desk studies close to deadline" },
        { label: "Overdue", value: overdue, helper: "Open document reviews already late" },
        { label: "Completed", value: completed, helper: "Studies already validated or completed" },
      ];
    }
    case "consultation": {
      const upcoming = rows.filter((row) => {
        const scheduleDate = row.start_datetime || row.planned_date;
        return scheduleDate && (daysUntil(scheduleDate) ?? 999) >= 0 && (daysUntil(scheduleDate) ?? 999) <= 30;
      }).length;
      const followUps = rows.filter((row) => row.next_follow_up_date && (daysUntil(row.next_follow_up_date) ?? 999) >= 0 && (daysUntil(row.next_follow_up_date) ?? 999) <= 14).length;
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Upcoming", value: upcoming, helper: "Meetings or calls planned in the next 30 days" },
        { label: "Follow-up due", value: followUps, helper: "Sessions needing a next action now" },
        { label: "Completed", value: completed, helper: "Consultations with minutes or outcome ready" },
      ];
    }
    case "capacity": {
      const highGap = rows.filter((row) => ["high", "critical"].includes(row.gap_level)).length;
      const dueSoon = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? 999) <= 30).length;
      const completed = countStatuses(rows, ["completed", "validated"]);
      return [
        { label: "High gaps", value: highGap, helper: "Assessments showing major readiness gaps" },
        { label: "Due in 30 days", value: dueSoon, helper: "Assessments that need attention this month" },
        { label: "Completed", value: completed, helper: "Assessments with a usable baseline" },
      ];
    }
    case "delivery": {
      const overdue = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? -999) < 0 && !["completed", "validated", "archived"].includes(row.status)).length;
      const dueSoon = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? 999) >= 0 && (daysUntil(row.due_date) ?? 999) <= 14).length;
      const completed = rows.filter((row) => ["completed", "validated"].includes(row.status)).length;
      return [
        { label: "Overdue", value: overdue, helper: "Past due active deliverables" },
        { label: "Due in 14 days", value: dueSoon, helper: "Near-term delivery pressure" },
        { label: "Completed", value: completed, helper: "Validated or completed items" },
      ];
    }
    case "exercise": {
      const planned = rows.filter((row) => row.status === "planned").length;
      const active = rows.filter((row) => row.status === "in_progress").length;
      const completed = rows.filter((row) => row.status === "completed").length;
      return [
        { label: "Planned", value: planned, helper: "Upcoming drills and simulations" },
        { label: "Active", value: active, helper: "Exercises currently running" },
        { label: "Completed", value: completed, helper: "Exercises with execution status complete" },
      ];
    }
    case "review": {
      const overdue = rows.filter((row) => row.next_review_date && (daysUntil(row.next_review_date) ?? -999) < 0).length;
      const dueSoon = rows.filter((row) => row.next_review_date && (daysUntil(row.next_review_date) ?? 999) >= 0 && (daysUntil(row.next_review_date) ?? 999) <= 30).length;
      const inReview = rows.filter((row) => ["in_review", "submitted", "validated"].includes(row.status)).length;
      return [
        { label: "Overdue reviews", value: overdue, helper: "Review dates already passed" },
        { label: "Due in 30 days", value: dueSoon, helper: "Review loop to schedule now" },
        { label: "In review", value: inReview, helper: "Records moving through validation" },
      ];
    }
    case "training": {
      const planned = countStatuses(rows, ["planned"]);
      const active = countStatuses(rows, ["in_progress", "active"]);
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Planned", value: planned, helper: "Programmes ready to launch" },
        { label: "Active", value: active, helper: "Training currently being delivered" },
        { label: "Completed", value: completed, helper: "Programmes that finished delivery" },
      ];
    }
    case "incident": {
      const active = rows.filter((row) => row.status !== "closed").length;
      const severe = rows.filter((row) => ["high", "critical", "national"].includes(row.severity)).length;
      const updateDue = rows.filter((row) => row.next_update_due && (daysUntil(row.next_update_due) ?? 999) <= 1).length;
      return [
        { label: "Active", value: active, helper: "Incidents still open in the response cycle" },
        { label: "High severity", value: severe, helper: "Incidents needing command attention" },
        { label: "Update due", value: updateDue, helper: "Incidents needing a fresh operational update" },
      ];
    }
    case "incident-task": {
      const blocked = rows.filter((row) => row.status === "blocked" || row.blocker_summary).length;
      const dueSoon = rows.filter((row) => row.due_at && (daysUntil(row.due_at) ?? 999) >= 0 && (daysUntil(row.due_at) ?? 999) <= 3).length;
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Blocked", value: blocked, helper: "Tasks currently slowed by a blocker" },
        { label: "Due in 3 days", value: dueSoon, helper: "Near-term response tasks" },
        { label: "Completed", value: completed, helper: "Tasks already closed in the incident cycle" },
      ];
    }
    case "action-plan": {
      const overdue = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? -999) < 0 && !["completed", "archived"].includes(row.status)).length;
      const blocked = rows.filter((row) => row.blocker_summary).length;
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Overdue", value: overdue, helper: "Action tasks already past due" },
        { label: "Blocked", value: blocked, helper: "Tasks carrying a blocker summary" },
        { label: "Completed", value: completed, helper: "Tasks with closed execution status" },
      ];
    }
    case "sop-execution": {
      const active = countStatuses(rows, ["planned", "active", "blocked"]);
      const blocked = rows.filter((row) => row.status === "blocked" || row.blocker_summary).length;
      const dueSoon = rows.filter((row) => row.target_completion_at && (daysUntil(row.target_completion_at) ?? 999) >= 0 && (daysUntil(row.target_completion_at) ?? 999) <= 1).length;
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Active runs", value: active, helper: "Playbooks still live in the response cycle" },
        { label: "Blocked", value: blocked, helper: "Executions needing command intervention" },
        { label: "Due in 24h", value: dueSoon, helper: "Runs close to target completion" },
        { label: "Completed", value: completed, helper: "Executions already closed out" },
      ];
    }
    case "allocation": {
      const pending = countStatuses(rows, ["requested", "approved"]);
      const deployed = countStatuses(rows, ["mobilizing", "deployed", "demobilizing"]);
      const released = countStatuses(rows, ["released"]);
      const constrained = rows.filter((row) => ["constrained", "unavailable"].includes(String(row.asset_availability_status || "").toLowerCase()) || ["maintenance"].includes(String(row.asset_deployment_status || "").toLowerCase())).length;
      return [
        { label: "Pending", value: pending, helper: "Allocations waiting for movement or approval" },
        { label: "Live deployments", value: deployed, helper: "Assets being mobilized or actively deployed" },
        { label: "Released", value: released, helper: "Allocations already demobilized" },
        { label: "Constrained", value: constrained, helper: "Allocations attached to limited or unavailable assets" },
      ];
    }
    case "conformity": {
      const nonConformant = rows.filter((row) => row.conformity_level === "non_conformant").length;
      const dueSoon = rows.filter((row) => row.next_review_date && (daysUntil(row.next_review_date) ?? 999) >= 0 && (daysUntil(row.next_review_date) ?? 999) <= 30).length;
      const validated = countStatuses(rows, ["validated", "completed"]);
      const evidenceGaps = rows.filter((row) => !row.evidence_summary && row.status !== "draft").length;
      return [
        { label: "Non-conformant", value: nonConformant, helper: "Assessments requiring remediation now" },
        { label: "Due in 30 days", value: dueSoon, helper: "Assessments needing a fresh review" },
        { label: "Validated", value: validated, helper: "Assessments already approved for use" },
        { label: "Evidence gaps", value: evidenceGaps, helper: "Assessments missing a usable evidence summary" },
      ];
    }
    case "evidence": {
      const available = countStatuses(rows, ["available", "reviewed"]);
      const pending = countStatuses(rows, ["pending"]);
      const expired = countStatuses(rows, ["expired"]);
      const dueSoon = rows.filter((row) => row.validity_until && (daysUntil(row.validity_until) ?? 999) >= 0 && (daysUntil(row.validity_until) ?? 999) <= 30).length;
      return [
        { label: "Available", value: available, helper: "Evidence items ready for audit or review" },
        { label: "Pending", value: pending, helper: "Evidence still to be captured or attached" },
        { label: "Expiring soon", value: dueSoon, helper: "Validity ending within 30 days" },
        { label: "Expired", value: expired, helper: "Evidence no longer valid for assurance" },
      ];
    }
    case "audit-plan": {
      const upcoming = rows.filter((row) => row.planned_start_date && (daysUntil(row.planned_start_date) ?? 999) >= 0 && (daysUntil(row.planned_start_date) ?? 999) <= 30).length;
      const active = countStatuses(rows, ["in_progress", "active", "in_review"]);
      const overdue = rows.filter((row) => row.planned_end_date && (daysUntil(row.planned_end_date) ?? -999) < 0 && !["completed", "archived"].includes(row.status)).length;
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Upcoming", value: upcoming, helper: "Audit plans starting in the next 30 days" },
        { label: "Active", value: active, helper: "Audit plans currently being executed or reviewed" },
        { label: "Overdue", value: overdue, helper: "Audit plans past their planned end date" },
        { label: "Completed", value: completed, helper: "Audit plans already closed out" },
      ];
    }
    case "audit-checklist": {
      const blocked = countStatuses(rows, ["blocked"]);
      const completed = countStatuses(rows, ["completed"]);
      const nonConformant = rows.filter((row) => row.result === "non_conformant").length;
      const openEvidence = rows.filter((row) => row.status === "completed" && !row.evidence_reference && !row.finding_summary).length;
      return [
        { label: "Blocked", value: blocked, helper: "Checklist items needing escalation or access" },
        { label: "Completed", value: completed, helper: "Audit checks already executed" },
        { label: "Non-conformant", value: nonConformant, helper: "Checks that produced a non-conformant result" },
        { label: "Evidence gap", value: openEvidence, helper: "Completed checks missing evidence or finding notes" },
      ];
    }
    case "finding": {
      const severe = rows.filter((row) => ["high", "critical"].includes(row.severity)).length;
      const dueSoon = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? 999) >= 0 && (daysUntil(row.due_date) ?? 999) <= 14).length;
      const open = rows.filter((row) => !["resolved", "closed"].includes(row.status)).length;
      const closed = countStatuses(rows, ["resolved", "closed"]);
      return [
        { label: "High severity", value: severe, helper: "Findings requiring executive attention" },
        { label: "Due in 14 days", value: dueSoon, helper: "Findings close to their target closure date" },
        { label: "Open", value: open, helper: "Findings still requiring remediation work" },
        { label: "Closed", value: closed, helper: "Findings already resolved or formally closed" },
      ];
    }
    case "non-conformity": {
      const open = rows.filter((row) => !["resolved", "closed"].includes(row.status)).length;
      const remediating = countStatuses(rows, ["remediating"]);
      const accepted = countStatuses(rows, ["accepted"]);
      const overdue = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? -999) < 0 && !["resolved", "closed"].includes(row.status)).length;
      return [
        { label: "Open", value: open, helper: "Non-conformities still in the remediation cycle" },
        { label: "Remediating", value: remediating, helper: "Non-conformities under active correction" },
        { label: "Accepted", value: accepted, helper: "Exceptions formally accepted" },
        { label: "Overdue", value: overdue, helper: "Non-conformities already past the target date" },
      ];
    }
    case "corrective-action": {
      const overdue = rows.filter((row) => row.due_date && (daysUntil(row.due_date) ?? -999) < 0 && !["completed", "archived"].includes(row.status)).length;
      const blocked = rows.filter((row) => row.blocker_summary).length;
      const inProgress = countStatuses(rows, ["in_progress"]);
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Overdue", value: overdue, helper: "Corrective actions past due" },
        { label: "Blocked", value: blocked, helper: "Actions with an active blocker summary" },
        { label: "In progress", value: inProgress, helper: "Actions actively being delivered" },
        { label: "Completed", value: completed, helper: "Actions already closed and evidenced" },
      ];
    }
    default:
      return [];
  }
}

function buildHighlights(config, rows) {
  switch (config.reportPreset) {
    case "mapping":
      return rows
        .filter((row) => ["planned", "in_progress"].includes(row.mapping_status) || ["high", "critical"].includes(row.vulnerability_level))
        .slice(0, 5)
        .map((row) => ({
          title: row.name || row.code,
          meta: joinMeta([row.mapping_status, row.criticality_level, row.vulnerability_level]),
        }));
    case "risk":
      return rows
        .filter((row) => ["high", "critical"].includes(row.risk_level) || row.response_deadline)
        .sort((left, right) => String(left.response_deadline || "9999-12-31").localeCompare(String(right.response_deadline || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.risk_level, row.treatment_status, row.response_deadline]),
        }));
    case "asset-inventory":
      return rows
        .filter((row) => row.criticality_level || row.status)
        .slice(0, 5)
        .map((row) => ({
          title: row.name,
          meta: joinMeta([row.asset_type, row.criticality_level, row.status, row.related_infrastructure_name || row.sector]),
        }));
    case "threat":
      return rows
        .filter((row) => row.severity || row.last_seen_at || row.first_seen_at)
        .sort((left, right) => String(left.last_seen_at || left.first_seen_at || "9999-12-31").localeCompare(String(right.last_seen_at || right.first_seen_at || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.threat_type, row.severity, row.status, row.last_seen_at || row.first_seen_at]),
        }));
    case "vulnerability":
      return rows
        .filter((row) => row.remediation_due_date || row.severity)
        .sort((left, right) => String(left.remediation_due_date || "9999-12-31").localeCompare(String(right.remediation_due_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.vulnerability_type, row.severity, row.status, row.remediation_due_date]),
        }));
    case "risk-scenario":
      return rows
        .filter((row) => row.review_due_date || row.risk_level)
        .sort((left, right) => String(left.review_due_date || "9999-12-31").localeCompare(String(right.review_due_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.risk_level, row.treatment_status, row.review_due_date, row.scenario_owner]),
        }));
    case "risk-review":
      return rows
        .filter((row) => row.follow_up_date || row.review_date || row.decision)
        .sort((left, right) => String(left.follow_up_date || left.review_date || "9999-12-31").localeCompare(String(right.follow_up_date || right.review_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.decision, row.residual_risk_level, row.follow_up_date || row.review_date]),
        }));
    case "bulletin":
      return rows
        .filter((row) => row.valid_until || row.issued_on || row.severity)
        .sort((left, right) => String(left.valid_until || left.issued_on || "9999-12-31").localeCompare(String(right.valid_until || right.issued_on || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.bulletin_type, row.severity, row.status, row.valid_until || row.issued_on]),
        }));
    case "indicator":
      return rows
        .filter((row) => row.last_seen_at || row.first_seen_at || row.status)
        .sort((left, right) => String(left.last_seen_at || left.first_seen_at || "9999-12-31").localeCompare(String(right.last_seen_at || right.first_seen_at || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.indicator_type, row.status, row.value, row.last_seen_at || row.first_seen_at]),
        }));
    case "distribution-group":
      return rows
        .filter((row) => row.status || row.group_type)
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.group_type, row.target_sector, row.status, Array.isArray(row.stakeholder_names) ? `${row.stakeholder_names.length} members` : ""]),
        }));
    case "information-share":
      return rows
        .filter((row) => row.acknowledgement_due_date || row.shared_at || row.status)
        .sort((left, right) => String(left.acknowledgement_due_date || left.shared_at || "9999-12-31").localeCompare(String(right.acknowledgement_due_date || right.shared_at || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.share_channel, row.status, row.target_stakeholder_name || row.distribution_group_title, row.acknowledgement_due_date || row.shared_at]),
        }));
    case "acknowledgement":
      return rows
        .filter((row) => row.status || row.responded_at)
        .sort((left, right) => String(left.responded_at || "9999-12-31").localeCompare(String(right.responded_at || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.stakeholder_name || row.information_share_title || "Acknowledgement",
          meta: joinMeta([row.status, row.information_share_title, row.responded_at]),
        }));
    case "generated-document":
      return rows
        .filter((row) => row.generated_on || row.status)
        .sort((left, right) => String(right.generated_on || "0000-01-01").localeCompare(String(left.generated_on || "0000-01-01")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.module_label, row.document_type, row.version_label, row.status, row.generated_on]),
        }));
    case "review-cycle":
      return rows
        .filter((row) => row.next_review_date || row.status)
        .sort((left, right) => String(left.next_review_date || "9999-12-31").localeCompare(String(right.next_review_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.module_label, row.current_version_label, row.status, row.next_review_date]),
        }));
    case "review-record":
      return rows
        .filter((row) => row.review_date || row.decision)
        .sort((left, right) => String(right.review_date || "0000-01-01").localeCompare(String(left.review_date || "0000-01-01")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.decision, row.status, row.version_label, row.review_date]),
        }));
    case "change-log":
      return rows
        .filter((row) => row.changed_on || row.change_type)
        .sort((left, right) => String(right.changed_on || "0000-01-01").localeCompare(String(left.changed_on || "0000-01-01")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.change_type, row.version_label, row.changed_by_name, row.changed_on]),
        }));
    case "desk-study":
      return rows
        .filter((row) => row.due_date || row.priority)
        .sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.source_type, row.priority, row.due_date]),
        }));
    case "consultation":
      return rows
        .filter((row) => row.start_datetime || row.planned_date || row.next_follow_up_date)
        .sort((left, right) => String(left.start_datetime || left.next_follow_up_date || left.planned_date || "9999-12-31").localeCompare(String(right.start_datetime || right.next_follow_up_date || right.planned_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.consultation_type, row.engagement_channel, row.status, row.start_datetime || row.next_follow_up_date || row.planned_date]),
        }));
    case "capacity":
      return rows
        .filter((row) => row.due_date || row.gap_level)
        .sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.assessment_area, row.gap_level, row.due_date]),
        }));
    case "delivery":
      return rows
        .filter((row) => row.due_date)
        .sort((left, right) => String(left.due_date).localeCompare(String(right.due_date)))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.phase, row.status, row.due_date]),
        }));
    case "exercise":
      return rows
        .filter((row) => row.planned_date || row.completed_date)
        .sort((left, right) => String(left.planned_date || left.completed_date || "9999-12-31").localeCompare(String(right.planned_date || right.completed_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.exercise_type, row.status, row.planned_date || row.completed_date]),
        }));
    case "review":
      return rows
        .filter((row) => row.next_review_date)
        .sort((left, right) => String(left.next_review_date).localeCompare(String(right.next_review_date)))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.status, row.next_review_date]),
        }));
    case "training":
      return rows
        .filter((row) => row.participant_target || row.status)
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.program_type, row.status, row.participant_target ? `${row.participant_target} participants` : ""]),
        }));
    case "incident":
      return rows
        .filter((row) => row.next_update_due || row.reported_at || row.severity)
        .sort((left, right) => String(left.next_update_due || left.reported_at || "9999-12-31").localeCompare(String(right.next_update_due || right.reported_at || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.severity, row.status, row.incident_coordinator_name, row.next_update_due || row.reported_at]),
        }));
    case "incident-task":
      return rows
        .filter((row) => row.due_at || row.blocker_summary || row.priority)
        .sort((left, right) => String(left.due_at || "9999-12-31").localeCompare(String(right.due_at || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.incident_title, row.priority, row.status, row.due_at, row.blocker_summary ? "Blocked" : ""]),
        }));
    case "action-plan":
      return rows
        .filter((row) => row.due_date || row.blocker_summary)
        .sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.priority, row.status, row.blocker_summary ? "Blocked" : "", row.due_date]),
        }));
    case "sop-execution":
      return rows
        .filter((row) => row.target_completion_at || row.blocker_summary || row.next_action)
        .sort((left, right) => String(left.target_completion_at || left.started_at || "9999-12-31").localeCompare(String(right.target_completion_at || right.started_at || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.incident_title, row.status, row.execution_commander_name, row.target_completion_at || row.started_at]),
        }));
    case "allocation":
      return rows
        .filter((row) => row.requested_at || row.deployed_at || row.status)
        .sort((left, right) => String(left.requested_at || left.deployed_at || "9999-12-31").localeCompare(String(right.requested_at || right.deployed_at || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.status, row.priority, row.emergency_asset_name, row.destination_infrastructure_name || row.destination, row.requested_at || row.deployed_at]),
        }));
    case "conformity":
      return rows
        .filter((row) => row.next_review_date || row.conformity_level)
        .sort((left, right) => String(left.next_review_date || left.assessed_on || "9999-12-31").localeCompare(String(right.next_review_date || right.assessed_on || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.related_standard_title, row.conformity_level, row.status, row.next_review_date || row.assessed_on]),
        }));
    case "evidence":
      return rows
        .filter((row) => row.validity_until || row.status)
        .sort((left, right) => String(left.validity_until || left.captured_on || "9999-12-31").localeCompare(String(right.validity_until || right.captured_on || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.evidence_type, row.status, row.related_control_title, row.validity_until || row.captured_on]),
        }));
    case "audit-plan":
      return rows
        .filter((row) => row.planned_start_date || row.planned_end_date || row.status)
        .sort((left, right) => String(left.planned_start_date || left.planned_end_date || "9999-12-31").localeCompare(String(right.planned_start_date || right.planned_end_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.related_framework_title, row.status, row.lead_auditor, row.planned_start_date || row.planned_end_date]),
        }));
    case "audit-checklist":
      return rows
        .filter((row) => row.status || row.result)
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.audit_plan_title, row.status, row.result, row.item_order ? `Item ${row.item_order}` : ""]),
        }));
    case "finding":
      return rows
        .filter((row) => row.due_date || row.severity)
        .sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.audit_plan_title, row.severity, row.status, row.due_date]),
        }));
    case "non-conformity":
      return rows
        .filter((row) => row.due_date || row.status)
        .sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.audit_finding_title, row.severity, row.status, row.due_date]),
        }));
    case "corrective-action":
      return rows
        .filter((row) => row.due_date || row.blocker_summary)
        .sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.priority, row.status, row.blocker_summary ? "Blocked" : "", row.due_date]),
        }));
    default:
      return [];
  }
}

function sortRows(config, rows) {
  switch (config.reportPreset) {
    case "mapping":
      return [...rows].sort((left, right) => String(left.mapping_status || "").localeCompare(String(right.mapping_status || "")));
    case "risk":
      return [...rows].sort((left, right) => String(left.response_deadline || "9999-12-31").localeCompare(String(right.response_deadline || "9999-12-31")));
    case "asset-inventory":
      return [...rows].sort((left, right) => String(left.name || "").localeCompare(String(right.name || "")));
    case "threat":
      return [...rows].sort((left, right) => String(left.last_seen_at || left.first_seen_at || "9999-12-31").localeCompare(String(right.last_seen_at || right.first_seen_at || "9999-12-31")));
    case "vulnerability":
      return [...rows].sort((left, right) => String(left.remediation_due_date || "9999-12-31").localeCompare(String(right.remediation_due_date || "9999-12-31")));
    case "risk-scenario":
      return [...rows].sort((left, right) => String(left.review_due_date || "9999-12-31").localeCompare(String(right.review_due_date || "9999-12-31")));
    case "risk-review":
      return [...rows].sort((left, right) => String(left.follow_up_date || left.review_date || "9999-12-31").localeCompare(String(right.follow_up_date || right.review_date || "9999-12-31")));
    case "bulletin":
      return [...rows].sort((left, right) => String(left.valid_until || left.issued_on || "9999-12-31").localeCompare(String(right.valid_until || right.issued_on || "9999-12-31")));
    case "indicator":
      return [...rows].sort((left, right) => String(left.last_seen_at || left.first_seen_at || "9999-12-31").localeCompare(String(right.last_seen_at || right.first_seen_at || "9999-12-31")));
    case "distribution-group":
      return [...rows].sort((left, right) => String(left.title || "").localeCompare(String(right.title || "")));
    case "information-share":
      return [...rows].sort((left, right) => String(left.acknowledgement_due_date || left.shared_at || "9999-12-31").localeCompare(String(right.acknowledgement_due_date || right.shared_at || "9999-12-31")));
    case "acknowledgement":
      return [...rows].sort((left, right) => String(left.responded_at || "9999-12-31").localeCompare(String(right.responded_at || "9999-12-31")));
    case "generated-document":
      return [...rows].sort((left, right) => String(right.generated_on || "0000-01-01").localeCompare(String(left.generated_on || "0000-01-01")));
    case "review-cycle":
      return [...rows].sort((left, right) => String(left.next_review_date || "9999-12-31").localeCompare(String(right.next_review_date || "9999-12-31")));
    case "review-record":
      return [...rows].sort((left, right) => String(right.review_date || "0000-01-01").localeCompare(String(left.review_date || "0000-01-01")));
    case "change-log":
      return [...rows].sort((left, right) => String(right.changed_on || "0000-01-01").localeCompare(String(left.changed_on || "0000-01-01")));
    case "desk-study":
      return [...rows].sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")));
    case "consultation":
      return [...rows].sort((left, right) => String(left.start_datetime || left.next_follow_up_date || left.planned_date || "9999-12-31").localeCompare(String(right.start_datetime || right.next_follow_up_date || right.planned_date || "9999-12-31")));
    case "capacity":
      return [...rows].sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")));
    case "delivery":
    case "incident":
      return [...rows].sort((left, right) => String(left.next_update_due || left.reported_at || "9999-12-31").localeCompare(String(right.next_update_due || right.reported_at || "9999-12-31")));
    case "incident-task":
      return [...rows].sort((left, right) => String(left.due_at || "9999-12-31").localeCompare(String(right.due_at || "9999-12-31")));
    case "action-plan":
      return [...rows].sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")));
    case "sop-execution":
      return [...rows].sort((left, right) => String(left.target_completion_at || left.started_at || "9999-12-31").localeCompare(String(right.target_completion_at || right.started_at || "9999-12-31")));
    case "allocation":
      return [...rows].sort((left, right) => String(left.requested_at || left.deployed_at || "9999-12-31").localeCompare(String(right.requested_at || right.deployed_at || "9999-12-31")));
    case "conformity":
      return [...rows].sort((left, right) => String(left.next_review_date || left.assessed_on || "9999-12-31").localeCompare(String(right.next_review_date || right.assessed_on || "9999-12-31")));
    case "evidence":
      return [...rows].sort((left, right) => String(left.validity_until || left.captured_on || "9999-12-31").localeCompare(String(right.validity_until || right.captured_on || "9999-12-31")));
    case "audit-plan":
      return [...rows].sort((left, right) => String(left.planned_start_date || left.planned_end_date || "9999-12-31").localeCompare(String(right.planned_start_date || right.planned_end_date || "9999-12-31")));
    case "audit-checklist":
      return [...rows].sort((left, right) => Number(left.item_order || 9999) - Number(right.item_order || 9999));
    case "finding":
    case "non-conformity":
    case "corrective-action":
      return [...rows].sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")));
    case "exercise":
      return [...rows].sort((left, right) => String(left.planned_date || "9999-12-31").localeCompare(String(right.planned_date || "9999-12-31")));
    case "review":
      return [...rows].sort((left, right) => String(left.next_review_date || "9999-12-31").localeCompare(String(right.next_review_date || "9999-12-31")));
    default:
      return rows;
  }
}

export default function OperationalReportView({
  config,
  rows = [],
  columns = [],
  onGenerateDocument = null,
  isGeneratingDocument = false,
  documentFormat = "pdf",
  onDocumentFormatChange = null,
  rowActions = null,
}) {
  if (!rows.length) {
    return <EmptyState title="No report rows" description="There is no data available for this operational report." />;
  }

  const summary = buildSummary(config, rows);
  const highlights = buildHighlights(config, rows);
  const orderedRows = sortRows(config, rows);

  return (
    <section className="space-y-6">
      {summary.length ? (
        <div className="grid gap-3 md:grid-cols-3">
          {summary.map((item, index) => (
            <article key={item.label} className="app-surface rounded-[20px] px-5 py-5">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-[11px] font-semibold text-[#554d46]">{item.label}</p>
                  <p className="mt-3 text-[2rem] font-semibold tracking-[-0.05em] text-slate-950">{item.value}</p>
                </div>
                <span className={`h-3.5 w-3.5 rounded-full ${["bg-[#ffd3b2]", "bg-[#93e1a4]", "bg-[#b8abff]"][index % 3]}`} />
              </div>
              <p className="mt-2 text-[12px] leading-5 text-[#5e5650]">{item.helper}</p>
            </article>
          ))}
        </div>
      ) : null}

      <div className="flex flex-col gap-6 xl:flex-row xl:items-start">
        <div className="app-surface rounded-[22px] p-5 xl:w-[23.5rem] xl:max-w-[23.5rem] xl:flex-none">
          <h3 className="text-sm font-semibold text-[#554d46]">Attention queue</h3>
          <div className="mt-4 space-y-2 pr-5">
            {highlights.length ? (
              highlights.map((item) => (
                <article key={`${item.title}-${item.meta}`} className="rounded-[16px] bg-white/82 px-4 py-4">
                  <p className="text-sm font-semibold text-slate-900">{item.title}</p>
                  <p className="mt-1 text-xs text-[#5e5650]">{item.meta}</p>
                </article>
              ))
            ) : (
              <div className="rounded-[16px] bg-white/58 px-4 py-8 text-center text-sm text-[#5e5650]">No highlighted items for this report.</div>
            )}
          </div>
        </div>

        <div className="app-surface min-w-0 flex-1 rounded-[22px] p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h3 className="text-sm font-semibold text-[#554d46]">Detailed report</h3>
            {onGenerateDocument ? (
              <div className="flex flex-wrap items-center gap-2">
                <MenuSelect
                  value={documentFormat}
                  onChange={(nextValue) => onDocumentFormatChange?.(nextValue)}
                  ariaLabel="Select export format"
                  options={[
                    { value: "pdf", label: "PDF" },
                    { value: "docx", label: "DOCX" },
                    { value: "markdown", label: "Markdown" },
                    { value: "text", label: "Plain text" },
                    { value: "json", label: "JSON" },
                  ]}
                  triggerClassName="min-w-[8.75rem] shadow-[inset_0_0_0_1px_rgba(17,17,17,0.08)]"
                  menuClassName="min-w-[8.75rem]"
                />
                <button
                  type="button"
                  onClick={onGenerateDocument}
                  disabled={isGeneratingDocument}
                  className="inline-flex h-9 items-center rounded-full bg-[#111111] px-4 text-[11px] font-semibold text-white transition hover:bg-black/84 disabled:cursor-wait disabled:opacity-65"
                >
                  {isGeneratingDocument ? "Generating..." : `Generate ${String(documentFormat).toUpperCase()}`}
                </button>
              </div>
            ) : null}
          </div>
          <div className="mt-4">
            <DataTable columns={columns} rows={orderedRows} variant="report" rowActions={rowActions} />
          </div>
        </div>
      </div>
    </section>
  );
}
