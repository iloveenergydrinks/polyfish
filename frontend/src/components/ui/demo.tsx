"use client"

import { Canvas } from "@react-three/fiber"
import { ShaderPlane } from "./background-paper-shaders"

type DemoOneProps = {
  className?: string
  backgroundColor?: string
  primaryColor?: string
  secondaryColor?: string
  accentColor?: string
}

export default function DemoOne({
  className = "",
  backgroundColor = "#111318",
  primaryColor = "#00f0ff",
  secondaryColor = "#7701d0",
  accentColor = "#dcb8ff",
}: DemoOneProps) {
  return (
    <div className={`relative h-full w-full overflow-hidden ${className}`.trim()}>
      <Canvas dpr={[1, 1.5]} camera={{ position: [0, 0, 4.8], fov: 42 }}>
        <color attach="background" args={[backgroundColor]} />
        <fog attach="fog" args={[backgroundColor, 4.5, 8]} />
        <ambientLight intensity={0.9} />
        <group rotation={[-0.12, 0.05, 0.02]}>
          <ShaderPlane
            position={[-1.85, 0.95, -1.15]}
            scale={[2.35, 1.9, 1]}
            color1={primaryColor}
            color2={secondaryColor}
          />
          <ShaderPlane
            position={[1.95, -1.15, -1.65]}
            scale={[1.75, 1.45, 1]}
            color1={accentColor}
            color2={primaryColor}
          />
          <ShaderPlane
            position={[0.25, 0.15, -2.1]}
            scale={[1.15, 1.05, 1]}
            color1="#243240"
            color2={secondaryColor}
          />
        </group>
      </Canvas>

      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(0,240,255,0.08),transparent_24%),radial-gradient(circle_at_18%_72%,rgba(220,184,255,0.08),transparent_20%),linear-gradient(180deg,rgba(17,19,24,0.12),rgba(17,19,24,0.58))]" />
      <div className="pointer-events-none absolute inset-x-0 top-0 h-48 bg-gradient-to-b from-[#111318] via-[#111318]/55 to-transparent" />
      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-56 bg-gradient-to-t from-[#111318] via-[#111318]/72 to-transparent" />
    </div>
  )
}
