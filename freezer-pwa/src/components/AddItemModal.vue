<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>{{ editItem ? "Modifier l'article" : "Nouvel article" }}</h2>

      <div class="form-group">
        <label>Nom *</label>
        <input v-model="form.name" placeholder="Ex: Poulet rôti" autofocus />
      </div>

      <div class="row">
        <div class="form-group">
          <label>Quantité</label>
          <input v-model.number="form.quantity" type="number" min="0" step="0.5" />
        </div>
        <div class="form-group">
          <label>Unité</label>
          <input v-model="form.unit" placeholder="kg, pcs, L…" list="units" />
          <datalist id="units">
            <option value="kg" /><option value="g" /><option value="L" />
            <option value="cl" /><option value="pcs" /><option value="portions" />
          </datalist>
        </div>
      </div>

      <div class="form-group">
        <label>Notes</label>
        <input v-model="form.notes" placeholder="Date de congélation, recette…" />
      </div>

      <p v-if="error" class="err">{{ error }}</p>

      <div class="actions">
        <button class="btn-ghost" @click="$emit('close')">Annuler</button>
        <button class="btn-primary" @click="save" :disabled="loading">
          {{ loading ? "…" : editItem ? "Enregistrer" : "Ajouter" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import { useItemStore } from "../store/items.js";

const props = defineProps({
  compartmentId: Number,
  editItem: { type: Object, default: null },
});
const emit = defineEmits(["close", "saved"]);
const itemStore = useItemStore();

const form = reactive({ name: "", quantity: 1, unit: "", notes: "" });
const error = ref("");
const loading = ref(false);

watch(
  () => props.editItem,
  (item) => {
    if (item) {
      form.name = item.name;
      form.quantity = item.quantity;
      form.unit = item.unit || "";
      form.notes = item.notes || "";
    }
  },
  { immediate: true }
);

async function save() {
  if (!form.name.trim()) { error.value = "Le nom est requis."; return; }
  loading.value = true;
  try {
    if (props.editItem) {
      await itemStore.editItem(props.editItem.id, props.compartmentId, {
        name: form.name,
        quantity: form.quantity,
        unit: form.unit || null,
        notes: form.notes || null,
      });
    } else {
      await itemStore.addItem({
        compartment_id: props.compartmentId,
        name: form.name,
        quantity: form.quantity,
        unit: form.unit || null,
        notes: form.notes || null,
      });
    }
    emit("saved");
  } catch (e) {
    error.value = e.response?.data?.error || "Erreur lors de l'enregistrement.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.row { display: flex; gap: 0.75rem; }
.row .form-group { flex: 1; }
.actions { display: flex; gap: 0.75rem; justify-content: flex-end; }
.err { color: #f87171; font-size: 0.85rem; }
</style>
