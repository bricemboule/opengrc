export default function EmptyState({ title = "No data", description = "" }) {
  return (
    <div className="app-surface-soft rounded-[30px] px-8 py-10 text-center">
      <h3 className="text-[14px] font-normal tracking-[-0.01em] text-slate-900">{title}</h3>
      {description ? <p className="mt-2 text-[13px] leading-6 text-slate-500">{description}</p> : null}
    </div>
  );
}
