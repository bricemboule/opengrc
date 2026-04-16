import { useEffect } from "react";
import { useDispatch } from "react-redux";

import { notificationReceived, notificationsLoaded } from "../features/notifications/notificationsSlice";
import { notifySuccess } from "../utils/toast";
import { fetchLatestNotifications } from "../utils/notifications";

function buildNotificationsSocketUrl() {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  const apiBaseUrl = import.meta.env.VITE_API_URL || "/api";
  const encodedToken = encodeURIComponent(token);

  if (apiBaseUrl.startsWith("http://") || apiBaseUrl.startsWith("https://")) {
    const url = new URL(apiBaseUrl);
    url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
    url.pathname = "/ws/notifications/";
    url.search = `token=${encodedToken}`;
    return url.toString();
  }

  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  return `${protocol}://${window.location.host}/ws/notifications/?token=${encodedToken}`;
}

function normalizeNotificationPayload(payload) {
  if (!payload || typeof payload !== "object") return null;
  const message = String(payload.message || "").trim();
  if (!message) return null;

  return {
    id: payload.id,
    title: payload.title || "",
    message,
    receivedAt: payload.receivedAt || payload.created_at || new Date().toISOString(),
    source: payload.source || "",
  };
}

export default function useNotificationsSocket() {
  const dispatch = useDispatch();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      dispatch(notificationsLoaded([]));
      return undefined;
    }

    let isMounted = true;
    fetchLatestNotifications(dispatch);

    const socketUrl = buildNotificationsSocketUrl();
    if (!socketUrl) {
      return () => {
        isMounted = false;
      };
    }

    const socket = new WebSocket(socketUrl);

    socket.onmessage = (event) => {
      const payload = normalizeNotificationPayload(JSON.parse(event.data));
      if (!payload) return;
      dispatch(notificationReceived(payload));
      notifySuccess(payload.message);
    };

    const intervalId = window.setInterval(() => {
      if (!isMounted) return;
      fetchLatestNotifications(dispatch);
    }, 30000);

    return () => {
      isMounted = false;
      window.clearInterval(intervalId);
      socket.close();
    };
  }, [dispatch]);
}
