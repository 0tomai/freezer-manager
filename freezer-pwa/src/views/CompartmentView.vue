<template>
  <div>
    <header class="topbar">
      <button class="btn-icon" @click="router.back()">←</button>
      <span class="topbar-title">{{ compartment?.name }}</span>
      <SyncBadge />
    </header>

    <main class="page">
      <div v-if="!compartment" class="empty">Compartiment introuvable.</div>

      <template v-else>
        <ItemCard
          v-for="item in compartment.items"
          :key="item.id"
          :item="item"
          @adjust="(delta) => itemStore.adjustQty(item.id, compartment.id, delta)"
          @edit="startEdit(item)"
          @delete="confirmDelete(item)"
        />

        <div v-if="compartment.items.length === 0" class="empty">
          <div class="empty-icon">🫙</div>
          <p>Ce compartiment est vide.</p>
        </div>

        <button class="btn-primary add-btn" @click="showAdd = true">
          + Ajouter un article
        </button>
      </template>
    </main>

    <AddItemModal
      v-if="showAdd && compartment"
      :compartment-id="compartment.id"
      :edit-item="editTarget"
      @close="closeModal"
      @saved="closeModal"
    />

    <ConfirmDialog
      v-if="toDelete"
      :message="`Supprimer « ${toDelete.name} » ?`"
      @confirm="doDelete"
      @cancel="toDelete = null"
    />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useFreezerStore } from "../store/freezers.js";
import { useItemStore } from "../store/items.js";
import ItemCard from "../components/ItemCard.vue";
import AddItemModal from "../components/AddItemModal.vue";
import SyncBadge from "../components/SyncBadge.vue";
import ConfirmDialog from "../components/ConfirmDialog.vue";

const props = defineProps({ compartmentId: Number });
const router = useRouter();
const freezerStore = useFreezerStore();
const itemStore = useItemStore();
const showAdd = ref(false);
const editTarget = ref(null);
const toDelete = ref(null);

const compartment = computed(() => {
  for (const f of freezerStore.freezers) {
    const c = f.compartments?.find((c) => c.id === props.compartmentId);
    if (c) return c;
  }
  return null;
});

function startEdit(item) {
  editTarget.value = item;
  showAdd.value = true;
}

function closeModal() {
  showAdd.value = false;
  editTarget.value = null;
}

function confirmDelete(item) { toDelete.value = item; }

async function doDelete() {
  await itemStore.removeItem(toDelete.value.id, compartment.value.id);
  toDelete.value = null;
}
</script>

<style scoped>
.add-btn { width: 100%; padding: 0.8rem; }
</style>
