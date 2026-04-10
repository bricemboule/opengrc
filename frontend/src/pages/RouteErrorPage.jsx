import { useRouteError } from "react-router-dom";

export default function RouteErrorPage() {
  const error = useRouteError();
  const message =
    error?.statusText ||
    error?.message ||
    "Une erreur inattendue est survenue.";

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#f8fafc] px-6">
      <div className="w-full max-w-xl rounded-3xl border border-slate-200 bg-white p-8 shadow-[0_20px_60px_rgba(2,6,23,0.08)]">
        <h1 className="text-2xl font-bold text-slate-900">Erreur d'application</h1>
        <p className="mt-3 text-sm text-slate-600">{message}</p>
      </div>
    </div>
  );
}
