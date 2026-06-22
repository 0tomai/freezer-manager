<template>
  <div v-if="visible" class="install-banner">
    <span class="install-icon">🧊</span>
    <div class="install-text">
      <strong>Installer l'app</strong>
      <span v-if="isIos">Appuie sur <b>Partager</b> puis <b>Sur l'écran d'accueil</b></span>
      <span v-else>Accès rapide depuis ton téléphone</span>
    </div>
    <button v-if="!isIos" class="btn-primary install-btn" @click="install">Installer</button>
    <button class="btn-icon close-btn" @click="dismiss">✕</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const visible = ref(false);
const isIos = ref(false);
let deferredPrompt = null;

onMounted(() => {
  // Ne pas afficher si déjà installée (mode standalone)
  if (window.matchMedia("(display-mode: standalone)").matches) return;
  if (localStorage.getItem("install_dismissed")) return;

  const ua = navigator.userAgent;
  const ios = /iphone|ipad|ipod/i.test(ua) && !/crios/i.test(ua);

  if (ios) {
    isIos.value = true;
    visible.value = true;
    return;
  }

  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
    visible.value = true;
  });
});

async function install() {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  if (outcome === "accepted") visible.value = false;
  deferredPrompt = null;
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
