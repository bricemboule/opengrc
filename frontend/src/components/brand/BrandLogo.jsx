import ministrySeal from "../../assets/gambia-mocde-seal.jpg";

export default function BrandLogo({
  title = "National-3CPERS",
  subtitle = "",
  className = "",
  textClassName = "",
  compact = false,
  collapsed = false,
}) {
  return (
    <div
      className={`flex items-center ${collapsed ? "gap-0" : compact ? "gap-2" : "gap-3"} ${className}`.trim()}
    >
      <img
        src={ministrySeal}
        alt=""
        className={`${compact ? "h-11 w-11" : "h-12 w-12"} shrink-0 rounded-full object-cover shadow-[0_8px_18px_rgba(9,30,55,0.1)]`}
        aria-hidden="true"
      />
      <div
        className={`min-w-0 overflow-hidden whitespace-nowrap transition-[max-width,opacity,margin] duration-300 ease-out ${collapsed ? "ml-0 max-w-0 opacity-0" : "ml-0.5 max-w-[220px] opacity-100"} ${textClassName}`.trim()}
      >
        <p className="text-[1.35rem] font-bold tracking-[-0.06em] text-[#091E37]">
          {title}
        </p>
        {subtitle ? (
          <p className="mt-0.5 text-sm text-slate-500">{subtitle}</p>
        ) : null}
      </div>
    </div>
  );
}
