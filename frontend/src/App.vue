<template>
  <div id="app-shell" class="grain">
    <router-view />
  </div>
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
  font-family: var(--font-geist-sans), monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--foreground);
  background-color: var(--background);
}

#app-shell {
  min-height: 100vh;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #0a0a0a;
}

::-webkit-scrollbar-thumb {
  background: #333333;
}

::-webkit-scrollbar-thumb:hover {
  background: #555555;
}

button {
  font-family: inherit;
}
</style>
