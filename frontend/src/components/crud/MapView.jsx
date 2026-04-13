import { useEffect, useMemo, useRef, useState } from "react";
import { CircleMarker, MapContainer, TileLayer, Tooltip, ZoomControl, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { Crosshair, Layers3, MapPin } from "lucide-react";

const DEFAULT_CENTER = [13.454876, -16.579032];
const TILE_LAYER_URL = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png";
const TILE_LAYER_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>';

function toNumber(value) {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function formatStatusLabel(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/(^|\s)\w/g, (character) => character.toUpperCase());
}

function getPointColor(status) {
  const value = String(status || "").toLowerCase();
  if (["reviewed", "mapped", "available", "completed", "validated", "closed", "ready"].some((token) => value.includes(token))) return "#8ecf9b";
  if (["critical", "high", "blocked", "overdue", "unavailable", "constrained"].some((token) => value.includes(token))) return "#d67863";
  if (["planned", "pending", "draft", "in_progress", "submitted"].some((token) => value.includes(token))) return "#f0be7c";
  return "#8d95d8";
}

function getStatusTone(status) {
  const value = String(status || "").toLowerCase();
  if (["reviewed", "mapped", "available", "completed", "validated", "closed", "ready"].some((token) => value.includes(token))) {
    return "bg-[#edf7ee] text-[#4f6854]";
  }
  if (["critical", "high", "blocked", "overdue", "unavailable", "constrained"].some((token) => value.includes(token))) {
    return "bg-[#fff0ea] text-[#8b5a4d]";
  }
  if (["planned", "pending", "draft", "in_progress", "submitted"].some((token) => value.includes(token))) {
    return "bg-[#fff5e8] text-[#8d6c49]";
  }
  return "bg-white/84 text-[#5f5750]";
}

function FitMapToPoints({ points }) {
  const map = useMap();

  useEffect(() => {
    const frame = window.requestAnimationFrame(() => {
      map.invalidateSize();
    });

    return () => window.cancelAnimationFrame(frame);
  }, [map, points.length]);

  useEffect(() => {
    if (!points.length) {
      map.setView(DEFAULT_CENTER, 8, { animate: false });
      return;
    }

    const bounds = L.latLngBounds(points.map((point) => [point.latitude, point.longitude]));
    map.fitBounds(bounds.pad(points.length === 1 ? 0.22 : 0.16), {
      animate: false,
      padding: [24, 24],
    });
  }, [map, points]);

  return null;
}

function FlyToSelectedPoint({ point }) {
  const map = useMap();
  const hasMountedRef = useRef(false);

  useEffect(() => {
    if (!point) return;

    if (!hasMountedRef.current) {
      hasMountedRef.current = true;
      return;
    }

    map.flyTo([point.latitude, point.longitude], Math.max(map.getZoom(), 10.5), {
      animate: true,
      duration: 0.8,
    });
  }, [map, point]);

  return null;
}

export default function MapView({ title, description, rows = [] }) {
  const points = useMemo(
    () =>
      rows
        .map((row) => ({
          id: row.id,
          name: row.name || row.title || row.code || `Point ${row.id}`,
          region: row.city || row.location || row.sector || "Unspecified area",
          detail: row.essential_service || row.owner_name || row.address || row.summary || "Operational record",
          latitude: toNumber(row.latitude),
          longitude: toNumber(row.longitude),
          status: row.mapping_status || row.availability_status || row.status || "-",
          sector: row.sector || row.target_sector || row.scope || "Unspecified sector",
        }))
        .filter((point) => point.latitude !== null && point.longitude !== null),
    [rows],
  );

  const sectorPreview = useMemo(
    () =>
      Array.from(
        points.reduce((accumulator, point) => {
          accumulator.set(point.sector, (accumulator.get(point.sector) || 0) + 1);
          return accumulator;
        }, new Map()),
      )
        .sort((left, right) => right[1] - left[1])
        .slice(0, 3),
    [points],
  );

  const [selectedPointId, setSelectedPointId] = useState(null);

  useEffect(() => {
    if (!points.length) {
      setSelectedPointId(null);
      return;
    }

    if (!points.some((point) => point.id === selectedPointId)) {
      setSelectedPointId(points[0].id);
    }
  }, [points, selectedPointId]);

  const selectedPoint = points.find((point) => point.id === selectedPointId) || points[0] || null;

  return (
    <section className="app-surface rounded-[24px] px-6 py-6">
      <div className="border-b border-black/8 pb-4">
        <h2 className="text-[1.55rem] font-semibold tracking-[-0.04em] text-[#111111]">{title}</h2>
        {description ? <p className="mt-1 text-sm leading-7 text-[#5e5650]">{description}</p> : null}
      </div>

      <div className="mt-5 flex flex-wrap gap-3">
        <div className="min-w-[150px] rounded-[10px] bg-white/88 px-5 py-3 shadow-[0_8px_18px_rgba(17,17,17,0.02)]">
          <p className="text-[11px] font-semibold text-[#554d46]">Geolocated</p>
          <p className="mt-1 text-xl font-semibold tracking-[-0.04em] text-[#111111]">{points.length}</p>
        </div>
        <div className="min-w-[150px] rounded-[10px] bg-white/88 px-5 py-3 shadow-[0_8px_18px_rgba(17,17,17,0.02)]">
          <p className="text-[11px] font-semibold text-[#554d46]">Results</p>
          <p className="mt-1 text-xl font-semibold tracking-[-0.04em] text-[#111111]">{rows.length}</p>
        </div>
        <div className="min-w-[220px] rounded-[10px] bg-white/88 px-5 py-3 shadow-[0_8px_18px_rgba(17,17,17,0.02)]">
          <p className="text-[11px] font-semibold text-[#554d46]">Focus</p>
          <p className="mt-1 text-sm font-semibold text-[#111111]">{selectedPoint?.region || "Operational map"}</p>
        </div>
      </div>

      <div className="mt-6 grid gap-5 xl:grid-cols-[minmax(0,1.12fr)_360px]">
        <div className="overflow-hidden rounded-[20px]">
          <div className="app-map-shell relative h-[540px] overflow-hidden rounded-[20px] bg-[#f9f4ee]">
            {points.length ? (
              <>
                <MapContainer center={DEFAULT_CENTER} zoom={8} minZoom={5} maxZoom={18} zoomControl={false} scrollWheelZoom className="app-operations-map h-full w-full">
                  <ZoomControl position="bottomright" />
                  <TileLayer attribution={TILE_LAYER_ATTRIBUTION} url={TILE_LAYER_URL} opacity={0.92} />
                  <FitMapToPoints points={points} />
                  <FlyToSelectedPoint point={selectedPoint} />

                  {points.map((point) => {
                    const isSelected = point.id === selectedPoint?.id;
                    const pointColor = getPointColor(point.status);

                    return (
                      <CircleMarker
                        key={point.id}
                        center={[point.latitude, point.longitude]}
                        radius={isSelected ? 10 : 7.5}
                        pathOptions={{
                          color: isSelected ? "#111111" : "#ffffff",
                          weight: isSelected ? 2.2 : 1.6,
                          fillColor: pointColor,
                          fillOpacity: isSelected ? 0.96 : 0.84,
                        }}
                        eventHandlers={{
                          click: () => setSelectedPointId(point.id),
                        }}
                      >
                        <Tooltip direction="top" offset={[0, -8]} opacity={1} className="app-map-tooltip">
                          <div>
                            <p className="text-[12px] font-semibold text-[#111111]">{point.name}</p>
                            <p className="mt-1 text-[11px] text-[#5e5650]">{point.region}</p>
                          </div>
                        </Tooltip>
                      </CircleMarker>
                    );
                  })}
                </MapContainer>

                <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_18%_18%,rgba(255,235,214,0.32),transparent_28%),radial-gradient(circle_at_82%_14%,rgba(221,235,213,0.28),transparent_30%),radial-gradient(circle_at_52%_82%,rgba(225,223,245,0.22),transparent_28%)]" />

                <div className="pointer-events-none absolute inset-x-4 top-4 z-[500] flex flex-wrap items-start justify-between gap-3">
                  <div className="pointer-events-auto w-full max-w-[360px] rounded-[14px] bg-white/82 px-4 py-3 backdrop-blur-sm">
                    <div className="flex items-center gap-2 text-[11px] font-semibold text-[#554d46]">
                      <Crosshair size={14} className="text-[#111111]" />
                      Infrastructure footprint
                    </div>
                    <p className="mt-1 text-[11px] leading-5 text-[#5e5650]">Grab the map to pan, use the wheel to zoom, or select a point to inspect its operational context.</p>
                  </div>

                  <div className="pointer-events-auto w-full min-w-[220px] max-w-[280px] rounded-[14px] bg-white/82 px-4 py-3 backdrop-blur-sm sm:w-auto">
                    <div className="flex items-center gap-2 text-[11px] font-semibold text-[#554d46]">
                      <Layers3 size={14} className="text-[#111111]" />
                      Coverage
                    </div>
                    <div className="mt-2 space-y-1.5">
                      {sectorPreview.length ? (
                        sectorPreview.map(([sector, total]) => (
                          <div key={sector} className="flex items-center justify-between gap-4 text-[11px] text-[#5e5650]">
                            <span>{sector}</span>
                            <span className="font-semibold text-[#111111]">{total}</span>
                          </div>
                        ))
                      ) : (
                        <p className="text-[11px] text-[#5e5650]">No sector split yet.</p>
                      )}
                    </div>
                  </div>
                </div>

                {selectedPoint ? (
                  <div className="pointer-events-none absolute bottom-4 left-4 z-[500] w-full max-w-[360px] pr-4 sm:pr-0">
                    <div className="pointer-events-auto rounded-[16px] bg-white/90 px-4 py-4 shadow-[0_18px_40px_rgba(17,17,17,0.08)] backdrop-blur-sm">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="text-[13px] font-semibold text-[#111111]">{selectedPoint.name}</p>
                          <p className="mt-1 text-[11px] leading-5 text-[#5e5650]">{selectedPoint.region}</p>
                        </div>
                        <span className={`shrink-0 whitespace-nowrap rounded-full px-3 py-1 text-[10px] font-medium ${getStatusTone(selectedPoint.status)}`}>{formatStatusLabel(selectedPoint.status)}</span>
                      </div>
                      <p className="mt-2 text-[11px] leading-5 text-[#5e5650]">{selectedPoint.detail}</p>
                      <div className="mt-3 flex items-center gap-2 text-[11px] text-[#6c645d]">
                        <MapPin size={12} className="text-[#111111]" />
                        {selectedPoint.latitude}, {selectedPoint.longitude}
                      </div>
                    </div>
                  </div>
                ) : null}
              </>
            ) : (
              <div className="absolute inset-0 flex items-center justify-center p-8">
                <div className="max-w-sm rounded-[18px] bg-white/78 px-6 py-6 text-center shadow-[0_18px_40px_rgba(17,17,17,0.08)]">
                  <MapPin size={20} className="mx-auto text-[#111111]" />
                  <p className="mt-3 text-sm font-semibold text-[#111111]">No mapped records yet</p>
                  <p className="mt-2 text-sm leading-6 text-[#5e5650]">This map will automatically populate once the infrastructure records carry coordinates.</p>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="flex h-[540px] flex-col rounded-[22px] bg-white/72 p-4">
          <div className="border-b border-black/8 pb-3">
            <h3 className="text-sm font-semibold text-[#554d46]">Mapped points</h3>
            <p className="mt-1 text-[12px] leading-5 text-[#5e5650]">Infrastructure entries with coordinates and operational context.</p>
          </div>
          <div className="app-scroll mt-4 min-h-0 flex-1 space-y-2 overflow-y-auto pr-1">
            {points.length ? (
              points.map((point) => {
                const isSelected = point.id === selectedPoint?.id;
                return (
                  <button
                    key={point.id}
                    type="button"
                    onClick={() => setSelectedPointId(point.id)}
                    className={`w-full rounded-[16px] px-4 py-4 text-left transition ${isSelected ? "bg-[#f0eded33] shadow-[inset_0_0_0_1px_rgba(17,17,17,0.06)]" : "bg-white/82 hover:bg-[#f9f5ef]"}`}
                  >
                    <div className="flex items-center justify-between gap-3">
                      <h4 className="text-sm font-semibold text-[#111111]">{point.name}</h4>
                      <span className={`shrink-0 whitespace-nowrap rounded-full px-3 py-1 text-[10px] font-medium ${getStatusTone(point.status)}`}>{formatStatusLabel(point.status)}</span>
                    </div>
                    <p className="mt-2 text-[12px] font-medium text-[#554d46]">{point.region}</p>
                    <p className="mt-1 text-[12px] leading-5 text-[#5e5650]">{point.detail}</p>
                    <p className="mt-2 text-[11px] text-[#6c645d]">
                      Lat {point.latitude} / Lng {point.longitude}
                    </p>
                  </button>
                );
              })
            ) : (
              <p className="py-6 text-sm text-[#5e5650]">No geolocated records are available for this operational view.</p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
