import logo from "../../assets/mocde-logo.jpeg";

export default function BrandLogo({ title = "National-3CPERS", subtitle = "", className = "", textClassName = "", compact = false, collapsed = false }) {
  return (
    <div className={`flex items-center ${collapsed ? "gap-0" : compact ? "gap-2" : "gap-3"} ${className}`.trim()}>
      <img src={logo} alt="National-3CPERS" className={`${compact ? "h-10 w-10" : "h-11 w-11"} shrink-0 rounded-full object-contain`} />
      <div className={`min-w-0 overflow-hidden whitespace-nowrap transition-[max-width,opacity,margin] duration-300 ease-out ${collapsed ? "ml-0 max-w-0 opacity-0" : "ml-0.5 max-w-[220px] opacity-100"} ${textClassName}`.trim()}>
        <p className="text-[1.2rem] font-bold tracking-[-0.03em] text-[#00336f]">{title}</p>
        {subtitle ? <p className="mt-0.5 text-sm text-slate-500">{subtitle}</p> : null}
      </div>
    </div>
  );
}
