<template>
  <div class="item-card card">
    <div class="item-main">
      <span class="item-name">{{ item.name }}</span>
      <span v-if="item.notes" class="item-notes">{{ item.notes }}</span>
    </div>

    <div class="item-qty">
      <button class="btn-icon qty-btn" @click="$emit('adjust', -1)" :disabled="item.quantity <= 0">−</button>
      <span class="qty-val">{{ displayQty }}</span>
      <button class="btn-icon qty-btn" @click="$emit('adjust', 1)">+</button>
    </div>

    <div class="item-actions">
      <button class="btn-icon" @click="$emit('edit', item)" title="Modifier">✏️</button>
      <button class="btn-icon" @click="$emit('delete', item)" title="Supprimer">🗑</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({ item: Object });
defineEmits(["adjust", "edit", "delete"]);

const displayQty = computed(() => {
  const q = props.item.quantity;
  const u = props.item.unit;
  const formatted = Number.isInteger(q) ? q : q.toFixed(1);
  return u ? `${formatted} ${u}` : String(formatted);
});
</script>

<style scoped>
.item-card { display: flex; align-items: center; gap: 0.75rem; }
.item-main { flex: 1; min-width: 0; }
.item-name { font-weight: 600; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.item-notes { font-size: 0.8rem; color: var(--muted); display: block; }
.item-qty   { display: flex; align-items: center; gap: 0.25rem; }
.qty-btn    { font-size: 1.3rem; width: 2rem; height: 2rem; background: var(--surface2); border-radius: 50%; }
.qty-btn:disabled { opacity: 0.3; }
.qty-val    { min-width: 3.5rem; text-align: center; font-weight: 600; font-size: 0.95rem; }
.item-actions { display: flex; gap: 0.25rem; }
</style>
