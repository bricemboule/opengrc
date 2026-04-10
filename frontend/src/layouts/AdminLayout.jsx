import { useEffect, useMemo, useState } from "react";
import { LogOut } from "lucide-react";
import { FiBarChart2, FiChevronDown, FiChevronRight, FiFileText, FiFolderPlus, FiList, FiMap, FiSearch, FiUpload } from "react-icons/fi";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { clearAuth } from "../features/auth/authSlice";
import { moduleConfigs } from "../config/modules";
import { buildMenu } from "./menu";
import useNotificationsSocket from "../hooks/useNotificationsSocket";

function buildOpenState(menuItems, location) {
  return menuItems.reduce((accumulator, item) => {
    if (item.type === "dropdown") {
      accumulator[item.key] = item.sections.some((section) =>
        section.items.some((child) => location.pathname + location.search === child.to || location.pathname === child.to),
      );
    }
    return accumulator;
  }, {});
}

export default function AdminLayout() {
  useNotificationsSocket();
  const user = useSelector((state) => state.auth.user);
  const permissions = user?.permissions || [];
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const menuItems = useMemo(() => buildMenu(moduleConfigs), []);
  const activeDropdowns = useMemo(
    () =>
      menuItems.reduce((accumulator, item) => {
        if (item.type === "dropdown") {
          accumulator[item.key] = item.sections.some((section) =>
            section.items.some((child) => location.pathname + location.search === child.to || location.pathname === child.to),
          );
        }
        return accumulator;
      }, {}),
    [location, menuItems],
  );
  const [openDropdowns, setOpenDropdowns] = useState(() => buildOpenState(menuItems, location));

  useEffect(() => {
    setOpenDropdowns((current) =>
      Object.entries(activeDropdowns).reduce((accumulator, [key, isActive]) => {
        accumulator[key] = isActive ? true : current[key] ?? false;
        return accumulator;
      }, { ...current }),
    );
  }, [activeDropdowns]);

  const filteredMenu = menuItems.filter((item) => {
    if (item.type === "dropdown") {
      return item.sections.some((section) => !section.permission || permissions.includes(section.permission));
    }
    return !item.permission || permissions.includes(item.permission);
  });

  function logout() {
    dispatch(clearAuth());
    navigate("/login");
  }

  function renderActionIcon(label) {
    if (label === "Create") return <FiFolderPlus size={14} />;
    if (label.includes("Import")) return <FiUpload size={14} />;
    if (label === "Map") return <FiMap size={14} />;
    if (label.includes("Search")) return <FiSearch size={14} />;
    if (label.includes("Report")) return <FiBarChart2 size={14} />;
    if (label.includes("List")) return <FiList size={14} />;
    return <FiFileText size={14} />;
  }

  function toggleDropdown(key) {
    setOpenDropdowns((current) => ({ ...current, [key]: !current[key] }));
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[280px_1fr]">
        <aside className="border-r border-slate-200 bg-white">
          <div className="p-6">
            <div className="overflow-hidden rounded-2xl shadow-sm">
              <div className="h-8 bg-[#CE1126]" />
              <div className="h-[6px] bg-white" />
              <div className="h-6 bg-[#0C1C8C]" />
              <div className="h-[6px] bg-white" />
              <div className="h-8 bg-[#3A7728]" />
            </div>
            <div className="mt-5">
              <h1 className="text-xl font-bold text-slate-900">Relief Admin</h1>
              <p className="text-sm text-slate-500">Plateforme multi-modules</p>
            </div>
          </div>

          <nav className="space-y-2 px-4 pb-6">
            {filteredMenu.map((item) => {
              if (item.type === "dropdown") {
                const Icon = item.icon;
                const visibleSections = item.sections.filter((section) => !section.permission || permissions.includes(section.permission));
                const isOpen = openDropdowns[item.key];
                const isActive = activeDropdowns[item.key];

                return (
                  <div key={item.key} className="rounded-2xl border border-slate-200/70 bg-slate-50/60">
                    <button
                      type="button"
                      onClick={() => toggleDropdown(item.key)}
                      className={`flex w-full items-center justify-between rounded-2xl px-4 py-3 text-sm font-medium transition ${
                        isOpen || isActive ? "bg-[#0C1C8C]/10 text-[#0C1C8C]" : "text-slate-700 hover:bg-slate-100"
                      }`}
                    >
                      <span className="flex items-center gap-3">
                        <Icon size={18} />
                        {item.label}
                      </span>
                      {isOpen ? <FiChevronDown size={16} /> : <FiChevronRight size={16} />}
                    </button>

                    {isOpen ? (
                      <div className="space-y-4 px-3 pb-4">
                        {visibleSections.map((section) => (
                          <div key={section.title} className="rounded-2xl bg-white p-3 shadow-sm">
                            <h3 className="mb-2 text-xs font-bold uppercase tracking-[0.08em] text-slate-600">{section.title}</h3>
                            {section.items.length ? (
                              <div className="space-y-1">
                                {section.items.map((child) => (
                                  <NavLink
                                    key={child.to}
                                    to={child.to}
                                    className={({ isActive: isChildActive }) =>
                                      `flex items-center gap-2 rounded-xl px-3 py-2 text-sm transition ${
                                        isChildActive || location.pathname + location.search === child.to
                                          ? "bg-[#3A7728]/10 text-[#2f651f]"
                                          : "text-slate-600 hover:bg-slate-100"
                                      }`
                                    }
                                  >
                                    {renderActionIcon(child.label)}
                                    {child.label}
                                  </NavLink>
                                ))}
                              </div>
                            ) : (
                              <p className="text-sm text-slate-400">Catalogue combiné à venir.</p>
                            )}
                          </div>
                        ))}
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
                  className={({ isActive }) =>
                    `flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition ${
                      isActive ? "bg-[#0C1C8C]/10 text-[#0C1C8C]" : "text-slate-600 hover:bg-slate-100"
                    }`
                  }
                >
                  <Icon size={18} />
                  {item.label}
                </NavLink>
              );
            })}
          </nav>
        </aside>

        <main>
          <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">Back Office</h2>
              <p className="text-sm text-slate-500">Bienvenue {user?.full_name || user?.email}</p>
            </div>
            <button
              onClick={logout}
              className="inline-flex items-center gap-2 rounded-2xl bg-[#3A7728] px-4 py-2 text-sm font-medium text-white transition hover:bg-[#2f621f]"
            >
              <LogOut size={16} />
              Déconnexion
            </button>
          </header>
          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
