import useCrudList from "../hooks/useCrudList";
import DataTable from "../components/crud/DataTable";
import PageHeader from "../components/crud/PageHeader";

export default function MessagesPage() {
  const { data, isLoading } = useCrudList("messages", "/communications/messages/");
  if (isLoading) return <p>Chargement...</p>;
  return (
    <div>
      <PageHeader title="Messages" description="Messages et notifications" />
      <DataTable
        columns={[
          { key: "recipient", label: "Destinataire" },
          { key: "channel", label: "Canal" },
          { key: "status", label: "Statut" },
        ]}
        rows={data?.results || []}
      />
    </div>
  );
}
