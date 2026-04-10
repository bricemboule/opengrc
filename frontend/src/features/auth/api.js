import api from "../../api/client";

export async function loginRequest(payload) {
  const { data } = await api.post("/auth/login/", payload);
  return data;
}

export async function meRequest() {
  const { data } = await api.get("/auth/me/");
  return data;
}
