import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowRight,
  Activity,
  AlertCircle,
  Boxes,
  CheckCircle2,
  Database,
  ClipboardList,
  LogIn,
  MapPin,
  Network,
  ShieldCheck,
} from "lucide-react";
import logo from "../assets/mocde-logo.jpeg";
import gictaLogo from "../assets/gicta-logo.jpg";
import heroImage from "../assets/hero-light.jpg";
import bannerImage from "../assets/banner-collaboration.jpg";

const partnerLogos = [
  {
    src: gictaLogo,
    alt: "The Gambia Information and Communication Technology Agency",
    label: "GICTA",
    stageClassName: "max-w-4xl",
    imageClassName: "max-h-[260px] max-w-full",
  },
  {
    src: "/gm-cert-logo.png",
    alt: "GM-CERT - Gambia Computer Emergency Response Team",
    label: "GM-CERT",
    stageClassName: "max-w-[520px]",
    imageClassName: "h-full max-h-[330px] w-auto",
  },
];

function ButtonLink({ to, href, variant = "solid", children }) {
  const className =
    variant === "outline"
      ? "inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border border-[#00336f]/25 bg-white px-5 py-3 text-sm font-bold text-[#00336f] shadow-sm transition hover:border-[#00336f]/45 hover:bg-[#f4f8ff]"
      : "landing-primary-cta inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-[#00336f] px-5 py-3 text-sm font-bold shadow-[0_14px_28px_rgba(0,51,111,0.2)] ring-1 ring-[#335d91]/25 transition hover:bg-[#002653] hover:shadow-[0_16px_32px_rgba(0,38,83,0.24)]";

  if (href) {
    return (
      <a href={href} className={className}>
        {children}
      </a>
    );
  }

  return (
    <Link to={to} className={className}>
      {children}
    </Link>
  );
}

function Card({ children, className = "" }) {
  return (
    <div className={`rounded-xl border border-border/60 bg-card ${className}`}>
      {children}
    </div>
  );
}

function LogoCarousel() {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const intervalId = window.setInterval(() => {
      setActiveIndex((current) => (current + 1) % partnerLogos.length);
    }, 4000);

    return () => window.clearInterval(intervalId);
  }, []);

  return (
    <div className="relative mx-auto max-w-5xl overflow-hidden rounded-xl border border-border/60 bg-white shadow-[var(--shadow-card)]">
      <div className="relative min-h-[300px] md:min-h-[390px]">
        {partnerLogos.map((item, index) => (
          <div
            key={item.label}
            className={`absolute inset-0 flex items-center justify-center px-6 py-10 transition-all duration-700 ease-out ${
              index === activeIndex
                ? "translate-x-0 opacity-100"
                : "translate-x-4 opacity-0"
            }`}
          >
            <div
              className={`flex h-full w-full items-center justify-center ${item.stageClassName}`}
            >
              <img
                src={item.src}
                alt={item.alt}
                loading={index === 0 ? "eager" : "lazy"}
                className={`object-contain ${item.imageClassName}`}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="absolute bottom-4 left-0 right-0 flex justify-center gap-2">
        {partnerLogos.map((item, index) => (
          <button
            key={item.label}
            type="button"
            onClick={() => setActiveIndex(index)}
            className={`h-2.5 rounded-full transition-all ${
              index === activeIndex
                ? "w-8 bg-[#00336f]"
                : "w-2.5 bg-[#00336f]/25"
            }`}
            aria-label={`Show ${item.label} logo`}
          />
        ))}
      </div>
    </div>
  );
}

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur-md">
        <div className="container mx-auto flex h-20 items-center justify-between px-6">
          <Link to="/" className="flex items-center gap-3">
            <img
              src={logo}
              alt="MOCDE - Republic of The Gambia"
              className="h-12 w-12 object-contain"
            />
            <div className="leading-tight">
              <div className="text-sm font-bold text-primary">
                National-3CPERS
              </div>
              <div className="hidden text-[11px] text-muted-foreground sm:block">
                National Cyber Coordination & Communication Platform
              </div>
            </div>
          </Link>

          <ButtonLink to="/login">
            <LogIn className="h-4 w-4" />
            Sign in
          </ButtonLink>
        </div>
      </header>

      <section className="relative isolate overflow-hidden bg-background">
        <div
          className="absolute inset-0 -z-10 opacity-[0.05]"
          style={{
            backgroundImage:
              "radial-gradient(circle at 20% 20%, oklch(0.30 0.10 240) 1px, transparent 1px), radial-gradient(circle at 80% 60%, oklch(0.30 0.10 240) 1px, transparent 1px)",
            backgroundSize: "60px 60px, 90px 90px",
          }}
        />
        <div className="container mx-auto px-6 pb-20 pt-16 md:pb-28 md:pt-20">
          <div className="grid items-center gap-10 lg:grid-cols-12 lg:gap-16">
            <div className="lg:col-span-6">
              <div className="mb-6 inline-flex rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
                WARDIP - Strategic Plan v1.0 - 2026
              </div>
              <h1 className="font-bold leading-[1.1] tracking-tight text-primary">
                <span className="block whitespace-nowrap text-3xl sm:text-4xl md:text-5xl lg:text-[3.25rem] xl:text-6xl">
                  National-3CPERS
                </span>
                <span className="mt-2 block bg-gradient-to-r from-primary via-primary to-secondary bg-clip-text text-2xl text-transparent sm:text-3xl md:text-4xl lg:text-5xl">
                  Cyber Emergency Coordination
                </span>
              </h1>
              <p className="mt-4 text-base leading-relaxed text-muted-foreground md:text-lg">
                <span className="font-medium text-foreground">
                  National Cyber Coordination and Communication Platform for
                  Emergency Response Situation.
                </span>{" "}
                A single pane of glass uniting government agencies, telecoms and
                banks, powered by enterprise-grade open-source engines for
                incident response, threat intelligence and GIS situational
                awareness.
              </p>
              <div className="mt-10 flex flex-wrap gap-4">
                <ButtonLink to="/login">
                  <LogIn className="h-4 w-4" />
                  Access the platform
                </ButtonLink>
                <ButtonLink href="#overview" variant="outline">
                  Learn more
                  <ArrowRight className="h-4 w-4" />
                </ButtonLink>
              </div>

              <div className="mt-12 grid grid-cols-2 gap-6 border-t border-border/60 pt-8 sm:grid-cols-4">
                {[{ k: "1", l: "Unified interface" }].map((s) => (
                  <div key={s.l}>
                    <div className="text-3xl font-bold text-primary">{s.k}</div>
                    <div className="mt-1 text-xs text-muted-foreground">
                      {s.l}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative lg:col-span-6">
              <div
                className="absolute -inset-6 -z-10 rounded-[2rem] opacity-30 blur-3xl"
                style={{ background: "var(--gradient-accent)" }}
              />
              <div className="relative overflow-hidden rounded-2xl border border-border/60 bg-card shadow-[var(--shadow-elegant)]">
                <img
                  src={heroImage}
                  alt="National-3CPERS coordination dashboard"
                  width={1280}
                  height={1280}
                  className="h-auto w-full"
                />
              </div>
              <div className="absolute -bottom-4 -left-4 flex items-center gap-3 rounded-xl border border-border bg-card px-4 py-3 shadow-[var(--shadow-card)] sm:-left-6">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-secondary/15 text-secondary">
                  <ShieldCheck className="h-5 w-5" />
                </div>
                <div className="leading-tight">
                  <div className="text-xs text-muted-foreground">Status</div>
                  <div className="text-sm font-semibold text-primary">
                    All systems live
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-border/60 bg-muted/30">
        <div className="container mx-auto px-6 py-10">
          <div className="grid items-center gap-8 md:grid-cols-12">
            <div className="md:col-span-4">
              <div className="mb-2 text-xs font-semibold uppercase tracking-wider text-accent">
                WARDIP Initiative
              </div>
              <h2 className="text-xl font-bold leading-tight text-primary md:text-2xl">
                One platform. Every responder. Real-time.
              </h2>
            </div>
            <div className="md:col-span-8">
              <div className="overflow-hidden rounded-xl border border-border/60 bg-card shadow-[var(--shadow-card)]">
                <img
                  src={bannerImage}
                  alt="WARDIP collaboration workspace"
                  className="h-full min-h-[220px] w-full object-cover"
                />
              </div>
            </div>
          </div>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-x-12 gap-y-4 text-sm font-medium text-muted-foreground">
            <span className="text-xs uppercase tracking-wider">
              Trusted stakeholders
            </span>
            <span>MOCDE</span>
            <span>National CERT</span>
            <span>Central Bank</span>
            <span>Telecom Operators</span>
            <span>Critical Infrastructure</span>
          </div>
        </div>
      </section>

      <section className="container mx-auto px-6 py-20">
        <div className="mb-8 max-w-2xl">
          <div className="mb-3 text-sm font-semibold uppercase tracking-wider text-accent">
            Institutional Partners
          </div>
          <h2 className="text-3xl font-bold text-primary md:text-4xl">
            Coordinated national cyber response ecosystem
          </h2>
        </div>
        <LogoCarousel />
      </section>

      <footer className="border-t border-border/60 bg-background">
        <div className="container mx-auto flex flex-col items-center justify-between gap-4 px-6 py-10 md:flex-row">
          <div className="flex items-center gap-3">
            <img src={logo} alt="MOCDE" className="h-10 w-10 object-contain" />
            <div className="text-sm">
              <div className="font-semibold text-primary">
                National-3CPERS - Republic of The Gambia
              </div>
              <div className="text-xs text-muted-foreground">
                Ministry of Communications & Digital Economy
              </div>
            </div>
          </div>
          <div className="text-xs text-muted-foreground">
            {new Date().getFullYear()} MOCDE - All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
