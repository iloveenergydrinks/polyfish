import fs from 'node:fs/promises'
import path from 'node:path'
import { Stitch, StitchToolClient } from '@google/stitch-sdk'

const prompt = `
Design a desktop landing page for a product called PolyFish.
PolyFish is a swarm prediction system for Polymarket.

Visual direction:
- light editorial interface with premium market-terminal discipline
- clean geometry, restrained glass, and low-noise gradients
- performance-first composition with minimal decorative motion
- sharp information hierarchy for live markets and written theses
- intentional whitespace and strong typography

Required sections:
- top navigation with PolyFish branding
- hero section about live markets and written theses
- selected market preview card with probability bars
- active market list with search and filters
- thesis prompt panel with CTA
- collapsed archive/history section that can be loaded on demand

Avoid:
- memecoin aesthetics
- neon overload
- clutter
- cheesy crypto motifs
- expensive blur stacks
- background effects that would hurt FPS on a market list
`.trim()

const outputDir = path.resolve('.stitch-artifacts')
const timeoutMs = Number(process.env.STITCH_TIMEOUT_MS || 240000)

if (!process.env.STITCH_API_KEY) {
  console.error('STITCH_API_KEY is required')
  process.exit(1)
}

const projectTitle = process.env.STITCH_PROJECT_TITLE || `PolyFish Landing ${new Date().toISOString()}`

try {
  await fs.mkdir(outputDir, { recursive: true })

  const client = new StitchToolClient({
    apiKey: process.env.STITCH_API_KEY,
    timeout: timeoutMs
  })
  const sdk = new Stitch(client)

  const withTimeout = async (task, label) => {
    return await Promise.race([
      task,
      new Promise((_, reject) => {
        setTimeout(() => reject(new Error(`${label} timed out after ${timeoutMs}ms`)), timeoutMs)
      })
    ])
  }

  const project = await withTimeout(sdk.createProject(projectTitle), 'createProject')
  const screen = await withTimeout(project.generate(prompt, 'DESKTOP'), 'generate')
  const htmlUrl = await screen.getHtml()
  const imageUrl = await screen.getImage()

  await fs.writeFile(
    path.join(outputDir, 'landing.json'),
    JSON.stringify(
      {
        projectId: project.projectId,
        screenId: screen.screenId,
        htmlUrl,
        imageUrl,
        prompt,
        createdAt: new Date().toISOString()
      },
      null,
      2
    )
  )

  const htmlResponse = await fetch(htmlUrl)
  if (!htmlResponse.ok) {
    throw new Error(`Failed to download HTML: ${htmlResponse.status}`)
  }
  const html = await htmlResponse.text()
  await fs.writeFile(path.join(outputDir, 'landing.html'), html)

  const imageResponse = await fetch(imageUrl)
  if (!imageResponse.ok) {
    throw new Error(`Failed to download image: ${imageResponse.status}`)
  }
  const imageBuffer = Buffer.from(await imageResponse.arrayBuffer())
  await fs.writeFile(path.join(outputDir, 'landing.png'), imageBuffer)

  console.log(JSON.stringify({ projectId: project.projectId, screenId: screen.screenId, outputDir }, null, 2))
} catch (error) {
  console.error('Stitch landing generation failed')
  console.error(error instanceof Error ? error.message : String(error))
  process.exit(1)
}
