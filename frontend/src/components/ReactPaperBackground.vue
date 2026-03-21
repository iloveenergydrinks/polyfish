<template>
  <div class="grid-background" aria-hidden="true">
    <div class="grid-background__mesh"></div>
    <div class="grid-background__debris-layer">
      <span class="grid-background__debris grid-background__debris--1"></span>
      <span class="grid-background__debris grid-background__debris--2"></span>
      <span class="grid-background__debris grid-background__debris--3"></span>
      <span class="grid-background__debris grid-background__debris--4"></span>
      <span class="grid-background__debris grid-background__debris--5"></span>
      <span class="grid-background__debris grid-background__debris--6"></span>
      <span class="grid-background__debris grid-background__debris--7"></span>
      <span class="grid-background__debris grid-background__debris--8"></span>
      <span class="grid-background__debris grid-background__debris--9"></span>
      <span class="grid-background__debris grid-background__debris--10"></span>
      <span class="grid-background__debris grid-background__debris--11"></span>
      <span class="grid-background__debris grid-background__debris--12"></span>
    </div>
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

.grid-background__debris-layer {
  position: absolute;
  inset: -8%;
  overflow: hidden;
}

.grid-background__debris {
  position: absolute;
  display: block;
  border-radius: 42% 58% 63% 37% / 39% 34% 66% 61%;
  background:
    linear-gradient(145deg, rgba(146, 186, 223, 0.32), rgba(59, 92, 126, 0.12)),
    radial-gradient(circle at 30% 30%, rgba(214, 237, 255, 0.22), transparent 58%);
  box-shadow:
    inset 0 0 0 1px rgba(214, 237, 255, 0.08),
    0 0 24px rgba(82, 133, 182, 0.08);
  opacity: 0.28;
  animation: debrisFloat 22s ease-in-out infinite;
  will-change: transform, opacity;
}

.grid-background__debris::after {
  content: "";
  position: absolute;
  inset: 18%;
  border-radius: inherit;
  background: linear-gradient(145deg, rgba(12, 21, 31, 0.36), rgba(12, 21, 31, 0));
  opacity: 0.7;
}

.grid-background__debris--1 {
  top: 10%;
  left: 8%;
  width: 24px;
  height: 18px;
  animation-delay: -2s;
}

.grid-background__debris--2 {
  top: 18%;
  left: 24%;
  width: 14px;
  height: 12px;
  animation-delay: -6s;
}

.grid-background__debris--3 {
  top: 14%;
  right: 20%;
  width: 18px;
  height: 14px;
  animation-delay: -4s;
}

.grid-background__debris--4 {
  top: 32%;
  left: 14%;
  width: 12px;
  height: 10px;
  animation-delay: -12s;
}

.grid-background__debris--5 {
  top: 36%;
  right: 12%;
  width: 28px;
  height: 22px;
  animation-delay: -8s;
}

.grid-background__debris--6 {
  top: 48%;
  left: 4%;
  width: 16px;
  height: 12px;
  animation-delay: -15s;
}

.grid-background__debris--7 {
  top: 58%;
  left: 22%;
  width: 22px;
  height: 17px;
  animation-delay: -9s;
}

.grid-background__debris--8 {
  top: 54%;
  right: 26%;
  width: 14px;
  height: 11px;
  animation-delay: -18s;
}

.grid-background__debris--9 {
  top: 70%;
  right: 10%;
  width: 26px;
  height: 19px;
  animation-delay: -5s;
}

.grid-background__debris--10 {
  bottom: 18%;
  left: 12%;
  width: 15px;
  height: 12px;
  animation-delay: -14s;
}

.grid-background__debris--11 {
  bottom: 10%;
  left: 40%;
  width: 20px;
  height: 16px;
  animation-delay: -7s;
}

.grid-background__debris--12 {
  bottom: 14%;
  right: 18%;
  width: 12px;
  height: 10px;
  animation-delay: -11s;
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

@keyframes debrisFloat {
  0% {
    transform: translate3d(0, 0, 0) rotate(0deg) scale(0.96);
    opacity: 0.18;
  }

  25% {
    transform: translate3d(12px, -10px, 0) rotate(18deg) scale(1);
    opacity: 0.28;
  }

  50% {
    transform: translate3d(-8px, 14px, 0) rotate(42deg) scale(1.06);
    opacity: 0.34;
  }

  75% {
    transform: translate3d(10px, 6px, 0) rotate(64deg) scale(0.98);
    opacity: 0.24;
  }

  100% {
    transform: translate3d(0, 0, 0) rotate(90deg) scale(0.96);
    opacity: 0.18;
  }
}
</style>
