import { useEffect, useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Activity, ClipboardList, Folder, MapPin, Shield, Target } from "lucide-react";
import { FiEdit2, FiPlus, FiTrash2 } from "react-icons/fi";
import { Link, useSearchParams } from "react-router-dom";
import PageHeader from "../components/crud/PageHeader";
import DataTable from "../components/crud/DataTable";
import DataToolbar from "../components/crud/DataToolbar";
import Pagination from "../components/crud/Pagination";
import EmptyState from "../components/crud/EmptyState";
import Create from "../components/crud/Create";
import ConfirmDialog from "../components/crud/ConfirmDialog";
import Import from "../components/crud/Import";
import MapView from "../components/crud/MapView";
import OperationalReportView from "../components/crud/OperationalReportView";
import WorkflowBoard from "../components/crud/WorkflowBoard";
import { buildFieldList, buildInitialValues, normalizeErrors, serializePayload } from "../components/crud/crudUtils";
import usePaginatedList from "../hooks/usePaginatedList";
import { useCreateItem, useDeleteItem, useUpdateItem } from "../hooks/useCrudMutations";
import { getFormPresentation, getModuleBehavior, getSupportedViews, getViewLabel, getWorkflowBlueprint } from "../config/moduleBehaviors";
import { moduleConfigs } from "../config/modules";
import api from "../api/client";
import { notifyError, notifySuccess } from "../utils/toast";

const ENHANCED_PAGINATION_MODULE_KEYS = new Set([
  "risk_register_entries",
  "capacity_assessments",
  "training_programs",
  "contingency_plans",
  "emergency_response_assets",
  "simulation_exercises",
  "cyber_standards",
  "audit_frameworks",
  "deliverable_milestones",
  "action_plan_tasks",
]);
const ENHANCED_PAGINATION_DEFAULT_PAGE_SIZE = 10;
const STANDARD_PAGE_SIZE = 20;

function getExtendedPageSize(activeMode, pageSize) {
  const baseline = activeMode === "workflow" ? 80 : 60;
  return Math.max(pageSize || 0, baseline);
}

function isReportMode(mode) {
  return String(mode || "").startsWith("report");
}

function differenceInDays(targetDate) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const target = new Date(targetDate);
  target.setHours(0, 0, 0, 0);
  return Math.round((target.getTime() - today.getTime()) / 86400000);
}

function filterRowsBySearch(rows, search) {
  const normalized = String(search || "")
    .trim()
    .toLowerCase();
  if (!normalized) return rows;

  return rows.filter((row) =>
    Object.values(row || {}).some((value) =>
      String(value ?? "")
        .toLowerCase()
        .includes(normalized),
    ),
  );
}

function getStakeholderStatusTone(status) {
  switch (status) {
    case "active":
    case "validated":
    case "completed":
      return { badge: "bg-[#f2f0ec] text-[#6f685f]", dot: "bg-[#a9a195]" };
    case "in_progress":
    case "planned":
      return { badge: "bg-[#f5efe9] text-[#8a6d59]", dot: "bg-[#d0a586]" };
    case "in_review":
    case "submitted":
      return { badge: "bg-[#f3eef1] text-[#7f6975]", dot: "bg-[#bc9dad]" };
    case "archived":
      return { badge: "bg-[#f1f0ef] text-[#76716a]", dot: "bg-[#b2aca4]" };
    case "draft":
    default:
      return { badge: "bg-[#f2f1ef] text-[#7a746d]", dot: "bg-[#b8b0a8]" };
  }
}

function getModuleSectionIcon(moduleKey) {
  if (["cybergrc_stakeholders", "desk_study_reviews", "stakeholder_consultations", "critical_infrastructure", "governance_artifacts"].includes(moduleKey)) return MapPin;
  if (["risk_register_entries", "capacity_assessments", "training_programs"].includes(moduleKey)) return Activity;
  if (["contingency_plans", "emergency_response_assets", "simulation_exercises"].includes(moduleKey)) return Target;
  if (["cyber_standards", "audit_frameworks"].includes(moduleKey)) return Shield;
  if (["deliverable_milestones", "action_plan_tasks"].includes(moduleKey)) return ClipboardList;
  return null;
}

function getModuleFormEyebrow(moduleKey) {
  if (["cybergrc_stakeholders", "desk_study_reviews", "stakeholder_consultations", "critical_infrastructure", "governance_artifacts"].includes(moduleKey)) return "Governance & Mapping";
  if (["risk_register_entries", "capacity_assessments", "training_programs"].includes(moduleKey)) return "Risk & Capacity";
  if (["contingency_plans", "emergency_response_assets", "simulation_exercises"].includes(moduleKey)) return "Contingency Planning";
  if (["cyber_standards", "audit_frameworks"].includes(moduleKey)) return "Standards & Audit";
  if (["deliverable_milestones", "action_plan_tasks"].includes(moduleKey)) return "Delivery Tracking";
  return "Cyber GRC";
}

function getQueryErrorMessage(error, fallback = "An error occurred while loading the data.") {
  const payload = error?.response?.data;
  if (typeof payload === "string" && payload.trim()) return payload;
  if (payload?.detail) return String(payload.detail);
  if (payload?.message) return String(payload.message);
  return error?.message || fallback;
}

function getModePresentation(config, activeMode) {
  const key = `${config?.key}:${activeMode}`;

  switch (key) {
    case "staff_skills:search":
      return {
        pageTitle: "Search by Skills",
        pageDescription: "Search staff by skill from the skills catalog.",
        searchPlaceholder: "Search for a skill or staff member...",
      };
    case "team_members:search":
      return {
        pageTitle: "Search Members",
        pageDescription: "Search team members by name, team, or role.",
        searchPlaceholder: "Search for a team member or team...",
      };
    case "training_participants:search":
      return {
        pageTitle: "Search Training Participants",
        pageDescription: "Search training participants by session or staff member.",
        searchPlaceholder: "Search for a training or participant...",
      };
    case "staffs:report-staff":
      return {
        pageTitle: "Staff Report",
        pageDescription: "Consolidated report of staff recorded in the organization.",
        searchPlaceholder: "Filter the staff report...",
      };
    case "staffs:report-contracts":
      return {
        pageTitle: "Expiring Staff Contracts Report",
        pageDescription: "Track contracts expiring in the next 90 days.",
        searchPlaceholder: "Filter the contracts report...",
      };
    case "training_participants:report-training":
      return {
        pageTitle: "Training Report",
        pageDescription: "Report of participants, completion statuses, and certificate issuance.",
        searchPlaceholder: "Filter the training report...",
      };
    default:
      break;
  }

  if (activeMode === "workflow") {
    return {
      pageTitle: getViewLabel(config, "workflow"),
      pageDescription: `Pilot the operational steps for ${config?.label?.toLowerCase()} and move records through the expected workflow.`,
      searchPlaceholder: `Filter ${config?.label?.toLowerCase()} workflow...`,
    };
  }

  if (activeMode === "map") {
    return {
      pageTitle: getViewLabel(config, "map"),
      pageDescription: `Inspect the geographic footprint of ${config?.label?.toLowerCase()} with coordinates ready for mapping.`,
      searchPlaceholder: `Filter mapped ${config?.label?.toLowerCase()}...`,
    };
  }

  if (activeMode === "report") {
    return {
      pageTitle: getViewLabel(config, "report"),
      pageDescription: `Review deadlines, priorities, and operational signals for ${config?.label?.toLowerCase()}.`,
      searchPlaceholder: `Filter ${config?.label?.toLowerCase()} report...`,
    };
  }

  return {
    pageTitle: config?.label,
    pageDescription: `Manage ${config?.label?.toLowerCase()}`,
    searchPlaceholder: "Search...",
  };
}

export default function ModuleListPage({ moduleKey: routeModuleKey }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(STANDARD_PAGE_SIZE);
  const [editingItem, setEditingItem] = useState(null);
  const [formValues, setFormValues] = useState({});
  const [formErrors, setFormErrors] = useState({});
  const [isImporting, setIsImporting] = useState(false);
  const [selectedRowIds, setSelectedRowIds] = useState([]);
  const [pendingDeleteItem, setPendingDeleteItem] = useState(null);
  const queryClient = useQueryClient();

  const config = moduleConfigs.find((item) => item.route === routeModuleKey);
  const moduleBehavior = useMemo(() => getModuleBehavior(config?.key), [config?.key]);
  const supportedViews = useMemo(() => getSupportedViews(config), [config]);
  const allowedModes = useMemo(() => new Set(supportedViews), [supportedViews]);
  const usesEnhancedPagination = useMemo(() => ENHANCED_PAGINATION_MODULE_KEYS.has(config?.key), [config?.key]);

  const { data, error: listError, isError: isListError, isLoading, refetch } = usePaginatedList(config?.key || routeModuleKey, config?.endpoint || "/", {
    search,
    page,
    page_size: pageSize,
    ordering: "-created_at",
  });

  const requestedMode = searchParams.get("mode") || "list";
  const activeMode = editingItem ? "edit" : allowedModes.has(requestedMode) ? requestedMode : "list";
  const shouldLoadMetadata = ["create", "edit", "import"].includes(activeMode);

  const { data: metadata } = useQuery({
    queryKey: [config?.key, "metadata"],
    queryFn: async () => (await api.options(config.endpoint)).data,
    enabled: Boolean(config?.endpoint) && shouldLoadMetadata,
    staleTime: 30000,
    refetchOnWindowFocus: false,
  });

  const createMutation = useCreateItem(config?.key, config?.endpoint, `${config?.label} created`);
  const updateMutation = useUpdateItem(config?.key, config?.endpoint, `${config?.label} updated`);
  const deleteMutation = useDeleteItem(config?.key, config?.endpoint, `${config?.label} deleted`);

  const formFields = useMemo(() => buildFieldList(config, metadata), [config, metadata]);
  const modePresentation = useMemo(() => getModePresentation(config, activeMode), [activeMode, config]);
  const SectionHeaderIcon = useMemo(() => getModuleSectionIcon(config?.key), [config?.key]);
  const baseFormPresentation = useMemo(() => getFormPresentation(config), [config]);
  const workflowBlueprint = useMemo(() => getWorkflowBlueprint(config), [config]);
  const formPresentation = useMemo(
    () => ({
      variant: "editorial",
      eyebrow: getModuleFormEyebrow(config?.key),
      sectionLabel: `${config?.label || "Record"} file`,
      ...(baseFormPresentation || {}),
      icon: SectionHeaderIcon ? <SectionHeaderIcon size={18} strokeWidth={2.15} /> : null,
      mode: activeMode,
    }),
    [SectionHeaderIcon, activeMode, baseFormPresentation, config?.key, config?.label],
  );
  const workflowField = moduleBehavior.workflowField || formFields.find((field) => ["status", "mapping_status", "treatment_status", "availability_status"].includes(field.name))?.name || null;
  const workflowFieldConfig = formFields.find((field) => field.name === workflowField);
  const workflowChoices = workflowFieldConfig?.choices || [];
  const reportPreset = moduleBehavior.reportPreset;
  const isOperationalReportMode = activeMode === "report" && Boolean(reportPreset);
  const needsExtendedRows = activeMode === "map" || activeMode === "workflow" || isReportMode(activeMode);
  const rows = data?.results || data || [];
  const totalRowCount = typeof data?.count === "number" ? data.count : rows.length;
  const shouldFetchExtendedRows = needsExtendedRows && totalRowCount > rows.length;
  const extendedPageSize = getExtendedPageSize(activeMode, pageSize);

  const { data: extendedData, error: extendedError, isError: isExtendedError, refetch: refetchExtended } = useQuery({
    queryKey: [config?.key, activeMode, extendedPageSize, "extended"],
    queryFn: async () => {
      const ordering = activeMode === "report-contracts" ? "contract_end_date" : "-created_at";
      const response = await api.get(config.endpoint, { params: { ordering, page_size: extendedPageSize } });
      return response.data;
    },
    enabled: Boolean(config?.endpoint) && shouldFetchExtendedRows,
    staleTime: 30000,
    refetchOnWindowFocus: false,
  });

  const extendedRows = shouldFetchExtendedRows && !isExtendedError ? extendedData?.results || extendedData || rows : rows;
  const filteredExtendedRows = filterRowsBySearch(extendedRows, search);
  const isStakeholderDirectory = config?.key === "cybergrc_stakeholders";
  const canCreate = supportedViews.includes("create") && formFields.length;
  const contractRows = extendedRows
    .filter((row) => row.contract_end_date)
    .map((row) => ({
      ...row,
      days_remaining: differenceInDays(row.contract_end_date),
    }))
    .filter((row) => row.days_remaining >= 0 && row.days_remaining <= 90);
  const reportRows = activeMode === "report-contracts" ? contractRows : isReportMode(activeMode) ? filteredExtendedRows : rows;
  const displayColumns = isStakeholderDirectory
    ? [
        {
          key: "name",
          label: "Name",
          render: (row) => (
            <div className="flex items-center gap-2.5">
              <Folder size={16} strokeWidth={1.7} className="shrink-0 text-[#111111]" />
              <span className="text-[13px] font-medium text-[#222028]">{row.name || "—"}</span>
            </div>
          ),
        },
        {
          key: "stakeholder_type",
          label: "Stakeholder Type",
          render: (row) => <span className="text-[13px] font-medium text-[#222028]">{row.stakeholder_type?.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase()) || "—"}</span>,
        },
        {
          key: "sector",
          label: "Sector",
          render: (row) => <span className="text-[13px] font-medium text-[#222028]">{row.sector || "—"}</span>,
        },
        {
          key: "status",
          label: "Status",
          render: (row) => {
            const tone = getStakeholderStatusTone(row.status);
            const label = row.status?.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase()) || "—";
            return (
              <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold ${tone.badge}`}>
                <span className={`h-1.5 w-1.5 rounded-full ${tone.dot}`} />
                {label}
              </span>
            );
          },
        },
      ]
    : activeMode === "report-contracts"
      ? [
          ...(config?.columns || []).map((key) => ({
            key,
            label: key.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase()),
            render: (row) => {
              const value = row[key];
              if (typeof value === "boolean") return value ? "Yes" : "No";
              return value ?? "-";
            },
          })),
          {
            key: "days_remaining",
            label: "Days Remaining",
            render: (row) => `${row.days_remaining} jour${row.days_remaining > 1 ? "s" : ""}`,
          },
        ]
      : (config?.columns || []).map((key) => ({
          key,
          label: key.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase()),
          render: (row) => {
            const value = row[key];
            if (typeof value === "boolean") return value ? "Yes" : "No";
            return value ?? "-";
          },
        }));
  const shouldRenderTable = activeMode === "list" || activeMode === "search" || (isReportMode(activeMode) && !isOperationalReportMode);
  const showToolbar = !["create", "edit", "import"].includes(activeMode);
  const showCreateAction = activeMode === "list" && canCreate;
  const rowSelectionEnabled = activeMode === "list" || activeMode === "search";
  const showFormBreadcrumb = activeMode === "create" || activeMode === "edit";
  const formBreadcrumbLabel =
    activeMode === "edit"
      ? formPresentation?.editTitle || `Edit ${config.label.toLowerCase()}`
      : formPresentation?.createTitle || `Create ${config.label.toLowerCase()}`;

  useEffect(() => {
    setFormValues(buildInitialValues(formFields, editingItem));
    setFormErrors({});
  }, [formFields, editingItem]);

  useEffect(() => {
    setEditingItem(null);
    setFormErrors({});
    setSearch("");
    setPage(1);
    setPageSize(ENHANCED_PAGINATION_MODULE_KEYS.has(config?.key) ? ENHANCED_PAGINATION_DEFAULT_PAGE_SIZE : STANDARD_PAGE_SIZE);
    setSelectedRowIds([]);
    setPendingDeleteItem(null);
  }, [config?.key, routeModuleKey]);

  useEffect(() => {
    const availableIds = new Set(reportRows.map((row, rowIndex) => row.id ?? `${config?.key || routeModuleKey}-${rowIndex}`));
    setSelectedRowIds((current) => current.filter((rowId) => availableIds.has(rowId)));
  }, [config?.key, reportRows, routeModuleKey]);

  useEffect(() => {
    if (requestedMode !== "list" && !allowedModes.has(requestedMode)) {
      setSearchParams({});
    }
  }, [allowedModes, requestedMode, setSearchParams]);

  function setMode(mode = null) {
    setFormErrors({});
    if (!mode || mode === "list") {
      setSearchParams({});
      return;
    }
    setSearchParams({ mode });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setFormErrors({});
    const payload = serializePayload(formFields, formValues);

    try {
      if (editingItem?.id) {
        await updateMutation.mutateAsync({ id: editingItem.id, payload });
        setEditingItem(null);
      } else {
        await createMutation.mutateAsync(payload);
        setMode();
      }
    } catch (error) {
      setFormErrors(normalizeErrors(error));
    }
  }

  async function handleDelete() {
    if (!pendingDeleteItem?.id) return;
    await deleteMutation.mutateAsync(pendingDeleteItem.id);
    setPendingDeleteItem(null);
  }

  async function handleImport(records) {
    if (!records.length) return;

    setIsImporting(true);
    const failures = [];
    let successCount = 0;

    for (const record of records) {
      try {
        await api.post(config.endpoint, serializePayload(formFields, record));
        successCount += 1;
      } catch (error) {
        failures.push(normalizeErrors(error));
      }
    }

    await queryClient.invalidateQueries({ queryKey: [config.key] });
    setIsImporting(false);

    if (successCount) {
      notifySuccess(`${successCount} row${successCount > 1 ? "s" : ""} imported`);
    }

    if (failures.length) {
      const firstFailure = failures[0];
      const firstMessage =
        firstFailure.non_field_errors ||
        Object.entries(firstFailure)
          .map(([key, value]) => `${key}: ${value}`)
          .join(" | ");

      notifyError(`${failures.length} row${failures.length > 1 ? "s" : ""} failed${firstMessage ? ` (${firstMessage})` : ""}`);
      return;
    }

    setMode();
  }

  async function handleWorkflowTransition(item, nextValue) {
    if (!workflowField) return;
    await updateMutation.mutateAsync({ id: item.id, payload: { [workflowField]: nextValue } });
  }

  function getRowId(row, rowIndex) {
    return row.id ?? `${config?.key || routeModuleKey}-${rowIndex}`;
  }

  function handleToggleRow(rowId, checked) {
    setSelectedRowIds((current) => {
      if (checked) return [...new Set([...current, rowId])];
      return current.filter((item) => item !== rowId);
    });
  }

  function handleToggleAllRows(checked) {
    if (!checked) {
      setSelectedRowIds([]);
      return;
    }
    setSelectedRowIds(reportRows.map((row, rowIndex) => getRowId(row, rowIndex)));
  }

  if (!config) {
    return <EmptyState title="Module not found" description="This resource is not configured." />;
  }

  if (isLoading) {
    return <div className="app-surface-soft rounded-[28px] px-6 py-8 text-sm text-slate-500">Loading...</div>;
  }

  if (isListError) {
    return (
      <EmptyState
        title={`Unable to load ${modePresentation.pageTitle.toLowerCase()}`}
        description={getQueryErrorMessage(listError)}
      />
    );
  }

  return (
    <div className="space-y-6">
      {showFormBreadcrumb ? (
        <div className="mb-5 flex flex-wrap items-center gap-2 text-[13px] font-medium text-black/42">
          <Link to={`/modules/${config.route}`} className="transition hover:text-black">
            {config.label}
          </Link>
          <span className="text-black/24">/</span>
          <span className="text-black">{formBreadcrumbLabel}</span>
        </div>
      ) : (
        <PageHeader
          title={modePresentation.pageTitle}
          description={modePresentation.pageDescription}
          descriptionClassName="text-slate-950"
          eyebrow={SectionHeaderIcon ? <SectionHeaderIcon size={22} strokeWidth={2.25} /> : null}
        />
      )}

      {showToolbar ? (
        <DataToolbar
          search={search}
          setSearch={setSearch}
          onRefresh={shouldFetchExtendedRows && !isExtendedError ? refetchExtended : refetch}
          placeholder={modePresentation.searchPlaceholder}
          action={
            showCreateAction ? (
              <button
                onClick={() => {
                  setEditingItem(null);
                  setMode("create");
                }}
                className="app-button app-button-dark"
                style={{ paddingLeft: "1.55rem", paddingRight: "1.55rem" }}
              >
                <FiPlus size={16} className="text-white" />
                Add row
              </button>
            ) : null
          }
        />
      ) : null}

      {shouldRenderTable ? (
        <>
          {reportRows.length ? (
            <DataTable
              columns={displayColumns}
              rows={reportRows}
              variant={isStakeholderDirectory ? "stakeholder" : "default"}
              selectable={rowSelectionEnabled}
              selectedRowIds={selectedRowIds}
              onToggleRow={handleToggleRow}
              onToggleAll={handleToggleAllRows}
              getRowId={getRowId}
              rowActions={
                activeMode === "list" && formFields.length
                  ? (row) => (
                      <div className="flex justify-start gap-2">
                        <button
                          onClick={() => {
                            setEditingItem(row);
                            setFormErrors({});
                          }}
                          className="flex h-9 w-9 items-center justify-center text-[#111111] transition hover:text-black/70"
                          aria-label={`Edit ${row.name || config.label}`}
                        >
                          <FiEdit2 size={14} />
                        </button>
                        <button
                          onClick={() => setPendingDeleteItem(row)}
                          className="flex h-9 w-9 items-center justify-center text-[#fa695f] transition hover:text-[#f28c6d]"
                          aria-label={`Delete ${row.name || config.label}`}
                        >
                          <FiTrash2 size={14} />
                        </button>
                      </div>
                    )
                  : null
              }
            />
          ) : (
            <EmptyState title={`No data for ${modePresentation.pageTitle.toLowerCase()}`} />
          )}

          {activeMode === "list" || activeMode === "search" ? (
            <Pagination
              data={data}
              currentPage={page}
              pageSize={pageSize}
              showPageCounter
              showPageSizeSelector
              minTotalForSummary={6}
              minTotalForNext={10}
              onPageSizeChange={(nextPageSize) => {
                setPage(1);
                setPageSize(nextPageSize);
              }}
              onPageChange={(direction) => {
                if (direction === "previous" && page > 1) setPage(page - 1);
                if (direction === "next") setPage(page + 1);
              }}
            />
          ) : null}
        </>
      ) : null}

      {activeMode === "workflow" ? (
        <WorkflowBoard
          rows={filteredExtendedRows}
          workflowField={workflowField}
          workflowChoices={workflowChoices}
          columnKeys={config.columns || []}
          onEdit={(row) => {
            setEditingItem(row);
            setFormErrors({});
          }}
          onTransition={handleWorkflowTransition}
          updating={updateMutation.isPending}
          moduleLabel={config?.label}
          workflowBlueprint={workflowBlueprint}
        />
      ) : null}

      {isOperationalReportMode ? <OperationalReportView config={{ ...config, reportPreset }} rows={reportRows} columns={displayColumns} /> : null}

      {activeMode === "create" || activeMode === "edit" ? (
        <Create
          title={
            activeMode === "create"
              ? formPresentation?.createTitle || `Create ${config.label.toLowerCase()}`
              : formPresentation?.editTitle || `Edit ${config.label.toLowerCase()}`
          }
          description={
            activeMode === "create"
              ? formPresentation?.createDescription || `Fill in the information for ${config.label.toLowerCase()}.`
              : formPresentation?.editDescription || `Update the information for ${config.label.toLowerCase()}.`
          }
          fields={formFields}
          values={formValues}
          errors={formErrors}
          onChange={(name, value) => setFormValues((current) => ({ ...current, [name]: value }))}
          onSubmit={handleSubmit}
          onCancel={() => {
            setEditingItem(null);
            setFormErrors({});
            setMode();
          }}
          submitLabel={activeMode === "create" ? "Create" : "Update"}
          loading={createMutation.isPending || updateMutation.isPending}
          presentation={formPresentation}
          showBackButton={!showFormBreadcrumb}
        />
      ) : null}

      {activeMode === "import" ? (
        <Import
          title={`Import ${config.label.toLowerCase()}`}
          description={`Upload a CSV file to create multiple ${config.label.toLowerCase()} at once.`}
          fields={formFields}
          loading={isImporting}
          onImport={handleImport}
          onCancel={() => setMode()}
        />
      ) : null}

      {activeMode === "map" ? (
        <MapView title={`Map of ${config.label.toLowerCase()}`} description={`Operational map of ${config.label.toLowerCase()} with usable coordinates.`} rows={filteredExtendedRows} />
      ) : null}

      <ConfirmDialog
        isOpen={Boolean(pendingDeleteItem)}
        title={`Delete ${config.label.toLowerCase()}`}
        description={`This action will permanently remove ${pendingDeleteItem?.name || pendingDeleteItem?.title || "this record"}. Make sure you no longer need to keep it in the list.`}
        confirmLabel="Delete"
        loading={deleteMutation.isPending}
        onClose={() => {
          if (deleteMutation.isPending) return;
          setPendingDeleteItem(null);
        }}
        onConfirm={handleDelete}
      />
    </div>
  );
}




