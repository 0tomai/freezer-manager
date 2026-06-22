<template>
  <div v-if="visible" class="install-banner">
    <span class="install-icon">🧊</span>
    <div class="install-text">
      <strong>Installer l'app</strong>
      <span v-if="isIos">Appuie sur <b>⎋ Partager</b> → <b>Sur l'écran d'accueil</b></span>
      <span v-else-if="canPrompt">Accès rapide depuis ton téléphone</span>
      <span v-else>Ouvre le menu de ton navigateur → <b>Ajouter à l'écran d'accueil</b></span>
    </div>
    <button v-if="canPrompt" class="btn-primary install-btn" @click="install">Installer</button>
    <button class="btn-icon close-btn" @click="dismiss">✕</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const visible = ref(false);
const isIos = ref(false);
const canPrompt = ref(false);
let deferredPrompt = null;

onMounted(() => {
  if (window.matchMedia("(display-mode: standalone)").matches) return;
  if (window.navigator.standalone === true) return;
  if (localStorage.getItem("install_dismissed")) return;

  const ua = navigator.userAgent;
  isIos.value = /iphone|ipad|ipod/i.test(ua) && !/crios/i.test(ua);

  // Toujours afficher le bandeau (avec instructions manuelles en fallback)
  visible.value = true;

  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
    canPrompt.value = true;
  });

  window.addEventListener("appinstalled", () => {
    visible.value = false;
  });
});

async function install() {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  if (outcome === "accepted") visible.value = false;
  deferredPrompt = null;
  canPrompt.value = false;
}

function dismiss() {
  visible.value = false;
  localStorage.setItem("install_dismissed", "1");
}
</script>

<style scoped>
.install-banner {
  display: flex; align-items: center; gap: 0.75rem;
  background: var(--primary-dark); color: #fff;
  padding: 0.75rem 1rem;
  position: sticky; bottom: 0; z-index: 50;
  border-top: 1px solid rgba(255,255,255,.15);
}
.install-icon { font-size: 1.5rem; flex-shrink: 0; }
.install-text { flex: 1; display: flex; flex-direction: column; font-size: 0.85rem; gap: 0.1rem; }
.install-text strong { font-size: 0.95rem; }
.install-btn { flex-shrink: 0; padding: 0.4rem 0.9rem; font-size: 0.85rem; }
.close-btn { color: rgba(255,255,255,.7); flex-shrink: 0; }
.close-btn:hover { color: #fff; background: rgba(255,255,255,.1); }
</style>
