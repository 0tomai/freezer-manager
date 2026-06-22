<template>
  <div>
    <header class="topbar">
      <span class="topbar-title">Mes congélateurs</span>
      <SyncBadge />
      <button class="btn-icon" @click="logout" title="Déconnexion">🚪</button>
    </header>

    <main class="page">
      <div v-if="store.loading" class="empty">Chargement…</div>

      <div v-else-if="store.freezers.length === 0" class="empty">
        <div class="empty-icon">🧊</div>
        <p>Aucun congélateur.<br />Ajoutez-en un !</p>
      </div>

      <FreezerCard
        v-for="f in store.freezers"
        :key="f.id"
        :freezer="f"
        @delete="confirmDelete(f)"
      />

      <button class="btn-primary add-btn" @click="showAdd = true">
        + Ajouter un congélateur
      </button>
    </main>

    <AddFreezerModal
      v-if="showAdd"
      @close="showAdd = false"
      @saved="showAdd = false"
    />

    <ConfirmDialog
      v-if="toDelete"
      :message="`Supprimer « ${toDelete.name} » et tout son contenu ?`"
      @confirm="doDelete"
      @cancel="toDelete = null"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useFreezerStore } from "../store/freezers.js";
import FreezerCard from "../components/FreezerCard.vue";
import AddFreezerModal from "../components/AddFreezerModal.vue";
import SyncBadge from "../components/SyncBadge.vue";
import ConfirmDialog from "../components/ConfirmDialog.vue";

const store = useFreezerStore();
const router = useRouter();
const showAdd = ref(false);
const toDelete = ref(null);

onMounted(() => store.loadFreezer());

function logout() {
  localStorage.removeItem("freezer_token");
  router.push("/login");
}

function confirmDelete(f) {
  toDelete.value = f;
}

async function doDelete() {
  await store.removeFreezer(toDelete.value.id);
  toDelete.value = null;
}
</script>

<style scoped>
.add-btn { width: 100%; padding: 0.8rem; }
</style>
