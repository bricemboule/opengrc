import { FiRefreshCw } from "react-icons/fi";

export default function DataToolbar({ search, setSearch, onRefresh, action, placeholder = "Rechercher..." }) {
  return (
    <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-2xl border border-slate-200 px-4 py-3 md:max-w-sm"
      />
      <div className="flex items-center gap-3">
        <button onClick={onRefresh} className="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium">
          <FiRefreshCw size={16} />
          Rafraîchir
        </button>
        {action}
      </div>
    </div>
  );
}
