function toLabel(value) {
  return value.replaceAll("_", " ").replace(/(^|\s)\w/g, (c) => c.toUpperCase());
}

export default function CrudField({ field, value, error, onChange }) {
  const inputClassName = "w-full rounded-2xl border border-slate-200 px-4 py-3";
  const label = field.label || toLabel(field.name);
  const placeholder = field.placeholder || label;
  const isWide = field.type === "textarea" || field.name === "description" || field.name === "comments";

  if (field.type === "boolean") {
    return (
      <label className={`flex items-center gap-3 rounded-2xl border border-slate-200 px-4 py-3 ${isWide ? "md:col-span-2" : ""}`}>
        <input type="checkbox" checked={Boolean(value)} onChange={(event) => onChange(field.name, event.target.checked)} />
        <span className="text-sm text-slate-700">{label}</span>
      </label>
    );
  }

  if (field.choices?.length) {
    return (
      <div className={`space-y-2 ${isWide ? "md:col-span-2" : ""}`}>
        <label className="text-sm font-medium text-slate-700">{label}</label>
        <select className={inputClassName} value={value ?? ""} onChange={(event) => onChange(field.name, event.target.value)}>
          <option value="">Selectionner</option>
          {field.choices.map((choice) => (
            <option key={`${field.name}-${choice.value}`} value={String(choice.value)}>
              {choice.display_name}
            </option>
          ))}
        </select>
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
      </div>
    );
  }

  const inputType = field.type === "date" ? "date" : field.type === "datetime" ? "datetime-local" : ["integer", "decimal", "float", "number"].includes(field.type) ? "number" : "text";
  const Component = isWide ? "textarea" : "input";

  return (
    <div className={`space-y-2 ${isWide ? "md:col-span-2" : ""}`}>
      <label className="text-sm font-medium text-slate-700">{label}</label>
      <Component
        type={Component === "input" ? inputType : undefined}
        className={inputClassName}
        placeholder={placeholder}
        value={value ?? ""}
        onChange={(event) => onChange(field.name, event.target.value)}
        rows={Component === "textarea" ? 4 : undefined}
      />
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
    </div>
  );
}
