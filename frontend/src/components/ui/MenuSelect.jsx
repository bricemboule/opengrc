import { useEffect, useMemo, useRef, useState } from "react";
import { Check, ChevronDown } from "lucide-react";

function normalizeOptions(options) {
  return (options || []).map((option) =>
    typeof option === "object"
      ? { value: option.value, label: option.label ?? String(option.value) }
      : { value: option, label: String(option) },
  );
}

export default function MenuSelect({
  value,
  options = [],
  onChange,
  ariaLabel = "Select option",
  placement = "bottom",
  triggerClassName = "",
  menuClassName = "",
  optionClassName = "",
}) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);
  const normalizedOptions = useMemo(() => normalizeOptions(options), [options]);
  const selectedOption = normalizedOptions.find((option) => String(option.value) === String(value)) || normalizedOptions[0] || null;

  useEffect(() => {
    if (!isOpen) return undefined;

    const handlePointerDown = (event) => {
      if (!containerRef.current?.contains(event.target)) {
        setIsOpen(false);
      }
    };

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        setIsOpen(false);
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
  }, [isOpen]);

  const menuPlacementClass =
    placement === "top" ? "bottom-[calc(100%+0.45rem)]" : "top-[calc(100%+0.45rem)]";

  return (
    <div ref={containerRef} className="relative inline-flex">
      <button
        type="button"
        aria-label={ariaLabel}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((open) => !open)}
        className={`inline-flex h-9 items-center justify-between gap-3 rounded-[10px] border border-black/10 bg-white px-3 text-[11px] font-semibold text-[#111111] transition hover:border-black/20 ${triggerClassName}`.trim()}
      >
        <span>{selectedOption?.label ?? ""}</span>
        <ChevronDown size={15} className={`text-black/70 transition ${isOpen ? "rotate-180" : ""}`} aria-hidden="true" />
      </button>

      {isOpen ? (
        <div
          role="listbox"
          aria-label={ariaLabel}
          className={`absolute left-0 z-30 min-w-full overflow-y-auto rounded-[10px] border border-black/10 bg-[#fffdfa] p-1.5 shadow-[0_14px_28px_rgba(17,17,17,0.06)] ${menuPlacementClass} ${menuClassName}`.trim()}
        >
          {normalizedOptions.map((option) => {
            const isActive = String(option.value) === String(value);

            return (
              <button
                key={option.value}
                type="button"
                role="option"
                aria-selected={isActive}
                onClick={() => {
                  onChange?.(option.value);
                  setIsOpen(false);
                }}
                className={`flex w-full items-center justify-between rounded-[8px] px-3 py-2 text-sm font-semibold transition ${
                  isActive ? "bg-[#111111] text-white" : "text-black hover:bg-black/[0.05]"
                } ${optionClassName}`.trim()}
              >
                <span>{option.label}</span>
                {isActive ? <Check size={14} aria-hidden="true" /> : null}
              </button>
            );
          })}
        </div>
      ) : null}
    </div>
  );
}
