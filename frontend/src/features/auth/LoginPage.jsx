import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { loginRequest } from "./api";
import { setAuth } from "./authSlice";

function GambiaFlagPanel() {
  return (
    <div className="relative min-h-[260px] overflow-hidden md:min-h-[320px] lg:min-h-full">
      <div className="absolute inset-0 flex h-full w-full flex-col">
        <div className="h-[33%] bg-[#CE1126]" />
        <div className="h-[4%] bg-white" />
        <div className="h-[22%] bg-[#0C1C8C]" />
        <div className="h-[4%] bg-white" />
        <div className="h-[37%] bg-[#3A7728]" />
      </div>
    </div>
  );
}

function Field({ label, type, placeholder, value, onChange }) {
  return (
    <div className="space-y-3">
      <label className="block text-[15px] font-medium text-[#161616]">{label}</label>
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="h-12 w-full rounded-xl border border-transparent bg-[#f6f6f6] px-4 text-sm text-slate-900 outline-none transition focus:border-[#0C1C8C]/20 focus:bg-white focus:ring-4 focus:ring-[#0C1C8C]/8"
      />
    </div>
  );
}

export default function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await loginRequest(form);
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      dispatch(setAuth(data.user));
      navigate("/dashboard");
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
        err?.response?.data?.non_field_errors?.[0] ||
        err?.response?.data?.non_field_errors ||
        (err?.response ? "Connexion échouée." : "Impossible de joindre l'API de connexion.")
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#f7f7f5] px-4 py-8 md:px-8">
      <div className="grid w-full max-w-[1088px] overflow-hidden rounded-[6px] bg-white shadow-[0_14px_48px_rgba(15,23,42,0.08)] lg:min-h-[528px] lg:grid-cols-[1.04fr_1fr]">
        <GambiaFlagPanel />

        <div className="flex items-center px-6 py-8 sm:px-10 md:px-12 lg:px-12">
          <div className="w-full">
            <p className="max-w-[420px] text-[14px] leading-8 text-[#8b8e98]">
              Bienvenue sur la plateforme de gestion OpenGRC. Connectez-vous pour accéder à votre espace.
            </p>

            <div className="mt-5 border-b border-[#e5e7eb] pb-3 text-[14px] text-[#8b8e98]">
              Informations sur le compte
            </div>

            <form onSubmit={handleSubmit} className="mt-8 space-y-9">
              <Field
                label="Identifiant"
                type="email"
                placeholder=""
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />

              <Field
                label="Mot de passe"
                type="password"
                placeholder=""
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
              />

              {error ? (
                <div className="rounded-xl border border-[#CE1126]/20 bg-[#fff4f4] px-4 py-3 text-sm text-[#A30D1D]">
                  {error}
                </div>
              ) : null}

              <button
                type="submit"
                disabled={loading}
                className="h-12 w-full rounded-lg bg-[#3A7728] text-[15px] font-semibold tracking-[0.08em] text-white transition hover:bg-[#2f651f] disabled:cursor-not-allowed disabled:opacity-70"
              >
                {loading ? "CONNEXION..." : "CONNEXION"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
