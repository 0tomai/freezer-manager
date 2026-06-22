<template>
  <div class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal">
      <h3>Confirmer</h3>
      <p>{{ message }}</p>
      <div class="actions">
        <button class="btn-ghost" @click="$emit('cancel')">Annuler</button>
        <button class="btn-danger" @click="$emit('confirm')">Supprimer</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ message: String });
defineEmits(["confirm", "cancel"]);
</script>

<style scoped>
.actions { display: flex; gap: 0.75rem; justify-content: flex-end; }
</style>
