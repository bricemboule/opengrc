import { useState } from "react";
import PageHeader from "../components/crud/PageHeader";
import DataTable from "../components/crud/DataTable";
import EmptyState from "../components/crud/EmptyState";
import FormModal from "../components/crud/FormModal";
import DataToolbar from "../components/crud/DataToolbar";
import Pagination from "../components/crud/Pagination";
import usePaginatedList from "../hooks/usePaginatedList";
import { useCreateItem } from "../hooks/useCrudMutations";
import { downloadFile } from "../utils/download";

export default function OrganizationsPage() {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState({ name: "", code: "", email: "", is_active: true });

  const { data, isLoading, refetch } = usePaginatedList("organizations", "/org/", {
    search, page, ordering: "-created_at",
  });
  const createMutation = useCreateItem("organizations", "/org/", "Organisation créée");

  async function handleSubmit(e) {
    e.preventDefault();
    await createMutation.mutateAsync(form);
    setIsOpen(false);
    setForm({ name: "", code: "", email: "", is_active: true });
  }

  if (isLoading) return <p>Chargement...</p>;
  const rows = data?.results || [];

  return (
    <div>
      <PageHeader
        title="Organisations"
        description="Gestion des organisations"
        action={
          <div className="flex gap-2">
            <button onClick={() => downloadFile("/org/export-csv/", "organizations.csv")} className="rounded-2xl bg-[#3A7728] px-4 py-2 text-sm font-medium text-white">Export CSV</button>
            <button onClick={() => setIsOpen(true)} className="rounded-2xl bg-[#0C1C8C] px-4 py-2 text-sm font-medium text-white">Ajouter</button>
          </div>
        }
      />

      <DataToolbar search={search} setSearch={setSearch} onRefresh={refetch} />

      {!rows.length ? (
        <EmptyState title="Aucune organisation" description="Commence par créer une organisation." />
      ) : (
        <>
          <DataTable
            columns={[
              { key: "name", label: "Nom" },
              { key: "code", label: "Code" },
              { key: "email", label: "Email" },
              { key: "is_active", label: "Actif", render: (row) => (row.is_active ? "Oui" : "Non") },
            ]}
            rows={rows}
          />
          <Pagination
            data={data}
            onPageChange={(direction) => {
              if (direction === "previous" && page > 1) setPage(page - 1);
              if (direction === "next") setPage(page + 1);
            }}
          />
        </>
      )}

      <FormModal title="Nouvelle organisation" isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input className="w-full rounded-2xl border border-slate-200 px-4 py-3" placeholder="Nom" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <input className="w-full rounded-2xl border border-slate-200 px-4 py-3" placeholder="Code" value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} />
          <input className="w-full rounded-2xl border border-slate-200 px-4 py-3" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <button type="submit" className="rounded-2xl bg-[#CE1126] px-4 py-3 font-semibold text-white">Enregistrer</button>
        </form>
      </FormModal>
    </div>
  );
}
