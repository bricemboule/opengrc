import { useEffect, useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { FiEdit2, FiPlus, FiTrash2 } from "react-icons/fi";
import { useSearchParams } from "react-router-dom";
import PageHeader from "../components/crud/PageHeader";
import DataTable from "../components/crud/DataTable";
import DataToolbar from "../components/crud/DataToolbar";
import Pagination from "../components/crud/Pagination";
import EmptyState from "../components/crud/EmptyState";
import Create from "../components/crud/Create";
import Import from "../components/crud/Import";
import MapView from "../components/crud/MapView";
import {
  buildFieldList,
  buildInitialValues,
  normalizeErrors,
  serializePayload,
} from "../components/crud/crudUtils";
import usePaginatedList from "../hooks/usePaginatedList";
import { useCreateItem, useDeleteItem, useUpdateItem } from "../hooks/useCrudMutations";
import { moduleConfigs } from "../config/modules";
import api from "../api/client";
import { notifyError, notifySuccess } from "../utils/toast";

function buildAllowedModes(config, formFields) {
  const configuredViews = config?.views || [];
  const modes = new Set(["list", ...configuredViews]);

  if (formFields.length) {
    modes.add("create");
  }

  return modes;
}

function isReportMode(mode) {
  return String(mode || "").startsWith("report");
}

function isTableMode(mode) {
  return mode === "list" || mode === "search" || isReportMode(mode);
}

function differenceInDays(targetDate) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const target = new Date(targetDate);
  target.setHours(0, 0, 0, 0);
  return Math.round((target.getTime() - today.getTime()) / 86400000);
}

function filterRowsBySearch(rows, search) {
  const normalized = String(search || "").trim().toLowerCase();
  if (!normalized) return rows;

  return rows.filter((row) =>
    Object.values(row || {}).some((value) => String(value ?? "").toLowerCase().includes(normalized)),
  );
}

function getModePresentation(config, activeMode) {
  const key = `${config?.key}:${activeMode}`;

  switch (key) {
    case "staff_skills:search":
      return {
        pageTitle: "Search by Skills",
        pageDescription: "Recherche du personnel par compétence à partir du catalogue de compétences.",
        searchPlaceholder: "Rechercher une compétence ou un membre du personnel...",
      };
    case "team_members:search":
      return {
        pageTitle: "Search Members",
        pageDescription: "Recherche des membres d’équipe par nom, équipe ou rôle.",
        searchPlaceholder: "Rechercher un membre ou une équipe...",
      };
    case "training_participants:search":
      return {
        pageTitle: "Search Training Participants",
        pageDescription: "Recherche des participants aux formations par session ou par membre du personnel.",
        searchPlaceholder: "Rechercher une formation ou un participant...",
      };
    case "staffs:report-staff":
      return {
        pageTitle: "Staff Report",
        pageDescription: "Rapport consolidé du personnel enregistré dans l’organisation.",
        searchPlaceholder: "Filtrer le rapport du personnel...",
      };
    case "staffs:report-contracts":
      return {
        pageTitle: "Expiring Staff Contracts Report",
        pageDescription: "Suivi des contrats arrivant à échéance dans les 90 prochains jours.",
        searchPlaceholder: "Filtrer le rapport des contrats...",
      };
    case "training_participants:report-training":
      return {
        pageTitle: "Training Report",
        pageDescription: "Rapport des participants, statuts de complétion et délivrance des certificats.",
        searchPlaceholder: "Filtrer le rapport de formation...",
      };
    default:
      return {
        pageTitle: config?.label,
        pageDescription: `Gestion de ${config?.label?.toLowerCase()}`,
        searchPlaceholder: "Rechercher...",
      };
  }
}

export default function ModuleListPage({ moduleKey: routeModuleKey }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [editingItem, setEditingItem] = useState(null);
  const [formValues, setFormValues] = useState({});
  const [formErrors, setFormErrors] = useState({});
  const [isImporting, setIsImporting] = useState(false);
  const queryClient = useQueryClient();

  const config = moduleConfigs.find((item) => item.route === routeModuleKey);
  const { data, isLoading, refetch } = usePaginatedList(config?.key || routeModuleKey, config?.endpoint || "/", {
    search,
    page,
    ordering: "-created_at",
  });

  const { data: metadata } = useQuery({
    queryKey: [config?.key, "metadata"],
    queryFn: async () => (await api.options(config.endpoint)).data,
    enabled: Boolean(config?.endpoint),
  });

  const createMutation = useCreateItem(config?.key, config?.endpoint, `${config?.label} cree`);
  const updateMutation = useUpdateItem(config?.key, config?.endpoint, `${config?.label} mis a jour`);
  const deleteMutation = useDeleteItem(config?.key, config?.endpoint, `${config?.label} supprime`);

  const formFields = useMemo(() => buildFieldList(config, metadata), [config, metadata]);
  const allowedModes = useMemo(() => buildAllowedModes(config, formFields), [config, formFields]);
  const requestedMode = searchParams.get("mode") || "list";
  const activeMode = editingItem ? "edit" : allowedModes.has(requestedMode) ? requestedMode : "list";
  const rows = data?.results || data || [];
  const modePresentation = useMemo(() => getModePresentation(config, activeMode), [activeMode, config]);
  const needsExtendedRows = activeMode === "map" || isReportMode(activeMode);

  const { data: extendedData, refetch: refetchExtended } = useQuery({
    queryKey: [config?.key, activeMode, "extended"],
    queryFn: async () => {
      const ordering = activeMode === "report-contracts" ? "contract_end_date" : "-created_at";
      const response = await api.get(config.endpoint, { params: { ordering, page_size: 200 } });
      return response.data;
    },
    enabled: Boolean(config?.endpoint) && needsExtendedRows,
  });

  const columns = useMemo(
    () =>
      (config?.columns || []).map((key) => ({
        key,
        label: key.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase()),
        render: (row) => {
          const value = row[key];
          if (typeof value === "boolean") return value ? "Oui" : "Non";
          return value ?? "—";
        },
      })),
    [config],
  );

  useEffect(() => {
    setFormValues(buildInitialValues(formFields, editingItem));
    setFormErrors({});
  }, [formFields, editingItem]);

  useEffect(() => {
    setEditingItem(null);
    setFormErrors({});
    setPage(1);
  }, [routeModuleKey]);

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

  async function handleDelete(item) {
    if (!window.confirm(`Supprimer ${config.label.toLowerCase()} ?`)) return;
    await deleteMutation.mutateAsync(item.id);
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
      notifySuccess(`${successCount} ligne${successCount > 1 ? "s" : ""} importée${successCount > 1 ? "s" : ""}`);
    }

    if (failures.length) {
      const firstFailure = failures[0];
      const firstMessage =
        firstFailure.non_field_errors ||
        Object.entries(firstFailure)
          .map(([key, value]) => `${key}: ${value}`)
          .join(" | ");

      notifyError(`${failures.length} ligne${failures.length > 1 ? "s" : ""} en échec${firstMessage ? ` (${firstMessage})` : ""}`);
      return;
    }

    setMode();
  }

  if (!config) {
    return <EmptyState title="Module introuvable" description="Cette ressource n'est pas configurée." />;
  }

  if (isLoading) {
    return <p>Chargement...</p>;
  }

  const extendedRows = extendedData?.results || extendedData || rows;
  const mapRows = extendedRows;
  const canCreate = allowedModes.has("create") && formFields.length;
  const contractRows = extendedRows
    .filter((row) => row.contract_end_date)
    .map((row) => ({
      ...row,
      days_remaining: differenceInDays(row.contract_end_date),
    }))
    .filter((row) => row.days_remaining >= 0 && row.days_remaining <= 90);
  const reportRows =
    activeMode === "report-contracts"
      ? contractRows
      : isReportMode(activeMode)
        ? extendedRows
        : rows;
  const displayRows = isReportMode(activeMode) ? filterRowsBySearch(reportRows, search) : reportRows;
  const displayColumns =
    activeMode === "report-contracts"
      ? [
          ...columns,
          {
            key: "days_remaining",
            label: "Days Remaining",
            render: (row) => `${row.days_remaining} jour${row.days_remaining > 1 ? "s" : ""}`,
          },
        ]
      : columns;
  const showCreateAction = activeMode === "list" && canCreate;

  return (
    <div>
      <PageHeader title={modePresentation.pageTitle} description={modePresentation.pageDescription} />

      {isTableMode(activeMode) ? (
        <>
          <DataToolbar
            search={search}
            setSearch={setSearch}
            onRefresh={needsExtendedRows ? refetchExtended : refetch}
            placeholder={modePresentation.searchPlaceholder}
            action={
              showCreateAction ? (
                <button
                  onClick={() => {
                    setEditingItem(null);
                    setMode("create");
                  }}
                  className="inline-flex items-center gap-2 rounded-2xl bg-[#0C1C8C] px-4 py-2 text-sm font-medium text-white"
                >
                  <FiPlus size={16} />
                  Ajouter
                </button>
              ) : null
            }
          />

          {displayRows.length ? (
            <DataTable
              columns={displayColumns}
              rows={displayRows}
              rowActions={
                activeMode === "list" && formFields.length
                  ? (row) => (
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => {
                            setEditingItem(row);
                            setFormErrors({});
                          }}
                          className="inline-flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-2 text-xs font-medium"
                        >
                          <FiEdit2 size={14} />
                          Modifier
                        </button>
                        <button
                          onClick={() => handleDelete(row)}
                          className="inline-flex items-center gap-2 rounded-xl bg-[#CE1126] px-3 py-2 text-xs font-medium text-white"
                        >
                          <FiTrash2 size={14} />
                          Supprimer
                        </button>
                      </div>
                    )
                  : null
              }
            />
          ) : (
            <EmptyState title={`Aucune donnée pour ${modePresentation.pageTitle.toLowerCase()}`} />
          )}

          {activeMode === "list" || activeMode === "search" ? (
            <Pagination
              data={data}
              onPageChange={(direction) => {
                if (direction === "previous" && page > 1) setPage(page - 1);
                if (direction === "next") setPage(page + 1);
              }}
            />
          ) : null}
        </>
      ) : null}

      {activeMode === "create" || activeMode === "edit" ? (
        <Create
          title={activeMode === "create" ? `Créer ${config.label.toLowerCase()}` : `Modifier ${config.label.toLowerCase()}`}
          description={
            activeMode === "create"
              ? `Renseigne les informations de ${config.label.toLowerCase()}.`
              : `Mets à jour les informations de ${config.label.toLowerCase()}.`
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
          submitLabel={activeMode === "create" ? "Créer" : "Mettre à jour"}
          loading={createMutation.isPending || updateMutation.isPending}
        />
      ) : null}

      {activeMode === "import" ? (
        <Import
          title={`Importer ${config.label.toLowerCase()}`}
          description={`Charge un fichier CSV pour créer plusieurs ${config.label.toLowerCase()} en une fois.`}
          fields={formFields}
          loading={isImporting}
          onImport={handleImport}
          onCancel={() => setMode()}
        />
      ) : null}

      {activeMode === "map" ? (
        <MapView
          title={`Carte des ${config.label.toLowerCase()}`}
          description={`Visualisation des ${config.label.toLowerCase()} disposant de coordonnées.`}
          rows={mapRows}
        />
      ) : null}
    </div>
  );
}
