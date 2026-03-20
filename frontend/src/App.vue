<template>
  <router-view />
</template>

<script setup>
// Use Vue Router to manage pages
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  font-family: var(--font-geist-sans), sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--foreground);
  background-color: var(--background);
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(26, 28, 32, 0.85);
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 240, 255, 0.24);
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 240, 255, 0.42);
}

button {
  font-family: inherit;
}
</style>
