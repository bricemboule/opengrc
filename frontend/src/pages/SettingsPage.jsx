import { ArrowRight, Boxes, Building2, Network, Settings, ShieldCheck, Users } from "lucide-react";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";

import PageHeader from "../components/crud/PageHeader";
import { moduleConfigs } from "../config/modules";
import { getSupportedViews } from "../config/moduleBehaviors";

function buildModuleRoute(moduleConfig, mode = null) {
  if (!moduleConfig) return "/settings";
  return mode && mode !== "list" ? `/modules/${moduleConfig.route}?mode=${mode}` : `/modules/${moduleConfig.route}`;
}

function SettingsCard({ moduleConfig, description }) {
  if (!moduleConfig) return null;
  const views = getSupportedViews(moduleConfig);
  const createHref = views.includes("create") ? buildModuleRoute(moduleConfig, "create") : null;

  return (
    <article className="rounded-[18px] bg-white/74 px-5 py-5 mt-2">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-[1rem] font-semibold text-slate-950">{moduleConfig.label}</h2>
          <p className="mt-1 text-sm leading-6 text-black/58">{description}</p>
        </div>
        <Link to={buildModuleRoute(moduleConfig)} className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-[#111111] text-white transition hover:bg-black/88">
          <ArrowRight size={15} strokeWidth={2.3} className="text-white" />
        </Link>
      </div>

      <div className="mt-4 flex flex-wrap gap-2.5">
        <Link
          to={buildModuleRoute(moduleConfig)}
          className="text-[0.85rem] inline-flex items-center justify-center rounded-full bg-white/80 font-medium text-[#111111] shadow-[0_0px_10px_rgba(17,17,17,0.03)] transition hover:bg-[#faf8f5]"
          style={{ paddingLeft: "2.15rem", paddingRight: "2.15rem", paddingTop: "0.58rem", paddingBottom: "0.58rem" }}
        >
          Open list
        </Link>
        {createHref ? (
          <Link
            to={createHref}
            className="text-[0.85rem] inline-flex items-center justify-center rounded-full bg-[#111111] font-medium text-white transition hover:bg-black/88"
            style={{ paddingLeft: "2.15rem", paddingRight: "2.15rem", paddingTop: "0.58rem", paddingBottom: "0.58rem", color: "#ffffff" }}
          >
            Create
          </Link>
        ) : null}
      </div>
    </article>
  );
}

export default function SettingsPage() {
  const user = useSelector((state) => state.auth.user);
  const permissions = user?.permissions || [];
  const isStaff = Boolean(user?.is_staff);

  function findModule(key) {
    return moduleConfigs.find((moduleConfig) => moduleConfig.key === key) || null;
  }

  function canAccess(moduleConfig) {
    if (!moduleConfig) return false;
    return !moduleConfig.permission || isStaff || permissions.includes(moduleConfig.permission);
  }

  const sections = [
    {
      key: "iam",
      title: "IAM & access",
      description: "Control who can enter the platform, what roles they hold, and which permissions are available.",
      icon: <ShieldCheck size={18} strokeWidth={2} />,
      cards: [
        { moduleConfig: findModule("users"), description: "Create users, assign workspace scope, activate or disable access, and manage temporary passwords." },
        { moduleConfig: findModule("roles"), description: "Here is where you can define reusable roles and assign grouped permissions to those roles." },
        { moduleConfig: findModule("permissions_catalog"), description: "Here is where you can review the permission catalog available for role design and for IAM checks." },
      ].filter((item) => canAccess(item.moduleConfig)),
    },
    {
      key: "institutions",
      title: "Institutions & sectors",
      description: "Manage the national institution directory and the sector registry those records should rely on.",
      icon: <Network size={18} strokeWidth={2} />,
      cards: [
        { moduleConfig: findModule("sectors"), description: "Create the official sector list which re going to be used by institutions, CII, and standards." },
        { moduleConfig: findModule("organizations"), description: "This is where you can manage workspace organizations and internal administrative entities." },
        { moduleConfig: findModule("organization_types"), description: "Here you can manage the organization type catalog which is used by workspace organizations." },
      ].filter((item) => canAccess(item.moduleConfig)),
    },
    {
      key: "assets",
      title: "Assets & ownership",
      description: "Maintain critical infrastructure and supporting resource registries with clear ownership links.",
      icon: <Boxes size={18} strokeWidth={2} />,
      cards: [
        { moduleConfig: findModule("assets"), description: "This is for management of generic operational resources which are used by the broader platform." },
        { moduleConfig: findModule("asset_types"), description: "Here you can manage the generic resource type catalog which is used by resource records." },
      ].filter((item) => canAccess(item.moduleConfig)),
    },
  ].filter((section) => section.cards.length);

  return (
    <div className="space-y-8">
      <PageHeader
        title="Settings"
        description="This workspace groups the setup records that drive access control, institutions, sectors, and asset ownership across the platform."
        eyebrow={
          <div className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/80 text-[#111111]">
            <Settings size={18} strokeWidth={2} />
          </div>
        }
      />

      {sections.length ? (
        <div className="space-y-6">
          {sections.map((section) => (
            <section key={section.key} className="space-y-4 mt-12">
              <div className="flex items-start gap-3">
                <span className="mt-1 inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/82 text-[#111111]">{section.icon}</span>
                <div>
                  <h2 className="text-[1.15rem] font-semibold text-slate-950">{section.title}</h2>
                  <p className="mt-1 text-sm leading-6 text-black/56">{section.description}</p>
                </div>
              </div>

              <div className="grid gap-4 xl:grid-cols-2">
                {section.cards.map((card) => (
                  <SettingsCard key={card.moduleConfig.key} moduleConfig={card.moduleConfig} description={card.description} />
                ))}
              </div>
            </section>
          ))}
        </div>
      ) : (
        <section className="rounded-[18px] bg-white/74 px-5 py-6">
          <div className="flex items-start gap-3">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white text-[#111111]">
              <Building2 size={18} strokeWidth={2} />
            </span>
            <div>
              <h2 className="text-[1rem] font-semibold text-slate-950">No settings modules available</h2>
              <p className="mt-1 text-sm leading-6 text-black/56">Your current account does not expose any settings modules yet.</p>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
