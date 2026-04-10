import { useQuery } from "@tanstack/react-query";
import api from "../api/client";
import PageHeader from "../components/crud/PageHeader";

export default function RolesPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["roles"],
    queryFn: async () => (await api.get("/rbac/roles/")).data,
  });

  if (isLoading) return <p>Chargement...</p>;

  return (
    <div>
      <PageHeader title="Rôles" description="Gestion des rôles" />
      <div className="space-y-4">
        {(data?.results || []).map((role) => (
          <div key={role.id} className="rounded-2xl border border-slate-200 bg-white p-4">
            <h2 className="font-semibold text-slate-900">{role.name}</h2>
            <p className="text-sm text-slate-500">{role.code}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
