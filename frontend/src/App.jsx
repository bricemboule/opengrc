import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import useBootstrapAuth from "./features/auth/useBootstrapAuth";
import LoginPage from "./features/auth/LoginPage";
import ProtectedRoute from "./routes/ProtectedRoute";
import PermissionRoute from "./routes/PermissionRoute";
import AdminLayout from "./layouts/AdminLayout";
import DashboardPage from "./pages/DashboardPage";
import ModuleListPage from "./pages/ModuleListPage";
import RouteErrorPage from "./pages/RouteErrorPage";
import { moduleConfigs } from "./config/modules";

const router = createBrowserRouter([
  { path: "/login", element: <LoginPage />, errorElement: <RouteErrorPage /> },
  {
    path: "/",
    element: <ProtectedRoute><AdminLayout /></ProtectedRoute>,
    errorElement: <RouteErrorPage />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "dashboard", element: <DashboardPage /> },
      ...moduleConfigs.map((item) => {
        const modulePage = <ModuleListPage key={item.route} moduleKey={item.route} />;
        return {
          path: `modules/${item.route}`,
          element: item.permission ? <PermissionRoute permission={item.permission}>{modulePage}</PermissionRoute> : modulePage,
        };
      }),
    ],
  },
]);

function AppRouter() {
  useBootstrapAuth();
  return <RouterProvider router={router} />;
}

export default AppRouter;
