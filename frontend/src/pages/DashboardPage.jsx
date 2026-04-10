import { useQuery } from "@tanstack/react-query";
import api from "../api/client";
import BarChartCard from "../components/dashboard/BarChartCard";

const EMPTY_DASHBOARD = {
  charts: [
    { name: "Org", total: 0 },
    { name: "People", total: 0 },
    { name: "Projects", total: 0 },
    { name: "Roles", total: 0 },
  ],
};

export default function DashboardPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["dashboard"],
    queryFn: async () => (await api.get("/projects/dashboard/")).data,
    placeholderData: EMPTY_DASHBOARD,
  });
  const dashboard = data ?? EMPTY_DASHBOARD;
  const charts = Array.isArray(dashboard.charts) ? dashboard.charts : EMPTY_DASHBOARD.charts;

  return (
    <div className="space-y-6">
      {isLoading ? <p className="text-sm text-slate-500">Chargement du tableau de bord...</p> : null}
      {isError ? <p className="text-sm text-red-600">Impossible de charger les statistiques du tableau de bord.</p> : null}
      <BarChartCard title="Vue synthétique" data={charts} dataKey="total" xKey="name" />
    </div>
  );
}
