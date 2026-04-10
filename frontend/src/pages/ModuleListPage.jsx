import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { FiEdit2, FiPlus, FiTrash2 } from "react-icons/fi";
import PageHeader from "../components/crud/PageHeader";
import DataTable from "../components/crud/DataTable";
import DataToolbar from "../components/crud/DataToolbar";
import Pagination from "../components/crud/Pagination";
import EmptyState from "../components/crud/EmptyState";
import Create from "../components/crud/Create";
import usePaginatedList from "../hooks/usePaginatedList";
import { useCreateItem, useDeleteItem, useUpdateItem } from "../hooks/useCrudMutations";
import { moduleConfigs } from "../config/modules";
import api from "../api/client";

const HIDDEN_FIELDS = new Set([
  "id",
  "is_deleted",
  "created_at",
  "updated_at",
  "created_by",
  "updated_by",
  "created_by_email",
  "updated_by_email",
  "organization_name",
  "site_name",
  "person_name",
  "project_name",
  "activity_name",
  "contact_person_name",
  "assigned_to_name",
]);

function buildFieldList(config, metadata) {
  const postFields = metadata?.actions?.POST || {};
  const preferred = config?.formFields || [];
  const allNames = preferred.length ? preferred.filter((name) => postFields[name]) : Object.keys(postFields);
  const remaining = preferred.length ? [] : Object.keys(postFields);
  return [...allNames, ...remaining]
    .filter((name, index, array) => array.indexOf(name) === index)
    .map((name) => ({ name, ...postFields[name] }))
    .filter((field) => !field.read_only && !HIDDEN_FIELDS.has(field.name));
}

function buildInitialValues(fields, item = null) {
  return fields.reduce((acc, field) => {
    if (item) {
      const value = item[field.name];
      if (field.type === "boolean") acc[field.name] = Boolean(value);
      else acc[field.name] = value ?? "";
    } else if (field.type === "boolean") {
      acc[field.name] = Boolean(field.default);
    } else {
      acc[field.name] = field.default ?? "";
    }
    return acc;
  }, {});
}

function normalizeErrors(error) {
  const payload = error?.response?.data;
  if (!payload || typeof payload !== "object") return {};
  return Object.entries(payload).reduce((acc, [key, value]) => {
    acc[key] = Array.isArray(value) ? value.join(" ") : String(value);
    return acc;
  }, {});
}

function resolveChoiceValue(field, rawValue) {
  if (rawValue === "") return rawValue;
  const choices = field.choices || [];
  const matched = choices.find((choice) => String(choice.value) === String(rawValue));
  return matched ? matched.value : rawValue;
}

function serializePayload(fields, values) {
  return fields.reduce((acc, field) => {
    const rawValue = values[field.name];
    if (field.type === "boolean") {
      acc[field.name] = Boolean(rawValue);
      return acc;
    }
    if (rawValue === "") {
      acc[field.name] = field.required ? "" : null;
      return acc;
    }
    if (field.choices?.length) {
      acc[field.name] = resolveChoiceValue(field, rawValue);
      return acc;
    }
    if (["integer"].includes(field.type)) {
      acc[field.name] = Number.parseInt(rawValue, 10);
      return acc;
    }
    if (["decimal", "float", "number"].includes(field.type)) {
      acc[field.name] = Number.parseFloat(rawValue);
      return acc;
    }
    acc[field.name] = rawValue;
    return acc;
  }, {});
}

export default function ModuleListPage({ moduleKey: routeModuleKey }) {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [activeForm, setActiveForm] = useState(null);
  const [editingItem, setEditingItem] = useState(null);
  const [formValues, setFormValues] = useState({});
  const [formErrors, setFormErrors] = useState({});
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
  const columns = useMemo(() => (config?.columns || []).map((key) => ({
    key,
    label: key.replaceAll("_", " ").replace(/(^|\s)\w/g, (c) => c.toUpperCase()),
    render: (row) => {
      const value = row[key];
      if (typeof value === "boolean") return value ? "Oui" : "Non";
      return value ?? "—";
    },
  })), [config]);

  useEffect(() => {
    setFormValues(buildInitialValues(formFields, editingItem));
    setFormErrors({});
  }, [formFields, editingItem]);

  async function handleSubmit(event) {
    event.preventDefault();
    setFormErrors({});
    const payload = serializePayload(formFields, formValues);
    try {
      if (editingItem?.id) {
        await updateMutation.mutateAsync({ id: editingItem.id, payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
      setActiveForm(null);
      setEditingItem(null);
    } catch (error) {
      setFormErrors(normalizeErrors(error));
    }
  }

  async function handleDelete(item) {
    if (!window.confirm(`Supprimer ${config.label.toLowerCase()} ?`)) return;
    await deleteMutation.mutateAsync(item.id);
  }

  if (!config) return <EmptyState title="Module introuvable" description="Cette ressource n'est pas configurée." />;
  if (isLoading) return <p>Chargement...</p>;
  const rows = data?.results || data || [];
  return (
    <div>
      <PageHeader title={config.label} description={`Gestion de ${config.label.toLowerCase()}`} />
      <DataToolbar
        search={search}
        setSearch={setSearch}
        onRefresh={refetch}
        action={
          formFields.length && !activeForm ? (
            <button
              onClick={() => {
                setEditingItem(null);
                setActiveForm("create");
              }}
              className="inline-flex items-center gap-2 rounded-2xl bg-[#0C1C8C] px-4 py-2 text-sm font-medium text-white"
            >
              <FiPlus size={16} />
              Ajouter
            </button>
          ) : null
        }
      />
      {activeForm ? (
        <Create
          title={activeForm === "create" ? `Créer ${config.label.toLowerCase()}` : `Modifier ${config.label.toLowerCase()}`}
          description={activeForm === "create" ? `Renseigne les informations de ${config.label.toLowerCase()}.` : `Mets à jour les informations de ${config.label.toLowerCase()}.`}
          fields={formFields}
          values={formValues}
          errors={formErrors}
          onChange={(name, value) => setFormValues((current) => ({ ...current, [name]: value }))}
          onSubmit={handleSubmit}
          onCancel={() => {
            setActiveForm(null);
            setEditingItem(null);
            setFormErrors({});
          }}
          submitLabel={activeForm === "create" ? "Créer" : "Mettre à jour"}
          loading={createMutation.isPending || updateMutation.isPending}
        />
      ) : null}
      {!activeForm ? rows.length ? (
        <DataTable
          columns={columns}
          rows={rows}
          rowActions={formFields.length ? (row) => (
            <div className="flex justify-end gap-2">
              <button
                onClick={() => {
                  setEditingItem(row);
                  setActiveForm("edit");
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
          ) : null}
        />
      ) : <EmptyState title={`Aucune donnée pour ${config.label.toLowerCase()}`} /> : null}
      {!activeForm ? (
        <Pagination data={data} onPageChange={(direction) => {
          if (direction === "previous" && page > 1) setPage(page - 1);
          if (direction === "next") setPage(page + 1);
        }} />
      ) : null}
    </div>
  );
}
