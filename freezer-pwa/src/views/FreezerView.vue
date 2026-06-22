<template>
  <div>
    <header class="topbar">
      <button class="btn-icon" @click="router.back()">←</button>
      <span class="topbar-title">{{ freezer?.icon }} {{ freezer?.name }}</span>
      <SyncBadge />
    </header>

    <main class="page">
      <div v-if="!freezer" class="empty">Congélateur introuvable.</div>

      <template v-else>
        <div
          v-for="c in freezer.compartments"
          :key="c.id"
          class="comp-row card"
          @click="router.push(`/compartment/${c.id}`)"
        >
          <div class="comp-info">
            <span class="comp-name">{{ c.name }}</span>
            <span class="comp-count">{{ c.items?.length ?? 0 }} article(s)</span>
          </div>
          <span class="comp-arrow">›</span>
          <button
            class="btn-icon comp-delete"
            @click.stop="confirmDelete(c)"
            title="Supprimer"
          >🗑</button>
        </div>

        <div v-if="freezer.compartments.length === 0" class="empty">
          <div class="empty-icon">📦</div>
          <p>Aucun compartiment.</p>
        </div>

        <button class="btn-primary add-btn" @click="showAdd = true">
          + Ajouter un compartiment
        </button>
      </template>
    </main>

    <AddCompartmentModal
      v-if="showAdd && freezer"
      :freezer-id="freezerId"
      @close="showAdd = false"
      @saved="showAdd = false"
    />

    <ConfirmDialog
      v-if="toDelete"
      :message="`Supprimer le compartiment « ${toDelete.name} » ?`"
      @confirm="doDelete"
      @cancel="toDelete = null"
    />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useFreezerStore } from "../store/freezers.js";
import AddCompartmentModal from "../components/AddCompartmentModal.vue";
import SyncBadge from "../components/SyncBadge.vue";
import ConfirmDialog from "../components/ConfirmDialog.vue";

const props = defineProps({ freezerId: Number });
const router = useRouter();
const store = useFreezerStore();
const showAdd = ref(false);
const toDelete = ref(null);

const freezer = computed(() => store.freezers.find((f) => f.id === props.freezerId));

function confirmDelete(c) { toDelete.value = c; }

async function doDelete() {
  await store.removeCompartment(props.freezerId, toDelete.value.id);
  toDelete.value = null;
}
</script>

<style scoped>
.comp-row {
  display: flex; align-items: center; gap: 0.75rem;
  cursor: pointer; transition: background .15s;
}
.comp-row:hover { background: var(--surface2); }
.comp-info { flex: 1; }
.comp-name  { display: block; font-weight: 600; }
.comp-count { font-size: 0.8rem; color: var(--muted); }
.comp-arrow { font-size: 1.4rem; color: var(--muted); }
.comp-delete { opacity: 0.5; }
.comp-delete:hover { opacity: 1; }
.add-btn { width: 100%; padding: 0.8rem; }
</style>
