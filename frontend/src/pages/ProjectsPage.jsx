import { useState } from "react";
import DataTable from "../components/crud/DataTable";
import PageHeader from "../components/crud/PageHeader";
import Pagination from "../components/crud/Pagination";
import usePaginatedList from "../hooks/usePaginatedList";

export default function ProjectsPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = usePaginatedList("projects", "/projects/", { page });

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <PageHeader title="Projects" description="Project list" />
      <DataTable
        columns={[
          { key: "name", label: "Name" },
          { key: "code", label: "Code" },
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
