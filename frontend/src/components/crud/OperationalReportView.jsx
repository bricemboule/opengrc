import DataTable from "./DataTable";
import EmptyState from "./EmptyState";

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
      const upcoming = rows.filter((row) => row.planned_date && (daysUntil(row.planned_date) ?? 999) >= 0 && (daysUntil(row.planned_date) ?? 999) <= 30).length;
      const followUps = rows.filter((row) => row.next_follow_up_date && (daysUntil(row.next_follow_up_date) ?? 999) <= 14).length;
      const completed = countStatuses(rows, ["completed"]);
      return [
        { label: "Upcoming", value: upcoming, helper: "Consultations planned in the next 30 days" },
        { label: "Follow-up due", value: followUps, helper: "Sessions needing a next action now" },
        { label: "Completed", value: completed, helper: "Sessions with a closed delivery loop" },
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
        .filter((row) => row.planned_date || row.next_follow_up_date)
        .sort((left, right) => String(left.next_follow_up_date || left.planned_date || "9999-12-31").localeCompare(String(right.next_follow_up_date || right.planned_date || "9999-12-31")))
        .slice(0, 5)
        .map((row) => ({
          title: row.title,
          meta: joinMeta([row.consultation_type, row.status, row.next_follow_up_date || row.planned_date]),
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
    case "action-plan":
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
    case "desk-study":
      return [...rows].sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")));
    case "consultation":
      return [...rows].sort((left, right) => String(left.next_follow_up_date || left.planned_date || "9999-12-31").localeCompare(String(right.next_follow_up_date || right.planned_date || "9999-12-31")));
    case "capacity":
      return [...rows].sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")));
    case "delivery":
    case "action-plan":
      return [...rows].sort((left, right) => String(left.due_date || "9999-12-31").localeCompare(String(right.due_date || "9999-12-31")));
    case "exercise":
      return [...rows].sort((left, right) => String(left.planned_date || "9999-12-31").localeCompare(String(right.planned_date || "9999-12-31")));
    case "review":
      return [...rows].sort((left, right) => String(left.next_review_date || "9999-12-31").localeCompare(String(right.next_review_date || "9999-12-31")));
    default:
      return rows;
  }
}

export default function OperationalReportView({ config, rows = [], columns = [] }) {
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
          <h3 className="text-sm font-semibold text-[#554d46]">Detailed report</h3>
          <div className="mt-4">
            <DataTable columns={columns} rows={orderedRows} variant="report" />
          </div>
        </div>
      </div>
    </section>
  );
}

