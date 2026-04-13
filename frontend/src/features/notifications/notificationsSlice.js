import { createSlice } from "@reduxjs/toolkit";

const MAX_ITEMS = 12;

const notificationsSlice = createSlice({
  name: "notifications",
  initialState: { items: [] },
  reducers: {
    notificationReceived(state, action) {
      const message = String(action.payload?.message || "").trim();
      if (!message) return;

      state.items = [
        {
          id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
          message,
          receivedAt: action.payload?.receivedAt || new Date().toISOString(),
        },
        ...state.items,
      ].slice(0, MAX_ITEMS);
    },
    clearNotifications(state) {
      state.items = [];
    },
  },
});

export const { notificationReceived, clearNotifications } = notificationsSlice.actions;


export default notificationsSlice.reducer;
