export default function EmptyState({ title = "Aucune donnée", description = "" }) {
  return (
    <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
      <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
      {description && <p className="mt-2 text-slate-500">{description}</p>}
    </div>
  );
}
