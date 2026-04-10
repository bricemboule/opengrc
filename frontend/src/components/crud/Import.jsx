import { useMemo, useState } from "react";
import { FiArrowLeft, FiDownload, FiUpload } from "react-icons/fi";
import { buildImportDataset, toLabel } from "./crudUtils";

function buildTemplate(fields) {
  return [
    fields.map((field) => field.name).join(","),
    fields.map(() => "").join(","),
  ].join("\n");
}

export default function Import({
  title,
  description,
  fields,
  loading = false,
  onImport,
  onCancel,
}) {
  const [rawText, setRawText] = useState("");
  const [fileName, setFileName] = useState("");
  const dataset = useMemo(() => buildImportDataset(rawText, fields), [fields, rawText]);
  const template = useMemo(() => buildTemplate(fields), [fields]);

  async function handleFileChange(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    const text = await file.text();
    setFileName(file.name);
    setRawText(text);
  }

  function downloadTemplate() {
    const blob = new Blob([template], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "template-import.csv";
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="mb-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-[0_10px_30px_rgba(2,6,23,0.06)]">
      <div className="mb-6 flex flex-col gap-4 border-b border-slate-200 pb-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">{title}</h2>
          {description ? <p className="mt-1 text-sm text-slate-500">{description}</p> : null}
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={downloadTemplate}
            className="inline-flex items-center justify-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700"
          >
            <FiDownload size={16} />
            Télécharger le modèle
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="inline-flex items-center justify-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700"
          >
            <FiArrowLeft size={16} />
            Retour a la liste
          </button>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-4">
          <label className="flex cursor-pointer items-center justify-center gap-3 rounded-3xl border border-dashed border-slate-300 bg-slate-50 px-6 py-8 text-sm text-slate-600 transition hover:border-[#0C1C8C]/40 hover:bg-[#0C1C8C]/5">
            <FiUpload size={18} />
            <span>{fileName ? `Fichier chargé: ${fileName}` : "Choisir un fichier CSV"}</span>
            <input type="file" accept=".csv,text/csv" className="hidden" onChange={handleFileChange} />
          </label>

          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700">Contenu CSV</label>
            <textarea
              value={rawText}
              onChange={(event) => {
                setFileName("");
                setRawText(event.target.value);
              }}
              placeholder={template}
              rows={14}
              className="w-full rounded-3xl border border-slate-200 px-4 py-3 font-mono text-sm"
            />
          </div>
        </div>

        <div className="space-y-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
            <h3 className="text-sm font-semibold text-slate-900">Colonnes reconnues</h3>
            <p className="mt-1 text-sm text-slate-500">
              Les en-têtes peuvent utiliser les noms API comme <code>organization</code> ou les libellés affichés.
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {fields.map((field) => (
                <span key={field.name} className="rounded-full bg-white px-3 py-1 text-xs font-medium text-slate-600 shadow-sm">
                  {toLabel(field.name)}
                </span>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-4">
            <h3 className="text-sm font-semibold text-slate-900">Prévisualisation</h3>
            <div className="mt-3 grid gap-3 sm:grid-cols-3">
              <div className="rounded-2xl bg-slate-50 p-3">
                <p className="text-xs uppercase tracking-[0.08em] text-slate-500">Lignes prêtes</p>
                <p className="mt-1 text-2xl font-bold text-slate-900">{dataset.records.length}</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-3">
                <p className="text-xs uppercase tracking-[0.08em] text-slate-500">Colonnes reconnues</p>
                <p className="mt-1 text-2xl font-bold text-slate-900">{dataset.matchedColumns.filter(Boolean).length}</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-3">
                <p className="text-xs uppercase tracking-[0.08em] text-slate-500">Colonnes ignorées</p>
                <p className="mt-1 text-2xl font-bold text-slate-900">{dataset.unknownColumns.length}</p>
              </div>
            </div>

            {dataset.unknownColumns.length ? (
              <p className="mt-4 rounded-2xl bg-amber-50 px-4 py-3 text-sm text-amber-800">
                Colonnes ignorées: {dataset.unknownColumns.join(", ")}
              </p>
            ) : null}

            {dataset.records.length ? (
              <div className="mt-4 overflow-x-auto rounded-2xl border border-slate-200">
                <table className="w-full border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-slate-200 bg-slate-50 text-left text-slate-500">
                      {dataset.headers.map((header, index) => (
                        <th key={`${header}-${index}`} className="px-4 py-3">
                          {header}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {dataset.records.slice(0, 5).map((record, rowIndex) => (
                      <tr key={`preview-${rowIndex}`} className="border-b border-slate-100">
                        {dataset.headers.map((header, columnIndex) => {
                          const fieldName = dataset.matchedColumns[columnIndex];
                          return (
                            <td key={`${header}-${rowIndex}`} className="px-4 py-3 text-slate-700">
                              {fieldName ? record[fieldName] || "—" : "Ignoré"}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="mt-4 text-sm text-slate-500">Charge un CSV pour voir l’aperçu avant import.</p>
            )}

            <div className="mt-6 flex justify-end">
              <button
                type="button"
                disabled={loading || !dataset.records.length}
                onClick={() => onImport(dataset.records)}
                className="inline-flex items-center justify-center gap-2 rounded-2xl bg-[#3A7728] px-4 py-3 text-sm font-semibold text-white transition hover:bg-[#2f651f] disabled:cursor-not-allowed disabled:opacity-70"
              >
                <FiUpload size={16} />
                {loading ? "Import en cours..." : `Importer ${dataset.records.length} ligne${dataset.records.length > 1 ? "s" : ""}`}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
