import { useQuery } from "@tanstack/react-query";
import api from "../api/client";

export default function usePaginatedList(queryKey, endpoint, params = {}) {
  return useQuery({
    queryKey: [queryKey, params],
    queryFn: async () => {
      const { data } = await api.get(endpoint, { params });
      return data;
    },
  });
}
