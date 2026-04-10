import { useQuery } from "@tanstack/react-query";
import api from "../api/client";

export default function useCrudList(queryKey, endpoint) {
  return useQuery({
    queryKey: [queryKey],
    queryFn: async () => {
      const { data } = await api.get(endpoint);
      return data;
    },
  });
}
