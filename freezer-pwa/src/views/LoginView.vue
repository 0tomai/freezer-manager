<template>
  <div class="login-page">
    <div class="login-card card">
      <div class="login-icon">🧊</div>
      <h1>Congélo</h1>
      <p class="login-sub">Entrez le PIN pour accéder</p>

      <form @submit.prevent="submit">
        <div class="form-group">
          <label>PIN</label>
          <input
            v-model="pin"
            type="password"
            inputmode="numeric"
            autocomplete="current-password"
            placeholder="••••"
            autofocus
          />
        </div>
        <p v-if="error" class="login-error">{{ error }}</p>
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? "Connexion…" : "Se connecter" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../api/auth.js";

const router = useRouter();
const pin = ref("");
const error = ref("");
const loading = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    const { data } = await login(pin.value);
    localStorage.setItem("freezer_token", data.token);
    router.push("/");
  } catch (e) {
    error.value = e.response?.data?.error || "Erreur de connexion.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100dvh; display: flex;
  align-items: center; justify-content: center; padding: 1rem;
}
.login-card {
  width: 100%; max-width: 360px;
  display: flex; flex-direction: column; gap: 1.25rem; text-align: center;
}
.login-icon { font-size: 3rem; }
.login-sub   { color: var(--muted); font-size: 0.9rem; }
.login-error { color: #f87171; font-size: 0.85rem; text-align: left; }
form { display: flex; flex-direction: column; gap: 1rem; text-align: left; }
button { width: 100%; padding: 0.75rem; }
</style>
