export default function Pagination({ data, onPageChange }) {
  if (!data) return null;
  const hasPrevious = !!data.previous;
  const hasNext = !!data.next;
  return (
    <div className="mt-4 flex items-center justify-between">
      <p className="text-sm text-slate-500">Total : {data.count ?? 0}</p>
      <div className="flex gap-2">
        <button disabled={!hasPrevious} onClick={() => onPageChange("previous")} className="rounded-xl border border-slate-200 px-4 py-2 text-sm disabled:opacity-50">Précédent</button>
        <button disabled={!hasNext} onClick={() => onPageChange("next")} className="rounded-xl border border-slate-200 px-4 py-2 text-sm disabled:opacity-50">Suivant</button>
      </div>
    </div>
  );
}
