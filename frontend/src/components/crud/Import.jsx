import { useMemo, useState } from "react";
import { FiArrowLeft, FiDownload, FiUpload } from "react-icons/fi";
import { buildImportDataset, toLabel } from "./crudUtils";

function buildTemplate(fields) {
  return [
    fields.map((field) => field.name).join(","),
    fields.map(() => "").join(","),
  ].join("\n");
}

export default function Import({ title, description, fields, loading = false, onImport, onCancel }) {
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
    <section className="app-surface mb-6 rounded-[38px] px-6 py-6 sm:px-7">
      <div className="mb-6 flex flex-col gap-4 border-b border-slate-200/70 pb-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-[1.6rem] font-semibold tracking-[-0.04em] text-slate-950">{title}</h2>
          {description ? <p className="mt-1 text-sm leading-7 text-slate-500">{description}</p> : null}
        </div>
        <div className="flex flex-wrap gap-3">
          <button type="button" onClick={downloadTemplate} className="app-button app-button-soft app-button-sm">
            <FiDownload size={15} />
            Download template
          </button>
          <button type="button" onClick={onCancel} className="app-button app-button-soft app-button-sm">
            <FiArrowLeft size={15} />
            Back to list
          </button>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-4">
          <label className="flex cursor-pointer items-center justify-center gap-3 rounded-[32px] bg-white/72 px-6 py-10 text-sm font-medium text-slate-600 transition hover:bg-white">
            <FiUpload size={18} />
            <span>{fileName ? `Loaded file: ${fileName}` : "Choose a CSV file"}</span>
            <input type="file" accept=".csv,text/csv" className="hidden" onChange={handleFileChange} />
          </label>

          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700">CSV content</label>
            <textarea
              value={rawText}
              onChange={(event) => {
                setFileName("");
                setRawText(event.target.value);
              }}
              placeholder={template}
              className="app-input min-h-[320px] font-mono text-sm leading-6"
            />
          </div>
        </div>

        <div className="space-y-4">
          <div className="rounded-[32px] bg-white/68 p-5">
            <h3 className="text-sm font-semibold uppercase tracking-[0.16em] text-slate-400">Recognized columns</h3>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              Headers can use API names such as <code className="rounded bg-white px-1 py-0.5 text-[13px]">organization</code> or the displayed labels.
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              {fields.map((field) => (
                <span key={field.name} className="app-pill text-xs font-medium text-slate-600">
                  {toLabel(field.name)}
                </span>
              ))}
            </div>
          </div>

          <div className="rounded-[32px] bg-white/68 p-5">
            <h3 className="text-sm font-semibold uppercase tracking-[0.16em] text-slate-400">Preview</h3>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              <div className="rounded-[24px] bg-white/78 px-4 py-4">
                <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-400">Rows ready</p>
                <p className="mt-2 text-[1.8rem] font-semibold tracking-[-0.05em] text-slate-950">{dataset.records.length}</p>
              </div>
              <div className="rounded-[24px] bg-white/78 px-4 py-4">
                <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-400">Matched</p>
                <p className="mt-2 text-[1.8rem] font-semibold tracking-[-0.05em] text-slate-950">{dataset.matchedColumns.filter(Boolean).length}</p>
              </div>
              <div className="rounded-[24px] bg-white/78 px-4 py-4">
                <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-400">Ignored</p>
                <p className="mt-2 text-[1.8rem] font-semibold tracking-[-0.05em] text-slate-950">{dataset.unknownColumns.length}</p>
              </div>
            </div>

            {dataset.unknownColumns.length ? <p className="mt-4 rounded-[24px] bg-[#fff4e8] px-4 py-3 text-sm text-[#9a6224]">Ignored columns: {dataset.unknownColumns.join(", ")}</p> : null}

            {dataset.records.length ? (
              <div className="app-scroll mt-4 overflow-x-auto">
                <table className="w-full min-w-[540px] border-separate border-spacing-y-2 text-sm">
                  <thead>
                    <tr className="text-left text-[11px] uppercase tracking-[0.16em] text-slate-400">
                      {dataset.headers.map((header, index) => (
                        <th key={`${header}-${index}`} className={`bg-white/56 px-4 py-3 font-semibold ${index === 0 ? "rounded-l-full" : ""} ${index === dataset.headers.length - 1 ? "rounded-r-full" : ""}`}>
                          {header}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {dataset.records.slice(0, 5).map((record, rowIndex) => (
                      <tr key={`preview-${rowIndex}`}>
                        {dataset.headers.map((header, columnIndex) => {
                          const fieldName = dataset.matchedColumns[columnIndex];
                          return (
                            <td key={`${header}-${rowIndex}`} className={`bg-white/82 px-4 py-4 text-slate-700 ${columnIndex === 0 ? "rounded-l-[22px]" : ""} ${columnIndex === dataset.headers.length - 1 ? "rounded-r-[22px]" : ""}`}>
                              {fieldName ? record[fieldName] || "—" : "Ignore"}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="mt-4 text-sm text-slate-500">Upload a CSV to preview it before import.</p>
            )}

            <div className="mt-6 flex justify-end">
              <button type="button" disabled={loading || !dataset.records.length} onClick={() => onImport(dataset.records)} className="app-button app-button-dark">
                <FiUpload size={15} />
                {loading ? "Importing..." : `Import ${dataset.records.length} row${dataset.records.length > 1 ? "s" : ""}`}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}