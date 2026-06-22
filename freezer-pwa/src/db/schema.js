import Dexie from "dexie";

export const db = new Dexie("FreezerDB");

db.version(1).stores({
  freezers: "id, name, updated_at",
  compartments: "id, freezer_id, name, position, updated_at",
  items: "id, compartment_id, name, quantity, updated_at",
  sync_queue: "++localId, entity, type, client_updated_at",
});
