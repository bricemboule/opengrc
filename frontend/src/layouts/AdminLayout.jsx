import { LogOut } from "lucide-react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { clearAuth } from "../features/auth/authSlice";
import { menuItems } from "./menu";
import useNotificationsSocket from "../hooks/useNotificationsSocket";

export default function AdminLayout() {
  useNotificationsSocket();
  const user = useSelector((state) => state.auth.user);
  const permissions = user?.permissions || [];
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const filteredMenu = menuItems.filter((item) => !item.permission || permissions.includes(item.permission));

  function logout() {
    dispatch(clearAuth());
    navigate("/login");
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
