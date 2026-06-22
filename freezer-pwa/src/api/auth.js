import client from "./client.js";

export const login = (pin) => client.post("/auth/login", { pin });
