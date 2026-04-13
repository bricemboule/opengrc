import { FiArrowLeft, FiSave } from "react-icons/fi";
import CrudField from "./CrudField";

function chunkFields(fields, size = 4) {
  const chunks = [];

  for (let index = 0; index < fields.length; index += size) {
    chunks.push(fields.slice(index, index + size));
  }

  return chunks;
}

function buildDefaultEditorialSections(fields) {
  const narrativeFields = fields.filter((field) => field.type === "textarea" || ["description", "notes", "comments", "summary"].includes(field.name));
  const narrativeNames = new Set(narrativeFields.map((field) => field.name));
  const structuredFields = fields.filter((field) => !narrativeNames.has(field.name));
  const structuredChunks = chunkFields(structuredFields, 4);
  const sections = structuredChunks.map((group, index) => ({
    key: `section-${index + 1}`,
    title: index === 0 ? "Core information" : `Section ${index + 1}`,
    description:
      index === 0
        ? "Fill in the main details for this record so it can be used quickly."
        : "Complete the additional information useful for managing this record.",
    fields: group,
  }));

  if (narrativeFields.length) {
    sections.push({
      key: "context-notes",
      title: "Context and notes",
      description: "Add comments, observations, or additional details related to this record here.",
      fields: narrativeFields,
    });
  }

  return sections.filter((section) => section.fields.length);
}

function buildSections(fields, presentation) {
  if (!presentation?.sections?.length) {
    return buildDefaultEditorialSections(fields);
  }

  const fieldMap = new Map(fields.map((field) => [field.name, field]));
  const usedFieldNames = new Set();
  const sections = presentation.sections
    .map((section, index) => {
      const sectionFields = (section.fields || []).map((name) => fieldMap.get(name)).filter(Boolean);
      sectionFields.forEach((field) => usedFieldNames.add(field.name));

      return {
        key: section.key || `${section.title || "section"}-${index}`,
        ...section,
        fields: sectionFields,
      };
    })
    .filter((section) => section.fields.length);

  const remainingFields = fields.filter((field) => !usedFieldNames.has(field.name));

  if (remainingFields.length) {
    sections.push({
      key: "additional-details",
      title: "Additional details",
      description: "Complete the remaining information for this record.",
      fields: remainingFields,
    });
  }

  return sections;
}

function resolveFieldLabel(field) {
  return field?.label || field?.name?.replaceAll("_", " ")?.replace(/(^|\s)\w/g, (character) => character.toUpperCase()) || "";
}

function buildDefaultEditorialPresentation({ title, description, fields, presentation }) {
  if (presentation?.variant === "editorial") return presentation;

  return {
    variant: "editorial",
    eyebrow: "Create record",
    sectionLabel: title,
    createTitle: title,
    editTitle: title,
    createDescription: description,
    editDescription: description,
    sections: buildDefaultEditorialSections(fields),
    sidePanel: {
      title: "Build a complete file",
      description: description || "Complete this record with the essential information and the operational details useful to the team.",
      keyFields: fields.slice(0, 4).map((field) => field.name),
      highlights: [
        "Start with the essential fields so the record can be used without manual rework.",
        "Use clear labels and values that stay consistent with the rest of the register.",
        "Add notes or observations that will help the next review.",
      ],
    },
  };
}

function renderLegacyCreate({ title, description, fields, values, errors, onChange, onSubmit, onCancel, submitLabel, loading }) {
  return (
    <section className="app-surface mb-6 rounded-[38px] px-6 py-6 sm:px-7">
      <div className="mb-6 flex flex-col gap-4 border-b border-slate-200/70 pb-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-[1.6rem] font-semibold tracking-[-0.04em] text-slate-950">{title}</h2>
          {description ? <p className="mt-1 text-sm leading-7 text-slate-500">{description}</p> : null}
        </div>
        <button type="button" onClick={onCancel} className="app-button app-button-soft app-button-sm">
          <FiArrowLeft size={15} />
          Back to list
        </button>
      </div>

      <form onSubmit={onSubmit} className="space-y-6">
        {errors.non_field_errors ? <p className="rounded-[24px] bg-[#fff1ef] px-4 py-3 text-sm text-[#a63d34]">{errors.non_field_errors}</p> : null}

        <div className="grid gap-5 md:grid-cols-2">
          {fields.map((field) => (
            <CrudField key={field.name} field={field} value={values[field.name]} error={errors[field.name]} onChange={onChange} />
          ))}
        </div>

        <div className="flex justify-end border-t border-slate-200/70 pt-4">
          <button type="submit" disabled={loading} className="app-button app-button-dark">
            <FiSave size={15} />
            {loading ? "Saving..." : submitLabel}
          </button>
        </div>
      </form>
    </section>
  );
}

export default function Create({ title, description, fields, values, errors, onChange, onSubmit, onCancel, submitLabel = "Save", loading = false, presentation = null, showBackButton = true }) {
  const editorialPresentation = buildDefaultEditorialPresentation({ title, description, fields, presentation });
  const modeLabel = editorialPresentation.mode === "edit" ? "Edit" : "Create";
  const sections = buildSections(fields, editorialPresentation);
  const requiredCount = fields.filter((field) => field.required).length;
  const fieldMap = new Map(fields.map((field) => [field.name, field]));
  const keyFieldLabels = (editorialPresentation.sidePanel?.keyFields || []).map((name) => resolveFieldLabel(fieldMap.get(name))).filter(Boolean);
  const highlights = editorialPresentation.sidePanel?.highlights || [];
  const footerNote = editorialPresentation.footerNote || "Check the essential information before saving this record.";

  return (
    <section className="mb-6 space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div className="flex items-start gap-3.5">
          <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-[18px] bg-white/84 text-[#111111]">{editorialPresentation.icon || <span className="text-lg font-semibold">01</span>}</span>

          <div className="space-y-1">
            {editorialPresentation.eyebrow ? <span className="text-[12px] font-semibold text-black/42">{editorialPresentation.eyebrow}</span> : null}
            <div className="flex flex-wrap items-center gap-2.5">
              <strong className="text-[1rem] font-semibold text-black">{editorialPresentation.sectionLabel || title}</strong>
              {/* <span className="rounded-full bg-white/80 px-3 py-1 text-[11px] font-semibold tracking-[0.16em] text-black/48">{modeLabel}</span> */}
            </div>
          </div>
        </div>

        {showBackButton ? (
          <button type="button" onClick={onCancel} className="app-button app-button-soft" style={{ paddingLeft: "1.55rem", paddingRight: "1.55rem" }}>
            <FiArrowLeft size={15} />
            Back to list
          </button>
        ) : null}
      </div>

      <div className="grid gap-5 xl:grid-cols-[minmax(0,1.02fr)_320px]">
        <article className="rounded-[25px] bg-[rgba(255,255,255,0.64)] px-6 py-6 sm:px-7 shadow-2xl shadow-black/[0.04]">
          {/* <article className="rounded-[25px] bg-[#f0eded] px-6 py-6 sm:px-7"> */}
          <div className="mb-7 space-y-4">
            {/* <div className="flex flex-wrap gap-2">
              <span className="rounded-full bg-[#111111] px-3 py-1 text-[11px] font-semibold tracking-[0.16em] text-white">{modeLabel}</span>
              <span className="rounded-full bg-white/78 px-3 py-1 text-[11px] font-semibold tracking-[0.16em] text-black/52">{fields.length} champs</span>
              {requiredCount ? <span className="rounded-full bg-white/78 px-3 py-1 text-[11px] font-semibold tracking-[0.16em] text-black/52">{requiredCount} obligatoires</span> : null}
            </div> */}

            <div className="space-y-1">
              <h2 className="text-[1.9rem] font-semibold tracking-[-0.05em] text-black">{title}</h2>
              {description ? <p className="max-w-3xl text-sm leading-7 text-black/56">{description}</p> : null}
            </div>
          </div>

          <form onSubmit={onSubmit} className="space-y-8">
            {errors.non_field_errors ? <p className="rounded-[22px] bg-[#fff1ef] px-4 py-3 text-sm text-[#a63d34]">{errors.non_field_errors}</p> : null}

            {sections.map((section) => (
              <section key={section.key} className="space-y-4">
                <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
                  <div className="max-w-2xl">
                    <h3 className="text-[1.08rem] font-semibold text-black">{section.title}</h3>
                    {section.description ? <p className="mt-1 text-sm leading-6 text-black/54">{section.description}</p> : null}
                  </div>

                  {/* <span className="text-[11px] font-semibold tracking-[0.16em] text-black/38">{section.fields.length} champs</span> */}
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  {section.fields.map((field) => (
                    <CrudField key={field.name} field={field} value={values[field.name]} error={errors[field.name]} onChange={onChange} appearance="editorial" />
                  ))}
                </div>
              </section>
            ))}

            <div className=" ">
              {/* <p className="max-w-xl text-sm leading-6 text-black/48">{footerNote}</p> */}

              <div className="flex flex-wrap justify-end gap-3">
                {/* <button type="button" onClick={onCancel} className="app-button app-button-soft" style={{ paddingLeft: "1.55rem", paddingRight: "1.55rem" }}>
                  Cancel
                </button> */}
                <button type="submit" disabled={loading} className="app-button app-button-dark" style={{ paddingLeft: "1.55rem", paddingRight: "1.55rem" }}>
                  <FiSave size={15} />
                  {loading ? "Saving..." : submitLabel}
                </button>
              </div>
            </div>
          </form>
        </article>

        <aside className="space-y-4">
          <div className="rounded-[20px] bg-[linear-gradient(160deg,rgba(255,255,255,0.78),rgba(247,244,239,0.94))] px-5 py-5">
            <span className="text-[12px] font-semibold text-black/40">Overview</span>
            <h3 className="mt-3 text-[1.12rem] font-semibold text-black">{editorialPresentation.sidePanel?.title || "Form context"}</h3>
            <p className="mt-2 text-sm leading-6 text-black/56">{editorialPresentation.sidePanel?.description || description}</p>
          </div>

          <div className="rounded-[20px] bg-white/62 px-5 py-5">
            <div className="flex items-center justify-between">
              <strong className="text-[0.96rem] font-semibold text-black">Structure</strong>
              <span className="text-sm text-black/42">{sections.length}</span>
            </div>

            <div className="mt-4 space-y-3">
              {sections.map((section, index) => (
                <div key={`${section.key}-summary`} className="flex items-start gap-3">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#111111] text-[11px] font-semibold text-white">{index + 1}</span>
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-black">{section.title}</p>
                    <p className="mt-1 text-xs leading-5 text-black/46">{section.fields.length} fields in this section</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* {keyFieldLabels.length ? (
            <div className="rounded-[26px] bg-white/58 px-5 py-5">
              <div className="flex items-center justify-between">
                <strong className="text-[0.96rem] font-semibold text-black">Key fields</strong>
                <span className="text-sm text-black/42">{keyFieldLabels.length}</span>
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                {keyFieldLabels.map((label) => (
                  <span key={label} className="rounded-full bg-white/84 px-3 py-1.5 text-[12px] font-medium text-black/76">
                    {label}
                  </span>
                ))}
              </div>
            </div>
          ) : null} */}

          {highlights.length ? (
            <div className="rounded-[20px] bg-white/58 px-5 py-5">
              <div className="flex items-center justify-between">
                <strong className="text-[0.96rem] font-semibold text-black">Tips</strong>
                <span className="text-sm text-black/42">{highlights.length}</span>
              </div>

              <div className="mt-4 space-y-3">
                {highlights.map((item) => (
                  <div key={item} className="flex items-start gap-3">
                    <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-black/32" />
                    <p className="text-sm leading-6 text-black/56">{item}</p>
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </aside>
      </div>
    </section>
  );
}
