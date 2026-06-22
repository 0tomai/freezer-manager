<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>Nouveau compartiment</h2>

      <div class="form-group">
        <label>Nom *</label>
        <input v-model="name" placeholder="Ex: Tiroir du bas" autofocus />
      </div>

      <p v-if="error" class="err">{{ error }}</p>

      <div class="actions">
        <button class="btn-ghost" @click="$emit('close')">Annuler</button>
        <button class="btn-primary" @click="save" :disabled="loading">
          {{ loading ? "…" : "Créer" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useFreezerStore } from "../store/freezers.js";

const props = defineProps({ freezerId: Number });
const emit = defineEmits(["close", "saved"]);
const store = useFreezerStore();

const name = ref("");
const error = ref("");
const loading = ref(false);

async function save() {
  if (!name.value.trim()) { error.value = "Le nom est requis."; return; }
  loading.value = true;
  try {
    await store.addCompartment(props.freezerId, { name: name.value });
    emit("saved");
  } catch (e) {
    error.value = e.response?.data?.error || "Erreur lors de la création.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.actions { display: flex; gap: 0.75rem; justify-content: flex-end; }
.err { color: #f87171; font-size: 0.85rem; }
</style>
