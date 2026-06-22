import { defineStore } from "pinia";
import {
  createItem as apiCreate,
  updateItem as apiUpdate,
  adjustQuantity as apiAdjust,
  deleteItem as apiDelete,
} from "../api/items.js";
import { localItemStore } from "../db/offline-store.js";
import { enqueue } from "../db/sync-queue.js";
import { useSyncStore } from "./sync.js";
import { useFreezerStore } from "./freezers.js";

export const useItemStore = defineStore("items", () => {
  function _findComp(comp_id) {
    const store = useFreezerStore();
    for (const f of store.freezers) {
      const c = f.compartments?.find((c) => c.id === comp_id);
      if (c) return c;
    }
    return null;
  }

  async function addItem(payload) {
    const syncStore = useSyncStore();
    try {
      const { data } = await apiCreate(payload);
      await localItemStore.save(data);
      _findComp(payload.compartment_id)?.items.push(data);
      return data;
    } catch {
      const temp = { id: `tmp_${Date.now()}`, ...payload, added_at: new Date().toISOString() };
      _findComp(payload.compartment_id)?.items.push(temp);
      await enqueue("item", "upsert", payload);
      syncStore.refreshPending();
    }
  }

  async function editItem(id, compartment_id, payload) {
    const syncStore = useSyncStore();
    try {
      const { data } = await apiUpdate(id, payload);
      await localItemStore.save(data);
      _patchItem(compartment_id, id, data);
    } catch {
      _patchItem(compartment_id, id, payload);
      await enqueue("item", "upsert", { id, ...payload });
      syncStore.refreshPending();
    }
  }

  async function adjustQty(id, compartment_id, delta) {
    const syncStore = useSyncStore();
    const comp = _findComp(compartment_id);
    const item = comp?.items.find((i) => i.id === id);
    if (!item) return;

    const newQty = Math.max(0, item.quantity + delta);
    item.quantity = newQty;

    try {
      const { data } = await apiAdjust(id, delta);
      await localItemStore.save(data);
    } catch {
      await enqueue("item", "upsert", { id, compartment_id, quantity: newQty });
      syncStore.refreshPending();
    }
  }

  async function removeItem(id, compartment_id) {
    const syncStore = useSyncStore();
    try {
      await apiDelete(id);
    } catch {
      await enqueue("item", "delete", { id });
      syncStore.refreshPending();
    }
    await localItemStore.delete(id);
    const comp = _findComp(compartment_id);
    if (comp) comp.items = comp.items.filter((i) => i.id !== id);
  }

  function _patchItem(compartment_id, item_id, patch) {
    const comp = _findComp(compartment_id);
    const item = comp?.items.find((i) => i.id === item_id);
    if (item) Object.assign(item, patch);
  }

  return { addItem, editItem, adjustQty, removeItem };
});
