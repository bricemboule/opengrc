import { FiArrowLeft, FiSave } from "react-icons/fi";
import CrudField from "./CrudField";

export default function Create({
  title,
  description,
  fields,
  values,
  errors,
  onChange,
  onSubmit,
  onCancel,
  submitLabel = "Enregistrer",
  loading = false,
}) {
  return (
    <section className="mb-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-[0_10px_30px_rgba(2,6,23,0.06)]">
      <div className="mb-6 flex flex-col gap-4 border-b border-slate-200 pb-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">{title}</h2>
          {description ? <p className="mt-1 text-sm text-slate-500">{description}</p> : null}
        </div>
        <button
          type="button"
          onClick={onCancel}
          className="inline-flex items-center justify-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700"
        >
          <FiArrowLeft size={16} />
          Retour a la liste
        </button>
      </div>

      <form onSubmit={onSubmit} className="space-y-6">
        {errors.non_field_errors ? (
          <p className="rounded-2xl bg-red-50 px-4 py-3 text-sm text-red-700">{errors.non_field_errors}</p>
        ) : null}

        <div className="grid gap-5 md:grid-cols-2">
          {fields.map((field) => (
            <CrudField
              key={field.name}
              field={field}
              value={values[field.name]}
              error={errors[field.name]}
              onChange={onChange}
            />
          ))}
        </div>

        <div className="flex justify-end border-t border-slate-200 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center gap-2 rounded-2xl bg-[#3A7728] px-4 py-3 text-sm font-semibold text-white transition hover:bg-[#2f651f] disabled:cursor-not-allowed disabled:opacity-70"
          >
            <FiSave size={16} />
            {loading ? "Enregistrement..." : submitLabel}
          </button>
        </div>
      </form>
    </section>
  );
}
