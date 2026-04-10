import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

export default function PermissionRoute({ permission, children }) {
  const user = useSelector((state) => state.auth.user);
  const permissions = user?.permissions || [];
  if (permission && !permissions.includes(permission)) {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
}
