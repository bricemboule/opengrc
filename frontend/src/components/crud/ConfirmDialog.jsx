import { FiAlertTriangle, FiTrash2, FiX } from "react-icons/fi";

export default function ConfirmDialog({
  isOpen,
  title,
  description,
  confirmLabel = "Delete",
  cancelLabel = "Cancel",
  loading = false,
  onConfirm,
  onClose,
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[90] flex items-center justify-center bg-[rgba(17,17,17,0.28)] p-4 backdrop-blur-[2px]">
      <div className="w-full max-w-md rounded-[24px] bg-[rgba(255,255,255,0.94)] px-6 py-6 shadow-[0_28px_60px_rgba(17,17,17,0.16)]">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <span className="mt-0.5 flex h-11 w-11 shrink-0 items-center justify-center rounded-[14px] bg-[#fff1ea] text-[#fa695f]">
              <FiAlertTriangle size={18} />
            </span>
            <div>
              <h2 className="text-[1.1rem] font-semibold tracking-[-0.03em] text-[#111111]">{title}</h2>
              {description ? <p className="mt-2 text-sm leading-6 text-black/56">{description}</p> : null}
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            disabled={loading}
            className="flex h-9 w-9 items-center justify-center rounded-full text-black/40 transition hover:bg-black/5 hover:text-black disabled:cursor-not-allowed disabled:opacity-50"
            aria-label="Close"
          >
            <FiX size={16} />
          </button>
        </div>

        <div className="mt-6 flex flex-wrap justify-end gap-3">
          <button type="button" onClick={onClose} disabled={loading} className="app-button app-button-soft" style={{ paddingLeft: "1.7rem", paddingRight: "1.7rem" }}>
            {cancelLabel}
          </button>
          <button
            type="button"
            onClick={onConfirm}
            disabled={loading}
            className="app-button app-button-dark"
            style={{ paddingLeft: "1.4rem", paddingRight: "1.4rem", backgroundColor: "#111111" }}
          >
            <FiTrash2 size={15} />
            {loading ? "Deleting..." : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
