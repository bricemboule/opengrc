import { useEffect } from "react";
import { useDispatch } from "react-redux";

import api from "../api/client";
import { notificationReceived, notificationsLoaded } from "../features/notifications/notificationsSlice";
import { notifySuccess } from "../utils/toast";

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
    api
      .get("/communications/notifications/", { params: { page_size: 12 } })
      .then((response) => {
        if (!isMounted) return;
        const rows = response.data?.results || response.data || [];
        dispatch(notificationsLoaded(rows));
      })
      .catch(() => {
        if (!isMounted) return;
        dispatch(notificationsLoaded([]));
      });

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

    return () => {
      isMounted = false;
      socket.close();
    };
  }, [dispatch]);
}
