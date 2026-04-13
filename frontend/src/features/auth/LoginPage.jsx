import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { loginRequest } from "./api";
import { setAuth } from "./authSlice";
import BrandLogo from "../../components/brand/BrandLogo";
import loginHeroServer from "../../assets/login-hero-server.jpg";

function Field({ label, type, placeholder, value, onChange }) {
  return (
    <div className="space-y-3">
      <label className="ml-4 block text-[13px] font-normal text-[#5e5650]">{label}</label>
      <input type={type} placeholder={placeholder} value={value} onChange={onChange} className="app-input login-input" />
    </div>
  );
}

export default function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
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
          (err?.response ? "Connexion echouee." : "Impossible de joindre l API de connexion."),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="h-screen overflow-hidden px-3 py-3 sm:px-4 sm:py-4">
      <div className="grid h-full w-full gap-4 lg:grid-cols-[1.12fr_0.88fr]">
        <section className="overflow-hidden rounded-[24px] pt-0 pr-2 pb-0 pl-0 sm:pt-0.5 sm:pr-2.5 sm:pb-0.5 sm:pl-0.5">
          <img src={loginHeroServer} alt="Critical infrastructure systems" className="h-full min-h-[300px] w-full rounded-[20px] object-cover object-center" />
        </section>

        <section className="flex items-center justify-center px-4 py-5 sm:px-8 lg:px-12">
          <div className="w-full max-w-[440px]">
            <BrandLogo title="OpenGRC" compact />

            <h1 className="mt-8 text-[2.2rem] font-semibold tracking-[-0.06em] text-slate-950">Welcome back</h1>
            <p className="mt-3 max-w-md text-sm leading-7 text-[#5e5650]">
              Connect to the OpenGRC workspace to continue with your dashboards, workflows, and operational reviews.
            </p>

            <div className="mt-8 border-b border-slate-200/70 pb-3 text-sm text-[#5e5650]">Account access</div>

            <form onSubmit={handleSubmit} className="mt-7 space-y-6">
              <Field
                label="Identifier"
                type="email"
                placeholder="name@company.com"
                value={form.email}
                onChange={(event) => setForm({ ...form, email: event.target.value })}
              />

              <Field
                label="Password"
                type="password"
                placeholder="Enter your password"
                value={form.password}
                onChange={(event) => setForm({ ...form, password: event.target.value })}
              />

              {error ? <div className="rounded-[24px] bg-[#fff1ef] px-4 py-3 text-sm text-[#a63d34]">{error}</div> : null}

              <div className="pt-3">
              <button type="submit" disabled={loading} className="app-button app-button-dark login-submit w-full">
                {loading ? "Connecting..." : "Connect"}
              </button>
              </div>
            </form>
          </div>
        </section>
      </div>
    </div>
  );
}

