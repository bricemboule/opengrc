import { useEffect } from "react";
import { notifySuccess } from "../utils/toast";

export default function useNotificationsSocket() {
  useEffect(() => {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/notifications/`);
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) notifySuccess(data.message);
    };
    return () => socket.close();
  }, []);
}
