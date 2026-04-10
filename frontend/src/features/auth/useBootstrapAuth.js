import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { meRequest } from "./api";
import { setAuth, clearAuth } from "./authSlice";

export default function useBootstrapAuth() {
  const dispatch = useDispatch();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;
    meRequest()
      .then((user) => dispatch(setAuth(user)))
      .catch(() => dispatch(clearAuth()));
  }, [dispatch]);
}
