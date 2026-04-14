import { createSlice } from "@reduxjs/toolkit";

const MAX_ITEMS = 12;

function normalizeNotification(payload) {
  const message = String(payload?.message || "").trim();
  if (!message) return null;

  return {
    id: payload?.id || `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    title: String(payload?.title || "").trim(),
    source: String(payload?.source || "").trim(),
    message,
    receivedAt: payload?.receivedAt || payload?.created_at || new Date().toISOString(),
  };
}

const notificationsSlice = createSlice({
  name: "notifications",
  initialState: { items: [] },
  reducers: {
    notificationsLoaded(state, action) {
      const items = Array.isArray(action.payload)
        ? action.payload.map(normalizeNotification).filter(Boolean)
        : [];
      state.items = items.slice(0, MAX_ITEMS);
    },
    notificationReceived(state, action) {
      const item = normalizeNotification(action.payload);
      if (!item) return;

      state.items = [item, ...state.items.filter((existing) => String(existing.id) !== String(item.id))].slice(0, MAX_ITEMS);
    },
    clearNotifications(state) {
      state.items = [];
    },
  },
});

export const { notificationsLoaded, notificationReceived, clearNotifications } = notificationsSlice.actions;
export default notificationsSlice.reducer;
