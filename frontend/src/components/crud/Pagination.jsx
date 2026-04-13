import { useEffect, useRef, useState } from "react";
import { FiCheck, FiChevronDown } from "react-icons/fi";

const DEFAULT_PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

export default function Pagination({
  data,
  onPageChange,
  currentPage = 1,
  pageSize = 20,
  onPageSizeChange,
  pageSizeOptions = DEFAULT_PAGE_SIZE_OPTIONS,
  showPageCounter = false,
  showPageSizeSelector = false,
  minTotalForSummary = 0,
  minTotalForNext = 0,
}) {
  const [isPageSizeMenuOpen, setIsPageSizeMenuOpen] = useState(false);
  const pageSizeMenuRef = useRef(null);

  useEffect(() => {
    if (!isPageSizeMenuOpen) return undefined;

    const handlePointerDown = (event) => {
      if (!pageSizeMenuRef.current?.contains(event.target)) {
        setIsPageSizeMenuOpen(false);
      }
    };

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        setIsPageSizeMenuOpen(false);
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
  }, [isPageSizeMenuOpen]);

  if (!data) return null;

  const total = Number(data.count ?? 0);
  const normalizedPageSize = Number(pageSize) || 20;
  const totalPages = Math.max(1, Math.ceil(total / normalizedPageSize));
  const normalizedCurrentPage = Math.min(Math.max(1, Number(currentPage) || 1), totalPages);
  const hasPrevious = !!data.previous;
  const hasNext = !!data.next;
  const showMeta = total > minTotalForSummary;
  const showTotal = showMeta;
  const shouldShowPageSizeSelector = showPageSizeSelector && showMeta;
  const shouldShowPageCounter = showPageCounter && showMeta;
  const showPrevious = hasPrevious;
  const showNext = total > minTotalForNext && hasNext;
  const showInfo = showTotal || shouldShowPageCounter || shouldShowPageSizeSelector;

  if (!showInfo && !showPrevious && !showNext) return null;

  const handlePageSizeSelect = (option) => {
    onPageSizeChange?.(Number(option));
    setIsPageSizeMenuOpen(false);
  };

  return (
    <div className="mt-6 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <div className="flex flex-wrap items-center gap-3 text-sm font-medium text-black">
        {showTotal ? <span className="text-black">Total: {total}</span> : null}
        {shouldShowPageSizeSelector ? (
          <div ref={pageSizeMenuRef} className="relative inline-flex items-center">
            <button
              type="button"
              aria-haspopup="listbox"
              aria-expanded={isPageSizeMenuOpen}
              onClick={() => setIsPageSizeMenuOpen((open) => !open)}
              className="inline-flex min-w-[4.75rem] items-center justify-between gap-3 rounded-[6px] border border-black/10 bg-white px-3 py-2 text-sm font-semibold text-black transition hover:border-black/20"
            >
              <span>{normalizedPageSize}</span>
              <FiChevronDown size={15} className={`text-black/70 transition ${isPageSizeMenuOpen ? "rotate-180" : ""}`} aria-hidden="true" />
            </button>

            {isPageSizeMenuOpen ? (
              <div
                role="listbox"
                aria-label="Elements per page"
                className="absolute bottom-[calc(100%+0.45rem)] left-0 z-30 min-w-full overflow-hidden rounded-[10px] border border-black/10 bg-[#fffdfa] p-1.5"
              >
                {pageSizeOptions.map((option) => {
                  const isActive = Number(option) === normalizedPageSize;

                  return (
                    <button
                      key={option}
                      type="button"
                      role="option"
                      aria-selected={isActive}
                      onClick={() => handlePageSizeSelect(option)}
                      className={`flex w-full items-center justify-between rounded-[8px] px-3 py-2 text-sm font-semibold transition ${
                        isActive ? "bg-[#111111] text-white" : "text-black hover:bg-black/[0.05]"
                      }`}
                    >
                      <span>{option}</span>
                      {isActive ? <FiCheck size={14} aria-hidden="true" /> : null}
                    </button>
                  );
                })}
              </div>
            ) : null}
          </div>
        ) : null}
        {shouldShowPageCounter ? (
          <span className="text-black" style={{ opacity: 0.4 }}>
            Page {normalizedCurrentPage} of {totalPages}
          </span>
        ) : null}
      </div>

      <div className="flex flex-wrap gap-2">
        {showPrevious ? (
          <button
            type="button"
            disabled={!hasPrevious}
            onClick={() => onPageChange("previous")}
            className="app-button app-button-dark"
            style={{ paddingLeft: "1.55rem", paddingRight: "1.55rem", backgroundColor: "rgba(255, 255, 255, 0.8)", color: "rgba(17, 17, 17, 0.8)" }}
          >
            Previous
          </button>
        ) : null}
        {showNext ? (
          <button type="button" disabled={!hasNext} onClick={() => onPageChange("next")} className="app-button app-button-dark" style={{ paddingLeft: "1.55rem", paddingRight: "1.55rem" }}>
            Next
          </button>
        ) : null}
      </div>
    </div>
  );
}

