import client from "./client.js";

export const createCompartment = (data) => client.post("/compartments/", data);
export const updateCompartment = (id, data) => client.put(`/compartments/${id}`, data);
export const deleteCompartment = (id) => client.delete(`/compartments/${id}`);
