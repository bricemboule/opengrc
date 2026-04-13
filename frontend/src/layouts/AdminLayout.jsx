import { useEffect, useMemo, useState } from "react";
import { ChevronDown, ChevronRight, LogOut, PanelLeftClose, PanelLeftOpen, Settings } from "lucide-react";
import { FiBarChart2, FiBell, FiFileText, FiFolderPlus, FiList, FiMap, FiSearch, FiUpload, FiX } from "react-icons/fi";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { clearAuth } from "../features/auth/authSlice";

import { moduleConfigs } from "../config/modules";
import { getSupportedViews } from "../config/moduleBehaviors";
import { buildMenu } from "./menu";
import useNotificationsSocket from "../hooks/useNotificationsSocket";
import BrandLogo from "../components/brand/BrandLogo";

function getLocationMode(location) {
  return new URLSearchParams(location.search).get("mode") || "list";
}

function getTargetMode(to) {
  const searchIndex = to.indexOf("?");
  const search = searchIndex >= 0 ? to.slice(searchIndex + 1) : "";
  return new URLSearchParams(search).get("mode") || "list";
}

function childIsActive(location, to) {
  const pathname = to.split("?")[0];
  return location.pathname === pathname && getLocationMode(location) === getTargetMode(to);
}

function buildOpenState(menuItems, location) {
  return menuItems.reduce((accumulator, item) => {
    if (item.type === "dropdown") {
      accumulator[item.key] = item.sections.some((section) => section.items.some((child) => childIsActive(location, child.to)));
    }
    return accumulator;
  }, {});
}

function buildSectionOpenState(menuItems, location) {
  return menuItems.reduce((accumulator, item) => {
    if (item.type === "dropdown") {
      const activeSection = item.sections.find((section) => section.items.some((child) => childIsActive(location, child.to)));
      accumulator[item.key] = activeSection?.title || null;
    }
    return accumulator;
  }, {});
}

function formatNotificationDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "Now" : date.toLocaleString();
}

const previewNotifications = [
  {
    id: "preview-1",
    message: "Desk study review for the national telecom backbone moved to In review and is due today.",
    receivedAt: "2026-04-13T08:30:00",
  },
  {
    id: "preview-2",
    message: "Stakeholder consultation with the national energy regulator was scheduled for April 15, 2026.",
    receivedAt: "2026-04-13T07:10:00",
  },
  {
    id: "preview-3",
    message: "Action plan task on backup power resilience is blocked pending infrastructure validation.",
    receivedAt: "2026-04-12T17:25:00",
  },
];

export default function AdminLayout() {
  useNotificationsSocket();
  const user = useSelector((state) => state.auth.user);
  const notifications = useSelector((state) => state.notifications.items);
  const visibleNotifications = notifications.length ? notifications : previewNotifications;
  const permissions = user?.permissions || [];
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const menuItems = useMemo(() => buildMenu(moduleConfigs), []);
  const activeDropdowns = useMemo(
    () =>
      menuItems.reduce((accumulator, item) => {
        if (item.type === "dropdown") {
          accumulator[item.key] = item.sections.some((section) => section.items.some((child) => childIsActive(location, child.to)));
        }
        return accumulator;
      }, {}),
    [location, menuItems],
  );
  const [openDropdowns, setOpenDropdowns] = useState(() => buildOpenState(menuItems, location));
  const [openSections, setOpenSections] = useState(() => buildSectionOpenState(menuItems, location));
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(() => {
    if (typeof window === "undefined") return false;
    return window.localStorage.getItem("opengrc-sidebar-collapsed") === "true";
  });

  useEffect(() => {
    if (typeof window === "undefined") return;
    window.localStorage.setItem("opengrc-sidebar-collapsed", String(isSidebarCollapsed));
  }, [isSidebarCollapsed]);

  useEffect(() => {
    setOpenDropdowns((current) =>
      Object.entries(activeDropdowns).reduce(
        (accumulator, [key, isActive]) => {
          accumulator[key] = isActive ? true : (current[key] ?? false);
          return accumulator;
        },
        { ...current },
      ),
    );
  }, [activeDropdowns]);

  useEffect(() => {
    setIsNotificationsOpen(false);
  }, [location.pathname, location.search]);

  useEffect(() => {
    setOpenSections((current) =>
      menuItems.reduce(
        (accumulator, item) => {
          if (item.type !== "dropdown") return accumulator;
          const activeSection = item.sections.find((section) => section.items.some((child) => childIsActive(location, child.to)));
          accumulator[item.key] = activeSection?.title || current[item.key] || null;
          return accumulator;
        },
        { ...current },
      ),
    );
  }, [location, menuItems]);

  const filteredMenu = menuItems.filter((item) => {
    if (item.type === "dropdown") {
      return item.sections.some((section) => !section.permission || permissions.includes(section.permission));
    }
    return !item.permission || permissions.includes(item.permission);
  });
  const currentModuleConfig = useMemo(() => moduleConfigs.find((item) => location.pathname.startsWith(`/modules/${item.route}`)) || null, [location.pathname]);
  const quickAddTarget = useMemo(() => {
    const getCreateRoute = (config) => {
      if (!config) return null;
      if (config.permission && !permissions.includes(config.permission)) return null;
      return getSupportedViews(config).includes("create") ? `/modules/${config.route}?mode=create` : null;
    };

    return getCreateRoute(currentModuleConfig) || moduleConfigs.map(getCreateRoute).find(Boolean) || null;
  }, [currentModuleConfig, permissions]);

  function logout() {
    dispatch(clearAuth());
    navigate("/login");
  }

  function renderActionIcon(label) {
    if (label === "Create") return <FiFolderPlus size={14} />;
    if (label.includes("Import")) return <FiUpload size={14} />;
    if (label.includes("GIS") || label.includes("Map")) return <FiMap size={14} />;
    if (label.includes("Search")) return <FiSearch size={14} />;
    if (label.includes("Report")) return <FiBarChart2 size={14} />;
    if (label.includes("Workflow") || label.includes("board")) return <FiList size={14} />;
    if (label.includes("List")) return <FiList size={14} />;
    return <FiFileText size={14} />;
  }

  function toggleDropdown(key) {
    setOpenDropdowns((current) => ({ ...current, [key]: !current[key] }));
  }

  function toggleSection(dropdownKey, sectionTitle) {
    setOpenSections((current) => ({
      ...current,
      [dropdownKey]: current[dropdownKey] === sectionTitle ? null : sectionTitle,
    }));
  }

  function handleQuickAdd() {
    if (quickAddTarget) navigate(quickAddTarget);
  }

  const sidebarWidth = isSidebarCollapsed ? "96px" : "290px";

  return (
    <div className="min-h-screen">
      <div className="min-h-screen xl:block" style={{ "--sidebar-width": sidebarWidth }}>
        <aside className="app-glass flex min-h-screen flex-col border-r border-slate-200/70 px-5 py-6 transition-[width] duration-300 ease-out xl:fixed xl:inset-y-0 xl:left-0 xl:z-30 xl:h-screen xl:w-[var(--sidebar-width)]">
          <div className={`flex w-full items-center ${isSidebarCollapsed ? "justify-center gap-2 px-0" : "justify-between pl-2 pr-0"} transition-all duration-300 ease-out`}>
            <BrandLogo title="OpenGRC" compact collapsed={isSidebarCollapsed} />
            <button
              type="button"
              onClick={() => setIsSidebarCollapsed((current) => !current)}
              className={`${isSidebarCollapsed ? "" : "ml-auto"} flex h-10 w-10 items-center justify-center rounded-full text-[#5e5650]/55 transition hover:bg-white/66 hover:text-[#111111] active:text-[#111111]`}
              aria-label={isSidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            >
              {isSidebarCollapsed ? <PanelLeftOpen size={18} strokeWidth={1.8} /> : <PanelLeftClose size={18} strokeWidth={1.8} />}
            </button>
          </div>

          <nav className="app-scroll app-scroll-hidden mt-6 flex-1 space-y-1 overflow-y-auto pr-1">
            {filteredMenu.map((item) => {
              if (item.type === "dropdown") {
                const Icon = item.icon;
                const visibleSections = item.sections.filter((section) => !section.permission || permissions.includes(section.permission));
                const isOpen = openDropdowns[item.key];
                const isActive = activeDropdowns[item.key];

                return (
                  <div key={item.key} className="pt-1">
                    <button
                      type="button"
                      onClick={() => toggleDropdown(item.key)}
                      title={isSidebarCollapsed ? item.label : undefined}
                      className={`flex w-full items-center ${isSidebarCollapsed ? "justify-center rounded-[18px] px-0 py-2.5" : "justify-between gap-3 rounded-full px-4 py-2"} text-[12px] font-medium transition ${
                        isActive ? "bg-[#111111] text-white" : "text-slate-600 hover:bg-white/66 hover:text-slate-900"
                      }`}
                      style={{ fontSize: "12px", lineHeight: "1.2" }}
                    >
                      <span className={`flex items-center ${isSidebarCollapsed ? "justify-center" : "gap-3"}`}>
                        <span className={`flex h-8 w-8 items-center justify-center rounded-full ${isActive ? "bg-white/12 text-white" : "bg-transparent text-slate-500"}`}>
                          <Icon size={16} />
                        </span>
                        {!isSidebarCollapsed ? (
                          <span className={`overflow-hidden whitespace-nowrap transition-[max-width,opacity] duration-200 ease-out ${isActive ? "text-white" : "text-slate-600"}`}>{item.label}</span>
                        ) : null}
                      </span>
                      {!isSidebarCollapsed ? (isOpen ? <ChevronDown size={20} strokeWidth={1.5} /> : <ChevronRight size={20} strokeWidth={1.5} />) : null}
                    </button>

                    {!isSidebarCollapsed && isOpen ? (
                      <div className="relative ml-5 mt-3 space-y-2 pl-7 before:absolute before:left-[15px] before:top-2 before:bottom-2 before:w-px before:bg-black/8">
                        {visibleSections.map((section) => {
                          const isSectionOpen = openSections[item.key] === section.title;
                          const isSectionActive = section.items.some((child) => childIsActive(location, child.to));

                          return (
                            <div key={section.title} className={`rounded-[22px] p-1 transition ${isSectionOpen || isSectionActive ? "bg-white/55" : "bg-transparent"}`}>
                              <button
                                type="button"
                                onClick={() => toggleSection(item.key, section.title)}
                                className={`flex w-full items-center justify-between gap-3 rounded-[18px] px-3 py-1.5 text-left text-[12px] font-semibold tracking-[0.02em] transition ${
                                  isSectionActive ? "text-slate-900" : "text-slate-500 hover:bg-black/5 hover:text-slate-800"
                                }`}
                                style={{ fontSize: "12px", lineHeight: "1.2" }}
                              >
                                <span>{section.title}</span>
                                {isSectionOpen ? <ChevronDown size={18} strokeWidth={1.5} /> : <ChevronRight size={18} strokeWidth={1.5} />}
                              </button>

                              {isSectionOpen ? (
                                section.items.length ? (
                                  <div className="space-y-1 px-1 pb-1">
                                    {section.items.map((child) => {
                                      const isChildActive = childIsActive(location, child.to);
                                      return (
                                        <NavLink
                                          key={child.to}
                                          to={child.to}
                                          className={() =>
                                            `group relative flex items-center gap-2.5 rounded-[16px] px-3 py-1.5 text-[13px] transition ${
                                              isChildActive
                                                ? "bg-[#f0eded33] text-slate-950"
                                                : "text-slate-500 hover:bg-black/5 hover:text-slate-900 focus-visible:bg-[#f0eded33] focus-visible:text-slate-950"
                                            }`
                                          }
                                        >
                                          <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${isChildActive ? "bg-[#111111]" : "bg-black/12 group-hover:bg-black/30"}`} />
                                          <span className={`text-[13px] ${isChildActive ? "text-slate-900" : "text-slate-400"}`}>{renderActionIcon(child.label)}</span>
                                          <span>{child.label}</span>
                                        </NavLink>
                                      );
                                    })}
                                  </div>
                                ) : (
                                  <p className="px-3 pb-2 text-xs text-slate-400">Catalogue coming soon.</p>
                                )
                              ) : null}
                            </div>
                          );
                        })}
                      </div>
                    ) : null}
                  </div>
                );
              }

              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  title={isSidebarCollapsed ? item.label : undefined}
                  className={({ isActive }) =>
                    `flex items-center ${isSidebarCollapsed ? "justify-center rounded-[18px] px-0 py-2.5" : "gap-3 rounded-full px-4 py-2"} text-[12px] font-medium transition ${isActive ? "bg-[#111111] text-white" : "text-slate-600 hover:bg-white/66 hover:text-slate-900"}`
                  }
                  style={{ fontSize: "12px", lineHeight: "1.2" }}
                >
                  {({ isActive }) => (
                    <span className={`flex items-center ${isSidebarCollapsed ? "justify-center" : "gap-3"}`}>
                      <span className={`flex h-8 w-8 items-center justify-center rounded-full ${isActive ? "bg-white/12 text-white" : "bg-transparent text-slate-500"}`}>
                        <Icon size={16} />
                      </span>
                      {!isSidebarCollapsed ? <span className={isActive ? "text-white" : "text-slate-600"}>{item.label}</span> : null}
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>

          <div className={`mt-8 rounded-[32px] bg-white/78 p-2 transition-all duration-300 ease-out ${isSidebarCollapsed ? "mx-auto w-fit" : ""}`}>
            <div className={`flex items-center ${isSidebarCollapsed ? "justify-center" : "gap-3"}`}>
              <button type="button" onClick={logout} className="app-button app-button-dark app-icon-button shrink-0" aria-label="Log out">
                <LogOut size={15} />
              </button>
              {!isSidebarCollapsed ? (
                <div className="min-w-0 flex-1 overflow-hidden transition-[max-width,opacity] duration-300 ease-out">
                  <p className="truncate text-sm font-semibold text-slate-900">{user?.full_name || "Workspace user"}</p>
                  <p className="truncate text-xs text-slate-500">{user?.email || "Session active"}</p>
                </div>
              ) : null}
            </div>
          </div>
        </aside>

        <main className="flex min-h-screen min-w-0 flex-col overflow-x-hidden transition-[margin-left] duration-300 ease-out xl:ml-[var(--sidebar-width)]">
          <header className="app-glass top-0 z-20 flex flex-col gap-4 border-b border-slate-200/70 px-6 py-5 transition-[left] duration-300 ease-out lg:px-8 xl:fixed xl:left-[var(--sidebar-width)] xl:right-0 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <h2 className="text-[1.55rem] font-semibold tracking-[-0.05em] text-slate-950">Cyber GRC Workspace</h2>
            </div>

            <div className="flex items-center gap-3 self-start xl:self-auto">
              <div className="relative">
                <button
                  type="button"
                  style={{ backgroundColor: isNotificationsOpen ? "rgba(255, 255, 255, 0.96)" : "rgba(248, 244, 239, 0.82)", width: "3rem", height: "3rem", padding: 0 }}
                  onClick={() => setIsNotificationsOpen((current) => !current)}
                  className={`app-button app-icon-button text-slate-700 ${isNotificationsOpen ? "shadow-[0_14px_34px_rgba(15,23,42,0.08)]" : "app-button-soft"}`}
                  aria-label="Alerts"
                >
                  <FiBell size={20} />
                </button>

                {isNotificationsOpen ? (
                  <div className="app-glass absolute right-0 z-20 mt-3 w-[380px] rounded-[18px] bg-white/94 p-4 shadow-[0_18px_48px_rgba(15,23,42,0.12)]">
                    <div className="mb-3 flex items-start justify-between gap-3">
                      <div>
                        <h3 className="text-sm font-semibold text-slate-900">Recent coordination alerts</h3>
                        <p className="mt-1 text-xs text-slate-500">Realtime updates from workflows, reviews, and delivery milestones.</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => setIsNotificationsOpen(false)}
                        className="app-button text-slate-500 hover:text-slate-700"
                        style={{ width: "2.1rem", height: "2.1rem", padding: 0, backgroundColor: "rgba(255, 255, 255, 0.88)" }}
                        aria-label="Close notifications"
                      >
                        <FiX size={13} />
                      </button>
                    </div>

                    <div className="app-scroll max-h-[360px] space-y-2 overflow-y-auto pr-1">
                      {visibleNotifications.length ? (
                        visibleNotifications.map((item) => (
                          <article key={item.id} className="rounded-[16px] bg-white/90 px-4 py-3 shadow-[0_10px_24px_rgba(15,23,42,0.04)]">
                            <p className="text-sm font-medium text-slate-800">{item.message}</p>
                            <p className="mt-1 text-xs text-slate-500">{formatNotificationDate(item.receivedAt)}</p>
                          </article>
                        ))
                      ) : (
                        <div className="rounded-[16px] bg-white/88 px-4 py-7 text-center text-[13px] font-medium leading-5 text-[#2c2824]/68">No realtime alerts yet. Workflow and deadline notifications will appear here.</div>
                      )}
                    </div>
                  </div>
                ) : null}
              </div>

              <button
                type="button"
                style={{ backgroundColor: "rgba(248, 244, 239, 0.82)", width: "3rem", height: "3rem", padding: 0 }}
                className="app-button app-button-soft app-icon-button relative text-slate-600"
                aria-label="Settings"
              >
                <Settings size={20} strokeWidth={1.9} />
                <span className="absolute right-3.5 top-3.5 h-1.5 w-1.5 rounded-full bg-[#fc8158]" aria-hidden="true" />
              </button>

              <button type="button" onClick={handleQuickAdd} disabled={!quickAddTarget} className="app-button app-button-dark min-w-[128px]  disabled:cursor-not-allowed disabled:opacity-50">
                Quick add
              </button>
            </div>
          </header>

          <div className="flex-1 min-w-0 px-6 py-6 lg:px-8 xl:pt-[108px]">
            <Outlet key={`${location.pathname}${location.search}`} />
          </div>
        </main>
      </div>
    </div>
  );
}


