<template>
  <RouterLink :to="`/freezer/${freezer.id}`" class="freezer-card card">
    <div class="fc-left">
      <span class="fc-icon">{{ freezer.icon }}</span>
      <div>
        <div class="fc-name">{{ freezer.name }}</div>
        <div class="fc-meta">{{ compartmentCount }} compartiment(s)</div>
      </div>
    </div>
    <div class="fc-right">
      <span class="fc-total">{{ itemCount }} article(s)</span>
      <button
        class="btn-icon"
        @click.prevent="$emit('delete', freezer)"
        title="Supprimer"
      >🗑</button>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({ freezer: Object });
defineEmits(["delete"]);

const compartmentCount = computed(() => props.freezer.compartments?.length ?? 0);
const itemCount = computed(() =>
  props.freezer.compartments?.reduce((s, c) => s + (c.items?.length ?? 0), 0) ?? 0
);
</script>

<style scoped>
.freezer-card {
  display: flex; align-items: center; justify-content: space-between;
  text-decoration: none; color: inherit; cursor: pointer;
  transition: background .15s;
}
.freezer-card:hover { background: var(--surface2); }
.fc-left  { display: flex; align-items: center; gap: 0.75rem; }
.fc-icon  { font-size: 2rem; }
.fc-name  { font-weight: 600; }
.fc-meta  { font-size: 0.8rem; color: var(--muted); }
.fc-right { display: flex; align-items: center; gap: 0.5rem; }
.fc-total { font-size: 0.8rem; color: var(--muted); }
</style>
