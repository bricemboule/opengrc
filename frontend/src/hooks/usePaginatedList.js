import { useQuery } from "@tanstack/react-query";
import api from "../api/client";

export default function usePaginatedList(queryKey, endpoint, params = {}) {
  return useQuery({
    queryKey: [queryKey, params],
    enabled: Boolean(endpoint) && endpoint !== "/",
    staleTime: 30000,
    refetchOnWindowFocus: false,
    placeholderData: (previousData) => previousData,
    queryFn: async () => {
      const cleanedParams = Object.fromEntries(Object.entries(params).filter(([, value]) => value !== undefined && value !== null && value !== ""));
      const { data } = await api.get(endpoint, { params: cleanedParams });
      return data;
    },
  });
}
