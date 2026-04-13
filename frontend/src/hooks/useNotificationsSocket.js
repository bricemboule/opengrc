import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { notificationReceived } from "../features/notifications/notificationsSlice";
import { notifySuccess } from "../utils/toast";

export default function useNotificationsSocket() {
  const dispatch = useDispatch();

  useEffect(() => {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/notifications/`);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (!data.message) return;

      dispatch(
        notificationReceived({
          message: data.message,
          receivedAt: new Date().toISOString(),
        }),
      );
      notifySuccess(data.message);
    };

    return () => socket.close();
  }, [dispatch]);
}
