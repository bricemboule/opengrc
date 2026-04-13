export default function BrandLogo({ title = "OpenGRC", subtitle = "", className = "", textClassName = "", compact = false, collapsed = false }) {
  return (
    <div className={`flex items-center ${collapsed ? "gap-0" : compact ? "gap-2" : "gap-3"} ${className}`.trim()}>
      <svg
        viewBox="0 0 48 48"
        className={`${compact ? "h-10 w-10" : "h-11 w-11"} shrink-0 text-[#111111]`}
        aria-hidden="true"
      >
        <path
          fill="currentColor"
          d="M6 13.5C6 9.358 9.358 6 13.5 6H24C28.142 6 31.5 9.358 31.5 13.5V16H35.5C39.642 16 43 19.358 43 23.5V27.5C43 31.642 39.642 35 35.5 35H24C19.858 35 16.5 31.642 16.5 27.5V25H13.5C9.358 25 6 21.642 6 17.5V13.5Z"
        />
        <path
          fill="#ffffff"
          d="M18 14C18 11.791 19.791 10 22 10H23.5V20H33.5C35.709 20 37.5 21.791 37.5 24V25H25.5C21.358 25 18 28.358 18 32.5V14Z"
        />
      </svg>
      <div className={`min-w-0 overflow-hidden whitespace-nowrap transition-[max-width,opacity,margin] duration-300 ease-out ${collapsed ? "ml-0 max-w-0 opacity-0" : "ml-0.5 max-w-[220px] opacity-100"} ${textClassName}`.trim()}>
        <p className="text-[1.55rem] font-bold tracking-[-0.05em] text-[#111111]">{title}</p>
        {subtitle ? <p className="mt-0.5 text-sm text-slate-500">{subtitle}</p> : null}
      </div>
    </div>
  );
}
