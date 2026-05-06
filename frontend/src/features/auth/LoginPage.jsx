import { useState } from "react";
import { useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Eye,
  EyeOff,
  KeyRound,
  Lock,
  Mail,
  Network,
  ShieldCheck,
} from "lucide-react";
import { loginRequest } from "./api";
import { setAuth } from "./authSlice";
import logo from "../../assets/mocde-logo.jpeg";

function normalizeLoginErrorMessage(message, hasResponse) {
  const normalizedMessage = String(message || "").trim();

  if (!normalizedMessage) {
    return hasResponse
      ? "Connection failed."
      : "Unable to reach the login API.";
  }

  const loweredMessage = normalizedMessage.toLowerCase();
  if (
    loweredMessage === "connexion echouee." ||
    loweredMessage === "connexion echouee"
  ) {
    return "Connection failed.";
  }

  if (
    loweredMessage === "impossible de joindre l api de connexion." ||
    loweredMessage === "impossible de joindre l api de connexion"
  ) {
    return "Unable to reach the login API.";
  }

  return normalizedMessage;
}

export default function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);

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
        normalizeLoginErrorMessage(
          err?.response?.data?.detail ||
            err?.response?.data?.non_field_errors?.[0] ||
            err?.response?.data?.non_field_errors,
          Boolean(err?.response),
        ),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid min-h-screen bg-background lg:grid-cols-2">
      <aside
        className="relative hidden flex-col justify-between overflow-hidden p-12 text-primary-foreground lg:flex"
        style={{ background: "var(--gradient-hero)" }}
      >
        <div
          className="absolute inset-0 opacity-[0.08]"
          style={{
            backgroundImage:
              "radial-gradient(circle at 20% 20%, white 1px, transparent 1px), radial-gradient(circle at 70% 60%, white 1px, transparent 1px)",
            backgroundSize: "60px 60px, 90px 90px",
          }}
        />
        <div className="relative">
          <Link to="/" className="group inline-flex items-center gap-3">
            <div className="h-14 w-14 rounded-xl bg-white/95 p-1.5 shadow-lg">
              <img
                src={logo}
                alt="MOCDE"
                className="h-full w-full rounded-md object-contain"
              />
            </div>
            <div className="leading-tight">
              <div className="text-base font-bold tracking-wide">
                National-3CPERS
              </div>
              <div className="text-xs text-white/75">
                Republic of The Gambia - MOCDE
              </div>
            </div>
          </Link>
        </div>

        <div className="relative max-w-md">
          <div className="mb-4 text-xs font-semibold uppercase tracking-[0.2em] text-white/70">
            Secure access
          </div>
          <h1 className="text-3xl font-bold leading-tight xl:text-4xl">
            Coordinated cyber response, in real time.
          </h1>
          <p className="mt-4 leading-relaxed text-white/85">
            One verified identity. One unified workspace. Sign in to coordinate
            incidents with government agencies, telecom operators, banks and the
            National CERT.
          </p>

          <div className="mt-10 space-y-4">
            {[
              { icon: ShieldCheck, text: "End-to-end encrypted sessions" },
              {
                icon: KeyRound,
                text: "Role-based access for verified responders",
              },
            ].map((feature) => (
              <div key={feature.text} className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white/15 backdrop-blur">
                  <feature.icon className="h-4 w-4" />
                </div>
                <div className="text-sm text-white/90">{feature.text}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="relative text-xs text-white/60">
          {new Date().getFullYear()} Ministry of Communications & Digital
          Economy
        </div>
      </aside>

      <main className="flex flex-col px-6 py-10 sm:px-12 lg:px-16">
        <div className="flex items-center justify-between">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-sm text-muted-foreground transition hover:text-primary"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to home
          </Link>
          <div className="flex items-center gap-2 lg:hidden">
            <img src={logo} alt="MOCDE" className="h-9 w-9 object-contain" />
            <span className="text-sm font-bold text-primary">
              National-3CPERS
            </span>
          </div>
        </div>

        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-md py-12">
            <div className="mb-8">
              <h2 className="text-3xl font-bold tracking-tight text-primary">
                Sign in
              </h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Enter your official credentials to access the platform.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-2">
                <label
                  htmlFor="email"
                  className="text-sm font-medium text-foreground"
                >
                  Official email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <input
                    id="email"
                    type="email"
                    autoComplete="email"
                    placeholder="you@agency.gov.gm"
                    value={form.email}
                    onChange={(event) =>
                      setForm({ ...form, email: event.target.value })
                    }
                    className="h-11 w-full rounded-md border border-input bg-background px-3 pl-9 text-sm outline-none transition focus:ring-2 focus:ring-ring/30"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label
                    htmlFor="password"
                    className="text-sm font-medium text-foreground"
                  >
                    Password
                  </label>
                  <button
                    type="button"
                    className="text-xs font-medium text-primary hover:underline"
                  >
                    Forgot password?
                  </button>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    autoComplete="current-password"
                    placeholder="Enter your password"
                    value={form.password}
                    onChange={(event) =>
                      setForm({ ...form, password: event.target.value })
                    }
                    className="h-11 w-full rounded-md border border-input bg-background px-3 pl-9 pr-10 text-sm outline-none transition focus:ring-2 focus:ring-ring/30"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((value) => !value)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground transition hover:text-primary"
                    aria-label={
                      showPassword ? "Hide password" : "Show password"
                    }
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <input
                  id="remember"
                  type="checkbox"
                  checked={remember}
                  onChange={(event) => setRemember(event.target.checked)}
                  className="h-4 w-4 rounded border-input accent-[#153b7a]"
                />
                <label
                  htmlFor="remember"
                  className="text-sm font-normal text-muted-foreground"
                >
                  Keep me signed in on this secure device
                </label>
              </div>

              {error ? (
                <p className="text-sm leading-6 text-[#a63d34]">{error}</p>
              ) : null}

              <button
                type="submit"
                className="inline-flex h-11 w-full items-center justify-center rounded-md bg-primary px-4 text-base font-semibold text-primary-foreground transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={loading}
              >
                {loading ? "Signing in..." : "Sign in"}
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
