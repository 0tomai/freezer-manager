<template>
  <span :class="['badge', badgeClass]" @click="syncStore.sync()">
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from "vue";
import { useSyncStore } from "../store/sync.js";

const syncStore = useSyncStore();

const badgeClass = computed(() => {
  if (syncStore.syncing) return "badge-syncing";
  if (!syncStore.online) return "badge-offline";
  return "badge-online";
});

const label = computed(() => {
  if (syncStore.syncing) return "⟳ sync…";
  if (!syncStore.online) return `✗ hors ligne${syncStore.pending > 0 ? ` (${syncStore.pending})` : ""}`;
  return "✓ en ligne";
});
</script>
