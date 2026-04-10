import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../api/client";
import { notifySuccess, notifyError } from "../utils/toast";

function extractErrorMessage(error, fallback) {
  const data = error?.response?.data;
  if (typeof data?.detail === "string") return data.detail;
  if (typeof data?.message === "string") return data.message;
  return fallback;
}

export function useCreateItem(queryKey, endpoint, successMessage = "Créé avec succès") {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload) => (await api.post(endpoint, payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [queryKey] });
      notifySuccess(successMessage);
    },
    onError: (error) => notifyError(extractErrorMessage(error, "Échec de la création")),
  });
}

export function useUpdateItem(queryKey, endpoint, successMessage = "Mis à jour avec succès") {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }) => (await api.patch(`${endpoint}${id}/`, payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [queryKey] });
      notifySuccess(successMessage);
    },
    onError: (error) => notifyError(extractErrorMessage(error, "Échec de la mise à jour")),
  });
}

export function useDeleteItem(queryKey, endpoint, successMessage = "Supprimé avec succès") {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id) => await api.delete(`${endpoint}${id}/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [queryKey] });
      notifySuccess(successMessage);
    },
    onError: (error) => notifyError(extractErrorMessage(error, "Échec de la suppression")),
  });
}
