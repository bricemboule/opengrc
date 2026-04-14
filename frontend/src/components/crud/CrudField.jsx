import { Check, Search, X } from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { FiCheck, FiChevronDown } from "react-icons/fi";

const CALENDAR_WEEKDAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"];
const CALENDAR_MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
const SELECT_MENU_MAX_HEIGHT_CLASS = "max-h-[24.5rem] overflow-y-auto pr-1";
const SELECT_MENU_ITEMS_MAX_HEIGHT_CLASS = "max-h-[20.75rem] overflow-y-auto pr-1";
const SELECT_SEARCH_THRESHOLD = 10;

function DateTriggerIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 12 14" fill="none" className={className} aria-hidden="true">
      <path d="M0.556885 5.02466H11.4493" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M8.7146 7.41162H8.7211" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M6.00305 7.41162H6.00955" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M3.28552 7.41162H3.29202" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M8.7146 9.78638H8.7211" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M6.00305 9.78638H6.00955" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M3.28552 9.78638H3.29202" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M8.47131 0.5V2.51116" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M3.53491 0.5V2.51116" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      <path
        d="M8.59004 1.46509H3.41558C1.62094 1.46509 0.5 2.46482 0.5 4.30249V9.83282C0.5 11.6994 1.62094 12.7222 3.41558 12.7222H8.58437C10.3847 12.7222 11.5 11.7167 11.5 9.87905V4.30249C11.5056 2.46482 10.3903 1.46509 8.59004 1.46509Z"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function toLabel(value) {
  return value.replaceAll("_", " ").replace(/(^|\s)\w/g, (character) => character.toUpperCase());
}

function toChoiceList(choices) {
  if (Array.isArray(choices)) return choices;
  if (!choices || typeof choices !== "object") return [];

  return Object.entries(choices).map(([optionValue, optionLabel]) => ({
    value: optionValue,
    display_name: optionLabel,
  }));
}

function resolveChoiceLabel(choices, value) {
  const matched = choices.find((choice) => String(choice.value) === String(value));
  return matched?.display_name || matched?.label || (value ? String(value) : "");
}

function resolveChoiceLabels(choices, values) {
  if (!Array.isArray(values)) return [];
  return values
    .map((value) => resolveChoiceLabel(choices, value))
    .filter(Boolean);
}

function getChoiceText(choice) {
  return choice?.display_name || choice?.label || String(choice?.value ?? "");
}

function filterChoiceList(choices, searchTerm) {
  const normalizedSearch = String(searchTerm || "")
    .trim()
    .toLowerCase();

  if (!normalizedSearch) return choices;

  return choices.filter((choice) => getChoiceText(choice).toLowerCase().includes(normalizedSearch));
}

function getInputType(field) {
  if (field.type === "date") return "date";
  if (field.type === "datetime") return "datetime-local";
  if (field.type === "password") return "password";
  if (["integer", "decimal", "float", "number"].includes(field.type)) return "number";
  if (field.type === "email" || field.name === "email") return "email";
  if (field.type === "url") return "url";
  if (field.type === "tel" || field.name === "phone") return "tel";
  return "text";
}

function createValidDate(year, monthIndex, day) {
  const parsedDate = new Date(year, monthIndex, day);
  if (
    parsedDate.getFullYear() !== year ||
    parsedDate.getMonth() !== monthIndex ||
    parsedDate.getDate() !== day
  ) {
    return null;
  }

  return parsedDate;
}

function parseDateValue(value) {
  const normalizedValue = String(value ?? "").trim();
  if (!normalizedValue) return null;

  const isoMatch = normalizedValue.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (isoMatch) {
    return createValidDate(Number(isoMatch[1]), Number(isoMatch[2]) - 1, Number(isoMatch[3]));
  }

  const displayMatch = normalizedValue.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if (displayMatch) {
    return createValidDate(Number(displayMatch[3]), Number(displayMatch[2]) - 1, Number(displayMatch[1]));
  }

  return null;
}

function formatStoredDate(date) {
  const year = date.getFullYear();
  const month = `${date.getMonth() + 1}`.padStart(2, "0");
  const day = `${date.getDate()}`.padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatDisplayDate(date) {
  const day = `${date.getDate()}`.padStart(2, "0");
  const month = `${date.getMonth() + 1}`.padStart(2, "0");
  return `${day}/${month}/${date.getFullYear()}`;
}

function isSameDate(left, right) {
  return (
    left.getFullYear() === right.getFullYear() &&
    left.getMonth() === right.getMonth() &&
    left.getDate() === right.getDate()
  );
}

function buildCalendarWeeks(displayedCalendarMonth, selectedDate) {
  const monthStart = new Date(displayedCalendarMonth.getFullYear(), displayedCalendarMonth.getMonth(), 1);
  const gridStart = new Date(monthStart);
  const firstDayOffset = (monthStart.getDay() + 6) % 7;
  gridStart.setDate(monthStart.getDate() - firstDayOffset);

  const today = new Date();
  const weeks = [];

  for (let weekIndex = 0; weekIndex < 6; weekIndex += 1) {
    const week = [];

    for (let dayIndex = 0; dayIndex < 7; dayIndex += 1) {
      const currentDate = new Date(gridStart);
      currentDate.setDate(gridStart.getDate() + weekIndex * 7 + dayIndex);

      week.push({
        value: currentDate,
        label: currentDate.getDate(),
        inCurrentMonth: currentDate.getMonth() === monthStart.getMonth(),
        isToday: isSameDate(currentDate, today),
        isSelected: selectedDate ? isSameDate(currentDate, selectedDate) : false,
      });
    }

    weeks.push(week);
  }

  return weeks;
}

function toggleArrayValue(values, nextValue) {
  const current = Array.isArray(values) ? values.map(String) : [];
  const normalizedValue = String(nextValue);
  return current.includes(normalizedValue)
    ? current.filter((item) => item !== normalizedValue)
    : [...current, normalizedValue];
}

export default function CrudField({ field, value, error, onChange, appearance = "default" }) {
  const [isSelectOpen, setIsSelectOpen] = useState(false);
  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);
  const [optionSearch, setOptionSearch] = useState("");
  const interactiveRef = useRef(null);
  const choiceList = useMemo(() => toChoiceList(field.choices), [field.choices]);
  const isRelationField = field.type === "relation";
  const isMultiRelationField = field.type === "multirelation";
  const isSelectableField = isRelationField || choiceList.length > 0;
  const label = field.label || toLabel(field.name);
  const placeholder = field.placeholder || label;
  const helperText = field.helperText || field.help_text || field.helpText;
  const isWide = field.type === "textarea" || field.type === "multirelation" || field.name === "description" || field.name === "comments" || field.span === 2;
  const isEditorial = appearance === "editorial";
  const inputType = getInputType(field);
  const Component = isWide && field.type !== "password" && field.type !== "multirelation" ? "textarea" : "input";
  const isEditorialDate = isEditorial && field.type === "date";
  const selectedDate = useMemo(() => parseDateValue(value), [value]);
  const selectedMultiLabels = useMemo(() => resolveChoiceLabels(choiceList, value), [choiceList, value]);
  const shouldEnableChoiceSearch = choiceList.length > SELECT_SEARCH_THRESHOLD;
  const filteredChoiceList = useMemo(
    () => (shouldEnableChoiceSearch ? filterChoiceList(choiceList, optionSearch) : choiceList),
    [choiceList, optionSearch, shouldEnableChoiceSearch],
  );
  const [displayedCalendarMonth, setDisplayedCalendarMonth] = useState(() => {
    const initialDate = parseDateValue(value) || new Date();
    return new Date(initialDate.getFullYear(), initialDate.getMonth(), 1);
  });
  const calendarWeeks = useMemo(
    () => buildCalendarWeeks(displayedCalendarMonth, selectedDate),
    [displayedCalendarMonth, selectedDate],
  );

  useEffect(() => {
    if (!isSelectOpen && !isDatePickerOpen) return undefined;

    const handlePointerDown = (event) => {
      if (!interactiveRef.current?.contains(event.target)) {
        setIsSelectOpen(false);
        setIsDatePickerOpen(false);
      }
    };

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        setIsSelectOpen(false);
        setIsDatePickerOpen(false);
      }
    };

    document.addEventListener("mousedown", handlePointerDown);
    document.addEventListener("touchstart", handlePointerDown);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("mousedown", handlePointerDown);
      document.removeEventListener("touchstart", handlePointerDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isDatePickerOpen, isSelectOpen]);

  useEffect(() => {
    if (!isSelectOpen) {
      setOptionSearch("");
    }
  }, [field.name, isSelectOpen]);

  function openDatePicker() {
    const baseDate = selectedDate || new Date();
    setIsSelectOpen(false);
    setDisplayedCalendarMonth(new Date(baseDate.getFullYear(), baseDate.getMonth(), 1));
    setIsDatePickerOpen(true);
  }

  function toggleDatePicker() {
    if (isDatePickerOpen) {
      setIsDatePickerOpen(false);
      return;
    }

    openDatePicker();
  }

  function shiftCalendarMonth(offset) {
    setDisplayedCalendarMonth((currentMonth) => new Date(currentMonth.getFullYear(), currentMonth.getMonth() + offset, 1));
  }

  function selectDateFromPicker(date) {
    onChange(field.name, formatStoredDate(date));
    setIsDatePickerOpen(false);
  }

  if (field.type === "boolean") {
    if (isEditorial) {
      const checked = Boolean(value);
      const fieldShellClassName = error ? "shadow-[inset_0_0_0_1px_rgba(166,61,52,0.24)]" : "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.04)]";
      const fieldFocusClassName = error
        ? "focus-visible:shadow-[inset_0_0_0_1px_rgba(166,61,52,0.28),0_0_0_2px_rgba(166,61,52,0.05)]"
        : "focus-visible:shadow-[inset_0_0_0_1px_rgba(17,17,17,0.12),0_0_0_2px_rgba(17,17,17,0.045)]";

      return (
        <div className={`space-y-2.5 ${isWide ? "md:col-span-2" : ""}`}>
          <div className="space-y-1">
            <label className="text-[12px] font-medium text-black/72 ml-3">
              {label}
              {field.required ? <span className="ml-1 text-[#a63d34]">*</span> : null}
            </label>
            {helperText ? <p className="text-sm leading-6 text-black/54">{helperText}</p> : null}
          </div>

          <button
            type="button"
            role="checkbox"
            aria-checked={checked}
            aria-label={label}
            onClick={() => onChange(field.name, !checked)}
            className={`flex min-h-[48px] w-full items-center justify-between gap-4 rounded-[99px] bg-white px-6 py-3 text-left outline-none transition hover:bg-white ${fieldShellClassName} ${fieldFocusClassName}`}
          >
            <span className={`text-[0.88rem] font-medium ${checked ? "text-black" : "text-black/32"}`}>{checked ? "Yes" : "No"}</span>

            <span
              aria-hidden="true"
              className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-[7px] transition ${
                checked ? "bg-[#111111] text-white" : "border border-black/8 bg-transparent text-transparent hover:border-black/14 hover:bg-white/40"
              }`}
            >
              {checked ? <Check size={11} strokeWidth={1.9} /> : null}
            </span>
          </button>

          {error ? <p className="text-sm text-[#a63d34]">{error}</p> : null}
        </div>
      );
    }

    return (
      <label className={`ml-3 flex items-center gap-3 rounded-[99px] bg-white/74 px-4 py-4 ${isWide ? "md:col-span-2" : ""}`}>
        <input type="checkbox" checked={Boolean(value)} onChange={(event) => onChange(field.name, event.target.checked)} className="h-4 w-4 rounded accent-[#111111]" />
        <span className="text-sm text-slate-700">{label}</span>
      </label>
    );
  }

  if (isMultiRelationField && isEditorial) {
    const emptyChoiceLabel = field.relationLoading ? "Loading options..." : field.relationError ? "Unable to load options" : placeholder || "Select";
    const selectedValues = Array.isArray(value) ? value.map(String) : [];
    const selectedLabel = selectedMultiLabels.length ? `${selectedMultiLabels.length} selected` : emptyChoiceLabel;
    const visibleChoices = shouldEnableChoiceSearch ? filteredChoiceList : choiceList;
    const emptyStateLabel = shouldEnableChoiceSearch && optionSearch.trim() ? "No matching options" : emptyChoiceLabel;
    const fieldShellClassName = error ? "shadow-[inset_0_0_0_1px_rgba(166,61,52,0.24)]" : "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.04)]";
    const fieldFocusClassName = error
      ? "focus-visible:shadow-[inset_0_0_0_1px_rgba(166,61,52,0.28),0_0_0_2px_rgba(166,61,52,0.05)]"
      : "focus-visible:shadow-[inset_0_0_0_1px_rgba(17,17,17,0.12),0_0_0_2px_rgba(17,17,17,0.045)]";
    const fieldActiveClassName = isSelectOpen
      ? error
        ? "shadow-[inset_0_0_0_1px_rgba(166,61,52,0.28),0_0_0_2px_rgba(166,61,52,0.05)]"
        : "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.12),0_0_0_2px_rgba(17,17,17,0.045)]"
      : "";

    return (
      <div className={`space-y-2.5 ${isWide ? "md:col-span-2" : ""}`}>
        <div className="space-y-1">
          <label className="text-[12px] font-medium text-black/72 ml-3">
            {label}
            {field.required ? <span className="ml-1 text-[#a63d34]">*</span> : null}
          </label>
          {helperText ? <p className="text-sm leading-6 text-black/54">{helperText}</p> : null}
        </div>

        <div ref={interactiveRef} className="relative">
          <button
            type="button"
            aria-haspopup="listbox"
            aria-expanded={isSelectOpen}
            onClick={() => {
              setIsDatePickerOpen(false);
              setIsSelectOpen((open) => !open);
            }}
            className={`flex min-h-[48px] w-full items-center justify-between gap-4 rounded-[24px] bg-white px-6 py-3 text-left text-[0.88rem] font-medium outline-none transition hover:bg-white ${fieldShellClassName} ${fieldFocusClassName} ${fieldActiveClassName}`}
          >
            <span className={selectedMultiLabels.length ? "text-black" : "text-black/28"}>{selectedLabel}</span>
            <FiChevronDown size={16} className={`shrink-0 text-black/62 transition ${isSelectOpen ? "rotate-180" : ""}`} aria-hidden="true" />
          </button>

          {isSelectOpen ? (
            <div role="listbox" className="absolute left-0 right-0 top-[calc(100%+0.55rem)] z-20 rounded-[20px] bg-[#ffffff] p-2 shadow-[0_18px_34px_rgba(17,17,17,0.06)]">
              {shouldEnableChoiceSearch ? (
                <div className="px-1 pb-2">
                  <div className="relative">
                    <Search size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-black/36" aria-hidden="true" />
                    <input
                      type="text"
                      value={optionSearch}
                      autoFocus
                      onChange={(event) => setOptionSearch(event.target.value)}
                      onClick={(event) => event.stopPropagation()}
                      onMouseDown={(event) => event.stopPropagation()}
                      placeholder={`Search ${label.toLowerCase()}...`}
                      className="h-10 w-full rounded-[14px] bg-[#f7f5f1] pl-9 pr-3 text-sm text-black placeholder:text-black/34 outline-none shadow-[inset_0_0_0_1px_rgba(17,17,17,0.05)] focus:shadow-[inset_0_0_0_1px_rgba(17,17,17,0.1)]"
                    />
                  </div>
                </div>
              ) : null}

              <div className={shouldEnableChoiceSearch ? SELECT_MENU_ITEMS_MAX_HEIGHT_CLASS : SELECT_MENU_MAX_HEIGHT_CLASS}>
                {visibleChoices.length ? (
                  visibleChoices.map((choice) => {
                    const isSelected = selectedValues.includes(String(choice.value));

                    return (
                      <button
                        key={`${field.name}-${choice.value}`}
                        type="button"
                        role="option"
                        aria-selected={isSelected}
                        onClick={() => {
                          onChange(field.name, toggleArrayValue(value, choice.value));
                          setIsSelectOpen(false);
                        }}
                        className={`flex w-full items-center justify-between rounded-[14px] px-3 py-2.5 text-sm font-medium transition ${
                          isSelected ? "bg-[#111111] text-white" : "text-black hover:bg-black/[0.05]"
                        }`}
                      >
                        <span>{getChoiceText(choice)}</span>
                        {isSelected ? <FiCheck size={14} aria-hidden="true" /> : null}
                      </button>
                    );
                  })
                ) : (
                  <div className="px-3 py-2.5 text-sm text-black/42">{emptyStateLabel}</div>
                )}
              </div>
            </div>
          ) : null}
        </div>

        {selectedValues.length ? (
          <div className="flex flex-wrap gap-2 pt-1">
            {selectedValues.map((selectedValue) => {
              const selectedChoiceLabel = resolveChoiceLabel(choiceList, selectedValue) || selectedValue;

              return (
                <button
                  key={`${field.name}-selected-${selectedValue}`}
                  type="button"
                  onClick={() => onChange(field.name, toggleArrayValue(value, selectedValue))}
                  className="inline-flex max-w-full items-center gap-2 rounded-full bg-white px-3 py-2 text-[0.8rem] font-medium text-black shadow-[inset_0_0_0_1px_rgba(17,17,17,0.05)] transition hover:bg-[#f8f6f2]"
                  title={selectedChoiceLabel}
                >
                  <span className="truncate">{selectedChoiceLabel}</span>
                  <X size={12} className="shrink-0 text-black/58" aria-hidden="true" />
                </button>
              );
            })}
          </div>
        ) : null}

        {error ? <p className="text-sm text-[#a63d34]">{error}</p> : null}
      </div>
    );
  }

  if (isSelectableField && isEditorial) {
    const selectedLabel = resolveChoiceLabel(choiceList, value);
    const visibleChoices = shouldEnableChoiceSearch ? filteredChoiceList : choiceList;
    const emptyChoiceLabel = field.relationLoading ? "Loading options..." : field.relationError ? "Unable to load options" : placeholder || "Select";
    const emptyStateLabel = shouldEnableChoiceSearch && optionSearch.trim() ? "No matching options" : emptyChoiceLabel;
    const fieldShellClassName = error ? "shadow-[inset_0_0_0_1px_rgba(166,61,52,0.24)]" : "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.04)]";
    const fieldFocusClassName = error
      ? "focus-visible:shadow-[inset_0_0_0_1px_rgba(166,61,52,0.28),0_0_0_2px_rgba(166,61,52,0.05)]"
      : "focus-visible:shadow-[inset_0_0_0_1px_rgba(17,17,17,0.12),0_0_0_2px_rgba(17,17,17,0.045)]";
    const fieldActiveClassName = isSelectOpen
      ? error
        ? "shadow-[inset_0_0_0_1px_rgba(166,61,52,0.28),0_0_0_2px_rgba(166,61,52,0.05)]"
        : "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.12),0_0_0_2px_rgba(17,17,17,0.045)]"
      : "";

    return (
      <div className={`space-y-2.5 ${isWide ? "md:col-span-2" : ""}`}>
        <div className="space-y-1">
          <label className="text-[12px] font-medium text-black/72 ml-3">
            {label}
            {field.required ? <span className="ml-1 text-[#a63d34]">*</span> : null}
          </label>
          {helperText ? <p className="text-sm leading-6 text-black/54">{helperText}</p> : null}
        </div>

        <div ref={interactiveRef} className="relative">
          <button
            type="button"
            aria-haspopup="listbox"
            aria-expanded={isSelectOpen}
            onClick={() => {
              setIsDatePickerOpen(false);
              setIsSelectOpen((open) => !open);
            }}
            className={`flex min-h-[48px] w-full items-center justify-between gap-4 rounded-[99px] bg-white px-6 py-3 text-left text-[0.88rem] font-medium outline-none transition hover:bg-white ${fieldShellClassName} ${fieldFocusClassName} ${fieldActiveClassName}`}
          >
            <span className={selectedLabel ? "text-black" : "text-black/28"}>{selectedLabel || emptyChoiceLabel}</span>
            <FiChevronDown size={16} className={`shrink-0 text-black/62 transition ${isSelectOpen ? "rotate-180" : ""}`} aria-hidden="true" />
          </button>

          {isSelectOpen ? (
            <div role="listbox" className="absolute left-0 right-0 top-[calc(100%+0.55rem)] z-20 rounded-[20px] bg-[#ffffff] p-2 shadow-[0_18px_34px_rgba(17,17,17,0.06)]">
              {shouldEnableChoiceSearch ? (
                <div className="px-1 pb-2">
                  <div className="relative">
                    <Search size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-black/36" aria-hidden="true" />
                    <input
                      type="text"
                      value={optionSearch}
                      autoFocus
                      onChange={(event) => setOptionSearch(event.target.value)}
                      onClick={(event) => event.stopPropagation()}
                      onMouseDown={(event) => event.stopPropagation()}
                      placeholder={`Search ${label.toLowerCase()}...`}
                      className="h-10 w-full rounded-[14px] bg-[#f7f5f1] pl-9 pr-3 text-sm text-black placeholder:text-black/34 outline-none shadow-[inset_0_0_0_1px_rgba(17,17,17,0.05)] focus:shadow-[inset_0_0_0_1px_rgba(17,17,17,0.1)]"
                    />
                  </div>
                </div>
              ) : null}

              <div className={shouldEnableChoiceSearch ? SELECT_MENU_ITEMS_MAX_HEIGHT_CLASS : SELECT_MENU_MAX_HEIGHT_CLASS}>
                {visibleChoices.length ? (
                  visibleChoices.map((choice) => {
                    const isSelected = String(choice.value) === String(value ?? "");

                    return (
                      <button
                        key={`${field.name}-${choice.value}`}
                        type="button"
                        role="option"
                        aria-selected={isSelected}
                        onClick={() => {
                          onChange(field.name, String(choice.value));
                          setIsSelectOpen(false);
                        }}
                        className={`flex w-full items-center justify-between rounded-[14px] px-3 py-2.5 text-sm font-medium transition ${
                          isSelected ? "bg-[#111111] text-white" : "text-black hover:bg-black/[0.05]"
                        }`}
                      >
                        <span>{getChoiceText(choice)}</span>
                        {isSelected ? <FiCheck size={14} aria-hidden="true" /> : null}
                      </button>
                    );
                  })
                ) : (
                  <div className="px-3 py-2.5 text-sm text-black/42">{emptyStateLabel}</div>
                )}
              </div>
            </div>
          ) : null}
        </div>

        {error ? <p className="text-sm text-[#a63d34]">{error}</p> : null}
      </div>
    );
  }

  if (isMultiRelationField) {
    const selectedValues = Array.isArray(value) ? value.map(String) : [];

    return (
      <div className={`space-y-2 ${isWide ? "md:col-span-2" : ""}`}>
        <label className="text-sm font-medium text-slate-700">{label}</label>
        {helperText ? <p className="text-sm leading-6 text-slate-500">{helperText}</p> : null}
        <div className={`app-input min-h-[56px] rounded-[18px] px-3 py-3 ${SELECT_MENU_MAX_HEIGHT_CLASS}`}>
          {choiceList.map((choice) => {
            const isSelected = selectedValues.includes(String(choice.value));
            return (
              <label key={`${field.name}-${choice.value}`} className="flex items-center justify-between gap-3 rounded-[10px] px-3 py-2 hover:bg-black/[0.04]">
                <span className="text-sm text-slate-700">{choice.display_name || choice.label || String(choice.value)}</span>
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => onChange(field.name, toggleArrayValue(value, choice.value))}
                  className="h-4 w-4 rounded accent-[#111111]"
                />
              </label>
            );
          })}
        </div>
        {error ? <p className="text-sm text-[#a63d34]">{error}</p> : null}
      </div>
    );
  }

  if (isSelectableField) {
    return (
      <div className={`space-y-2 ${isWide ? "md:col-span-2" : ""}`}>
        <label className="text-sm font-medium text-slate-700">{label}</label>
        {helperText ? <p className="text-sm leading-6 text-slate-500">{helperText}</p> : null}
        <select className="app-input min-h-[56px] appearance-none" value={value ?? ""} onChange={(event) => onChange(field.name, event.target.value)}>
          <option value="">{field.relationLoading ? "Loading options..." : field.relationError ? "Unable to load options" : "Select"}</option>
          {choiceList.map((choice) => (
            <option key={`${field.name}-${choice.value}`} value={String(choice.value)}>
              {choice.display_name || choice.label || String(choice.value)}
            </option>
          ))}
        </select>
        {error ? <p className="text-sm text-[#a63d34]">{error}</p> : null}
      </div>
    );
  }

  if (isEditorialDate) {
    const fieldShellClassName = error ? "shadow-[inset_0_0_0_1px_rgba(166,61,52,0.24)]" : "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.04)]";
    const fieldFocusClassName = error
      ? "focus:shadow-[inset_0_0_0_1px_rgba(166,61,52,0.28),0_0_0_2px_rgba(166,61,52,0.05)]"
      : "focus:shadow-[inset_0_0_0_1px_rgba(17,17,17,0.12),0_0_0_2px_rgba(17,17,17,0.045)]";
    const fieldActiveClassName = isDatePickerOpen
      ? error
        ? "shadow-[inset_0_0_0_1px_rgba(166,61,52,0.28),0_0_0_2px_rgba(166,61,52,0.05)]"
        : "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.12),0_0_0_2px_rgba(17,17,17,0.045)]"
      : "";
    const displayedDateValue = selectedDate ? formatDisplayDate(selectedDate) : (value ? String(value) : "");
    const displayedMonthLabel = `${CALENDAR_MONTH_NAMES[displayedCalendarMonth.getMonth()]} ${displayedCalendarMonth.getFullYear()}`;

    return (
      <div className={`space-y-2.5 ${isWide ? "md:col-span-2" : ""}`}>
        <div className="space-y-1">
          <label className="text-[12px] font-medium text-black/72 ml-3">
            {label}
            {field.required ? <span className="ml-1 text-[#a63d34]">*</span> : null}
          </label>
          {helperText ? <p className="text-sm leading-6 text-black/54">{helperText}</p> : null}
        </div>

        <div ref={interactiveRef} className="relative">
          <input
            type="text"
            readOnly
            value={displayedDateValue}
            placeholder="DD/MM/YYYY"
            onClick={openDatePicker}
            onFocus={openDatePicker}
            className={`w-full bg-white px-6 py-2 pr-14 text-[14px] text-black placeholder:text-black/28 outline-none transition min-h-[48px] rounded-[99px] ${fieldShellClassName} ${fieldFocusClassName} ${fieldActiveClassName}`}
          />

          <button
            type="button"
            aria-label={`Select ${label}`}
            onClick={toggleDatePicker}
            className="absolute right-[0.62rem] top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-full text-black/62 transition hover:bg-black/[0.05] hover:text-black"
          >
            <DateTriggerIcon className="h-[14px] w-[12px]" />
          </button>

          {isDatePickerOpen ? (
            <div role="dialog" aria-label={`Calendar ${label}`} className="absolute bottom-[calc(100%+0.55rem)] right-0 z-30 w-[16.5rem] rounded-[1rem] border border-black/[0.08] bg-white p-[0.9rem] shadow-[0_20px_45px_rgba(17,17,17,0.12)]">
              <div className="mb-3 flex items-center justify-between gap-2.5">
                <button
                  type="button"
                  onClick={() => shiftCalendarMonth(-1)}
                  className="inline-flex h-[1.8rem] w-[1.8rem] items-center justify-center rounded-full border border-black/[0.08] bg-white text-black/72 transition hover:bg-black/[0.04]"
                >
                  <FiChevronDown size={12} className="rotate-90" aria-hidden="true" />
                </button>
                <strong className="text-[0.82rem] font-semibold text-black">{displayedMonthLabel}</strong>
                <button
                  type="button"
                  onClick={() => shiftCalendarMonth(1)}
                  className="inline-flex h-[1.8rem] w-[1.8rem] items-center justify-center rounded-full border border-black/[0.08] bg-white text-black/72 transition hover:bg-black/[0.04]"
                >
                  <FiChevronDown size={12} className="-rotate-90" aria-hidden="true" />
                </button>
              </div>

              <div className="mb-[0.35rem] grid grid-cols-7 gap-1">
                {CALENDAR_WEEKDAYS.map((weekday) => (
                  <span key={weekday} className="text-center text-[0.68rem] font-semibold text-black/46">
                    {weekday}
                  </span>
                ))}
              </div>

              <div className="grid gap-1">
                {calendarWeeks.map((week, weekIndex) => (
                  <div key={`${displayedMonthLabel}-${weekIndex}`} className="grid grid-cols-7 gap-1">
                    {week.map((day) => (
                      <button
                        key={day.value.toISOString()}
                        type="button"
                        onClick={() => selectDateFromPicker(day.value)}
                        className={`aspect-square rounded-full text-[0.76rem] font-medium transition ${
                          day.isSelected
                            ? "bg-[#111111] text-white"
                            : day.isToday
                              ? "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.14)] text-black"
                              : day.inCurrentMonth
                                ? "text-black hover:bg-black/[0.06]"
                                : "text-black/24 hover:bg-black/[0.04]"
                        }`}
                      >
                        {day.label}
                      </button>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </div>

        {error ? <p className="text-sm text-[#a63d34]">{error}</p> : null}
      </div>
    );
  }

  if (isEditorial) {
    const editorialFieldClassName = error ? "shadow-[inset_0_0_0_1px_rgba(166,61,52,0.24)]" : "shadow-[inset_0_0_0_1px_rgba(17,17,17,0.04)]";
    const editorialFieldFocusClassName = error
      ? "focus:bg-white focus:shadow-[inset_0_0_0_1px_rgba(166,61,52,0.28),0_0_0_2px_rgba(166,61,52,0.05)]"
      : "focus:bg-white focus:shadow-[inset_0_0_0_1px_rgba(17,17,17,0.12),0_0_0_2px_rgba(17,17,17,0.045)]";

    return (
      <div className={`space-y-2.5 ${isWide ? "md:col-span-2" : ""}`}>
        <div className="space-y-1">
          <label className="text-[12px] font-medium text-black/72 ml-3">
            {label}
            {field.required ? <span className="ml-1 text-[#a63d34]">*</span> : null}
          </label>
          {helperText ? <p className="text-sm leading-6 text-black/54">{helperText}</p> : null}
        </div>

        <Component
          type={Component === "input" ? inputType : undefined}
          className={`w-full bg-white px-6 py-2 text-[14px] text-black placeholder:text-black/28 outline-none transition ${editorialFieldClassName} ${editorialFieldFocusClassName} ${Component === "textarea" ? "min-h-[168px] resize-y pt-4 rounded-[14px] " : "min-h-[48px] rounded-[99px] "}`}
          placeholder={placeholder}
          value={value ?? ""}
          onChange={(event) => onChange(field.name, event.target.value)}
          rows={Component === "textarea" ? 6 : undefined}
        />

        {error ? <p className="text-sm text-[#a63d34]">{error}</p> : null}
      </div>
    );
  }

  const inputClassName = "app-input min-h-[56px]";

  return (
    <div className={`space-y-2 ${isWide ? "md:col-span-2" : ""}`}>
      <label className="text-sm font-medium text-slate-700">{label}</label>
      {helperText ? <p className="text-sm leading-6 text-slate-500">{helperText}</p> : null}
      <Component
        type={Component === "input" ? inputType : undefined}
        className={`${inputClassName} ${Component === "textarea" ? "min-h-[160px] resize-y" : ""}`}
        placeholder={placeholder}
        value={value ?? ""}
        onChange={(event) => onChange(field.name, event.target.value)}
        rows={Component === "textarea" ? 5 : undefined}
      />
      {error ? <p className="text-sm text-[#a63d34]">{error}</p> : null}
    </div>
  );
}
