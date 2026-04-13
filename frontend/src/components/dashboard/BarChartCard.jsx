import { BarChart, Bar, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const BAR_COLORS = ["#ffd3b2", "#93e1a4", "#b8abff", "#f0be7c", "#8eb2ff"];

export default function BarChartCard({ title, data = [], dataKey, xKey }) {
  return (
    <section className="app-surface rounded-[24px] p-5 sm:p-6">
      <div>
        <h3 className="text-xl font-semibold tracking-[-0.04em] text-slate-950">{title}</h3>
        <p className="mt-1 text-[13px] text-[#5e5650]">Operational distribution across the selected records.</p>
      </div>

      <div className="mt-5 h-72 sm:h-80">
        {data.length ? (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} barCategoryGap={18}>
              <CartesianGrid vertical={false} stroke="rgba(17,17,17,0.08)" />
              <XAxis dataKey={xKey} axisLine={false} tickLine={false} tick={{ fill: "#78716c", fontSize: 12 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fill: "#78716c", fontSize: 12 }} />
              <Tooltip
                cursor={{ fill: "rgba(255,255,255,0.25)" }}
                contentStyle={{
                  border: 0,
                  borderRadius: 12,
                  background: "rgba(255,255,255,0.95)",
                  color: "#111111",
                  boxShadow: "none",
                }}
              />
              <Bar dataKey={dataKey} radius={[12, 12, 4, 4]}>
                {data.map((entry, index) => (
                  <Cell key={`${title}-${entry[xKey] ?? index}`} fill={BAR_COLORS[index % BAR_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex h-full items-center justify-center rounded-[18px] bg-white/64 text-sm text-[#5e5650]">
            No chart data available yet.
          </div>
        )}
      </div>
    </section>
  );
}
