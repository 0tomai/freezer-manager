<template>
  <div class="app-wrapper">
    <RouterView />
    <InstallBanner />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import InstallBanner from "./components/InstallBanner.vue";
</script>

<style>
.app-wrapper { min-height: 100dvh; display: flex; flex-direction: column; }
</style>
