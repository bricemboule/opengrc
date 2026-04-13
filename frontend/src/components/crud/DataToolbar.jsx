import { FiRefreshCw, FiSearch } from "react-icons/fi";

export default function DataToolbar({ search, setSearch, onRefresh, action, placeholder = "Search..." }) {
  return (
    <div className="mb-6 flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
      <div className="relative w-full xl:max-w-md">
        <span className="pointer-events-none absolute inset-y-0 left-3.5 flex items-center text-[#111111]">
          <FiSearch size={15} />
        </span>
        <input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder={placeholder}
          className="app-input app-input-search"
          style={{ paddingLeft: "2.45rem" }}
        />
      </div>

      <div className="flex flex-wrap items-center gap-3">
        {/* <button
          type="button"
          onClick={onRefresh}
          className="app-button app-button-soft app-button-sm"
          style={{ paddingLeft: "1.8rem", paddingRight: "1.8rem", fontWeight: 500 }}
        >
          <FiRefreshCw size={15} />
          Rafraichir la liste
        </button> */}
        {action}
      </div>
    </div>
  );
}
