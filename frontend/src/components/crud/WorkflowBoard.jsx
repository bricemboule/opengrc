import { useEffect, useMemo, useState } from "react";
import { AlertCircle, CheckCircle2, Clock3, GripVertical, UserRound } from "lucide-react";
import { FiArrowLeft, FiArrowRight, FiEdit2 } from "react-icons/fi";
import EmptyState from "./EmptyState";

const LANE_TONES = [
  {
    accent: "bg-black",
    accentSoft: "bg-black/6",
    badge: "bg-black text-white",
    ring: "ring-black/14",
  },
  {
    accent: "bg-[#f0be7c]",
    accentSoft: "bg-[#fff2df]",
    badge: "bg-[#fff2df] text-[#8d6128]",
    ring: "ring-[#f0be7c]/30",
  },
  {
    accent: "bg-[#93e1a4]",
    accentSoft: "bg-[#eef9f0]",
    badge: "bg-[#eef9f0] text-[#2e6940]",
    ring: "ring-[#93e1a4]/30",
  },
  {
    accent: "bg-[#b8abff]",
    accentSoft: "bg-[#f1eeff]",
    badge: "bg-[#f1eeff] text-[#5d4db0]",
    ring: "ring-[#b8abff]/32",
  },
  {
    accent: "bg-[#8eb2ff]",
    accentSoft: "bg-[#edf3ff]",
    badge: "bg-[#edf3ff] text-[#3153a5]",
    ring: "ring-[#8eb2ff]/28",
  },
];

const DEFAULT_STAGE_NOTES = {
  draft: "Work is being framed and the record is not yet ready for active use.",
  planned: "The activity is scheduled and waiting for execution to begin.",
  in_progress: "The work is actively moving and needs regular operational updates.",
  active: "The record is live in the operating cycle and should stay current.",
  in_review: "Outputs are being checked before validation or closure.",
  submitted: "The record has been routed for validation, approval, or decision.",
  validated: "The result is approved and can now be used operationally.",
  completed: "The main objective is closed and the record remains for traceability.",
  archived: "The record is retained for reference and is no longer active.",
};

function getLaneTone(index) {
  return LANE_TONES[index % LANE_TONES.length];
}

function getTitle(row) {
  return row.title || row.name || row.code || `Record ${row.id}`;
}

function formatDate(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleDateString();
}

function normalizeText(value) {
  if (value === null || value === undefined || value === "") return "";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (typeof value === "string") {
    if (/^\d{4}-\d{2}-\d{2}/.test(value)) return formatDate(value);
    if (value.includes("@") || /\d/.test(value) || /[A-Z]/.test(value)) return value;
    return value.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase());
  }
  return String(value);
}

function getFirstValue(row, fields = []) {
  for (const field of fields) {
    const value = row?.[field];
    if (value !== null && value !== undefined && value !== "") return value;
  }
  return null;
}

function getContextLines(row, blueprint, columnKeys, workflowField) {
  const candidateFields = blueprint?.contextFields?.length
    ? blueprint.contextFields
    : columnKeys.filter((key) => key !== workflowField).slice(0, 3);

  return candidateFields.map((field) => normalizeText(row?.[field])).filter(Boolean).slice(0, 3);
}

function getDueDateValue(row, blueprint) {
  if (blueprint?.dueFields?.length) {
    return getFirstValue(row, blueprint.dueFields);
  }

  return getFirstValue(row, [
    "response_deadline",
    "due_date",
    "next_review_date",
    "planned_date",
    "completed_date",
    "last_assessed_at",
  ]);
}

function describeDueDate(value) {
  if (!value) return null;
  const due = new Date(value);
  if (Number.isNaN(due.getTime())) {
    return { label: String(value), tone: "bg-black/[0.05] text-slate-700" };
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  due.setHours(0, 0, 0, 0);
  const difference = Math.round((due.getTime() - today.getTime()) / 86400000);

  if (difference < 0) {
    return { label: `Overdue ${formatDate(value)}`, tone: "bg-[#fff1ef] text-[#b3473a]" };
  }
  if (difference <= 14) {
    return { label: `Due ${formatDate(value)}`, tone: "bg-[#fff5e8] text-[#8c6848]" };
  }
  return { label: formatDate(value), tone: "bg-black/[0.05] text-slate-700" };
}

function resolveBlockers(row, blueprint) {
  if (!blueprint?.blockerRules?.length) return [];

  return blueprint.blockerRules
    .filter((rule) => rule.when?.(row))
    .map((rule) => (typeof rule.label === "function" ? rule.label(row) : rule.label))
    .filter(Boolean);
}

function getNextAction(row, workflowValue, blueprint) {
  if (row?.next_action) return row.next_action;
  if (row?.next_step) return row.next_step;
  return blueprint?.nextActionLabels?.[workflowValue] || "Review this record with the responsible team and move it to the next operational step.";
}

function getStageNote(workflowValue, blueprint) {
  return blueprint?.stageNotes?.[workflowValue] || DEFAULT_STAGE_NOTES?.[workflowValue] || "";
}

function buildSummary(rows, groupedRows, blueprint) {
  const dueStates = rows.map((row) => describeDueDate(getDueDateValue(row, blueprint)));
  const overdue = dueStates.filter((item) => item?.label?.startsWith("Overdue")).length;
  const dueSoon = dueStates.filter((item) => item && !item.label.startsWith("Overdue") && item.label.startsWith("Due")).length;
  const blocked = rows.filter((row) => resolveBlockers(row, blueprint).length > 0).length;
  const finalized = groupedRows[groupedRows.length - 1]?.records?.length || 0;

  return [
    { label: "Total", value: rows.length, helper: "Tracked workflow records" },
    { label: "Blocked", value: blocked, helper: "Items with blockers to resolve" },
    { label: "Due soon", value: dueSoon, helper: "Items due in the next 14 days" },
    { label: "Finalized", value: finalized, helper: "Items currently in the last stage" },
    { label: "Overdue", value: overdue, helper: "Items already past the due date" },
  ];
}

export default function WorkflowBoard({
  rows = [],
  workflowField,
  workflowChoices = [],
  columnKeys = [],
  onEdit,
  onTransition,
  updating,
  moduleLabel,
  workflowBlueprint,
}) {
  const [localRows, setLocalRows] = useState(rows);
  const [dragState, setDragState] = useState(null);
  const [dropTarget, setDropTarget] = useState(null);
  const [transitioningId, setTransitioningId] = useState(null);

  useEffect(() => {
    setLocalRows(rows);
  }, [rows]);

  const normalizedChoices = useMemo(
    () =>
      workflowChoices.length
        ? workflowChoices
        : Array.from(new Set(localRows.map((row) => row?.[workflowField]).filter(Boolean))).map((value) => ({
            value,
            display_name: normalizeText(value),
          })),
    [localRows, workflowChoices, workflowField],
  );

  const groupedRows = useMemo(
    () =>
      normalizedChoices.map((choice, index) => ({
        ...choice,
        index,
        records: localRows.filter((row) => String(row?.[workflowField]) === String(choice.value)),
      })),
    [localRows, normalizedChoices, workflowField],
  );

  const summary = useMemo(() => buildSummary(localRows, groupedRows, workflowBlueprint), [groupedRows, localRows, workflowBlueprint]);
  const draggingDisabled = Boolean(updating || transitioningId);

  function handleDragStart(event, row) {
    if (draggingDisabled) return;
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", String(row.id));
    setDragState({ rowId: row.id, from: row[workflowField] });
  }

  function handleDragEnd() {
    setDragState(null);
    setDropTarget(null);
  }

  function handleDragOver(event, targetValue) {
    if (!dragState || dragState.from === targetValue) return;
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
    if (dropTarget !== targetValue) {
      setDropTarget(targetValue);
    }
  }

  async function commitTransition(row, targetValue) {
    if (!row || row[workflowField] === targetValue || draggingDisabled) {
      handleDragEnd();
      return;
    }

    const snapshot = localRows;
    setLocalRows((current) => current.map((item) => (item.id === row.id ? { ...item, [workflowField]: targetValue } : item)));
    setTransitioningId(row.id);

    try {
      await onTransition(row, targetValue);
    } catch {
      setLocalRows(snapshot);
    } finally {
      setTransitioningId(null);
      handleDragEnd();
    }
  }

  async function handleDrop(event, targetValue) {
    event.preventDefault();
    if (!dragState || dragState.from === targetValue || draggingDisabled) {
      setDropTarget(null);
      return;
    }

    const movedRow = localRows.find((row) => row.id === dragState.rowId);
    await commitTransition(movedRow, targetValue);
  }

  if (!workflowField) {
    return <EmptyState title="Workflow unavailable" description="No workflow field is configured for this module." />;
  }

  if (!localRows.length) {
    return <EmptyState title="No workflow items" description="There are no records matching the current workflow filters." />;
  }

  return (
    <section className="space-y-5">
      <div className="app-surface rounded-[18px] p-5 sm:p-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h3 className="text-[1.65rem] font-semibold tracking-[-0.05em] text-slate-950">
              {moduleLabel ? `${moduleLabel} workflow` : "Operational workflow"}
            </h3>
            <p className="mt-1 max-w-3xl text-sm leading-7 text-[#554d46]">
              {workflowBlueprint?.objective || "Review blockers, due pressure, ownership, and next actions for the active workflow records."}
            </p>
          </div>
          <span className="app-button app-button-dark app-button-sm">Operational playbook</span>
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-5">
          {summary.map((item, index) => {
            const tone = getLaneTone(index);
            return (
              <article key={item.label} className="rounded-[18px] border border-black/6 bg-white/84 px-4 py-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-[11px] font-semibold text-slate-400">{item.label}</p>
                    <p className="mt-2 text-[1.55rem] font-semibold tracking-[-0.05em] text-slate-950">{item.value}</p>
                  </div>
                  <span className={`h-3 w-3 rounded-full ${tone.accent}`} />
                </div>
                <p className="mt-2 text-xs leading-6 text-slate-500">{item.helper}</p>
              </article>
            );
          })}
        </div>
      </div>

      <div className="app-scroll overflow-x-auto pb-3">
        <div className="flex min-w-max items-start gap-3 pr-4">
          {groupedRows.map((group) => {
            const tone = getLaneTone(group.index);
            const isDropActive = dropTarget === group.value && dragState?.from !== group.value;

            return (
              <section
                key={group.value}
                onDragOver={(event) => handleDragOver(event, group.value)}
                onDrop={(event) => handleDrop(event, group.value)}
                className={`w-[19rem] shrink-0 rounded-[20px] border border-black/7 p-3.5 transition ${isDropActive ? `bg-white ring-1 ${tone.ring}` : "app-surface"}`}
              >
                <div className="space-y-3 border-b border-black/7 pb-4">
                  {/* <div className={`h-1.5 w-full rounded-full ${tone.accent}`} /> */}
                  <div className="flex items-start justify-between gap-3">
                    <div className={`inline-flex min-h-[34px] items-center gap-2 rounded-[8px] border border-black/6 px-2.5 py-2 ${tone.accentSoft}`}>
                      <span className={`inline-flex h-2.5 w-2.5 rounded-full ${tone.accent}`} />
                      <h3 className="text-[12px] font-semibold text-[#322d29]">{group.display_name}</h3>
                      <span className="text-[11px] font-medium text-[#5f5750]">({group.records.length} item{group.records.length > 1 ? "s" : ""})</span>
                    </div>
                  </div>
                  {getStageNote(group.value, workflowBlueprint) ? (
                    <p className="text-[11px] leading-5 text-[#554d46]">{getStageNote(group.value, workflowBlueprint)}</p>
                  ) : null}
                </div>

                <div className="mt-3.5 min-h-[12rem] space-y-2.5">
                  {group.records.length ? (
                    group.records.map((row) => {
                      const previousChoice = group.index > 0 ? groupedRows[group.index - 1] : null;
                      const nextChoice = group.index < groupedRows.length - 1 ? groupedRows[group.index + 1] : null;
                      const contextLines = getContextLines(row, workflowBlueprint, columnKeys, workflowField);
                      const owner = normalizeText(getFirstValue(row, workflowBlueprint?.ownerFields || []));
                      const dueState = describeDueDate(getDueDateValue(row, workflowBlueprint));
                      const blockers = resolveBlockers(row, workflowBlueprint);
                      const nextAction = getNextAction(row, row[workflowField], workflowBlueprint);
                      const isDragging = dragState?.rowId === row.id;
                      const isTransitioning = transitioningId === row.id;

                      return (
                        <article
                          key={row.id}
                          draggable={!draggingDisabled}
                          onDragStart={(event) => handleDragStart(event, row)}
                          onDragEnd={handleDragEnd}
                          className={`cursor-grab rounded-[16px] border border-black/8 bg-white px-3.5 py-3.5 transition ${isDragging ? "opacity-50" : "opacity-100"} ${isTransitioning ? "pointer-events-none opacity-70" : ""}`}
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div className="min-w-0 flex-1">
                              <div className="flex items-start gap-1.5">
                                <GripVertical size={15} className="mt-0.5 shrink-0 text-black/28" />
                                <div className="min-w-0 flex-1">
                                  <h4 className="truncate text-[14px] font-semibold text-slate-950">{getTitle(row)}</h4>
                                  {contextLines.map((line) => (
                                    <div key={`${row.id}-${line}`} className="mt-1 flex items-start gap-2">
                                      <span className="mt-[0.42rem] h-1.5 w-1.5 shrink-0 rounded-full bg-[#111111]" />
                                      <p className="min-w-0 truncate text-[11px] leading-5 text-[#554d46]">{line}</p>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            </div>
                            <button type="button" onClick={() => onEdit(row)} className="app-button app-button-soft app-button-sm app-icon-button h-8 w-8 text-slate-500">
                              <FiEdit2 size={13} />
                            </button>
                          </div>

                          <div className="mt-3.5 flex flex-wrap gap-1.5">
                            {owner ? (
                              <span className="inline-flex items-center gap-1.5 rounded-full bg-black/[0.05] px-2.5 py-1 text-[10px] font-medium text-slate-700">
                                <UserRound size={11} />
                                {owner}
                              </span>
                            ) : null}
                            {dueState ? (
                              <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[10px] font-medium ${dueState.tone}`}>
                                <Clock3 size={11} />
                                {dueState.label}
                              </span>
                            ) : null}
                            {!blockers.length && nextChoice === null ? (
                              <span className="inline-flex items-center gap-1.5 rounded-full bg-[#ecf9ef] px-2.5 py-1 text-[10px] font-medium text-[#25664a]">
                                <CheckCircle2 size={11} />
                                Final stage
                              </span>
                            ) : null}
                          </div>

                          {blockers.length ? (
                            <div className="mt-3.5 rounded-[12px] bg-[#fff4f1] px-3 py-2.5">
                              <div className="flex items-center gap-2 text-[11px] font-semibold text-[#bc5446]">
                                <AlertCircle size={13} />
                                Blockers
                              </div>
                              <div className="mt-2 space-y-1">
                                {blockers.slice(0, 3).map((blocker) => (
                                  <p key={`${row.id}-${blocker}`} className="text-[11px] leading-5 text-[#985346]">{blocker}</p>
                                ))}
                              </div>
                            </div>
                          ) : null}

                          <div className="mt-3.5 rounded-[12px] bg-black/[0.035] px-3 py-2.5">
                            <p className="text-[11px] font-semibold text-[#554d46]">Next action</p>
                            <p className="mt-1.5 text-[11px] leading-5 text-[#5e5650]">{nextAction}</p>
                          </div>

                          {/* <div className="mt-3.5 flex flex-wrap gap-2">
                            {previousChoice ? (
                              <button
                                type="button"
                                disabled={updating || Boolean(transitioningId)}
                                onClick={() => commitTransition(row, previousChoice.value)}
                                className="app-button app-button-soft app-button-sm"
                                style={{ borderRadius: "8px", paddingLeft: "1rem", paddingRight: "1rem" }}
                              >
                                <FiArrowLeft size={12} />
                                {previousChoice.display_name}
                              </button>
                            ) : null}
                            {nextChoice ? (
                              <button
                                type="button"
                                disabled={updating || Boolean(transitioningId)}
                                onClick={() => commitTransition(row, nextChoice.value)}
                                className="app-button app-button-dark app-button-sm"
                                style={{ borderRadius: "8px", paddingLeft: "1rem", paddingRight: "1rem" }}
                              >
                                {nextChoice.display_name}
                                <FiArrowRight size={12} />
                              </button>
                            ) : null}
                          </div> */}
                        </article>
                      );
                    })
                  ) : (
                    <div className={`rounded-[16px] border border-dashed border-black/10 px-4 py-10 text-center text-sm text-slate-500 ${isDropActive ? tone.accentSoft : "bg-white/58"}`}>
                      {isDropActive ? "Drop here to move the record into this stage." : "No records in this stage yet."}
                    </div>
                  )}
                </div>
              </section>
            );
          })}
        </div>
      </div>
    </section>
  );
}


