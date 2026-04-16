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
  "owner_stakeholder_name",
  "sector_name",
  "target_sector_name",
  "start_reminder_sent_for",
  "follow_up_reminder_sent_for",
]);

const TEXTAREA_FIELD_NAMES = new Set([
  "description",
  "comments",
  "notes",
  "summary",
  "risk_summary",
  "scenario",
  "response_plan",
  "update_notes",
  "communication_procedure",
  "coordination_mechanism",
  "information_sharing_protocol",
  "activation_trigger",
  "activation_notes",
  "participating_sectors",
  "findings",
  "lessons_learned",
  "control_focus",
  "compliance_focus",
  "incident_response_procedure",
  "recovery_procedure",
  "review_notes",
  "objective",
  "agenda",
  "attendees",
  "dial_in_details",
  "minutes",
  "outcome_summary",
  "follow_up_actions",
  "gap_summary",
  "recommendation_summary",
  "baseline_summary",
  "priority_actions",
  "blocker_summary",
  "progress_note",
]);

const BOOLEAN_FIELD_NAMES = new Set([
  "requires_nda",
  "critical_asset",
  "certificate_required",
  "is_staff",
  "is_active",
  "is_verified",
]);

const INTEGER_FIELD_NAMES = new Set([
  "likelihood",
  "impact",
  "duration_days",
  "participant_target",
  "planned_week",
  "current_maturity",
  "target_maturity",
]);

const DECIMAL_FIELD_NAMES = new Set([
  "latitude",
  "longitude",
  "risk_score",
]);

const EMAIL_FIELD_NAMES = new Set(["email"]);
const URL_FIELD_NAMES = new Set(["document_reference", "source_url", "url"]);
const PASSWORD_FIELD_NAMES = new Set(["password"]);
const MULTI_RELATION_FIELD_NAMES = new Set(["role_ids", "permission_ids"]);

export function toLabel(value) {
  return value.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase());
}

function inferFieldType(name) {
  if (MULTI_RELATION_FIELD_NAMES.has(name)) return "multirelation";
  if (PASSWORD_FIELD_NAMES.has(name)) return "password";
  if (BOOLEAN_FIELD_NAMES.has(name)) return "boolean";
  if (INTEGER_FIELD_NAMES.has(name)) return "integer";
  if (DECIMAL_FIELD_NAMES.has(name)) return "decimal";
  if (EMAIL_FIELD_NAMES.has(name)) return "email";
  if (URL_FIELD_NAMES.has(name)) return "url";
  if (TEXTAREA_FIELD_NAMES.has(name)) return "textarea";
  if (name.endsWith("_datetime")) return "datetime";
  if (name.endsWith("_date") || name.endsWith("_at")) return "date";
  return "string";
}

function buildFallbackField(name, configuredField = {}) {
  return {
    name,
    label: configuredField.label || toLabel(name),
    type: configuredField.type || inferFieldType(name),
    required: configuredField.required || false,
    read_only: false,
    choices: configuredField.choices || [],
    placeholder: configuredField.placeholder,
    default: configuredField.default,
    relation: configuredField.relation,
  };
}

export function buildFieldList(config, metadata) {
  const postFields = metadata?.actions?.POST || {};
  const configuredDefinitions = new Map((config?.fieldDefinitions || []).map((field) => [field.name, field]));
  const preferred = config?.formFields || [];
  const metadataNames = Object.keys(postFields);
  const allNames = preferred.length
    ? preferred
    : metadataNames.length
      ? metadataNames
      : Array.from(configuredDefinitions.keys());
  const remaining = preferred.length ? metadataNames.filter((name) => !preferred.includes(name)) : [];

  return [...allNames, ...remaining]
    .filter((name, index, array) => array.indexOf(name) === index)
    .map((name) => ({
      ...buildFallbackField(name, configuredDefinitions.get(name)),
      ...(postFields[name] || {}),
      ...(configuredDefinitions.get(name) || {}),
      name,
    }))
    .filter((field) => !field.read_only && !HIDDEN_FIELDS.has(field.name));
}

function normalizeMultiValue(value) {
  if (!Array.isArray(value)) return [];

  return value
    .map((item) => {
      if (item && typeof item === "object") return item.id ?? item.value ?? "";
      return item;
    })
    .filter((item) => item !== "" && item !== null && item !== undefined);
}

export function buildInitialValues(fields, item = null) {
  return fields.reduce((accumulator, field) => {
    if (item) {
      const value = item[field.name];
      if (field.type === "boolean") {
        accumulator[field.name] = parseBooleanValue(value);
      } else if (field.type === "multirelation") {
        accumulator[field.name] = normalizeMultiValue(value);
      } else {
        accumulator[field.name] = value ?? "";
      }
    } else if (field.type === "boolean") {
      accumulator[field.name] = parseBooleanValue(field.default);
    } else if (field.type === "multirelation") {
      accumulator[field.name] = normalizeMultiValue(field.default);
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

function shouldSerializeEmptyAsNull(field) {
  return ["relation", "multirelation", "date", "datetime", "integer", "decimal", "float", "number"].includes(field.type);
}

function normalizeDateTimeValue(value) {
  if (typeof value !== "string") return value;
  return /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(value) ? `${value}:00` : value;
}

export function serializePayload(fields, values) {
  return fields.reduce((accumulator, field) => {
    const rawValue = values[field.name];

    if (field.type === "boolean") {
      accumulator[field.name] = parseBooleanValue(rawValue);
      return accumulator;
    }

    if (field.type === "multirelation") {
      accumulator[field.name] = normalizeMultiValue(rawValue).map((item) => resolveChoiceValue(field, item));
      return accumulator;
    }

    if (rawValue === "") {
      accumulator[field.name] = field.required ? "" : shouldSerializeEmptyAsNull(field) ? null : "";
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

    if (field.type === "datetime") {
      accumulator[field.name] = normalizeDateTimeValue(rawValue);
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
    .replace(/[̀-ͯ]/g, "")
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
  const cleaned = String(rawText ?? "").replace(/^﻿/, "").trim();
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

  const normalizedHeaders = headers.map((header) => normalizeFieldToken(header));
  const fieldMap = new Map(fields.map((field) => [normalizeFieldToken(field.label || field.name), field]));

  return rows.map((row) =>
    normalizedHeaders.reduce((accumulator, token, index) => {
      const field = fieldMap.get(token);
      if (field) {
        accumulator[field.name] = row[index] ?? "";
      }
      return accumulator;
    }, {}),
  );
}
