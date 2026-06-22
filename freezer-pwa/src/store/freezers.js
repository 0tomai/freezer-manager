import { defineStore } from "pinia";
import { ref } from "vue";
import {
  getFreezersFull,
  createFreezer as apiCreate,
  updateFreezer as apiUpdate,
  deleteFreezer as apiDelete,
} from "../api/freezers.js";
import {
  createCompartment as apiCreateComp,
  updateCompartment as apiUpdateComp,
  deleteCompartment as apiDeleteComp,
} from "../api/compartments.js";
import { localFreezerStore, localCompartmentStore } from "../db/offline-store.js";
import { enqueue } from "../db/sync-queue.js";
import { useSyncStore } from "./sync.js";

export const useFreezerStore = defineStore("freezers", () => {
  const freezers = ref([]);
  const loading = ref(false);
  const error = ref(null);

  async function loadFreezer() {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await getFreezersFull();
      freezers.value = data;
      await localFreezerStore.saveMany(data);
    } catch {
      freezers.value = await localFreezerStore.getAll();
    } finally {
      loading.value = false;
    }
  }

  async function addFreezer(payload) {
    const { data } = await apiCreate(payload);
    await localFreezerStore.save(data);
    freezers.value.push({ ...data, compartments: [] });
    return data;
  }

  async function editFreezer(id, payload) {
    const { data } = await apiUpdate(id, payload);
    await localFreezerStore.save(data);
    const idx = freezers.value.findIndex((f) => f.id === id);
    if (idx !== -1) Object.assign(freezers.value[idx], data);
  }

  async function removeFreezer(id) {
    await apiDelete(id);
    await localFreezerStore.delete(id);
    freezers.value = freezers.value.filter((f) => f.id !== id);
  }

  async function addCompartment(freezer_id, payload) {
    const syncStore = useSyncStore();
    const fullPayload = { ...payload, freezer_id };
    try {
      const { data } = await apiCreateComp(fullPayload);
      await localCompartmentStore.save(data);
      _insertCompartment(freezer_id, { ...data, items: [] });
      return data;
    } catch {
      const temp = { id: `tmp_${Date.now()}`, ...fullPayload, items: [], position: 0 };
      _insertCompartment(freezer_id, temp);
      await enqueue("compartment", "upsert", fullPayload);
      syncStore.refreshPending();
    }
  }

  async function editCompartment(id, payload) {
    const syncStore = useSyncStore();
    try {
      const { data } = await apiUpdateComp(id, payload);
      await localCompartmentStore.save(data);
      _patchCompartment(id, data);
    } catch {
      _patchCompartment(id, payload);
      await enqueue("compartment", "upsert", { id, ...payload });
      syncStore.refreshPending();
    }
  }

  async function removeCompartment(freezer_id, comp_id) {
    const syncStore = useSyncStore();
    try {
      await apiDeleteComp(comp_id);
    } catch {
      await enqueue("compartment", "delete", { id: comp_id });
      syncStore.refreshPending();
    }
    await localCompartmentStore.delete(comp_id);
    _removeCompartment(freezer_id, comp_id);
  }

  function _insertCompartment(freezer_id, comp) {
    const f = freezers.value.find((f) => f.id === freezer_id);
    if (f) f.compartments.push(comp);
  }

  function _patchCompartment(comp_id, patch) {
    for (const f of freezers.value) {
      const c = f.compartments?.find((c) => c.id === comp_id);
      if (c) { Object.assign(c, patch); return; }
    }
  }

  function _removeCompartment(freezer_id, comp_id) {
    const f = freezers.value.find((f) => f.id === freezer_id);
    if (f) f.compartments = f.compartments.filter((c) => c.id !== comp_id);
  }

  return {
    freezers, loading, error,
    loadFreezer, addFreezer, editFreezer, removeFreezer,
    addCompartment, editCompartment, removeCompartment,
  };
});
