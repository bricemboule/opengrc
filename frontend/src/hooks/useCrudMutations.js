import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../api/client";
import { notifySuccess, notifyError } from "../utils/toast";

function extractErrorMessage(error, fallback) {
  const data = error?.response?.data;
  if (typeof data?.detail === "string") return data.detail;
  if (typeof data?.message === "string") return data.message;
  if (data && typeof data === "object") {
    const firstFieldEntry = Object.entries(data).find(([, value]) => Array.isArray(value) || typeof value === "string");
    if (firstFieldEntry) {
      const [field, value] = firstFieldEntry;
      const message = Array.isArray(value) ? value.join(" ") : value;
      return field === "non_field_errors" ? message : `${field}: ${message}`;
    }
  }
  return fallback;
}

export function useCreateItem(queryKey, endpoint, successMessage = "Created successfully") {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload) => (await api.post(endpoint, payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [queryKey] });
      notifySuccess(successMessage);
    },
    onError: (error) => notifyError(extractErrorMessage(error, "Creation failed")),
  });
}

export function useUpdateItem(queryKey, endpoint, successMessage = "Updated successfully") {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }) => (await api.patch(`${endpoint}${id}/`, payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [queryKey] });
      notifySuccess(successMessage);
    },
    onError: (error) => notifyError(extractErrorMessage(error, "Update failed")),
  });
}

export function useDeleteItem(queryKey, endpoint, successMessage = "Deleted successfully") {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id) => await api.delete(`${endpoint}${id}/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [queryKey] });
      notifySuccess(successMessage);
    },
    onError: (error) => notifyError(extractErrorMessage(error, "Deletion failed")),
  });
}
