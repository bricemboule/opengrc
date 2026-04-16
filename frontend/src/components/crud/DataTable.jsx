import { Check, Minus } from "lucide-react";
import { isValidElement, useEffect, useMemo, useState } from "react";

const MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function formatStructuredDateValue(year, month, day) {
  const monthLabel = MONTH_LABELS[month - 1];
  if (!monthLabel) return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
  return `${monthLabel} ${day}, ${year}`;
}

function formatStructuredTimeValue(hour, minute) {
  const safeMinute = Number.isFinite(minute) ? minute : 0;
  const meridiem = hour >= 12 ? "PM" : "AM";
  const normalizedHour = hour % 12 || 12;
  return `${normalizedHour}:${String(safeMinute).padStart(2, "0")} ${meridiem}`;
}

function formatTemporalValue(value) {
  const normalized = String(value || "").trim();
  if (!normalized) return value;

  const dateTimeMatch = normalized.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
  if (dateTimeMatch) {
    const [, year, month, day, hour, minute] = dateTimeMatch;
    return `${formatStructuredDateValue(Number(year), Number(month), Number(day))}, ${formatStructuredTimeValue(Number(hour), Number(minute))}`;
  }

  const dateMatch = normalized.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (dateMatch) {
    const [, year, month, day] = dateMatch;
    return formatStructuredDateValue(Number(year), Number(month), Number(day));
  }

  return value;
}

function renderCellContent(value) {
  if (value === null || value === undefined || value === "") return "\u2014";
  if (typeof value === "string") return formatTemporalValue(value);
  return value;
}

function getColumnSignature(column) {
  return `${column?.key || ""} ${column?.label || ""}`.trim().toLowerCase();
}

function isStatusColumn(column) {
  const signature = getColumnSignature(column);
  return signature.includes("status") || signature.includes("statut");
}

function isPrimaryNameColumn(column) {
  const key = String(column?.key || "").trim().toLowerCase();
  const label = String(column?.label || "").trim().toLowerCase();
  return key === "title" || key === "name" || label === "title" || label === "name";
}

function getReportColumnWidthClass(column) {
  if (isPrimaryNameColumn(column)) return "min-w-[18rem] w-[18rem]";
  if (isStatusColumn(column)) return "min-w-[10rem]";

  const labelLength = String(column?.label || "").trim().length;
  if (labelLength >= 18) return "min-w-[13rem]";
  if (labelLength >= 12) return "min-w-[11rem]";
  if (labelLength >= 8) return "min-w-[9.5rem]";
  return "min-w-[8rem]";
}

function formatStatusLabel(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/(^|\s)\w/g, (character) => character.toUpperCase());
}

function getStatusTone(status) {
  switch (String(status || "").toLowerCase()) {
    case "active":
    case "completed":
    case "validated":
    case "approved":
    case "confirmed":
      return { badge: "bg-[#f2f0ec] text-[#6f685f]", dot: "bg-[#a9a195]" };
    case "in_progress":
    case "planned":
    case "ongoing":
    case "scheduled":
    case "rescheduled":
      return { badge: "bg-[#f5efe9] text-[#8a6d59]", dot: "bg-[#d0a586]" };
    case "in_review":
    case "submitted":
    case "pending":
      return { badge: "bg-[#f3eef1] text-[#7f6975]", dot: "bg-[#bc9dad]" };
    case "missed":
      return { badge: "bg-[#f8ece9] text-[#8b5f56]", dot: "bg-[#d2a29a]" };
    case "archived":
    case "inactive":
    case "cancelled":
      return { badge: "bg-[#f1f0ef] text-[#76716a]", dot: "bg-[#b2aca4]" };
    default:
      return { badge: "bg-[#f2f1ef] text-[#7a746d]", dot: "bg-[#b8b0a8]" };
  }
}

function renderStatusBadge(value) {
  const renderedValue = renderCellContent(value);
  if (renderedValue === "—") return renderedValue;

  const tone = getStatusTone(renderedValue);
  const label = formatStatusLabel(renderedValue);

  return (
    <span className={`inline-flex whitespace-nowrap items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold ${tone.badge}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${tone.dot}`} />
      {label}
    </span>
  );
}

function renderTruncatedValue(value, variant, column) {
  const renderedValue = renderCellContent(value);
  if (renderedValue === "—") return renderedValue;

  const label = String(renderedValue);
  const widthClassName = variant === "report"
    ? isPrimaryNameColumn(column)
      ? "w-[18rem] max-w-[18rem]"
      : "max-w-[24rem]"
    : "max-w-[24rem]";

  return (
    <span className={`block truncate ${widthClassName}`} title={label}>
      {label}
    </span>
  );
}

function resolveCellContent(column, row, variant) {
  const rawValue = column.render ? column.render(row) : row[column.key];

  if (isValidElement(rawValue)) return rawValue;
  if (isStatusColumn(column)) return renderStatusBadge(rawValue);

  return renderTruncatedValue(rawValue, variant, column);
}

function resolveRowId(row, rowIndex, getRowId) {
  return getRowId ? getRowId(row, rowIndex) : row.id ?? rowIndex;
}

function SelectionControl({ checked = false, mixed = false, onToggle, label }) {
  return (
    <button
      type="button"
      role="checkbox"
      aria-checked={mixed ? "mixed" : checked}
      aria-label={label}
      onClick={onToggle}
      className={`flex h-5 w-5 items-center justify-center rounded-[7px] transition ${
        checked || mixed ? "bg-[#111111] text-white" : "border border-black/8 bg-transparent text-transparent hover:border-black/14 hover:bg-white/40"
      }`}
    >
      {mixed ? <Minus size={11} strokeWidth={1.9} /> : checked ? <Check size={11} strokeWidth={1.9} /> : null}
    </button>
  );
}

export default function DataTable({ columns, rows = [], rowActions, variant = "default", selectable = false, selectedRowIds = [], onToggleRow, onToggleAll, getRowId }) {
  const isStakeholderVariant = variant === "stakeholder";
  const isReportVariant = variant === "report";
  const rowIds = useMemo(() => rows.map((row, rowIndex) => resolveRowId(row, rowIndex, getRowId)), [getRowId, rows]);
  const isControlledSelection = typeof onToggleRow === "function" && typeof onToggleAll === "function";
  const [internalSelectedRowIds, setInternalSelectedRowIds] = useState([]);
  const effectiveSelectedRowIds = isControlledSelection ? selectedRowIds : internalSelectedRowIds;
  const selectedSet = useMemo(() => new Set(effectiveSelectedRowIds), [effectiveSelectedRowIds]);
  const selectedCount = rowIds.filter((rowId) => selectedSet.has(rowId)).length;
  const showSelection = selectable;
  const allSelected = showSelection && rowIds.length > 0 && selectedCount === rowIds.length;
  const partiallySelected = showSelection && selectedCount > 0 && selectedCount < rowIds.length;

  const tableClassName = isStakeholderVariant
    ? "w-full min-w-[860px] border-separate border-spacing-y-[0.16rem] text-[14px]"
    : isReportVariant
      ? "w-max min-w-full border-separate border-spacing-y-[0.12rem] text-[13px]"
      : "w-full min-w-[760px] border-separate border-spacing-y-[0.16rem] text-[14px]";
  const tableStyle = { fontFamily: "var(--app-table-font)" };
  const headerRowClassName = "text-left text-[13px] tracking-[0.01em] text-[#111111]";
  const headerCellBaseClassName = isReportVariant ? "bg-[#f0eded] px-3.5 py-[14px] font-semibold" : "bg-[#f0eded] px-4 py-[18px] font-semibold";
  const bodyRowClassName = "text-[#111111]";
  const bodyCellBaseClassName = isReportVariant ? "px-3.5 py-3 align-middle" : "px-4 py-3.5 align-middle";
  const headerRadiusClassName = isReportVariant ? "rounded-[8px]" : "rounded-[14px]";

  useEffect(() => {
    if (isControlledSelection) return;
    const availableRowIds = new Set(rowIds);
    setInternalSelectedRowIds((current) => current.filter((rowId) => availableRowIds.has(rowId)));
  }, [isControlledSelection, rowIds]);

  function handleToggleAllSelection(checked) {
    if (isControlledSelection) {
      onToggleAll(checked);
      return;
    }
    setInternalSelectedRowIds(checked ? rowIds : []);
  }

  function handleToggleSingleRow(rowId, checked) {
    if (isControlledSelection) {
      onToggleRow(rowId, checked);
      return;
    }

    setInternalSelectedRowIds((current) => {
      if (checked) return current.includes(rowId) ? current : [...current, rowId];
      return current.filter((value) => value !== rowId);
    });
  }

  return (
    <div className="app-scroll overflow-x-auto">
      <table className={tableClassName} style={tableStyle}>
        <thead>
          <tr className={headerRowClassName}>
            {showSelection ? (
              <th className={`${headerCellBaseClassName} w-14 ${headerRadiusClassName.replace("rounded-[", "rounded-l-[")} text-center`}>
                <SelectionControl checked={allSelected} mixed={partiallySelected} onToggle={() => handleToggleAllSelection(!allSelected)} label="Select all rows" />
              </th>
            ) : null}
            {columns.map((column, index) => {
              const reportWidthClassName = isReportVariant ? `${getReportColumnWidthClass(column)} whitespace-nowrap` : "";
              return (
                <th
                  key={column.key}
                  className={`${headerCellBaseClassName} ${reportWidthClassName} ${index === 0 && !showSelection ? (isReportVariant ? "rounded-l-[8px]" : "rounded-l-[14px]") : ""} ${index === columns.length - 1 && !rowActions ? (isReportVariant ? "rounded-r-[8px]" : "rounded-r-[14px]") : ""}`}
                  title={column.label}
                >
                  {column.label}
                </th>
              );
            })}
            {rowActions ? <th className={`${isReportVariant ? "rounded-r-[8px] whitespace-nowrap min-w-[8rem]" : "rounded-r-[14px]"} text-left ${headerCellBaseClassName}`}>Actions</th> : null}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => {
            const rowId = resolveRowId(row, rowIndex, getRowId);
            const isSelected = selectedSet.has(rowId);
            const bodySurfaceClassName = showSelection ? (isSelected ? "bg-white/82" : "bg-transparent") : "bg-white/82";

            return (
              <tr key={rowId} className={bodyRowClassName}>
                {showSelection ? (
                  <td className={`${bodyCellBaseClassName} ${bodySurfaceClassName} ${isReportVariant ? "rounded-l-[4px]" : "rounded-l-[14px]"} text-center`}>
                    <SelectionControl checked={isSelected} onToggle={() => handleToggleSingleRow(rowId, !isSelected)} label={`Select row ${rowIndex + 1}`} />
                  </td>
                ) : null}
                {columns.map((column, index) => {
                  const reportWidthClassName = isReportVariant ? getReportColumnWidthClass(column) : "";
                  const reportWrapClassName = isReportVariant && isStatusColumn(column) ? "whitespace-nowrap" : "";
                  return (
                    <td
                      key={column.key}
                      className={`${bodyCellBaseClassName} ${bodySurfaceClassName} ${reportWidthClassName} ${reportWrapClassName} ${
                        index === 0 && !showSelection ? (isReportVariant ? "rounded-l-[4px]" : "rounded-l-[14px]") : ""
                      } ${index === columns.length - 1 && !rowActions ? (isReportVariant ? "rounded-r-[4px]" : "rounded-r-[14px]") : ""}`}
                    >
                      {resolveCellContent(column, row, variant)}
                    </td>
                  );
                })}
                {rowActions ? <td className={`${bodyCellBaseClassName} ${bodySurfaceClassName} ${isReportVariant ? "rounded-r-[4px] min-w-[8rem]" : "rounded-r-[14px]"} text-left`}>{rowActions(row)}</td> : null}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
