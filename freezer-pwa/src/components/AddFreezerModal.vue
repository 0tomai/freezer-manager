<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>Nouveau congélateur</h2>

      <div class="form-group">
        <label>Icône</label>
        <div class="emoji-picker">
          <button
            v-for="e in EMOJIS"
            :key="e"
            :class="['emoji-btn', { active: icon === e }]"
            type="button"
            @click="icon = e"
          >{{ e }}</button>
        </div>
      </div>

      <div class="form-group">
        <label>Nom *</label>
        <input v-model="name" placeholder="Ex: Grand congélo cuisine" autofocus />
      </div>

      <div class="form-group">
        <label>Description</label>
        <input v-model="description" placeholder="Facultatif" />
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

const EMOJIS = ["🧊", "❄️", "🏔️", "🌨️", "🍦", "🥶", "📦", "🗄️"];

const emit = defineEmits(["close", "saved"]);
const store = useFreezerStore();

const name = ref("");
const description = ref("");
const icon = ref("🧊");
const error = ref("");
const loading = ref(false);

async function save() {
  if (!name.value.trim()) { error.value = "Le nom est requis."; return; }
  loading.value = true;
  try {
    await store.addFreezer({ name: name.value, description: description.value, icon: icon.value });
    emit("saved");
  } catch (e) {
    error.value = e.response?.data?.error || "Erreur lors de la création.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.emoji-picker { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.emoji-btn {
  font-size: 1.5rem; padding: 0.3rem; border-radius: var(--radius-sm);
  background: var(--surface2); border: 2px solid transparent;
}
.emoji-btn.active { border-color: var(--primary); }
.actions { display: flex; gap: 0.75rem; justify-content: flex-end; }
.err { color: #f87171; font-size: 0.85rem; }
</style>
