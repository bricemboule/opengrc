const HIDDEN_FIELDS = new Set([
  "id",
  "is_deleted",
  "created_at",
  "updated_at",
  "created_by",
  "updated_by",
  "created_by_email",
  "updated_by_email",
  "organization_name",
  "site_name",
  "person_name",
  "project_name",
  "activity_name",
  "contact_person_name",
  "assigned_to_name",
]);

export function toLabel(value) {
  return value.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase());
}

export function buildFieldList(config, metadata) {
  const postFields = metadata?.actions?.POST || {};
  const preferred = config?.formFields || [];
  const allNames = preferred.length ? preferred.filter((name) => postFields[name]) : Object.keys(postFields);
  const remaining = preferred.length ? [] : Object.keys(postFields);

  return [...allNames, ...remaining]
    .filter((name, index, array) => array.indexOf(name) === index)
    .map((name) => ({ name, ...postFields[name] }))
    .filter((field) => !field.read_only && !HIDDEN_FIELDS.has(field.name));
}

export function buildInitialValues(fields, item = null) {
  return fields.reduce((accumulator, field) => {
    if (item) {
      const value = item[field.name];
      if (field.type === "boolean") {
        accumulator[field.name] = parseBooleanValue(value);
      } else {
        accumulator[field.name] = value ?? "";
      }
    } else if (field.type === "boolean") {
      accumulator[field.name] = parseBooleanValue(field.default);
    } else {
      accumulator[field.name] = field.default ?? "";
    }

    return accumulator;
  }, {});
}

export function normalizeErrors(error) {
  const payload = error?.response?.data;
  if (!payload || typeof payload !== "object") return {};

  return Object.entries(payload).reduce((accumulator, [key, value]) => {
    accumulator[key] = Array.isArray(value) ? value.join(" ") : String(value);
    return accumulator;
  }, {});
}

export function resolveChoiceValue(field, rawValue) {
  if (rawValue === "") return rawValue;

  const matched = (field.choices || []).find((choice) => {
    const displayName = String(choice.display_name ?? "").trim().toLowerCase();
    const incomingValue = String(rawValue ?? "").trim().toLowerCase();
    return String(choice.value) === String(rawValue) || displayName === incomingValue;
  });

  return matched ? matched.value : rawValue;
}

export function parseBooleanValue(value) {
  if (typeof value === "boolean") return value;
  const normalized = String(value ?? "").trim().toLowerCase();
  if (["true", "1", "yes", "oui", "y"].includes(normalized)) return true;
  if (["false", "0", "no", "non", "n", ""].includes(normalized)) return false;
  return Boolean(value);
}

export function serializePayload(fields, values) {
  return fields.reduce((accumulator, field) => {
    const rawValue = values[field.name];

    if (field.type === "boolean") {
      accumulator[field.name] = parseBooleanValue(rawValue);
      return accumulator;
    }

    if (rawValue === "") {
      accumulator[field.name] = field.required ? "" : null;
      return accumulator;
    }

    if (field.choices?.length) {
      accumulator[field.name] = resolveChoiceValue(field, rawValue);
      return accumulator;
    }

    if (["integer"].includes(field.type)) {
      accumulator[field.name] = Number.parseInt(rawValue, 10);
      return accumulator;
    }

    if (["decimal", "float", "number"].includes(field.type)) {
      accumulator[field.name] = Number.parseFloat(rawValue);
      return accumulator;
    }

    accumulator[field.name] = rawValue;
    return accumulator;
  }, {});
}

export function normalizeFieldToken(value) {
  return String(value ?? "")
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

function parseCsvLine(line) {
  const result = [];
  let current = "";
  let isQuoted = false;

  for (let index = 0; index < line.length; index += 1) {
    const character = line[index];

    if (character === '"') {
      if (isQuoted && line[index + 1] === '"') {
        current += '"';
        index += 1;
      } else {
        isQuoted = !isQuoted;
      }
      continue;
    }

    if (character === "," && !isQuoted) {
      result.push(current.trim());
      current = "";
      continue;
    }

    current += character;
  }

  result.push(current.trim());
  return result;
}

function parseCsvText(rawText) {
  const cleaned = String(rawText ?? "").replace(/^\uFEFF/, "").trim();
  if (!cleaned) {
    return { headers: [], rows: [] };
  }

  const lines = cleaned.split(/\r?\n/).filter((line) => line.trim() !== "");
  if (!lines.length) {
    return { headers: [], rows: [] };
  }

  return {
    headers: parseCsvLine(lines[0]),
    rows: lines.slice(1).map((line) => parseCsvLine(line)),
  };
}

export function buildImportDataset(rawText, fields) {
  const { headers, rows } = parseCsvText(rawText);

  if (!headers.length) {
    return {
      headers: [],
      matchedColumns: [],
      unknownColumns: [],
      records: [],
    };
  }

  const fieldLookup = fields.reduce((accumulator, field) => {
    accumulator.set(normalizeFieldToken(field.name), field.name);
    accumulator.set(normalizeFieldToken(field.label || toLabel(field.name)), field.name);
    return accumulator;
  }, new Map());

  const matchedColumns = headers.map((header) => fieldLookup.get(normalizeFieldToken(header)) || null);
  const unknownColumns = headers.filter((_, index) => !matchedColumns[index]);
  const records = rows
    .map((columns) =>
      matchedColumns.reduce((accumulator, fieldName, index) => {
        if (fieldName) {
          accumulator[fieldName] = columns[index] ?? "";
        }
        return accumulator;
      }, {}),
    )
    .filter((record) => Object.values(record).some((value) => String(value ?? "").trim() !== ""));

  return {
    headers,
    matchedColumns,
    unknownColumns,
    records,
  };
}
