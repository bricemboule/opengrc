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

function AppRouter() {
  useBootstrapAuth();
  const router = createBrowserRouter([
    { path: "/login", element: <LoginPage />, errorElement: <RouteErrorPage /> },
    {
      path: "/",
      element: <ProtectedRoute><AdminLayout /></ProtectedRoute>,
      errorElement: <RouteErrorPage />,
      children: [
        { index: true, element: <Navigate to="/dashboard" replace /> },
        { path: "dashboard", element: <DashboardPage /> },
        ...moduleConfigs.map((item) => ({
          path: `modules/${item.route}`,
          element: item.permission ? <PermissionRoute permission={item.permission}><ModuleListPage moduleKey={item.route} /></PermissionRoute> : <ModuleListPage moduleKey={item.route} />,
        })),
      ],
    },
  ]);
  return <RouterProvider router={router} />;
}

export default AppRouter;
