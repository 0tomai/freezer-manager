import client from "./client.js";

export const createItem = (data) => client.post("/items/", data);
export const updateItem = (id, data) => client.put(`/items/${id}`, data);
export const adjustQuantity = (id, delta) =>
  client.patch(`/items/${id}/quantity`, { delta });
export const deleteItem = (id) => client.delete(`/items/${id}`);
export const syncOffline = (operations) =>
  client.post("/items/sync", { operations });
