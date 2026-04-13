import { useState } from "react";
import DataTable from "../components/crud/DataTable";
import Pagination from "../components/crud/Pagination";
import PageHeader from "../components/crud/PageHeader";
import usePaginatedList from "../hooks/usePaginatedList";

export default function RolesPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = usePaginatedList("roles", "/rbac/roles/", { page });

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <PageHeader title="Roles" description="Role management" />
      <DataTable
        columns={[
          { key: "name", label: "Name" },
          { key: "code", label: "Code" },
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
