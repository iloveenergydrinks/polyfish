<template>
  <div class="grid-background" aria-hidden="true">
    <div class="grid-background__mesh"></div>
    <div class="grid-background__glow grid-background__glow--left"></div>
    <div class="grid-background__glow grid-background__glow--right"></div>
    <div class="grid-background__vignette"></div>
  </div>
</template>

<style scoped>
.grid-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.grid-background__mesh {
  position: absolute;
  inset: 0;
  background-color: #111318;
  background-image:
    linear-gradient(rgba(0, 240, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 240, 255, 0.06) 1px, transparent 1px),
    linear-gradient(rgba(220, 184, 255, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(220, 184, 255, 0.025) 1px, transparent 1px);
  background-size: 72px 72px, 72px 72px, 18px 18px, 18px 18px;
  background-position: -1px -1px, -1px -1px, -1px -1px, -1px -1px;
  opacity: 0.52;
}

.grid-background__glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(90px);
  opacity: 0.14;
}

.grid-background__glow--left {
  top: 8%;
  left: -8%;
  width: 40vw;
  height: 32vw;
  background: radial-gradient(circle, rgba(0, 240, 255, 0.7) 0%, rgba(0, 240, 255, 0) 72%);
}

.grid-background__glow--right {
  top: 24%;
  right: -10%;
  width: 34vw;
  height: 30vw;
  background: radial-gradient(circle, rgba(220, 184, 255, 0.55) 0%, rgba(220, 184, 255, 0) 72%);
}

.grid-background__vignette {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at center, transparent 34%, rgba(17, 19, 24, 0.2) 72%, rgba(17, 19, 24, 0.72) 100%),
    linear-gradient(180deg, rgba(17, 19, 24, 0.08) 0%, rgba(17, 19, 24, 0.28) 100%);
}
</style>
