import { AlertCircle, CheckCircle2, Clock3, FileText, PlayCircle } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import api from "../../api/client";
import EmptyState from "../crud/EmptyState";
import { notifyError, notifySuccess } from "../../utils/toast";

function formatLabel(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/(^|\s)\w/g, (character) => character.toUpperCase());
}

function formatDateTime(value) {
  if (!value) return "";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return String(value);
  return parsed.toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
}

function getStatusTone(status) {
  switch (String(status || "").toLowerCase()) {
    case "completed":
    case "ready":
      return "bg-[#edf7ee] text-[#3d6a49]";
    case "active":
    case "in_progress":
      return "bg-[#fff5e8] text-[#8b6a48]";
    case "blocked":
      return "bg-[#fff0ea] text-[#a2574a]";
    case "cancelled":
    case "skipped":
    case "archived":
      return "bg-[#f1f0ef] text-[#76716a]";
    default:
      return "bg-black/[0.05] text-[#5f5750]";
  }
}

function buildExecutionSummary(rows) {
  const active = rows.filter((row) => ["planned", "active", "blocked"].includes(row.status)).length;
  const blocked = rows.filter((row) => row.status === "blocked" || row.blocker_summary).length;
  const dueSoon = rows.filter((row) => {
    if (!row.target_completion_at) return false;
    const due = new Date(row.target_completion_at);
    const now = new Date();
    return !Number.isNaN(due.getTime()) && due.getTime() - now.getTime() <= 86400000 && due.getTime() >= now.getTime();
  }).length;
  const completed = rows.filter((row) => row.status === "completed").length;

  return [
    { label: "Active runs", value: active, helper: "Planned, active, or blocked executions" },
    { label: "Blocked", value: blocked, helper: "Executions needing intervention now" },
    { label: "Due soon", value: dueSoon, helper: "Target completion within 24 hours" },
    { label: "Completed", value: completed, helper: "Executions already closed out" },
  ];
}

function getStepActions(step) {
  switch (step.status) {
    case "planned":
      return [
        { label: "Start", status: "in_progress", tone: "dark" },
        { label: "Block", status: "blocked", tone: "soft" },
        { label: "Skip", status: "skipped", tone: "soft" },
      ];
    case "in_progress":
      return [
        { label: "Complete", status: "completed", tone: "dark" },
        { label: "Block", status: "blocked", tone: "soft" },
        { label: "Reset", status: "planned", tone: "soft" },
      ];
    case "blocked":
      return [
        { label: "Resume", status: "in_progress", tone: "dark" },
        { label: "Complete", status: "completed", tone: "soft" },
      ];
    case "completed":
    case "skipped":
      return [{ label: "Reopen", status: "planned", tone: "soft" }];
    default:
      return [];
  }
}

export default function SopExecutionView({ rows = [], workflowChoices = [], onEdit, onRefresh }) {
  const [selectedExecutionId, setSelectedExecutionId] = useState(null);
  const [busyExecutionStatus, setBusyExecutionStatus] = useState(null);
  const [busyStepId, setBusyStepId] = useState(null);
  const summary = useMemo(() => buildExecutionSummary(rows), [rows]);
  const selectedExecution = rows.find((row) => row.id === selectedExecutionId) || rows[0] || null;

  useEffect(() => {
    if (!rows.length) {
      setSelectedExecutionId(null);
      return;
    }

    if (!rows.some((row) => row.id === selectedExecutionId)) {
      setSelectedExecutionId(rows[0].id);
    }
  }, [rows, selectedExecutionId]);

  const stepBoardQuery = useQuery({
    queryKey: ["sop-execution-step-board", selectedExecution?.id],
    queryFn: async () => (await api.get(`/incident-management/sop-executions/${selectedExecution.id}/step-board/`)).data,
    enabled: Boolean(selectedExecution?.id),
    staleTime: 0,
    refetchOnWindowFocus: false,
  });

  const stepRows = stepBoardQuery.data?.steps || [];
  const stepSummary = stepBoardQuery.data?.step_summary || [];

  async function handleExecutionStatusChange(nextStatus) {
    if (!selectedExecution?.id || busyExecutionStatus === nextStatus) return;

    setBusyExecutionStatus(nextStatus);
    try {
      await api.patch(`/incident-management/sop-executions/${selectedExecution.id}/`, { status: nextStatus });
      notifySuccess("Execution updated");
      await onRefresh?.();
      await stepBoardQuery.refetch();
    } catch (error) {
      notifyError(error?.response?.data?.detail || "Unable to update execution status.");
    } finally {
      setBusyExecutionStatus(null);
    }
  }

  async function handleStepStatusChange(stepId, nextStatus) {
    if (!stepId || busyStepId === stepId) return;

    setBusyStepId(stepId);
    try {
      await api.patch(`/incident-management/sop-execution-steps/${stepId}/`, { status: nextStatus });
      notifySuccess("Step updated");
      await onRefresh?.();
      await stepBoardQuery.refetch();
    } catch (error) {
      notifyError(error?.response?.data?.detail || "Unable to update the SOP step.");
    } finally {
      setBusyStepId(null);
    }
  }

  if (!rows.length) {
    return <EmptyState title="No SOP executions" description="Launch an SOP execution from a template to start tracking live runbook steps." />;
  }

  return (
    <section className="space-y-5">
      <div className="app-surface rounded-[18px] p-5 sm:p-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h3 className="text-[1.65rem] font-semibold tracking-[-0.05em] text-slate-950">SOP execution workspace</h3>
            <p className="mt-1 max-w-3xl text-sm leading-7 text-[#554d46]">
              Run live checklists, keep step ownership visible, and close blockers before they slow incident coordination.
            </p>
          </div>
          <span className="app-button app-button-dark app-button-sm">Operational playbook</span>
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {summary.map((item, index) => (
            <article key={item.label} className="rounded-[18px] border border-black/6 bg-white/84 px-4 py-4">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-[11px] font-semibold text-slate-400">{item.label}</p>
                  <p className="mt-2 text-[1.55rem] font-semibold tracking-[-0.05em] text-slate-950">{item.value}</p>
                </div>
                <span className={`h-3 w-3 rounded-full ${["bg-black", "bg-[#d67863]", "bg-[#f0be7c]", "bg-[#93e1a4]"][index % 4]}`} />
              </div>
              <p className="mt-2 text-xs leading-6 text-slate-500">{item.helper}</p>
            </article>
          ))}
        </div>
      </div>

      <div className="grid gap-5 xl:grid-cols-[320px_minmax(0,1fr)]">
        <aside className="app-surface rounded-[18px] p-4">
          <div className="border-b border-black/8 pb-3">
            <h4 className="text-sm font-semibold text-[#554d46]">Execution queue</h4>
            <p className="mt-1 text-[12px] leading-5 text-[#5e5650]">Choose a run to inspect its live steps and blockers.</p>
          </div>

          <div className="app-scroll mt-4 max-h-[46rem] space-y-2 overflow-y-auto pr-1">
            {rows.map((row) => {
              const isSelected = row.id === selectedExecution?.id;
              return (
                <button
                  key={row.id}
                  type="button"
                  onClick={() => setSelectedExecutionId(row.id)}
                  className={`w-full rounded-[16px] px-4 py-4 text-left transition ${
                    isSelected ? "bg-[#f4efe9] shadow-[inset_0_0_0_1px_rgba(17,17,17,0.05)]" : "bg-white/82 hover:bg-[#f9f5ef]"
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="truncate text-sm font-semibold text-slate-950">{row.title}</p>
                      <p className="mt-1 truncate text-[12px] text-[#5e5650]">{row.incident_title || row.template_title}</p>
                    </div>
                    <span className={`shrink-0 rounded-full px-2.5 py-1 text-[10px] font-medium ${getStatusTone(row.status)}`}>
                      {formatLabel(row.status)}
                    </span>
                  </div>
                  <div className="mt-3 flex items-center justify-between gap-3 text-[11px] text-[#5e5650]">
                    <span>{row.execution_commander_name || "No commander"}</span>
                    <span>{row.completion_ratio ?? 0}% done</span>
                  </div>
                </button>
              );
            })}
          </div>
        </aside>

        <div className="space-y-5">
          {selectedExecution ? (
            <section className="app-surface rounded-[18px] p-5 sm:p-6">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                <div className="space-y-2">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`rounded-full px-2.5 py-1 text-[10px] font-medium ${getStatusTone(selectedExecution.status)}`}>
                      {formatLabel(selectedExecution.status)}
                    </span>
                    <span className="rounded-full bg-black/[0.05] px-2.5 py-1 text-[10px] font-medium text-[#5f5750]">
                      {selectedExecution.completion_ratio ?? 0}% complete
                    </span>
                  </div>
                  <h3 className="text-[1.5rem] font-semibold tracking-[-0.05em] text-slate-950">{selectedExecution.title}</h3>
                  <p className="text-sm leading-7 text-[#554d46]">
                    {selectedExecution.incident_title || "No linked incident"} • {selectedExecution.template_title || "No template"} • {selectedExecution.execution_commander_name || "No commander"}
                  </p>
                </div>

                <div className="flex flex-wrap gap-2">
                  {workflowChoices.map((choice) => {
                    const isActive = String(choice.value) === String(selectedExecution.status);
                    return (
                      <button
                        key={choice.value}
                        type="button"
                        disabled={Boolean(busyExecutionStatus)}
                        onClick={() => handleExecutionStatusChange(choice.value)}
                        className={isActive ? "app-button app-button-dark app-button-sm" : "app-button app-button-soft app-button-sm"}
                      >
                        {choice.display_name}
                      </button>
                    );
                  })}
                  <button type="button" onClick={() => onEdit?.(selectedExecution)} className="app-button app-button-soft app-button-sm">
                    Edit run
                  </button>
                </div>
              </div>

              <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                <article className="rounded-[16px] bg-white/84 px-4 py-4">
                  <div className="flex items-center gap-2 text-[11px] font-semibold text-[#554d46]">
                    <Clock3 size={13} />
                    Target completion
                  </div>
                  <p className="mt-2 text-sm font-semibold text-slate-950">{formatDateTime(selectedExecution.target_completion_at) || "Not set"}</p>
                </article>
                <article className="rounded-[16px] bg-white/84 px-4 py-4">
                  <div className="flex items-center gap-2 text-[11px] font-semibold text-[#554d46]">
                    <PlayCircle size={13} />
                    Started
                  </div>
                  <p className="mt-2 text-sm font-semibold text-slate-950">{formatDateTime(selectedExecution.started_at) || "Not started"}</p>
                </article>
                <article className="rounded-[16px] bg-white/84 px-4 py-4">
                  <div className="flex items-center gap-2 text-[11px] font-semibold text-[#554d46]">
                    <CheckCircle2 size={13} />
                    Completed
                  </div>
                  <p className="mt-2 text-sm font-semibold text-slate-950">{formatDateTime(selectedExecution.completed_at) || "Open"}</p>
                </article>
                <article className="rounded-[16px] bg-white/84 px-4 py-4">
                  <div className="flex items-center gap-2 text-[11px] font-semibold text-[#554d46]">
                    <AlertCircle size={13} />
                    Next action
                  </div>
                  <p className="mt-2 text-sm font-semibold text-slate-950">{selectedExecution.next_action || "Advance the active checklist."}</p>
                </article>
              </div>

              {selectedExecution.summary || selectedExecution.outcome_summary || selectedExecution.blocker_summary ? (
                <div className="mt-5 grid gap-3 xl:grid-cols-3">
                  {selectedExecution.summary ? (
                    <article className="rounded-[16px] bg-white/84 px-4 py-4">
                      <p className="text-[11px] font-semibold text-[#554d46]">Execution summary</p>
                      <p className="mt-2 text-sm leading-6 text-[#5e5650]">{selectedExecution.summary}</p>
                    </article>
                  ) : null}
                  {selectedExecution.outcome_summary ? (
                    <article className="rounded-[16px] bg-white/84 px-4 py-4">
                      <p className="text-[11px] font-semibold text-[#554d46]">Outcome</p>
                      <p className="mt-2 text-sm leading-6 text-[#5e5650]">{selectedExecution.outcome_summary}</p>
                    </article>
                  ) : null}
                  {selectedExecution.blocker_summary ? (
                    <article className="rounded-[16px] bg-[#fff4f1] px-4 py-4">
                      <p className="text-[11px] font-semibold text-[#a2574a]">Blocker</p>
                      <p className="mt-2 text-sm leading-6 text-[#8a5a50]">{selectedExecution.blocker_summary}</p>
                    </article>
                  ) : null}
                </div>
              ) : null}
            </section>
          ) : null}

          <section className="app-surface rounded-[18px] p-5 sm:p-6">
            <div className="flex flex-col gap-3 border-b border-black/8 pb-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <h4 className="text-sm font-semibold text-[#554d46]">Execution steps</h4>
                <p className="mt-1 text-[12px] leading-5 text-[#5e5650]">Progress each step in sequence and surface blockers as soon as they appear.</p>
              </div>
              <div className="flex flex-wrap gap-2">
                {stepSummary.map((item) => (
                  <span key={item.value} className={`rounded-full px-2.5 py-1 text-[10px] font-medium ${getStatusTone(item.value)}`}>
                    {item.label}: {item.total}
                  </span>
                ))}
              </div>
            </div>

            {stepBoardQuery.isLoading ? (
              <div className="py-10 text-sm text-[#5e5650]">Loading execution steps...</div>
            ) : stepRows.length ? (
              <div className="mt-5 space-y-3">
                {stepRows.map((step) => (
                  <article key={step.id} className="rounded-[18px] border border-black/7 bg-white px-4 py-4">
                    <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                      <div className="min-w-0 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="rounded-full bg-black/[0.05] px-2.5 py-1 text-[10px] font-medium text-[#5f5750]">
                            Step {step.step_order}
                          </span>
                          <span className={`rounded-full px-2.5 py-1 text-[10px] font-medium ${getStatusTone(step.status)}`}>
                            {formatLabel(step.status)}
                          </span>
                          <span className="rounded-full bg-[#f7f5f1] px-2.5 py-1 text-[10px] font-medium text-[#5f5750]">
                            {formatLabel(step.step_type)}
                          </span>
                          {step.is_required ? (
                            <span className="rounded-full bg-[#fff5e8] px-2.5 py-1 text-[10px] font-medium text-[#8b6a48]">Required</span>
                          ) : null}
                        </div>
                        <h5 className="mt-3 text-[15px] font-semibold text-slate-950">{step.title}</h5>
                        {step.instruction ? <p className="mt-2 text-sm leading-6 text-[#5e5650]">{step.instruction}</p> : null}
                        <div className="mt-3 flex flex-wrap gap-4 text-[11px] text-[#5e5650]">
                          <span>{step.assigned_to_name || "No assignee"}</span>
                          <span>{formatDateTime(step.started_at) || "Not started"}</span>
                          <span>{formatDateTime(step.completed_at) || "Open"}</span>
                        </div>
                        {step.blocker_summary ? (
                          <div className="mt-3 rounded-[12px] bg-[#fff4f1] px-3 py-2.5 text-[11px] leading-5 text-[#8a5a50]">
                            {step.blocker_summary}
                          </div>
                        ) : null}
                        {step.notes ? (
                          <div className="mt-3 rounded-[12px] bg-black/[0.035] px-3 py-2.5 text-[11px] leading-5 text-[#5e5650]">
                            {step.notes}
                          </div>
                        ) : null}
                        {step.evidence_reference ? (
                          <a
                            href={step.evidence_reference}
                            target="_blank"
                            rel="noreferrer"
                            className="mt-3 inline-flex items-center gap-2 text-[11px] font-medium text-[#111111] underline underline-offset-4"
                          >
                            <FileText size={12} />
                            Open evidence
                          </a>
                        ) : null}
                      </div>

                      <div className="flex flex-wrap gap-2 lg:justify-end">
                        {getStepActions(step).map((action) => (
                          <button
                            key={`${step.id}-${action.status}`}
                            type="button"
                            disabled={busyStepId === step.id}
                            onClick={() => handleStepStatusChange(step.id, action.status)}
                            className={action.tone === "dark" ? "app-button app-button-dark app-button-sm" : "app-button app-button-soft app-button-sm"}
                          >
                            {action.label}
                          </button>
                        ))}
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <EmptyState title="No execution steps" description="This SOP execution has no cloned steps yet. Add steps to the template, then create a new run." />
            )}
          </section>
        </div>
      </div>
    </section>
  );
}
