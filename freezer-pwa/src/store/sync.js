import { defineStore } from "pinia";
import { ref } from "vue";
import { flushQueue, pendingCount } from "../db/sync-queue.js";

export const useSyncStore = defineStore("sync", () => {
  const online = ref(navigator.onLine);
  const syncing = ref(false);
  const pending = ref(0);

  async function refreshPending() {
    pending.value = await pendingCount();
  }

  async function sync() {
    if (!online.value || syncing.value) return;
    syncing.value = true;
    try {
      await flushQueue();
      await refreshPending();
    } finally {
      syncing.value = false;
    }
  }

  window.addEventListener("online", () => {
    online.value = true;
    sync();
  });
  window.addEventListener("offline", () => {
    online.value = false;
  });

  refreshPending();

  return { online, syncing, pending, sync, refreshPending };
});
