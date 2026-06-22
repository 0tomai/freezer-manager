import client from "./client.js";

export const getFreezersFull = () => client.get("/freezers/");
export const createFreezer = (data) => client.post("/freezers/", data);
export const updateFreezer = (id, data) => client.put(`/freezers/${id}`, data);
export const deleteFreezer = (id) => client.delete(`/freezers/${id}`);
