export default function DataTable({ columns, rows = [], rowActions }) {
  return (
    <div className="overflow-x-auto bg-white shadow-[0_10px_30px_rgba(2,6,23,0.06)]">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-left text-slate-500">
            {columns.map((column) => (
              <th key={column.key} className="px-6 py-4">{column.label}</th>
            ))}
            {rowActions ? <th className="px-6 py-4 text-right">Actions</th> : null}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={row.id || index} className="border-b border-slate-100">
              {columns.map((column) => (
                <td key={column.key} className="px-6 py-4 text-slate-800">
                  {column.render ? column.render(row) : row[column.key]}
                </td>
              ))}
              {rowActions ? <td className="px-6 py-4 text-right">{rowActions(row)}</td> : null}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
