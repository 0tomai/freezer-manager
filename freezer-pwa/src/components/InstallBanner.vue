<template>
  <!-- Android / Desktop -->
  <div id="install-banner" class="install-banner" :class="{ 'install-visible': showAndroid }">
    <span class="install-icon">🧊</span>
    <div class="install-text">
      <strong>Installer Congélo</strong>
      <span>Accès direct depuis votre écran d'accueil</span>
    </div>
    <button class="btn-primary install-btn" @click="triggerInstall">Installer</button>
    <button class="install-close" @click="dismiss" aria-label="Fermer">&times;</button>
  </div>

  <!-- iOS -->
  <div id="install-ios" class="install-banner install-ios" :class="{ 'install-visible': showIos }">
    <span class="install-icon">🧊</span>
    <div class="install-text">
      <strong>Installer l'application</strong>
      <span>Appuyez sur <strong>⎋ Partager</strong> puis <strong>"Sur l'écran d'accueil"</strong></span>
    </div>
    <button class="install-close" @click="dismiss" aria-label="Fermer">&times;</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const showAndroid = ref(false);
const showIos = ref(false);
let deferredPrompt = null;

function isIOS() {
  return /iphone|ipad|ipod/i.test(navigator.userAgent) && !window.MSStream;
}
function isStandalone() {
  return window.matchMedia("(display-mode: standalone)").matches
    || window.navigator.standalone === true;
}
function isDismissed() {
  return localStorage.getItem("install-dismissed") === "1";
}

onMounted(() => {
  if (isStandalone() || isDismissed()) return;

  if (isIOS()) {
    setTimeout(() => { showIos.value = true; }, 2500);
    return;
  }

  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
    setTimeout(() => { showAndroid.value = true; }, 2500);
  });

  window.addEventListener("appinstalled", () => {
    showAndroid.value = false;
  });
});

function triggerInstall() {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then((r) => {
    if (r.outcome === "accepted") dismiss();
    deferredPrompt = null;
  });
}

function dismiss() {
  showAndroid.value = false;
  showIos.value = false;
  localStorage.setItem("install-dismissed", "1");
}
</script>

<style scoped>
.install-banner {
  position: fixed;
  bottom: -120px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 999;
  width: calc(100% - 2rem);
  max-width: 520px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 3px solid var(--primary);
  padding: 0.85rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.6);
  border-radius: var(--radius) var(--radius) 0 0;
  transition: bottom 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.install-banner.install-visible {
  bottom: 0;
}
.install-icon {
  font-size: 2rem;
  line-height: 1;
  flex-shrink: 0;
}
.install-text {
  flex: 1;
  min-width: 0;
}
.install-text strong {
  display: block;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.15rem;
}
.install-text span {
  display: block;
  font-size: 0.8rem;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.install-ios .install-text span {
  white-space: normal;
}
.install-btn {
  flex-shrink: 0;
  padding: 0.4rem 0.9rem;
  font-size: 0.85rem;
}
.install-close {
  background: none;
  border: none;
  color: var(--muted);
  font-size: 1.4rem;
  cursor: pointer;
  line-height: 1;
  padding: 0.2rem 0.4rem;
  flex-shrink: 0;
}
.install-close:hover {
  color: var(--text);
}
</style>
