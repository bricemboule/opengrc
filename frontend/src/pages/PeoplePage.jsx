import useCrudList from "../hooks/useCrudList";
import DataTable from "../components/crud/DataTable";
import PageHeader from "../components/crud/PageHeader";

export default function PeoplePage() {
  const { data, isLoading } = useCrudList("people", "/people/");
  if (isLoading) return <p>Chargement...</p>;
  return (
    <div>
      <PageHeader title="Personnes" description="Annuaire des personnes" />
      <DataTable
        columns={[
          { key: "first_name", label: "Prénom" },
          { key: "last_name", label: "Nom" },
          { key: "gender", label: "Genre" },
        ]}
        rows={data?.results || []}
      />
    </div>
  );
}
