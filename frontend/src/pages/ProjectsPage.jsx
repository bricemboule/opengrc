import useCrudList from "../hooks/useCrudList";
import DataTable from "../components/crud/DataTable";
import PageHeader from "../components/crud/PageHeader";

export default function ProjectsPage() {
  const { data, isLoading } = useCrudList("projects", "/projects/");
  if (isLoading) return <p>Chargement...</p>;
  return (
    <div>
      <PageHeader title="Projets" description="Liste des projets" />
      <DataTable
        columns={[
          { key: "name", label: "Nom" },
          { key: "code", label: "Code" },
          { key: "status", label: "Statut" },
        ]}
        rows={data?.results || []}
      />
    </div>
  );
}
