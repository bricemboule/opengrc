import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useSelector } from "react-redux";
import api from "../api/client";
import PageHeader from "../components/crud/PageHeader";
import EmptyState from "../components/crud/EmptyState";
import MapView from "../components/crud/MapView";
import BarChartCard from "../components/dashboard/BarChartCard";

const EMPTY_DASHBOARD = {
  charts: [],
  deliverables_by_phase: [],
  critical_risks: [],
  due_deliverables: [],
  review_queue: [],
  desk_study_queue: [],
  consultation_queue: [],
  capacity_queue: [],
  action_plan_queue: [],
  workflow_summary: [],
  attention_items: [],
  priority_distribution: [],
  map_points: [],
  upcoming_exercises: [],
  mapping_coverage: 0,
  mapped_infrastructure: 0,
  high_risks: 0,
  reviews_due: 0,
  overdue_deliverables: 0,
  blocked_actions: 0,
  capacity_due: 0,
  pending_consultations: 0,
  open_desk_studies: 0,
};

const METRIC_TONES = ["bg-[#ffd3b2]", "bg-[#93e1a4]", "bg-[#b8abff]", "bg-[#f0be7c]"];
const LIST_TONES = ["bg-[#ffd3b2]", "bg-[#93e1a4]", "bg-[#b8abff]", "bg-[#f0be7c]"];
const DONUT_COLORS = ["#ffd3b2", "#93e1a4", "#b8abff", "#f0be7c", "#8eb2ff"];

function formatDate(value) {
  if (!value) return "No date";
  return new Date(value).toLocaleDateString();
}

function formatDateTime(value) {
  if (!value) return "No timestamp";
  return new Date(value).toLocaleString();
}

function formatWorkflowLabel(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .toLowerCase()
    .replace(/(^|\s)\w/g, (character) => character.toUpperCase());
}

function MetricStrip({ label, value, helper, tone }) {
  return (
    <article className="app-surface rounded-[20px] px-5 py-5">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-[10px] font-semibold tracking-[0.04em] text-[#5e5650]">{label}</p>
          <p className="mt-3 text-[2rem] font-semibold tracking-[-0.05em] text-slate-950">{value}</p>
        </div>
        <span className={`h-3.5 w-3.5 rounded-full ${tone}`} />
      </div>
      <p className="mt-2 text-[13px] leading-6 text-[#5e5650]">{helper}</p>
    </article>
  );
}

function QueueList({ title, subtitle, items, renderMeta, emptyTitle = "No items", emptyDescription = "There is nothing to display yet." }) {
  return (
    <section className="app-surface rounded-[16px] p-5">
      <div>
        <h3 className="text-xl font-semibold tracking-[-0.04em] text-slate-950">{title}</h3>
        {subtitle ? <p className="mt-1 text-[13px] leading-6 text-[#5e5650]">{subtitle}</p> : null}
      </div>

      <div className="mt-4 space-y-2">
        {items.length ? (
          items.map((item, index) => {
            const heading = item.title || item.name || item.message || `Item ${index + 1}`;
            return (
              <article key={`${title}-${item.id || heading}-${index}`} className="rounded-[12px] bg-white/82 px-4 py-4">
                <div className="flex items-start gap-3">
                  <span className={`mt-1 h-2.5 w-2.5 shrink-0 rounded-full ${LIST_TONES[index % LIST_TONES.length]}`} />
                  <div>
                    <p className="text-sm font-semibold text-slate-900">{heading}</p>
                    <p className="mt-1 text-xs leading-6 text-[#5e5650]">{renderMeta(item)}</p>
                  </div>
                </div>
              </article>
            );
          })
        ) : (
          <EmptyState title={emptyTitle} description={emptyDescription} />
        )}
      </div>
    </section>
  );
}

function WorkflowMatrix({ items }) {
  if (!items.length) {
    return <EmptyState title="No workflow summary" description="Workflow status counts will appear once cyber GRC records exist." />;
  }

  return (
    <section className="app-surface rounded-[24px] p-5 sm:p-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h3 className="text-[1.7rem] font-semibold tracking-[-0.05em] text-slate-950">Operational matrix</h3>
          <p className="mt-1 max-w-2xl text-[13px] leading-6 text-[#5e5650]">
            Scan workflow volume, dominant status, and next action the same way you would review a live delivery board.
          </p>
        </div>
        <span className="app-button app-button-dark app-button-sm">Workflow pulse</span>
      </div>

      <div className="app-scroll mt-5 overflow-x-auto">
        <table className="w-full min-w-[760px] border-separate border-spacing-y-2 text-sm">
          <thead>
            <tr className="text-left text-[12px] tracking-[0.04em] text-[#5e5650]">
              {["Workflow", "Focus", "Volume", "Status split", "Open"].map((label, index) => (
                <th key={label} className={`bg-white/56 px-4 py-3 font-semibold ${index === 0 ? "rounded-l-[12px]" : ""} ${index === 4 ? "rounded-r-[12px] text-left" : ""}`}>
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {items.map((item) => {
              const sortedStatuses = item.statuses.filter((statusItem) => statusItem.total > 0).sort((left, right) => right.total - left.total);
              const focusStatus = sortedStatuses[0];
              const previewStatuses = sortedStatuses.slice(0, 3);
              return (
                <tr key={item.name}>
                  <td className="rounded-l-[14px] bg-white/82 px-4 py-4 align-top">
                    <p className="text-sm font-semibold text-slate-900">{item.name}</p>
                    <p className="mt-1 text-xs text-[#5e5650]">Operational module</p>
                  </td>
                  <td className="bg-white/82 px-4 py-4 align-top text-sm text-[#5e5650]">
                    {focusStatus ? `${formatWorkflowLabel(focusStatus.label)}: ${focusStatus.total}` : "No active states"}
                  </td>
                  <td className="bg-white/82 px-4 py-4 align-top text-sm font-semibold text-slate-900">{item.total}</td>
                  <td className="bg-white/82 px-4 py-4 align-top">
                    <div className="flex flex-wrap gap-2">
                      {previewStatuses.length ? (
                        previewStatuses.map((statusItem, index) => (
                          <span key={`${item.name}-${statusItem.value}`} className={`rounded-full px-3 py-1 text-xs font-medium text-[#5e5650] ${index === 0 ? "bg-[#fff1e8]" : index === 1 ? "bg-[#ecf9ef]" : "bg-[#efebff]"}`}>
                            {formatWorkflowLabel(statusItem.label)}: {statusItem.total}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-slate-400">No status data</span>
                      )}
                    </div>
                  </td>
                  <td className="rounded-r-[14px] bg-white/82 px-4 py-4 align-top text-left">
                    <div className="flex justify-start">
                      <a href={`/modules/${item.route}?mode=workflow`} className="app-button app-button-dark app-button-sm">
                        Open workflow
                      </a>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function buildDonutBackground(items) {
  const total = items.reduce((sum, item) => sum + item.total, 0);
  if (!total) return "conic-gradient(#ede9e2 0deg 360deg)";

  let progress = 0;
  const segments = items.map((item, index) => {
    const start = (progress / total) * 360;
    progress += item.total;
    const end = (progress / total) * 360;
    return `${DONUT_COLORS[index % DONUT_COLORS.length]} ${start}deg ${end}deg`;
  });

  return `conic-gradient(${segments.join(", ")})`;
}

function DistributionDonut({ items }) {
  const visibleItems = items.slice(0, 5);
  const total = visibleItems.reduce((sum, item) => sum + item.total, 0);

  return (
    <section className="app-surface rounded-[24px] p-5 sm:p-6">
      <div>
        <h3 className="text-[1.5rem] font-semibold tracking-[-0.05em] text-slate-950">Priority mix</h3>
        <p className="mt-1 text-[13px] leading-6 text-[#5e5650]">A pastel breakdown of the active risk profile across the workspace.</p>
      </div>

      {visibleItems.length ? (
        <div className="mt-6 grid gap-6 lg:grid-cols-[0.82fr_1.18fr] lg:items-center">
          <div className="space-y-3">
            {visibleItems.map((item, index) => (
              <div key={`${item.label}-${index}`} className="flex items-center gap-3 rounded-[14px] bg-white/82 px-4 py-3">
                <span className="h-3 w-3 rounded-full" style={{ backgroundColor: DONUT_COLORS[index % DONUT_COLORS.length] }} />
                <div className="flex-1">
                  <p className="text-sm font-medium text-[#5e5650]">{item.label}</p>
                </div>
                <span className="text-sm font-semibold text-slate-900">{item.total}</span>
              </div>
            ))}
          </div>

          <div className="mx-auto grid h-[250px] w-[250px] place-items-center rounded-full" style={{ background: buildDonutBackground(visibleItems) }}>
            <div className="grid h-[138px] w-[138px] place-items-center rounded-full bg-white/92 text-center">
              <p className="text-[1.8rem] font-semibold tracking-[-0.05em] text-slate-950">{total}</p>
              <p className="text-[10px] font-semibold tracking-[0.04em] text-[#5e5650]">Tracked levels</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="mt-6">
          <EmptyState title="No risk distribution" description="Risk level counts will appear once risk register entries are added." />
        </div>
      )}
    </section>
  );
}

export default function DashboardPage() {
  const notifications = useSelector((state) => state.notifications.items);
  const { data, isLoading, isError } = useQuery({
    queryKey: ["cybergrc-overview"],
    queryFn: async () => (await api.get("/cybergrc/overview/")).data,
    placeholderData: EMPTY_DASHBOARD,
  });

  const dashboard = data ?? EMPTY_DASHBOARD;
  const workflowSummary = dashboard.workflow_summary || [];
  const priorityDistribution = useMemo(() => (dashboard.priority_distribution || []).filter((item) => item.total > 0), [dashboard.priority_distribution]);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Cyber GRC Operations Hub"
        description="Track mapping coverage, treatment workflows, document analysis, capacity gaps, consultations, action plans, and realtime coordination alerts in one place."
      />

      {isLoading ? <p className="text-sm text-slate-500">Loading the cyber GRC operational overview...</p> : null}
      {isError ? <p className="rounded-[24px] bg-[#fff1ef] px-4 py-3 text-sm text-[#a63d34]">Unable to load the cyber GRC operational overview.</p> : null}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricStrip label="Mapping coverage" value={`${dashboard.mapping_coverage || 0}%`} helper={`${dashboard.mapped_infrastructure || 0} mapped infrastructure records`} tone={METRIC_TONES[0]} />
        <MetricStrip label="High risks" value={dashboard.high_risks || 0} helper="High and critical risks needing treatment" tone={METRIC_TONES[1]} />
        <MetricStrip label="Blocked actions" value={dashboard.blocked_actions || 0} helper="Action tasks currently carrying blockers" tone={METRIC_TONES[2]} />
        <MetricStrip label="Reviews due" value={dashboard.reviews_due || 0} helper="Governance, standards, audits, and plans due now" tone={METRIC_TONES[3]} />
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricStrip label="Overdue deliverables" value={dashboard.overdue_deliverables || 0} helper="Active milestones already past due" tone={METRIC_TONES[0]} />
        <MetricStrip label="Desk studies open" value={dashboard.open_desk_studies || 0} helper="Document reviews still in the active queue" tone={METRIC_TONES[1]} />
        <MetricStrip label="Capacity due" value={dashboard.capacity_due || 0} helper="Assessments already due for delivery attention" tone={METRIC_TONES[2]} />
        <MetricStrip label="Pending consultations" value={dashboard.pending_consultations || 0} helper="Stakeholder sessions and follow-ups still open" tone={METRIC_TONES[3]} />
      </div>

      <div className="grid gap-6">
        <WorkflowMatrix items={workflowSummary} />
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.82fr_1.18fr]">
        <DistributionDonut items={priorityDistribution} />
        <BarChartCard title="Operational load" data={dashboard.charts || []} dataKey="total" xKey="name" />
      </div>

      <div className="grid gap-6">
        <BarChartCard title="Delivery by phase" data={dashboard.deliverables_by_phase || []} dataKey="total" xKey="name" />
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <QueueList
          title="Coordination alerts"
          subtitle="Recent realtime notifications from cyber GRC workflows."
          items={notifications.slice(0, 6)}
          renderMeta={(item) => formatDateTime(item.receivedAt)}
          emptyTitle="No realtime alerts"
          emptyDescription="Workflow and deadline notifications will appear here after record updates."
        />
        <QueueList
          title="Critical risks"
          subtitle="Entries needing the fastest response and executive attention."
          items={dashboard.critical_risks || []}
          renderMeta={(item) => [item.risk_level, item.infrastructure_name, item.response_deadline ? `Due ${formatDate(item.response_deadline)}` : "No response date"].filter(Boolean).join(" | ")}
          emptyTitle="No critical risks"
          emptyDescription="Critical risk entries will appear here once the register is populated."
        />
        <QueueList
          title="Attention queue"
          subtitle="Items with imminent dates, escalations, or unresolved workflow pressure."
          items={dashboard.attention_items || []}
          renderMeta={(item) => [item.type, item.context, item.due_date ? `Due ${formatDate(item.due_date)}` : item.severity].filter(Boolean).join(" | ")}
          emptyTitle="No attention items"
          emptyDescription="Attention items will surface once deadlines and review loops start moving."
        />
      </div>

      <div className="grid gap-6">
        <MapView
          title="CII mapping view"
          description="Infrastructure records with geographic coordinates to support mapping, cross-sector visibility, and dashboard-ready raw data."
          rows={dashboard.map_points || []}
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <QueueList
          title="Due deliverables"
          subtitle="Milestones and outputs that need follow-up now."
          items={dashboard.due_deliverables || []}
          renderMeta={(item) => [item.phase, item.status, item.due_date ? formatDate(item.due_date) : "No due date"].filter(Boolean).join(" | ")}
          emptyTitle="No due deliverables"
          emptyDescription="Upcoming milestone pressure will appear here once deliverables exist."
        />
        <QueueList
          title="Review queue"
          subtitle="Reviews and validations that should be scheduled or completed."
          items={dashboard.review_queue || []}
          renderMeta={(item) => [item.type, item.status, item.next_review_date ? formatDate(item.next_review_date) : "No review date"].filter(Boolean).join(" | ")}
          emptyTitle="No review queue"
          emptyDescription="Review dates and validation steps will appear here once records are created."
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <QueueList
          title="Desk study backlog"
          subtitle="Document analysis items that still need gap extraction or delivery follow-through."
          items={dashboard.desk_study_queue || []}
          renderMeta={(item) => [item.source_type, item.priority, item.due_date ? formatDate(item.due_date) : item.status].filter(Boolean).join(" | ")}
          emptyTitle="No desk study items"
          emptyDescription="Desk study activity will appear here once reviews are added."
        />
        <QueueList
          title="Capacity queue"
          subtitle="Readiness assessments that should feed into strengthening actions."
          items={dashboard.capacity_queue || []}
          renderMeta={(item) => [item.assessment_area, item.gap_level, item.due_date ? formatDate(item.due_date) : item.status].filter(Boolean).join(" | ")}
          emptyTitle="No capacity assessments"
          emptyDescription="Capacity analysis activity will appear here once assessments are created."
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <QueueList
          title="Consultation queue"
          subtitle="Upcoming sessions and follow-ups that should stay visible to the coordination team."
          items={dashboard.consultation_queue || []}
          renderMeta={(item) => [item.consultation_type, item.status, item.next_follow_up_date ? `Follow-up ${formatDate(item.next_follow_up_date)}` : item.planned_date ? formatDate(item.planned_date) : "No date"].filter(Boolean).join(" | ")}
          emptyTitle="No consultations"
          emptyDescription="Stakeholder consultation activity will appear here once sessions are scheduled."
        />
        <QueueList
          title="Action plan queue"
          subtitle="Tasks that convert gaps, findings, and decisions into tracked execution."
          items={dashboard.action_plan_queue || []}
          renderMeta={(item) => [item.priority, item.blocked ? "Blocked" : item.status, item.due_date ? formatDate(item.due_date) : "No due date"].filter(Boolean).join(" | ")}
          emptyTitle="No action plan tasks"
          emptyDescription="Action tasks will appear here once monitoring starts."
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <QueueList
          title="Upcoming exercises"
          subtitle="Planned simulations and drills that should stay visible to the delivery team."
          items={dashboard.upcoming_exercises || []}
          renderMeta={(item) => [item.exercise_type, item.status, item.planned_date ? formatDate(item.planned_date) : "No planned date"].filter(Boolean).join(" | ")}
          emptyTitle="No upcoming exercises"
          emptyDescription="Exercise planning will appear here once drills are scheduled."
        />
      </div>
    </div>
  );
}
