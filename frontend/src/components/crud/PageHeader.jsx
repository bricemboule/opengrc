export default function PageHeader({ title, description, action, eyebrow = null, descriptionClassName = "" }) {
  return (
    <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div>
        {eyebrow ? <div className="text-[#111111]">{eyebrow}</div> : <p className="text-[12.5px] font-semibold tracking-[0.04em] text-[#5e5650]">Workspace view</p>}
        <h1 className={`${eyebrow ? "mt-2" : "mt-3"} text-[2rem] font-semibold leading-tight tracking-[-0.05em] text-slate-950`}>{title}</h1>
        {description ? <p className={`mt-1 max-w-3xl text-sm leading-7 ${descriptionClassName || "text-slate-500"}`}>{description}</p> : null}
      </div>
      {action}
    </div>
  );
}
