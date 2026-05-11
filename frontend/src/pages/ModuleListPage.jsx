import { useEffect, useMemo, useState } from "react";
import { useQueries, useQuery, useQueryClient } from "@tanstack/react-query";
import { Activity, AlertCircle, ClipboardList, Download, FileText, Folder, MapPin, Settings, Shield, Target } from "lucide-react";
import { FiEdit2, FiPlus, FiTrash2 } from "react-icons/fi";
import { Link, useSearchParams } from "react-router-dom";
import PageHeader from "../components/crud/PageHeader";
import DataTable from "../components/crud/DataTable";
import DataToolbar from "../components/crud/DataToolbar";
import Pagination from "../components/crud/Pagination";
import EmptyState from "../components/crud/EmptyState";
import Create from "../components/crud/Create";
import ConfirmDialog from "../components/crud/ConfirmDialog";
import ConsultationCalendarView from "../components/crud/ConsultationCalendarView";
import Import from "../components/crud/Import";
import MapView from "../components/crud/MapView";
import OperationalReportView from "../components/crud/OperationalReportView";
import SopExecutionView from "../components/incident/SopExecutionView";
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
  "asset_inventory_items",
  "threat_events",
  "vulnerability_records",
  "risk_scenarios",
  "risk_assessment_reviews",
  "threat_bulletins",
  "indicators",
  "distribution_groups",
  "information_shares",
  "acknowledgements",
  "generated_documents",
  "review_cycles",
  "review_records",
  "change_log_entries",
  "capacity_assessments",
  "training_programs",
  "contingency_plans",
  "emergency_response_assets",
  "simulation_exercises",
  "cyber_standards",
  "standard_requirements",
  "standard_controls",
  "conformity_assessments",
  "control_evidence",
  "audit_frameworks",
  "audit_plans",
  "audit_checklists",
  "audit_findings",
  "non_conformities",
  "corrective_actions",
  "deliverable_milestones",
  "action_plan_tasks",
  "incidents",
  "incident_updates",
  "incident_tasks",
  "incident_assignments",
  "incident_communications",
  "incident_attachments",
  "sop_templates",
  "sop_steps",
  "sop_executions",
  "asset_allocations",
]);
const ENHANCED_PAGINATION_DEFAULT_PAGE_SIZE = 10;
const STANDARD_PAGE_SIZE = 20;
const RELATION_OPTION_PAGE_SIZE = 200;
const RELATION_OPTION_MAX_PAGES = 5;
const SETTINGS_ONLY_FORM_MODULE_KEYS = new Set(["users", "roles", "sectors", "organizations", "organization_types", "asset_types", "assets"]);
const INFRASTRUCTURE_DEPENDENT_FIELDS = {
  asset_item: "related_infrastructure",
  related_threat_event: "related_infrastructure",
  vulnerability_record: "related_infrastructure",
  risk_register_entry: "infrastructure",
};

function getExtendedPageSize(activeMode, pageSize) {
  const baseline = ["workflow", "calendar"].includes(activeMode) ? 80 : 60;
  return Math.max(pageSize || 0, baseline);
}

function resolveRelationOptionLabel(item, labelField) {
  if (labelField && item?.[labelField]) return item[labelField];

  return item?.name || item?.title || item?.code || item?.label || (item?.id ? `#${item.id}` : "");
}

function getRelationIdentity(item, fieldName) {
  if (!item || !fieldName) return null;
  const value = item[fieldName] ?? item[`${fieldName}_id`];
  if (value && typeof value === "object") return value.id ?? value.value ?? null;
  return value ?? null;
}

async function fetchRelationChoices(relation) {
  if (!relation?.endpoint) return [];

  const choices = [];

  for (let pageIndex = 1; pageIndex <= RELATION_OPTION_MAX_PAGES; pageIndex += 1) {
    const response = await api.get(relation.endpoint, {
      params: {
        page: pageIndex,
        page_size: RELATION_OPTION_PAGE_SIZE,
        ordering: relation.ordering || relation.labelField || "name",
      },
    });
    const payload = response.data;
    const results = Array.isArray(payload?.results) ? payload.results : Array.isArray(payload) ? payload : [];

    choices.push(
      ...results
        .filter((item) => item?.id != null)
        .map((item) => ({
          value: item.id,
          display_name: resolveRelationOptionLabel(item, relation.labelField),
          related_infrastructure: getRelationIdentity(item, "related_infrastructure"),
          infrastructure: getRelationIdentity(item, "infrastructure"),
        })),
    );

    if (!payload?.next || !Array.isArray(payload?.results)) break;
  }

  return choices;
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
  if (["incidents", "incident_updates", "incident_tasks", "incident_assignments", "incident_communications", "incident_attachments", "sop_templates", "sop_steps", "sop_executions", "asset_allocations"].includes(moduleKey)) return AlertCircle;
  if (["cybergrc_stakeholders", "desk_study_reviews", "stakeholder_consultations", "critical_infrastructure", "governance_artifacts", "asset_inventory_items"].includes(moduleKey)) return MapPin;
  if (["risk_register_entries", "threat_events", "vulnerability_records", "risk_scenarios", "risk_assessment_reviews", "capacity_assessments", "training_programs"].includes(moduleKey)) return Activity;
  if (["threat_bulletins", "indicators", "distribution_groups", "information_shares", "acknowledgements"].includes(moduleKey)) return Folder;
  if (["generated_documents", "review_cycles", "review_records", "change_log_entries"].includes(moduleKey)) return FileText;
  if (["contingency_plans", "emergency_response_assets", "simulation_exercises"].includes(moduleKey)) return Target;
  if (["cyber_standards", "standard_requirements", "standard_controls", "conformity_assessments", "control_evidence", "audit_frameworks", "audit_plans", "audit_checklists", "audit_findings", "non_conformities", "corrective_actions"].includes(moduleKey)) return Shield;
  if (["deliverable_milestones", "action_plan_tasks"].includes(moduleKey)) return ClipboardList;
  return null;
}

function getModuleFormEyebrow(moduleKey) {
  if (["incidents", "incident_updates", "incident_tasks", "incident_assignments", "incident_communications", "incident_attachments", "sop_templates", "sop_steps", "sop_executions", "asset_allocations"].includes(moduleKey)) return "Incident Operations";
  if (["cybergrc_stakeholders", "desk_study_reviews", "stakeholder_consultations", "critical_infrastructure", "governance_artifacts", "asset_inventory_items"].includes(moduleKey)) return "Governance & Mapping";
  if (["risk_register_entries", "threat_events", "vulnerability_records", "risk_scenarios", "risk_assessment_reviews", "capacity_assessments", "training_programs"].includes(moduleKey)) return "Risk & Capacity";
  if (["threat_bulletins", "indicators", "distribution_groups", "information_shares", "acknowledgements"].includes(moduleKey)) return "Threat & Sharing";
  if (["generated_documents", "review_cycles", "review_records", "change_log_entries"].includes(moduleKey)) return "Documents & Review";
  if (["contingency_plans", "emergency_response_assets", "simulation_exercises"].includes(moduleKey)) return "Contingency Planning";
  if (["cyber_standards", "standard_requirements", "standard_controls", "conformity_assessments", "control_evidence", "audit_frameworks", "audit_plans", "audit_checklists", "audit_findings", "non_conformities", "corrective_actions"].includes(moduleKey)) return "Standards & Audit";
  if (["deliverable_milestones", "action_plan_tasks"].includes(moduleKey)) return "Delivery Tracking";
  return "Cyber GRC";
}

function formatChoiceLabel(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/(^|\s)\w/g, (character) => character.toUpperCase());
}

function resolveChoiceDisplayValue(field, value) {
  if (value === null || value === undefined || value === "") return value;
  if (!field?.choices?.length) return value;

  const matchedChoice = field.choices.find((choice) => String(choice?.value) === String(value));
  return matchedChoice?.display_name || formatChoiceLabel(value);
}

function getQueryErrorMessage(error, fallback = "An error occurred while loading the data.") {
  const payload = error?.response?.data;
  if (typeof payload === "string" && payload.trim()) return payload;
  if (payload?.detail) return String(payload.detail);
  if (payload?.message) return String(payload.message);
  return error?.message || fallback;
}

function extractFilenameFromDisposition(disposition) {
  const match = String(disposition || "").match(/filename=\"?([^\";]+)\"?/i);
  return match?.[1] || "";
}

function downloadBlobResponse(response, fallbackFilename) {
  const filename = extractFilenameFromDisposition(response.headers?.["content-disposition"]) || fallbackFilename;
  const objectUrl = window.URL.createObjectURL(response.data);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(objectUrl);
}

function buildGeneratedDocumentFilename(row) {
  const extension =
    row?.output_format === "pdf"
      ? "pdf"
      : row?.output_format === "docx"
        ? "docx"
        : row?.output_format === "json"
          ? "json"
          : row?.output_format === "markdown"
            ? "md"
            : "txt";

  return `${String(row?.title || "generated_document").replace(/\s+/g, "_")}.${extension}`;
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

  if (activeMode === "calendar") {
    return {
      pageTitle: getViewLabel(config, "calendar"),
      pageDescription: `Track upcoming meetings, calls, and follow-up actions for ${config?.label?.toLowerCase()}.`,
      searchPlaceholder: `Filter ${config?.label?.toLowerCase()} calendar...`,
    };
  }

  if (activeMode === "execute") {
    return {
      pageTitle: getViewLabel(config, "execute"),
      pageDescription: `Run the active checklist, unblock delayed steps, and keep ${config?.label?.toLowerCase()} execution current.`,
      searchPlaceholder: `Filter ${config?.label?.toLowerCase()} executions...`,
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
  const [isGeneratingDocument, setIsGeneratingDocument] = useState(false);
  const [documentFormat, setDocumentFormat] = useState("pdf");
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

  const baseFormFields = useMemo(() => buildFieldList(config, metadata), [config, metadata]);
  const relationFields = useMemo(() => baseFormFields.filter((field) => field.relation?.endpoint), [baseFormFields]);
  const relationQueries = useQueries({
    queries: relationFields.map((field) => ({
      queryKey: [config?.key, "relation-options", field.name, field.relation?.endpoint],
      queryFn: async () => fetchRelationChoices(field.relation),
      enabled: Boolean(field.relation?.endpoint) && shouldLoadMetadata,
      staleTime: 60000,
      refetchOnWindowFocus: false,
    })),
  });
  const formFields = useMemo(() => {
    if (!relationFields.length) return baseFormFields;

    const relationStates = new Map(
      relationFields.map((field, index) => [field.name, relationQueries[index] || {}]),
    );
    const selectedInfrastructureId = formValues.related_infrastructure || formValues.infrastructure;

    return baseFormFields.map((field) => {
      if (!field.relation?.endpoint) return field;

      const relationState = relationStates.get(field.name) || {};
      const dependencyRelationName = INFRASTRUCTURE_DEPENDENT_FIELDS[field.name];
      const relationChoices = dependencyRelationName && selectedInfrastructureId
        ? (relationState.data || []).filter((choice) => String(choice[dependencyRelationName] || "") === String(selectedInfrastructureId))
        : relationState.data || [];
      const relationPlaceholder = relationState.isLoading
        ? `Loading ${String(field.label || field.name || "options").toLowerCase()}...`
        : relationState.isError
          ? `Unable to load ${String(field.label || field.name || "options").toLowerCase()}`
          : dependencyRelationName && selectedInfrastructureId && !relationChoices.length
            ? "No matching records for the selected infrastructure"
            : field.placeholder;

      return {
        ...field,
        type: field.type === "multirelation" ? "multirelation" : "relation",
        choices: relationChoices,
        placeholder: relationPlaceholder,
        relationLoading: Boolean(relationState.isLoading),
        relationError: Boolean(relationState.isError),
      };
    });
  }, [baseFormFields, formValues.infrastructure, formValues.related_infrastructure, relationFields, relationQueries]);
  const modePresentation = useMemo(() => getModePresentation(config, activeMode), [activeMode, config]);
  const SectionHeaderIcon = useMemo(() => getModuleSectionIcon(config?.key), [config?.key]);
  const baseFormPresentation = useMemo(() => getFormPresentation(config), [config]);
  const workflowBlueprint = useMemo(() => getWorkflowBlueprint(config), [config]);
  const formIcon = useMemo(() => {
    if (SETTINGS_ONLY_FORM_MODULE_KEYS.has(config?.key)) {
      return <Settings size={18} strokeWidth={2.15} />;
    }

    return SectionHeaderIcon ? <SectionHeaderIcon size={18} strokeWidth={2.15} /> : null;
  }, [SectionHeaderIcon, config?.key]);
  const formPresentation = useMemo(
    () => ({
      variant: "editorial",
      eyebrow: getModuleFormEyebrow(config?.key),
      sectionLabel: `${config?.label || "Record"} file`,
      ...(baseFormPresentation || {}),
      icon: formIcon,
      mode: activeMode,
    }),
    [activeMode, baseFormPresentation, config?.key, config?.label, formIcon],
  );
  const workflowField = moduleBehavior.workflowField || formFields.find((field) => ["status", "mapping_status", "treatment_status", "availability_status"].includes(field.name))?.name || null;
  const workflowFieldConfig = formFields.find((field) => field.name === workflowField);
  const workflowChoices = workflowFieldConfig?.choices || [];
  const reportPreset = moduleBehavior.reportPreset;
  const isOperationalReportMode = activeMode === "report" && Boolean(reportPreset);
  const needsExtendedRows = activeMode === "map" || activeMode === "workflow" || activeMode === "calendar" || activeMode === "execute" || isReportMode(activeMode);
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
            const field = formFields.find((item) => item.name === key);
            if (typeof value === "boolean") return value ? "Yes" : "No";
            if (Array.isArray(value)) return value.length ? value.join(", ") : "-";
            return resolveChoiceDisplayValue(field, value) ?? "-";
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

  const formFieldSignature = useMemo(() => baseFormFields.map((field) => field.name).join("|"), [baseFormFields]);

  useEffect(() => {
    setFormValues(buildInitialValues(formFields, editingItem));
    setFormErrors({});
  }, [editingItem, formFieldSignature]);

  useEffect(() => {
    setFormValues((currentValues) => {
      let nextValues = currentValues;

      formFields.forEach((field) => {
        if (!INFRASTRUCTURE_DEPENDENT_FIELDS[field.name] || !currentValues[field.name] || field.relationLoading || field.relationError) return;
        const hasSelectedChoice = (field.choices || []).some((choice) => String(choice.value) === String(currentValues[field.name]));

        if (!hasSelectedChoice) {
          nextValues = nextValues === currentValues ? { ...currentValues } : nextValues;
          nextValues[field.name] = "";
        }
      });

      return nextValues;
    });
  }, [formFields]);

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

  async function handleGenerateReportDocument() {
    if (!config?.key || !reportRows.length) return;

    setIsGeneratingDocument(true);
    try {
      const response = await api.post("/cybergrc/generated-documents/generate-report/", {
        module_key: config.key,
        module_label: config.label,
        report_preset: reportPreset,
        title: `${config.label} report`,
        output_format: documentFormat,
        rows: reportRows,
        columns: displayColumns.map((column) => ({ key: column.key, label: column.label })),
        search,
      });
      if (response.data?.id) {
        const downloadResponse = await api.get(`/cybergrc/generated-documents/${response.data.id}/download/`, {
          responseType: "blob",
        });
        downloadBlobResponse(downloadResponse, buildGeneratedDocumentFilename(response.data));
      }
      await queryClient.invalidateQueries({ queryKey: ["generated_documents"] });
      notifySuccess(`Document generated and downloaded in ${documentFormat.toUpperCase()}: ${response.data?.title || `${config.label} report`}`);
    } catch (error) {
      notifyError(getQueryErrorMessage(error, "Unable to generate the report document."));
    } finally {
      setIsGeneratingDocument(false);
    }
  }

  async function handleDownloadGeneratedDocument(row) {
    if (!row?.id) return;

    try {
      const response = await api.get(`/cybergrc/generated-documents/${row.id}/download/`, {
        responseType: "blob",
      });
      downloadBlobResponse(response, buildGeneratedDocumentFilename(row));
    } catch (error) {
      notifyError(getQueryErrorMessage(error, "Unable to download this document."));
    }
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
                        {config.key === "generated_documents" ? (
                          <button
                            onClick={() => handleDownloadGeneratedDocument(row)}
                            className="flex h-9 w-9 items-center justify-center text-[#111111] transition hover:text-black/70"
                            aria-label={`Download ${row.title || config.label}`}
                          >
                            <Download size={14} strokeWidth={2} />
                          </button>
                        ) : null}
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

      {isOperationalReportMode ? (
        <OperationalReportView
          config={{ ...config, reportPreset }}
          rows={reportRows}
          columns={displayColumns}
          onGenerateDocument={config.key !== "generated_documents" ? handleGenerateReportDocument : null}
          isGeneratingDocument={isGeneratingDocument}
          documentFormat={documentFormat}
          onDocumentFormatChange={setDocumentFormat}
          rowActions={
            config.key === "generated_documents"
              ? (row) => (
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => handleDownloadGeneratedDocument(row)}
                      className="inline-flex h-8 items-center gap-1 rounded-full bg-[#111111] px-3.5 text-[11px] font-semibold text-white transition hover:bg-black/84"
                    >
                      <Download size={12} strokeWidth={2} />
                      Download
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setEditingItem(row);
                        setFormErrors({});
                      }}
                      className="inline-flex h-8 items-center rounded-full bg-[#f3efe8] px-3.5 text-[11px] font-semibold text-[#111111] transition hover:bg-[#ece6dc]"
                    >
                      Open
                    </button>
                  </div>
                )
              : null
          }
        />
      ) : null}

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
        <MapView
          title={`Map of ${config.label.toLowerCase()}`}
          description={`Operational map of ${config.label.toLowerCase()} with usable coordinates.`}
          rows={filteredExtendedRows}
          endpoint={config.endpoint}
          search={search}
        />
      ) : null}

      {activeMode === "calendar" ? <ConsultationCalendarView rows={filteredExtendedRows} /> : null}

      {activeMode === "execute" ? (
        <SopExecutionView
          rows={filteredExtendedRows}
          workflowChoices={workflowChoices}
          onEdit={(row) => {
            setEditingItem(row);
            setFormErrors({});
          }}
          onRefresh={async () => {
            await refetch();
            if (shouldFetchExtendedRows) {
              await refetchExtended();
            }
          }}
        />
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
