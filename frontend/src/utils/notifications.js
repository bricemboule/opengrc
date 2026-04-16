import api from "../api/client";
import { notificationsLoaded } from "../features/notifications/notificationsSlice";

export async function fetchLatestNotifications(dispatch, pageSize = 12) {
  try {
    const response = await api.get("/communications/notifications/", { params: { page_size: pageSize } });
    const rows = response.data?.results || response.data || [];
    dispatch(notificationsLoaded(rows));
    return rows;
  } catch {
    dispatch(notificationsLoaded([]));
    return [];
  }
}
