function toNumber(value) {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function projectPoint(latitude, longitude, bounds) {
  const width = 100;
  const height = 100;
  const lngRange = bounds.maxLongitude - bounds.minLongitude || 1;
  const latRange = bounds.maxLatitude - bounds.minLatitude || 1;

  return {
    x: ((longitude - bounds.minLongitude) / lngRange) * width,
    y: height - ((latitude - bounds.minLatitude) / latRange) * height,
  };
}

export default function MapView({ title, description, rows = [] }) {
  const points = rows
    .map((row) => ({
      id: row.id,
      name: row.name || row.code || `Point ${row.id}`,
      city: row.city || "—",
      address: row.address || "—",
      latitude: toNumber(row.latitude),
      longitude: toNumber(row.longitude),
      status: row.status || "—",
    }))
    .filter((point) => point.latitude !== null && point.longitude !== null);

  const bounds = points.reduce(
    (accumulator, point) => ({
      minLatitude: Math.min(accumulator.minLatitude, point.latitude),
      maxLatitude: Math.max(accumulator.maxLatitude, point.latitude),
      minLongitude: Math.min(accumulator.minLongitude, point.longitude),
      maxLongitude: Math.max(accumulator.maxLongitude, point.longitude),
    }),
    {
      minLatitude: Number.POSITIVE_INFINITY,
      maxLatitude: Number.NEGATIVE_INFINITY,
      minLongitude: Number.POSITIVE_INFINITY,
      maxLongitude: Number.NEGATIVE_INFINITY,
    },
  );

  return (
    <section className="mb-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-[0_10px_30px_rgba(2,6,23,0.06)]">
      <div className="mb-6 border-b border-slate-200 pb-4">
        <h2 className="text-xl font-bold text-slate-900">{title}</h2>
        {description ? <p className="mt-1 text-sm text-slate-500">{description}</p> : null}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
          <div className="mb-4 flex flex-wrap gap-3">
            <div className="rounded-2xl bg-white px-4 py-3 shadow-sm">
              <p className="text-xs uppercase tracking-[0.08em] text-slate-500">Bureaux géolocalisés</p>
              <p className="mt-1 text-2xl font-bold text-slate-900">{points.length}</p>
            </div>
            <div className="rounded-2xl bg-white px-4 py-3 shadow-sm">
              <p className="text-xs uppercase tracking-[0.08em] text-slate-500">Total résultats</p>
              <p className="mt-1 text-2xl font-bold text-slate-900">{rows.length}</p>
            </div>
          </div>

          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-[linear-gradient(135deg,#ecfccb_0%,#dbeafe_100%)] p-4">
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.85),transparent_45%)]" />
            <div className="relative h-[420px] rounded-[28px] border border-white/60 bg-white/40">
              <div className="absolute inset-0 grid grid-cols-4 grid-rows-4">
                {Array.from({ length: 16 }).map((_, index) => (
                  <div key={`grid-${index}`} className="border border-white/40" />
                ))}
              </div>

              {points.length ? (
                <svg viewBox="0 0 100 100" className="absolute inset-0 h-full w-full">
                  {points.map((point) => {
                    const projected = projectPoint(point.latitude, point.longitude, bounds);
                    return (
                      <g key={point.id} transform={`translate(${projected.x}, ${projected.y})`}>
                        <circle r="2.7" fill="#CE1126" stroke="white" strokeWidth="1.2" />
                        <circle r="6" fill="rgba(206,17,38,0.18)" />
                      </g>
                    );
                  })}
                </svg>
              ) : (
                <div className="absolute inset-0 flex items-center justify-center p-6 text-center text-sm text-slate-600">
                  Aucun point cartographiable. Renseigne <code className="mx-1 rounded bg-white px-1 py-0.5">latitude</code> et{" "}
                  <code className="rounded bg-white px-1 py-0.5">longitude</code> sur les bureaux pour alimenter cette vue.
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white">
          <div className="border-b border-slate-200 px-5 py-4">
            <h3 className="text-sm font-semibold text-slate-900">Points affichés</h3>
          </div>
          <div className="max-h-[520px] overflow-y-auto">
            {points.length ? (
              <div className="divide-y divide-slate-100">
                {points.map((point) => (
                  <article key={point.id} className="px-5 py-4">
                    <div className="flex items-center justify-between gap-3">
                      <h4 className="font-semibold text-slate-900">{point.name}</h4>
                      <span className="rounded-full bg-[#0C1C8C]/10 px-3 py-1 text-xs font-medium text-[#0C1C8C]">
                        {point.status}
                      </span>
                    </div>
                    <p className="mt-2 text-sm text-slate-600">{point.city}</p>
                    <p className="mt-1 text-sm text-slate-500">{point.address}</p>
                    <p className="mt-2 text-xs text-slate-500">
                      Lat {point.latitude} / Lng {point.longitude}
                    </p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="px-5 py-8 text-sm text-slate-500">Aucun bureau avec coordonnées n’est disponible pour cette vue.</p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
