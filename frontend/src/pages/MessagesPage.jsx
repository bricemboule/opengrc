import { useState } from "react";
import DataTable from "../components/crud/DataTable";
import PageHeader from "../components/crud/PageHeader";
import Pagination from "../components/crud/Pagination";
import usePaginatedList from "../hooks/usePaginatedList";

export default function MessagesPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = usePaginatedList("messages", "/communications/messages/", { page });

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <PageHeader title="Messages" description="Messages and notifications" />
      <DataTable
        columns={[
          { key: "recipient", label: "Recipient" },
          { key: "channel", label: "Channel" },
          { key: "status", label: "Status" },
        ]}
        rows={data?.results || []}
        selectable
      />
      <Pagination
        data={data}
        onPageChange={(direction) => {
          if (direction === "previous" && page > 1) setPage(page - 1);
          if (direction === "next") setPage(page + 1);
        }}
      />
    </div>
  );
}
