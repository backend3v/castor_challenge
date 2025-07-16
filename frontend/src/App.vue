<script setup>
// Home minimalista
const appName = import.meta.env.VITE_APP_NAME || 'App';
</script>

<template>
  <div class="app-home">
    <h1>{{ appName }}</h1>
  </div>
</template>

<style scoped>
.app-home {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  padding: 0;
  margin: 0;
}
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
  color: #22223b;
  font-family: 'Inter', Arial, sans-serif;
  letter-spacing: 2px;
  text-align: center;
  margin: 0;
  padding: 0;
}
</style>
