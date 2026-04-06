<template>
  <div class="terminal-background ascii-grid" aria-hidden="true">
    <div class="terminal-background__vignette"></div>
  </div>
</template>

<style scoped>
.terminal-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  background: #0a0a0a;
}

.terminal-background__vignette {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at center,
    transparent 40%,
    rgba(0, 0, 0, 0.4) 80%,
    rgba(0, 0, 0, 0.7) 100%
  );
}
</style>
