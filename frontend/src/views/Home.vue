<template>
  <div class="obsidian-page">
    <ReactPaperBackground />

    <nav class="topbar">
      <div class="topbar-inner">
        <div class="brand-lockup">
          <img class="brand-logo" src="/polyfish-logo.png" alt="PolyFish logo">
          <div class="brand-wordmark">PolyFish</div>
        </div>
        <div class="topbar-links">
          <a href="#ecosystem">Why PolyFish</a>
          <a href="#methodology">How It Works</a>
          <a href="#integrations">What Powers It</a>
          <a href="#launch">Start Simulation</a>
        </div>
        <div class="topbar-actions">
          <button class="primary-button" type="button" @click="scrollToLaunch">Start Simulation</button>
        </div>
      </div>
    </nav>

    <main class="page-main">
      <div class="hero-media-layer" aria-hidden="true">
        <div class="hero-media-frame">
          <video
            class="hero-background-video"
            autoplay
            muted
            loop
            playsinline
          >
            <source src="/hero-background.mp4" type="video/mp4">
            <source src="/hero-background.mov" type="video/quicktime">
          </video>
        </div>
      </div>

      <section class="hero-section">
        <div class="hero-grid">
          <div class="hero-copy">
            <div class="hero-brand-pill">
              <img class="hero-brand-logo" src="/polyfish-logo.png" alt="PolyFish logo">
              <div class="hero-brand-copy">
                <strong>PolyFish</strong>
                <span>Swarm prediction for live markets</span>
              </div>
            </div>
            <h1>
              See what the market
              <span>is missing.</span>
              <br>
              Start with a question. Leave with conviction.
            </h1>
            <p>
              PolyFish turns live prediction markets into guided AI simulations that surface sentiment, pressure-test
              the consensus, and help you decide faster. Pick a market, define your angle, and get a sharper read on
              what could happen next.
            </p>
            <div class="hero-actions">
              <button class="primary-button large" type="button" @click="scrollToLaunch">Start Simulation</button>
              <button class="ghost-button large" type="button" @click="scrollToIntegrations">See How It Works</button>
            </div>
          </div>
        </div>
      </section>

      <section id="launch" ref="launchSection" class="content-section launch-section launch-section-priority">
        <div class="section-head launch-head">
          <div>
            <div class="eyebrow">Start Simulation</div>
            <h2>Choose a live market and build your edge</h2>
          </div>
          <p>
            Start with a live market, tell PolyFish what you want to test, and launch a simulation built to expose
            hidden pressure points, narrative shifts, and asymmetric opportunities.
          </p>
        </div>

        <div ref="wizardCard" class="glass-card wizard-card">
          <div class="wizard-steps">
            <button
              class="wizard-step"
              :class="{ active: currentWizardStep === 1, complete: currentWizardStep > 1 }"
              type="button"
              @click="goToWizardStep(1)"
            >
              <span class="wizard-step-index">1</span>
              <span class="wizard-step-copy">
                <strong>Choose Market</strong>
                <em>Browse active markets or paste a Polymarket link</em>
              </span>
            </button>

            <button
              class="wizard-step"
              :class="{ active: currentWizardStep === 2, complete: currentWizardStep > 2 }"
              type="button"
              @click="goToWizardStep(2)"
            >
              <span class="wizard-step-index">2</span>
              <span class="wizard-step-copy">
                <strong>Shape Brief</strong>
                <em>Tell PolyFish what to test and stress</em>
              </span>
            </button>

            <button
              class="wizard-step"
              :class="{ active: currentWizardStep === 3 }"
              type="button"
              @click="goToWizardStep(3)"
            >
              <span class="wizard-step-index">3</span>
              <span class="wizard-step-copy">
                <strong>Review & Launch</strong>
                <em>Confirm the market and start the run</em>
              </span>
            </button>
          </div>

          <div v-if="currentWizardStep === 1" class="wizard-panel wizard-panel-market">
            <div class="wizard-panel-head">
              <div>
                <span class="browser-label">Step 1</span>
                <h3>{{ loadingMarkets ? 'Refreshing active markets…' : 'Choose the market you want to simulate' }}</h3>
                <p>Use the table to compare current opportunities, or paste a direct Polymarket link if you already know the market.</p>
              </div>
              <button class="ghost-button compact" type="button" @click="refreshMarkets" :disabled="loadingMarkets">
                {{ loadingMarkets ? 'Refreshing…' : 'Refresh' }}
              </button>
            </div>

            <div class="market-control-bar wizard-market-controls">
              <label class="market-search market-search-direct">
                <span class="material-symbols-outlined">link</span>
                <input
                  v-model="directLookup"
                  type="text"
                  placeholder="Paste a Polymarket URL, event slug, or market id"
                  @keydown.enter.prevent="lookupSpecificMarket"
                >
              </label>

              <button
                class="primary-button compact-primary"
                type="button"
                :disabled="lookupLoading || !directLookup.trim()"
                @click="lookupSpecificMarket"
              >
                {{ lookupLoading ? 'Finding…' : 'Find market' }}
              </button>

              <label class="market-search">
                <span class="material-symbols-outlined">search</span>
                <input
                  v-model="marketSearch"
                  type="text"
                  placeholder="Search by topic, event, person, or ticker"
                >
              </label>

              <label class="market-sort market-sort-compact">
                <span>Sort</span>
                <select v-model="marketSort">
                  <option value="closingSoon">Closing soon</option>
                  <option value="highestVolume">Highest volume</option>
                  <option value="mostContested">Most contested</option>
                </select>
              </label>
            </div>

            <div v-if="lookupSuccess" class="state-box success lookup-success">
              <strong>Market found and selected</strong>
              <span>
                <b>{{ lookupSuccess.question }}</b>
                <em>{{ formatPercent(getBinaryProbability(lookupSuccess)) }} consensus • closes {{ formatDate(lookupSuccess.end_date) }}</em>
              </span>
              <small>You can review it below or move straight to Step 2.</small>
            </div>

            <div v-if="lookupError" class="state-box error lookup-error">{{ lookupError }}</div>

            <div class="market-filter-row">
              <div class="market-filter-chips">
                <button
                  v-for="category in marketCategories"
                  :key="category.id"
                  class="filter-chip"
                  :class="{ active: marketCategory === category.id }"
                  type="button"
                  @click="marketCategory = category.id"
                >
                  <span>{{ category.label }}</span>
                  <em>{{ category.count }}</em>
                </button>

                <button
                  v-if="hasActiveMarketFilters"
                  class="filter-reset"
                  type="button"
                  @click="clearMarketFilters"
                >
                  Reset
                </button>
              </div>

              <div class="market-results-meta">
                <span>{{ displayedMarkets.length }} shown</span>
                <span>{{ filteredMarkets.length }} matching</span>
                <span>{{ markets.length }} loaded</span>
              </div>
            </div>

            <div v-if="marketError" class="state-box error">{{ marketError }}</div>
            <div v-else-if="loadingMarkets && markets.length === 0" class="state-box">Loading active markets…</div>
            <div v-else-if="filteredMarkets.length === 0" class="state-box">No markets match those filters. Clear them and try again.</div>
            <div v-else-if="displayedMarkets.length === 0" class="state-box">No active markets available.</div>

            <div v-else class="market-table-shell">
              <table class="market-table">
                <thead>
                  <tr>
                    <th>Market</th>
                    <th>Event</th>
                    <th>Category</th>
                    <th>Close</th>
                    <th>Consensus</th>
                    <th>24h Vol</th>
                    <th>Liquidity</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="market in displayedMarkets"
                    :key="market.id || market.slug"
                    class="market-table-row"
                    :class="{ selected: selectedMarket?.slug === market.slug }"
                    tabindex="0"
                    @click="selectMarket(market)"
                    @keydown.enter.prevent="selectMarket(market)"
                    @keydown.space.prevent="selectMarket(market)"
                  >
                    <td class="market-title-cell">
                      <div class="market-title-main">{{ market.question }}</div>
                      <div class="market-title-sub">{{ market.slug }}</div>
                    </td>
                    <td class="market-event-cell">
                      <div class="market-event-main">{{ truncateText(market.event?.title || market.event?.slug || 'Independent market', 44) }}</div>
                      <div class="market-event-sub">{{ truncateText(market.description || 'No market description available.', 78) }}</div>
                    </td>
                    <td>
                      <span class="market-cell-chip">{{ getCategoryLabel(getMarketCategory(market)) }}</span>
                    </td>
                    <td>{{ formatDate(market.end_date) }}</td>
                    <td class="market-number-cell">{{ formatPercent(getBinaryProbability(market)) }}</td>
                    <td class="market-number-cell">{{ formatCompactNumber(market.volume_24h) }}</td>
                    <td class="market-number-cell">{{ formatCompactNumber(market.liquidity) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="filteredMarkets.length > displayedMarkets.length" class="market-list-actions">
              <button class="ghost-button compact" type="button" @click="showMoreMarkets">
                Show 50 more markets
              </button>
            </div>

            <div class="wizard-footer">
              <div class="wizard-footer-summary" v-if="selectedMarket">
                <span class="wizard-footer-label">Selected</span>
                <strong>{{ selectedMarket.question }}</strong>
                <em>{{ formatPercent(getBinaryProbability(selectedMarket)) }} consensus • closes {{ formatDate(selectedMarket.end_date) }}</em>
              </div>
              <div class="wizard-footer-summary" v-else>
                <span class="wizard-footer-label">Next step</span>
                <strong>Select a market</strong>
                <em>Choose any active market or paste a direct Polymarket link.</em>
              </div>

              <button class="primary-button large" type="button" :disabled="!selectedMarket" @click="goToWizardStep(2)">
                Continue to brief
              </button>
            </div>
          </div>

          <div v-else-if="currentWizardStep === 2" class="wizard-panel wizard-panel-brief">
            <div class="wizard-panel-head">
              <div>
                <span class="browser-label">Step 2</span>
                <h3>{{ selectedMarket?.question || 'Select a market first' }}</h3>
                <p>Write the exact angle you want PolyFish to test. Good prompts focus on catalysts, mispricing, timing, and downside risk.</p>
              </div>
            </div>

            <div v-if="selectedMarket" class="selected-market-grid">
              <div class="selected-market-stat">
                <span>Category</span>
                <strong>{{ getCategoryLabel(getMarketCategory(selectedMarket)) }}</strong>
              </div>
              <div class="selected-market-stat">
                <span>Consensus</span>
                <strong>{{ formatPercent(getBinaryProbability(selectedMarket)) }}</strong>
              </div>
              <div class="selected-market-stat">
                <span>24h Volume</span>
                <strong>{{ formatCompactNumber(selectedMarket.volume_24h) }}</strong>
              </div>
              <div class="selected-market-stat">
                <span>Liquidity</span>
                <strong>{{ formatCompactNumber(selectedMarket.liquidity) }}</strong>
              </div>
            </div>

            <div v-if="selectedMarket" class="selected-outcomes">
              <div
                v-for="outcome in selectedMarket.outcomes"
                :key="outcome.name"
                class="selected-outcome"
              >
                <div class="selected-outcome-row">
                  <span>{{ outcome.name }}</span>
                  <span>{{ formatPercent(outcome.price) }}</span>
                </div>
                <div class="progress-track"><div class="progress-fill fill-a" :style="getOutcomeFillStyle(outcome.price)"></div></div>
              </div>
            </div>

            <label class="prompt-field">
              <span>Simulation Brief</span>
              <textarea
                v-model="simulationRequirement"
                rows="9"
                placeholder="Example: Identify which catalyst is most underpriced, where the market could re-rate quickly, and what evidence would invalidate the current consensus."
              ></textarea>
            </label>

            <div class="prompt-presets">
              <div class="prompt-presets-head">
                <span>Quick start prompts</span>
                <p>Use one as-is or edit it before moving to review.</p>
              </div>

              <div class="prompt-preset-list">
                <button
                  v-for="template in simulationTemplates"
                  :key="template.label"
                  class="prompt-preset"
                  type="button"
                  @click="applySimulationTemplate(template.prompt)"
                >
                  {{ template.label }}
                </button>
              </div>
            </div>

            <div class="wizard-footer">
              <button class="ghost-button large" type="button" @click="goToWizardStep(1)">
                Back to markets
              </button>
              <button class="primary-button large" type="button" :disabled="!simulationRequirement.trim()" @click="goToWizardStep(3)">
                Review simulation
              </button>
            </div>
          </div>

          <div v-else class="wizard-panel wizard-panel-review">
            <div class="wizard-panel-head">
              <div>
                <span class="browser-label">Step 3</span>
                <h3>Review and launch</h3>
                <p>Check the selected market and the exact brief that will be sent into the simulation pipeline.</p>
              </div>
            </div>

            <div class="review-grid">
              <div class="review-card">
                <span class="review-label">Chosen Market</span>
                <h4>{{ selectedMarket?.question || 'No market selected' }}</h4>
                <p>{{ truncateText(selectedMarket?.description, 260) }}</p>

                <div v-if="selectedMarket" class="selected-market-grid review-stats-grid">
                  <div class="selected-market-stat">
                    <span>Category</span>
                    <strong>{{ getCategoryLabel(getMarketCategory(selectedMarket)) }}</strong>
                  </div>
                  <div class="selected-market-stat">
                    <span>Consensus</span>
                    <strong>{{ formatPercent(getBinaryProbability(selectedMarket)) }}</strong>
                  </div>
                  <div class="selected-market-stat">
                    <span>24h Volume</span>
                    <strong>{{ formatCompactNumber(selectedMarket.volume_24h) }}</strong>
                  </div>
                  <div class="selected-market-stat">
                    <span>Close</span>
                    <strong>{{ formatDate(selectedMarket.end_date) }}</strong>
                  </div>
                </div>
              </div>

              <div class="review-card">
                <span class="review-label">Simulation Brief</span>
                <h4>Your thesis prompt</h4>
                <pre class="review-brief">{{ simulationRequirement || 'No simulation brief added yet.' }}</pre>
              </div>
            </div>

            <div class="wizard-footer">
              <button class="ghost-button large" type="button" @click="goToWizardStep(2)">
                Back to brief
              </button>
              <a class="ghost-button large" :href="selectedMarket?.url || 'https://polymarket.com'" target="_blank" rel="noreferrer">
                Open on Polymarket
              </a>
              <button class="primary-button large" type="button" :disabled="!canSubmit" @click="startSimulation">
                Start Simulation
              </button>
            </div>
          </div>
        </div>
      </section>

      <section id="methodology" class="content-section">
        <div class="section-head">
          <div>
            <div class="eyebrow">How It Works</div>
            <h2>From market noise to usable insight</h2>
          </div>
          <p>
            PolyFish pulls in live market context, tests competing narratives through multiple AI viewpoints, and turns
            that friction into a more disciplined read on where conviction is justified.
          </p>
        </div>

        <div class="feature-grid three-up">
          <article class="glass-card feature-card">
            <span class="material-symbols-outlined">hub</span>
            <h3>Live Market Context</h3>
            <p>Every simulation starts with fresh market data, event framing, and the signals shaping trader behavior right now.</p>
          </article>
          <article class="glass-card feature-card feature-card-accent">
            <span class="material-symbols-outlined">psychology</span>
            <h3>Competing AI Perspectives</h3>
            <p>Multiple agents challenge each other’s assumptions so you get a stronger answer than a single summary or one-shot prediction.</p>
          </article>
          <article class="glass-card feature-card">
            <span class="material-symbols-outlined">analytics</span>
            <h3>Actionable Output</h3>
            <p>The result is a structured thesis you can review, refine, and use to decide whether the market is priced correctly.</p>
          </article>
        </div>
      </section>

      <section id="integrations" class="content-section integrations-section">
        <div class="integration-layout">
          <div class="glass-card integration-chart ai-glow">
            <div class="swarm-panel-head">
              <span class="swarm-kicker">Swarm Infographic</span>
              <strong>How PolyFish turns noisy markets into a single decision path</strong>
            </div>

            <div class="swarm-stage">
              <div class="swarm-stage-grid"></div>

              <div class="swarm-column-label swarm-column-label--signals">Signals</div>
              <div class="swarm-column-label swarm-column-label--agents">Agent swarm</div>
              <div class="swarm-column-label swarm-column-label--output">Thesis</div>

              <div class="swarm-signal-stack">
                <div class="swarm-signal-card">
                  <span>Live markets</span>
                  <strong>{{ markets.length || '--' }}</strong>
                </div>
                <div class="swarm-signal-card">
                  <span>Event memory</span>
                  <strong>linked</strong>
                </div>
                <div class="swarm-signal-card">
                  <span>Stress prompts</span>
                  <strong>active</strong>
                </div>
              </div>

              <div class="swarm-node-field">
                <div
                  v-for="node in swarmNodes"
                  :key="node.id"
                  class="swarm-node"
                  :class="`swarm-node--${node.tone}`"
                  :style="{
                    left: node.left,
                    top: node.top,
                    width: node.size,
                    height: node.size,
                    animationDelay: node.delay
                  }"
                >
                  <span class="swarm-node-core"></span>
                </div>

                <div
                  v-for="trail in swarmTrails"
                  :key="trail.id"
                  class="swarm-trail"
                  :style="{
                    left: trail.left,
                    top: trail.top,
                    width: trail.width,
                    transform: trail.transform,
                    animationDelay: trail.delay
                  }"
                ></div>

                <div class="swarm-core">
                  <span class="swarm-core-ring swarm-core-ring--outer"></span>
                  <span class="swarm-core-ring swarm-core-ring--inner"></span>
                  <span class="swarm-core-label">Consensus under pressure</span>
                </div>
              </div>

              <div class="swarm-output-card">
                <span class="swarm-output-label">Decision output</span>
                <strong>Structured thesis</strong>
                <p>Bull case, bear case, catalyst timing, and asymmetric risk in one readable brief.</p>
                <div class="swarm-output-lines">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>

              <div class="swarm-caption-row">
                <span>Signals split</span>
                <span>Agents collide</span>
                <span>Weak narratives fail</span>
                <span>One thesis survives</span>
              </div>
            </div>
          </div>

          <div class="integration-copy">
            <div class="eyebrow">Why It Works</div>
            <h2>Built to turn complexity into confidence</h2>
            <p>
              Most market tools stop at charts or headlines. PolyFish goes further by combining live market context,
              persistent memory, and adversarial AI simulation to show you where consensus looks strong and where it can break.
            </p>
            <ul class="integration-list">
              <li><span class="material-symbols-outlined">check_circle</span> Live market inputs instead of static snapshots</li>
              <li><span class="material-symbols-outlined">check_circle</span> Memory that keeps track of people, events, and narrative links</li>
              <li><span class="material-symbols-outlined">check_circle</span> Simulations that test both bullish and bearish cases</li>
              <li><span class="material-symbols-outlined">check_circle</span> A final thesis designed to support real decisions</li>
            </ul>
          </div>
        </div>
      </section>

      <section id="ecosystem" class="content-section">
        <h2 class="section-title-centered">Why people will use PolyFish</h2>
        <div class="feature-grid four-up">
          <article class="stack-card">
            <span class="material-symbols-outlined">speed</span>
            <h3>Faster Clarity</h3>
            <p>Get from open question to structured market view in minutes, not hours of scattered research.</p>
          </article>
          <article class="stack-card">
            <span class="material-symbols-outlined">shield</span>
            <h3>Better Risk Framing</h3>
            <p>Test overconfidence, weak assumptions, and downside scenarios before you commit to a position.</p>
          </article>
          <article class="stack-card">
            <span class="material-symbols-outlined">lan</span>
            <h3>One Guided Workflow</h3>
            <p>Move from market discovery to simulation to written thesis inside one flow instead of juggling separate tools.</p>
          </article>
          <article class="stack-card">
            <span class="material-symbols-outlined">public</span>
            <h3>Made for Real Event Markets</h3>
            <p>Built for politics, macro, sports, crypto, and any market where narrative and timing drive price.</p>
          </article>
        </div>
      </section>

      <section class="content-section proof-section">
        <div class="proof-grid">
          <div class="proof-stats">
            <div class="proof-stat">
              <strong>{{ markets.length || '24+' }}</strong>
              <span>Live Markets Loaded</span>
            </div>
            <div class="proof-stat">
              <strong>1,024</strong>
              <span>AI perspectives per run</span>
            </div>
            <div class="proof-stat">
              <strong>24/7</strong>
              <span>Simulation availability</span>
            </div>
            <div class="proof-stat">
              <strong>1</strong>
              <span>clear thesis at the end</span>
            </div>
          </div>

          <div class="proof-quote">
            <blockquote>
              “The best consumer product here is not another dashboard. It is a faster way to understand what the
              market believes, what it is ignoring, and where conviction actually belongs.”
            </blockquote>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="footer-inner">
        <div>
          <div class="footer-brand">PolyFish</div>
          <div class="footer-copy">Built from MiroFish as the core inspiration, then adapted into a Polymarket-native workflow.</div>
        </div>
        <div class="footer-links">
          <a href="#integrations">Why It Works</a>
          <a href="#launch">Start Simulation</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, defineAsyncComponent, nextTick, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getActiveMarkets, lookupMarket } from '../api/markets'
import { setPendingUpload } from '../store/pendingUpload'

const ReactPaperBackground = defineAsyncComponent(() => import('../components/ReactPaperBackground.vue'))

const router = useRouter()
const launchSection = ref(null)
const wizardCard = ref(null)

const markets = ref([])
const selectedMarket = ref(null)
const simulationRequirement = ref('')
const loadingMarkets = ref(false)
const marketError = ref('')
const marketSearch = ref('')
const marketCategory = ref('all')
const marketSort = ref('closingSoon')
const visibleMarketCount = ref(100)
const directLookup = ref('')
const lookupLoading = ref(false)
const lookupError = ref('')
const lookupSuccess = ref(null)
const currentWizardStep = ref(1)

const categoryLabelMap = {
  all: 'All',
  politics: 'Politics',
  crypto: 'Crypto',
  sports: 'Sports',
  business: 'Business',
  world: 'World',
  culture: 'Culture',
  other: 'Other'
}

const simulationTemplates = [
  {
    label: 'Consensus check',
    prompt: 'Explain the strongest case on each side, identify what current market pricing assumes, and highlight the one variable most likely to break consensus.'
  },
  {
    label: 'Timing edge',
    prompt: 'Map the most important catalysts over the next two weeks, estimate how each could move sentiment, and identify where timing matters more than conviction.'
  },
  {
    label: 'Risk audit',
    prompt: 'Stress-test the dominant market narrative, surface the biggest blind spots, and explain what would make this market move sharply against the crowd.'
  }
]

const swarmNodes = [
  { id: 'n1', left: '12%', top: '18%', size: '16px', tone: 'cyan', delay: '0s' },
  { id: 'n2', left: '19%', top: '34%', size: '12px', tone: 'cyan', delay: '0.4s' },
  { id: 'n3', left: '14%', top: '55%', size: '10px', tone: 'violet', delay: '0.8s' },
  { id: 'n4', left: '23%', top: '68%', size: '14px', tone: 'white', delay: '1.2s' },
  { id: 'n5', left: '33%', top: '22%', size: '11px', tone: 'violet', delay: '0.2s' },
  { id: 'n6', left: '39%', top: '41%', size: '15px', tone: 'cyan', delay: '1s' },
  { id: 'n7', left: '31%', top: '61%', size: '9px', tone: 'white', delay: '1.4s' },
  { id: 'n8', left: '45%', top: '16%', size: '13px', tone: 'white', delay: '0.6s' },
  { id: 'n9', left: '50%', top: '31%', size: '10px', tone: 'violet', delay: '1.1s' },
  { id: 'n10', left: '47%', top: '56%', size: '14px', tone: 'cyan', delay: '0.9s' },
  { id: 'n11', left: '56%', top: '71%', size: '11px', tone: 'white', delay: '1.5s' },
  { id: 'n12', left: '62%', top: '42%', size: '12px', tone: 'cyan', delay: '0.5s' }
]

const swarmTrails = [
  { id: 't1', left: '24%', top: '23%', width: '170px', transform: 'rotate(12deg)', delay: '0s' },
  { id: 't2', left: '22%', top: '48%', width: '200px', transform: 'rotate(-5deg)', delay: '0.5s' },
  { id: 't3', left: '35%', top: '65%', width: '160px', transform: 'rotate(-18deg)', delay: '1s' },
  { id: 't4', left: '49%', top: '28%', width: '170px', transform: 'rotate(18deg)', delay: '0.7s' },
  { id: 't5', left: '54%', top: '55%', width: '180px', transform: 'rotate(-10deg)', delay: '1.2s' }
]

const marketCategories = computed(() => {
  const counts = new Map()

  for (const market of markets.value) {
    const category = getMarketCategory(market)
    counts.set(category, (counts.get(category) || 0) + 1)
  }

  const order = ['politics', 'crypto', 'sports', 'business', 'world', 'culture', 'other']

  return [
    { id: 'all', label: 'All', count: markets.value.length },
    ...order
      .filter((category) => counts.get(category))
      .map((category) => ({
        id: category,
        label: getCategoryLabel(category),
        count: counts.get(category)
      }))
  ]
})

const filteredMarkets = computed(() => {
  const term = marketSearch.value.trim().toLowerCase()

  const filtered = markets.value.filter((market) => {
    const categoryMatch = marketCategory.value === 'all' || getMarketCategory(market) === marketCategory.value
    if (!categoryMatch) return false

    if (!term) return true

    const haystack = [market.question, market.description, market.slug]
      .filter(Boolean)
      .join(' ')
      .toLowerCase()

    return haystack.includes(term)
  })

  return filtered.sort((a, b) => sortMarkets(a, b, marketSort.value))
})

const displayedMarkets = computed(() => filteredMarkets.value.slice(0, visibleMarketCount.value))

const hasActiveMarketFilters = computed(() => {
  return Boolean(marketSearch.value.trim()) || marketCategory.value !== 'all' || marketSort.value !== 'closingSoon'
})

const canSubmit = computed(() => {
  return Boolean(selectedMarket.value?.slug && simulationRequirement.value.trim())
})

const simulationCtaLabel = computed(() => {
  if (!selectedMarket.value?.slug) return 'Select a market first'
  if (!simulationRequirement.value.trim()) return 'Add your simulation brief'
  return 'Start Simulation'
})

const canOpenWizardStep = (step) => {
  if (step <= 1) return true
  if (step === 2) return Boolean(selectedMarket.value)
  return Boolean(selectedMarket.value && simulationRequirement.value.trim())
}

const goToWizardStep = (step) => {
  if (!canOpenWizardStep(step)) return
  currentWizardStep.value = step

  nextTick(() => {
    wizardCard.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

const fetchMarkets = async () => {
  loadingMarkets.value = true
  marketError.value = ''

  try {
    const pageSize = 120
    const maxPages = 3
    const mergedMarkets = []
    const seenSlugs = new Set()

    for (let page = 0; page < maxPages; page += 1) {
      const res = await getActiveMarkets({ limit: pageSize, offset: page * pageSize })
      const pageMarkets = res.data?.markets || []

      for (const market of pageMarkets) {
        const key = market.slug || market.id
        if (!key || seenSlugs.has(key)) continue
        seenSlugs.add(key)
        mergedMarkets.push(market)
      }

      if (pageMarkets.length < pageSize) break
    }

    markets.value = mergedMarkets
    if (!selectedMarket.value && markets.value.length > 0) {
      selectedMarket.value = markets.value[0]
    }
  } catch (error) {
    marketError.value = error.message || 'Failed to load active markets.'
  } finally {
    loadingMarkets.value = false
  }
}

const refreshMarkets = async () => {
  await fetchMarkets()
}

const clearMarketFilters = () => {
  marketSearch.value = ''
  marketCategory.value = 'all'
  marketSort.value = 'closingSoon'
  visibleMarketCount.value = 100
}

const showMoreMarkets = () => {
  visibleMarketCount.value += 50
}

const parseMarketReference = (value) => {
  const raw = (value || '').trim()
  if (!raw) return {}

  try {
    if (raw.startsWith('http://') || raw.startsWith('https://')) {
      const url = new URL(raw)
      const parts = url.pathname.split('/').filter(Boolean)
      const eventIndex = parts.findIndex((part) => part === 'event')
      const marketIndex = parts.findIndex((part) => part === 'market')
      const lastPart = parts[parts.length - 1]

      if (eventIndex !== -1 && parts[eventIndex + 1]) {
        return { slug: parts[eventIndex + 1] }
      }

      if (marketIndex !== -1 && parts[marketIndex + 1]) {
        return { slug: parts[marketIndex + 1] }
      }

      if (url.searchParams.get('slug')) {
        return { slug: url.searchParams.get('slug') }
      }

      if (url.searchParams.get('id')) {
        return { id: url.searchParams.get('id') }
      }

      if (lastPart) {
        return { slug: lastPart }
      }
    }
  } catch {
    // Fall through to plain slug/id parsing.
  }

  if (/^\d+$/.test(raw)) {
    return { id: raw }
  }

  return { slug: raw.replace(/^\/+|\/+$/g, '') }
}

const upsertMarket = (market) => {
  const key = market.slug || market.id
  const nextMarkets = [...markets.value]
  const existingIndex = nextMarkets.findIndex((item) => (item.slug || item.id) === key)

  if (existingIndex === -1) {
    nextMarkets.unshift(market)
  } else {
    nextMarkets.splice(existingIndex, 1)
    nextMarkets.unshift(market)
  }

  markets.value = nextMarkets
}

const selectMarket = (market, { fromLookup = false } = {}) => {
  selectedMarket.value = market

  if (!fromLookup) {
    lookupSuccess.value = null
  }
}

const lookupSpecificMarket = async () => {
  const reference = parseMarketReference(directLookup.value)
  if (!reference.slug && !reference.id) {
    lookupError.value = 'Enter a valid Polymarket URL, slug, or market id.'
    lookupSuccess.value = null
    return
  }

  lookupLoading.value = true
  lookupError.value = ''
  lookupSuccess.value = null

  try {
    const res = await lookupMarket(reference)
    const market = res.data?.market

    if (!market?.question) {
      throw new Error('Market not found.')
    }

    upsertMarket(market)
    selectMarket(market, { fromLookup: true })
    lookupSuccess.value = market
    marketSearch.value = ''
    marketCategory.value = 'all'
    visibleMarketCount.value = Math.max(visibleMarketCount.value, 100)
  } catch (error) {
    lookupError.value = error.message || 'Could not find that Polymarket market.'
  } finally {
    lookupLoading.value = false
  }
}

const scrollToLaunch = () => {
  launchSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const scrollToIntegrations = () => {
  document.getElementById('integrations')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const startSimulation = () => {
  if (!canSubmit.value) return

  setPendingUpload(selectedMarket.value, simulationRequirement.value)
  router.push({
    name: 'Process',
    params: { projectId: 'new' }
  })
}

const formatCompactNumber = (value) => {
  const numeric = Number(value || 0)
  if (!Number.isFinite(numeric)) return '0'
  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 1
  }).format(numeric)
}

const formatPercent = (value) => {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return '--'
  return `${Math.round(Number(value) * 100)}%`
}

const getCategoryLabel = (category) => {
  return categoryLabelMap[category] || 'Other'
}

const formatDate = (value) => {
  if (!value) return 'No end date'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getBinaryProbability = (market) => {
  if (!market?.outcomes?.length) return null

  const yesOutcome = market.outcomes.find((outcome) => outcome.name?.toLowerCase() === 'yes')
  if (yesOutcome && Number.isFinite(Number(yesOutcome.price))) {
    return Number(yesOutcome.price)
  }

  if (market.outcomes.length === 2 && Number.isFinite(Number(market.outcomes[0]?.price))) {
    return Number(market.outcomes[0].price)
  }

  return null
}

const getMarketCategory = (market) => {
  const haystack = [market?.question, market?.description, market?.slug]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()

  if (/(election|president|senate|house|vote|trump|biden|democrat|republican|government|congress|policy)/.test(haystack)) {
    return 'politics'
  }

  if (/(bitcoin|btc|ethereum|eth|solana|crypto|token|coin|airdrop|defi|nft)/.test(haystack)) {
    return 'crypto'
  }

  if (/(nba|nfl|mlb|nhl|soccer|football|fifa|ufc|tennis|golf|playoff|final|championship|world cup)/.test(haystack)) {
    return 'sports'
  }

  if (/(fed|inflation|gdp|stocks|stock|nasdaq|s&p|sp500|earnings|tariff|recession|oil|gold)/.test(haystack)) {
    return 'business'
  }

  if (/(war|china|russia|ukraine|israel|gaza|nato|europe|india|taiwan|global|world)/.test(haystack)) {
    return 'world'
  }

  if (/(movie|music|album|award|celebrity|tv|show|streaming|box office|festival)/.test(haystack)) {
    return 'culture'
  }

  return 'other'
}

const getMarketEndTimestamp = (market) => {
  const timestamp = new Date(market?.end_date || '').getTime()
  return Number.isNaN(timestamp) ? Number.POSITIVE_INFINITY : timestamp
}

const sortMarkets = (left, right, mode) => {
  if (mode === 'highestVolume') {
    return Number(right?.volume || 0) - Number(left?.volume || 0)
  }

  if (mode === 'mostContested') {
    const leftDistance = Math.abs((getBinaryProbability(left) ?? 0.5) - 0.5)
    const rightDistance = Math.abs((getBinaryProbability(right) ?? 0.5) - 0.5)
    return leftDistance - rightDistance
  }

  return getMarketEndTimestamp(left) - getMarketEndTimestamp(right)
}

const getOutcomeFillStyle = (price) => {
  const width = Math.max(4, Math.min(100, Number(price || 0) * 100))
  return { width: `${width}%` }
}

const applySimulationTemplate = (prompt) => {
  simulationRequirement.value = prompt
}

watch([marketSearch, marketCategory, marketSort], () => {
  visibleMarketCount.value = 100
})

watch(directLookup, () => {
  lookupError.value = ''
  lookupSuccess.value = null
})

watch(filteredMarkets, (nextMarkets) => {
  if (!nextMarkets.length) return

  if (!selectedMarket.value || !nextMarkets.some((market) => market.slug === selectedMarket.value.slug)) {
    selectMarket(nextMarkets[0])
  }
})

watch(selectedMarket, (nextMarket) => {
  if (!nextMarket && currentWizardStep.value > 1) {
    currentWizardStep.value = 1
    return
  }

  if (nextMarket && currentWizardStep.value === 1 && !simulationRequirement.value.trim()) {
    return
  }
})

watch(simulationRequirement, (nextRequirement) => {
  if (!nextRequirement.trim() && currentWizardStep.value === 3) {
    currentWizardStep.value = 2
  }
})

const truncateText = (text, maxLength) => {
  if (!text) return 'No description available.'
  return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text
}

onMounted(() => {
  fetchMarkets()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

.obsidian-page {
  --primary: #dbfcff;
  --secondary: #dcb8ff;
  --outline-variant: #3b494b;
  --surface-container-highest: #333539;
  --background: #111318;
  --surface: #111318;
  --surface-container-lowest: #0c0e12;
  --surface-container-low: #1a1c20;
  --surface-container: #1e2024;
  --surface-container-high: #282a2e;
  --surface-bright: #37393e;
  --surface-dim: #111318;
  --surface-tint: #00dbe9;
  --outline: #849495;
  --on-surface-variant: #b9cacb;
  --on-surface: #e2e2e8;
  --primary-container: #00f0ff;
  --primary-fixed-dim: #00dbe9;
  --secondary-container: #7701d0;
  --on-primary: #00363a;
  --radius-control: 12px;
  --radius-surface: 16px;
  --radius-pill: 999px;
  min-height: 100vh;
  position: relative;
  isolation: isolate;
  background:
    radial-gradient(circle at top right, rgba(0, 240, 255, 0.08), transparent 28%),
    radial-gradient(circle at 18% 26%, rgba(119, 1, 208, 0.1), transparent 24%),
    radial-gradient(circle at 50% 72%, rgba(51, 53, 57, 0.9), transparent 34%),
    linear-gradient(180deg, #15171c 0%, #111318 32%, #111318 100%);
  color: var(--on-surface);
  font-family: 'Montech', sans-serif;
}

.obsidian-page::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background:
    radial-gradient(circle at 70% 18%, rgba(0, 240, 255, 0.05), transparent 20%),
    radial-gradient(circle at 24% 78%, rgba(220, 184, 255, 0.05), transparent 18%);
}

.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 450, 'GRAD' 0, 'opsz' 24;
}

.topbar {
  position: fixed;
  inset: 0 0 auto 0;
  z-index: 50;
  backdrop-filter: blur(26px);
  background: linear-gradient(180deg, rgba(17, 19, 24, 0.92), rgba(17, 19, 24, 0.66));
  box-shadow:
    inset 0 -1px 0 rgba(59, 73, 75, 0.12),
    0 18px 48px rgba(0, 0, 0, 0.22);
}

.page-main,
.footer {
  position: relative;
  z-index: 1;
}

.topbar-inner,
.footer-inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 18px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  object-fit: cover;
  box-shadow:
    0 10px 22px rgba(0, 0, 0, 0.24),
    inset 0 0 0 1px rgba(255, 255, 255, 0.04);
}

.brand-wordmark,
.footer-brand {
  font-family: '403 Technul Soft', 'Montech', sans-serif;
  font-size: 1.55rem;
  font-weight: 400;
  letter-spacing: 0.01em;
  color: var(--primary-container);
}

.topbar-links,
.topbar-actions,
.footer-links {
  display: flex;
  align-items: center;
  gap: 18px;
}

.topbar-links a,
.footer-links a {
  color: #a1a1aa;
  text-decoration: none;
  transition: color 0.2s ease;
}

.topbar-links a:hover,
.footer-links a:hover {
  color: white;
}

.primary-button,
.ghost-button {
  border-radius: var(--radius-control);
  font-family: 'Montech', sans-serif;
  font-weight: 700;
  border: 1px solid transparent;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    filter 0.2s ease,
    background 0.2s ease,
    color 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.primary-button {
  background: linear-gradient(180deg, #00f0ff 0%, #00dbe9 100%);
  color: var(--on-primary);
  padding: 12px 22px;
  box-shadow:
    0 0 26px rgba(0, 219, 233, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.ghost-button {
  background: rgba(26, 28, 32, 0.4);
  color: var(--primary);
  padding: 12px 20px;
  border-color: rgba(59, 73, 75, 0.18);
  box-shadow: inset 0 0 0 1px rgba(219, 252, 255, 0.02);
  text-decoration: none;
}

.primary-button.large,
.ghost-button.large {
  padding: 16px 28px;
  font-size: 1rem;
}

.ghost-button.compact {
  padding: 10px 16px;
}

.primary-button:hover,
.ghost-button:hover {
  filter: brightness(1.08);
}

.primary-button:hover {
  box-shadow:
    0 0 30px rgba(0, 219, 233, 0.24),
    0 0 0 1px rgba(220, 184, 255, 0.16),
    inset 0 1px 0 rgba(255, 255, 255, 0.22);
}

.ghost-button:hover {
  border-color: rgba(0, 240, 255, 0.24);
  box-shadow: inset 0 0 0 1px rgba(0, 240, 255, 0.08);
}

.primary-button:disabled,
.ghost-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
  filter: none;
}

.primary-button:active,
.ghost-button:active {
  transform: scale(0.98);
}

.page-main {
  position: relative;
  padding-top: 96px;
  overflow-x: hidden;
}

.content-section {
  position: relative;
  z-index: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: 96px 32px;
}

.hero-section {
  position: relative;
  z-index: 1;
  width: 100%;
  min-height: 760px;
  display: flex;
  align-items: center;
  overflow: visible;
  padding: 96px 0;
}

.hero-media-layer {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.hero-media-frame {
  position: absolute;
  top: 0;
  left: 50%;
  width: 100vw;
  height: min(1200px, 130vh);
  transform: translateX(-50%);
  overflow: hidden;
}

.hero-background-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  opacity: 0.18;
  filter: saturate(0.82) blur(0.8px);
  transform: scale(1.04);
  -webkit-mask-image:
    linear-gradient(90deg, transparent 0%, rgba(0, 0, 0, 0.92) 14%, #000 26%, #000 74%, rgba(0, 0, 0, 0.92) 86%, transparent 100%),
    linear-gradient(180deg, #000 0%, #000 40%, rgba(0, 0, 0, 0.9) 56%, rgba(0, 0, 0, 0.52) 72%, rgba(0, 0, 0, 0.16) 84%, transparent 100%);
  -webkit-mask-composite: source-in;
  mask-image:
    linear-gradient(90deg, transparent 0%, rgba(0, 0, 0, 0.92) 14%, #000 26%, #000 74%, rgba(0, 0, 0, 0.92) 86%, transparent 100%),
    linear-gradient(180deg, #000 0%, #000 40%, rgba(0, 0, 0, 0.9) 56%, rgba(0, 0, 0, 0.52) 72%, rgba(0, 0, 0, 0.16) 84%, transparent 100%);
  mask-composite: intersect;
}

.hero-media-layer::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(17, 19, 24, 0.98) 0%, rgba(17, 19, 24, 0.82) 14%, rgba(17, 19, 24, 0.34) 30%, rgba(17, 19, 24, 0.34) 70%, rgba(17, 19, 24, 0.82) 86%, rgba(17, 19, 24, 0.98) 100%),
    linear-gradient(180deg, rgba(17, 19, 24, 0.58) 0%, rgba(17, 19, 24, 0.44) 22%, rgba(17, 19, 24, 0.48) 42%, rgba(17, 19, 24, 0.66) 58%, rgba(17, 19, 24, 0.84) 72%, rgba(17, 19, 24, 0.96) 84%, rgba(17, 19, 24, 1) 100%),
    radial-gradient(circle at 20% 20%, rgba(0, 240, 255, 0.08), transparent 32%);
}

.hero-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 48px;
  align-items: center;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
}

.integration-layout,
.launch-layout,
.proof-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: 48px;
  align-items: center;
}

.hero-copy h1,
.section-head h2,
.section-title-centered,
.integration-copy h2 {
  font-family: 'Montech', sans-serif;
  font-weight: 700;
  letter-spacing: -0.05em;
  color: white;
}

.hero-copy {
  width: 100%;
  max-width: 100%;
}

.hero-brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
  padding: 10px 16px 10px 10px;
  border-radius: 999px;
  background: rgba(17, 19, 24, 0.68);
  box-shadow:
    inset 0 0 0 1px rgba(0, 240, 255, 0.1),
    0 14px 32px rgba(0, 0, 0, 0.18);
}

.hero-brand-logo {
  width: 54px;
  height: 54px;
  border-radius: 18px;
  object-fit: cover;
  box-shadow:
    0 12px 28px rgba(0, 0, 0, 0.28),
    inset 0 0 0 1px rgba(255, 255, 255, 0.04);
}

.hero-brand-copy {
  display: grid;
  gap: 2px;
}

.hero-brand-copy strong {
  font-family: '403 Technul Soft', 'Montech', sans-serif;
  font-size: 0.92rem;
  font-weight: 400;
  letter-spacing: 0.04em;
  color: white;
}

.hero-brand-copy span {
  color: var(--on-surface-variant);
  font-size: 0.84rem;
}

.hero-copy h1 {
  font-size: clamp(2.1rem, 3.8vw, 3.6rem);
  line-height: 1.08;
  margin: 0 0 18px;
}

.hero-copy h1 span {
  color: var(--primary-container);
}

.hero-copy p,
.section-head p,
.integration-copy p,
.feature-card p,
.stack-card p,
.proof-quote blockquote,
.proof-attribution span,
.launch-panel-head p,
.state-box,
.market-copy p {
  color: var(--on-surface-variant);
  line-height: 1.7;
}

.hero-copy p {
  font-size: 1rem;
  max-width: 72ch;
  margin: 0 0 28px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.glass-card {
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(51, 53, 57, 0.48), rgba(30, 32, 36, 0.78)),
    rgba(51, 53, 57, 0.4);
  backdrop-filter: blur(28px);
  border: 1px solid rgba(59, 73, 75, 0.14);
  border-radius: var(--radius-surface);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.03),
    inset 0 0 0 1px rgba(0, 240, 255, 0.04);
}

.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(circle at top right, rgba(0, 240, 255, 0.08), transparent 34%);
}

.section-head,
.launch-head {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 24px;
  margin-bottom: 56px;
}

.launch-section-priority {
  padding-top: 24px;
}

.launch-section-priority .launch-head {
  margin-bottom: 32px;
}

.section-head h2,
.integration-copy h2 {
  font-size: 3rem;
  margin: 0;
}

.section-head p,
.integration-copy p {
  max-width: 520px;
  margin: 0;
}

.eyebrow,
.browser-label {
  font-family: 'Montech', sans-serif;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.28em;
  color: var(--primary-container);
  margin-bottom: 14px;
}

.feature-grid {
  display: grid;
  gap: 24px;
}

.three-up {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.four-up {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.feature-card,
.stack-card {
  padding: 32px;
}

.feature-card-accent {
  background:
    radial-gradient(circle at top, rgba(0, 240, 255, 0.12), transparent 38%),
    linear-gradient(180deg, rgba(51, 53, 57, 0.48), rgba(30, 32, 36, 0.78));
}

.feature-card .material-symbols-outlined,
.stack-card .material-symbols-outlined {
  font-size: 2rem;
  color: var(--primary-container);
  margin-bottom: 22px;
}

.feature-card h3,
.stack-card h3,
.browser-head h3,
.launch-panel-head h3 {
  font-family: 'Montech', sans-serif;
  color: white;
  font-size: 1.4rem;
  margin: 0 0 14px;
}

.integration-chart,
.market-browser,
.launch-panel {
  padding: 28px;
}

.integration-header,
.browser-head {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 16px;
  margin-bottom: 24px;
}

.browser-head-tight {
  align-items: end;
  gap: 24px;
}

.wizard-card {
  padding: 0;
}

.wizard-steps {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(59, 73, 75, 0.12);
  background: rgba(12, 14, 18, 0.22);
}

.wizard-step {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  padding: 14px 16px;
  border: 1px solid rgba(59, 73, 75, 0.14);
  border-radius: var(--radius-surface);
  background: rgba(17, 19, 24, 0.52);
  color: var(--on-surface);
  text-align: left;
  cursor: pointer;
  transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease;
}

.wizard-step:hover {
  border-color: rgba(0, 240, 255, 0.18);
  transform: translateY(-1px);
}

.wizard-step.active {
  border-color: rgba(0, 240, 255, 0.3);
  background: rgba(0, 240, 255, 0.08);
}

.wizard-step.complete .wizard-step-index {
  background: rgba(0, 240, 255, 0.18);
  color: var(--primary);
}

.wizard-step-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: var(--radius-pill);
  background: rgba(26, 28, 32, 0.9);
  box-shadow: inset 0 0 0 1px rgba(59, 73, 75, 0.18);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.84rem;
}

.wizard-step-copy strong,
.review-card h4,
.wizard-footer-summary strong {
  display: block;
  font-family: 'Montech', sans-serif;
  color: white;
}

.wizard-step-copy em,
.wizard-footer-summary em,
.review-card p {
  display: block;
  margin-top: 4px;
  color: var(--on-surface-variant);
  font-style: normal;
  line-height: 1.5;
}

.wizard-panel {
  display: grid;
  gap: 20px;
  padding: 24px;
}

.wizard-panel-head {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: end;
}

.wizard-panel-head h3 {
  margin: 0 0 10px;
  font-family: 'Montech', sans-serif;
  font-size: 1.6rem;
  color: white;
}

.wizard-panel-head p {
  color: var(--on-surface-variant);
  max-width: 72ch;
  line-height: 1.6;
}

.browser-head-copy {
  max-width: 640px;
}

.browser-head-copy p {
  color: var(--on-surface-variant);
  font-size: 0.95rem;
  line-height: 1.6;
}

.browser-head-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.browser-stat {
  min-width: 84px;
  padding: 10px 12px;
  border-radius: var(--radius-control);
  background: rgba(17, 19, 24, 0.62);
  box-shadow: inset 0 0 0 1px rgba(59, 73, 75, 0.12);
}

.browser-stat strong,
.selected-market-stat strong {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  color: white;
  line-height: 1.1;
}

.browser-stat span,
.selected-market-stat span {
  display: block;
  margin-top: 4px;
  color: var(--on-surface-variant);
  font-size: 0.74rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.market-control-bar {
  display: grid;
  grid-template-columns: minmax(280px, 1.1fr) 150px minmax(260px, 1fr) 180px;
  gap: 14px;
  margin-bottom: 18px;
}

.market-search,
.market-sort {
  display: grid;
  gap: 8px;
}

.market-search {
  position: relative;
}

.market-search-direct input {
  padding-right: 18px;
}

.market-search .material-symbols-outlined {
  position: absolute;
  top: 50%;
  left: 14px;
  transform: translateY(-50%);
  font-size: 1.05rem;
  color: var(--on-surface-variant);
}

.market-search input,
.market-sort select {
  width: 100%;
  min-height: 48px;
  border-radius: var(--radius-control);
  border: 1px solid transparent;
  background:
    linear-gradient(180deg, rgba(12, 14, 18, 0.98), rgba(26, 28, 32, 0.96)),
    rgba(17, 19, 24, 0.92);
  color: var(--on-surface);
  padding: 0 14px;
  box-shadow:
    inset 0 0 0 1px rgba(59, 73, 75, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.02);
  outline: none;
}

.market-search input {
  padding-left: 44px;
}

.market-search input:focus,
.market-sort select:focus {
  border-color: rgba(219, 252, 255, 0.18);
  box-shadow:
    inset 0 0 0 1px rgba(0, 240, 255, 0.2),
    inset 0 0 18px rgba(0, 240, 255, 0.08),
    0 0 0 1px rgba(0, 240, 255, 0.06);
}

.market-sort span {
  font-family: 'Montech', sans-serif;
  font-size: 0.76rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--on-surface-variant);
}

.market-sort-compact {
  min-width: 0;
}

.compact-primary {
  min-height: 48px;
  padding: 0 18px;
}

.market-filter-chips,
.prompt-preset-list,
.launch-market-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.market-filter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  margin-bottom: 18px;
}

.market-filter-chips {
  margin: 0;
}

.filter-chip,
.filter-reset,
.launch-meta-chip,
.prompt-preset {
  border: 1px solid rgba(59, 73, 75, 0.14);
  background: rgba(26, 28, 32, 0.62);
  color: var(--on-surface);
  border-radius: var(--radius-pill);
  padding: 10px 14px;
  font: inherit;
  cursor: pointer;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02);
  transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease;
}

.filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.filter-chip em {
  font-style: normal;
  font-family: 'JetBrains Mono', monospace;
  color: var(--on-surface-variant);
  opacity: 0.9;
}

.filter-chip.active,
.prompt-preset:hover,
.filter-reset:hover {
  border-color: rgba(0, 240, 255, 0.22);
  background: rgba(0, 240, 255, 0.08);
}

.filter-chip.active {
  color: var(--primary);
}

.market-results-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--on-surface-variant);
  font-size: 0.84rem;
  white-space: nowrap;
}

.lookup-error {
  margin-bottom: 14px;
}

.lookup-success {
  display: grid;
  gap: 6px;
  margin-bottom: 14px;
  padding: 16px 18px;
  border: 1px solid rgba(0, 240, 255, 0.18);
  border-radius: var(--radius-control);
  background: linear-gradient(180deg, rgba(0, 240, 255, 0.08), rgba(0, 240, 255, 0.03));
}

.lookup-success strong,
.lookup-success b,
.lookup-success em,
.lookup-success small {
  font-style: normal;
}

.lookup-success strong,
.lookup-success b {
  color: white;
}

.lookup-success span {
  display: grid;
  gap: 3px;
}

.lookup-success em,
.lookup-success small {
  color: var(--on-surface-variant);
}

.market-table-shell {
  max-height: 980px;
  overflow: auto;
  border-radius: var(--radius-surface);
  background:
    linear-gradient(180deg, rgba(12, 14, 18, 0.9), rgba(17, 19, 24, 0.82)),
    rgba(17, 19, 24, 0.76);
  box-shadow:
    inset 0 0 0 1px rgba(59, 73, 75, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.02);
}

.market-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1120px;
}

.market-table thead th {
  position: sticky;
  top: 0;
  z-index: 2;
  padding: 14px 16px;
  text-align: left;
  font-family: 'Montech', sans-serif;
  font-size: 0.76rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--on-surface-variant);
  background: rgba(17, 19, 24, 0.94);
  backdrop-filter: blur(18px);
  box-shadow: inset 0 -1px 0 rgba(59, 73, 75, 0.12);
}

.market-table tbody td {
  padding: 14px 16px;
  vertical-align: middle;
  border-top: 1px solid rgba(59, 73, 75, 0.1);
  color: var(--on-surface);
}

.market-table-row {
  cursor: pointer;
  transition: background 0.18s ease, box-shadow 0.18s ease;
}

.market-table-row:hover {
  background: rgba(255, 255, 255, 0.02);
}

.market-table-row.selected {
  background:
    linear-gradient(90deg, rgba(0, 240, 255, 0.1), transparent 18%),
    rgba(255, 255, 255, 0.02);
  box-shadow: inset 3px 0 0 rgba(0, 240, 255, 0.68);
}

.market-table-row:focus-visible {
  outline: none;
  background: rgba(0, 240, 255, 0.06);
}

.market-title-cell {
  min-width: 330px;
}

.market-title-main {
  font-family: 'Montech', sans-serif;
  font-size: 0.98rem;
  line-height: 1.45;
  color: white;
  margin-bottom: 4px;
}

.market-title-sub {
  color: var(--on-surface-variant);
  font-size: 0.78rem;
  line-height: 1.45;
  font-family: 'JetBrains Mono', monospace;
}

.market-event-cell {
  min-width: 240px;
}

.market-event-main {
  color: white;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 4px;
}

.market-event-sub {
  color: var(--on-surface-variant);
  font-size: 0.78rem;
  line-height: 1.45;
}

.market-cell-chip {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: var(--radius-pill);
  background: rgba(26, 28, 32, 0.86);
  color: var(--on-surface-variant);
  box-shadow: inset 0 0 0 1px rgba(59, 73, 75, 0.14);
}

.market-number-cell {
  font-family: 'JetBrains Mono', monospace;
  white-space: nowrap;
}

.metric-row,
.selected-outcome-row,
.market-row-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
  font-size: 0.88rem;
}

.metric-row strong,
.selected-outcome-row span:last-child,
.market-side strong,
.proof-stat strong {
  color: white;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: -0.02em;
}

.progress-track {
  width: 100%;
  height: 10px;
  border-radius: var(--radius-pill);
  background: linear-gradient(180deg, rgba(12, 14, 18, 0.92), rgba(30, 32, 36, 0.88));
  overflow: hidden;
  box-shadow: inset 0 0 0 1px rgba(59, 73, 75, 0.12);
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  box-shadow: 0 0 18px rgba(0, 240, 255, 0.14);
}

.fill-a { width: 88%; background: linear-gradient(90deg, var(--primary-container), var(--secondary)); }

.swarm-panel-head {
  display: grid;
  gap: 8px;
  margin-bottom: 22px;
}

.swarm-kicker {
  font-family: 'Montech', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.78rem;
  color: var(--on-surface-variant);
}

.swarm-panel-head strong {
  font-family: 'Montech', sans-serif;
  font-size: 1.45rem;
  line-height: 1.15;
  color: white;
}

.swarm-stage {
  position: relative;
  min-height: 430px;
  overflow: hidden;
  border-radius: calc(var(--radius-surface) - 6px);
  background:
    radial-gradient(circle at 22% 18%, rgba(0, 240, 255, 0.14), transparent 26%),
    radial-gradient(circle at 78% 30%, rgba(220, 184, 255, 0.1), transparent 24%),
    linear-gradient(180deg, rgba(12, 14, 18, 0.94), rgba(17, 19, 24, 0.9));
  box-shadow:
    inset 0 0 0 1px rgba(59, 73, 75, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.02);
}

.swarm-stage::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(100deg, transparent 0%, rgba(255, 255, 255, 0.06) 46%, transparent 54%);
  transform: translateX(-120%);
  animation: swarmSweep 8s linear infinite;
  pointer-events: none;
  will-change: transform, opacity;
}

.swarm-stage-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px);
  background-size: 36px 36px;
  opacity: 0.38;
}

.swarm-column-label {
  position: absolute;
  top: 18px;
  font-family: 'Montech', sans-serif;
  font-size: 0.66rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--on-surface-variant);
}

.swarm-column-label--signals {
  left: 22px;
}

.swarm-column-label--agents {
  left: 44%;
  transform: translateX(-50%);
}

.swarm-column-label--output {
  right: 26px;
}

.swarm-signal-stack {
  position: absolute;
  top: 56px;
  left: 22px;
  display: grid;
  gap: 12px;
  width: 140px;
}

.swarm-signal-card {
  position: relative;
  padding: 12px 14px;
  border-radius: 16px;
  background: rgba(17, 19, 24, 0.78);
  box-shadow:
    inset 0 0 0 1px rgba(59, 73, 75, 0.16),
    0 16px 32px rgba(0, 0, 0, 0.12);
  animation: swarmSignalPulse 5.6s ease-in-out infinite;
  will-change: transform, opacity;
}

.swarm-signal-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(90deg, transparent 0%, rgba(0, 240, 255, 0.16) 50%, transparent 100%);
  transform: translateX(-120%);
  animation: swarmSignalSweep 4.8s ease-in-out infinite;
  will-change: transform, opacity;
}

.swarm-signal-card:nth-child(2) {
  animation-delay: 0.8s;
}

.swarm-signal-card:nth-child(2)::after {
  animation-delay: 1.1s;
}

.swarm-signal-card:nth-child(3) {
  animation-delay: 1.6s;
}

.swarm-signal-card:nth-child(3)::after {
  animation-delay: 2s;
}

.swarm-signal-card span,
.swarm-output-label {
  display: block;
  font-size: 0.66rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--on-surface-variant);
}

.swarm-signal-card strong,
.swarm-output-card strong {
  display: block;
  margin-top: 6px;
  color: white;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem;
}

.swarm-node-field {
  position: absolute;
  inset: 56px 156px 70px 188px;
}

.swarm-node {
  position: absolute;
  border-radius: 999px;
  display: grid;
  place-items: center;
  animation: swarmFloat 5.2s ease-in-out infinite;
  will-change: transform, opacity;
}

.swarm-node-core {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.08), 0 0 24px currentColor;
  opacity: 0.92;
  animation: swarmNodeCorePulse 3.8s ease-in-out infinite;
  will-change: transform, opacity;
}

.swarm-node--cyan {
  color: #00f0ff;
}

.swarm-node--violet {
  color: #dcb8ff;
}

.swarm-node--white {
  color: #f2f6ff;
}

.swarm-trail {
  position: absolute;
  height: 1px;
  background: linear-gradient(90deg, rgba(0, 240, 255, 0), rgba(0, 240, 255, 0.78), rgba(220, 184, 255, 0.32), rgba(220, 184, 255, 0));
  transform-origin: left center;
  opacity: 0.42;
  animation: swarmPulse 3.8s ease-in-out infinite;
  will-change: opacity, transform;
}

.swarm-core {
  position: absolute;
  top: 50%;
  left: 63%;
  width: 124px;
  height: 124px;
  transform: translate(-50%, -50%);
  border-radius: 999px;
  display: grid;
  place-items: center;
}

.swarm-core-ring {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: 1px solid rgba(0, 240, 255, 0.22);
}

.swarm-core-ring--outer {
  box-shadow:
    0 0 38px rgba(0, 240, 255, 0.16),
    inset 0 0 32px rgba(0, 240, 255, 0.08);
  animation: swarmCoreOuter 7s linear infinite;
  will-change: transform;
}

.swarm-core-ring--inner {
  inset: 16px;
  border-color: rgba(220, 184, 255, 0.28);
  box-shadow: inset 0 0 22px rgba(220, 184, 255, 0.08);
  animation: swarmCoreInner 5s linear infinite reverse;
  will-change: transform;
}

.swarm-core-label {
  position: relative;
  z-index: 1;
  width: 92px;
  text-align: center;
  font-family: 'Montech', sans-serif;
  font-size: 0.74rem;
  line-height: 1.25;
  color: white;
  animation: swarmLabelPulse 2.8s ease-in-out infinite;
  will-change: opacity, transform;
}

.swarm-output-card {
  position: absolute;
  top: 88px;
  right: 22px;
  width: 176px;
  padding: 16px;
  border-radius: 18px;
  background:
    linear-gradient(180deg, rgba(20, 24, 29, 0.92), rgba(30, 32, 36, 0.88)),
    rgba(17, 19, 24, 0.82);
  box-shadow:
    inset 0 0 0 1px rgba(59, 73, 75, 0.16),
    0 22px 44px rgba(0, 0, 0, 0.16);
  animation: swarmOutputLift 5.4s ease-in-out infinite;
  will-change: transform, opacity;
}

.swarm-output-card p {
  margin: 10px 0 0;
  font-size: 0.82rem;
  line-height: 1.55;
  color: var(--on-surface-variant);
}

.swarm-output-lines {
  display: grid;
  gap: 7px;
  margin-top: 16px;
}

.swarm-output-lines span {
  display: block;
  height: 6px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(0, 240, 255, 0.6), rgba(220, 184, 255, 0.2));
  animation: swarmOutputLine 2.6s ease-in-out infinite;
  will-change: transform, opacity;
}

.swarm-output-lines span:nth-child(2) {
  width: 82%;
  animation-delay: 0.35s;
}

.swarm-output-lines span:nth-child(3) {
  width: 61%;
  animation-delay: 0.7s;
}

.swarm-caption-row {
  position: absolute;
  right: 24px;
  bottom: 18px;
  left: 24px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.swarm-caption-row span {
  padding-top: 10px;
  border-top: 1px solid rgba(59, 73, 75, 0.12);
  font-size: 0.72rem;
  color: var(--on-surface-variant);
}

.integration-list {
  list-style: none;
  padding: 0;
  margin: 28px 0 0;
  display: grid;
  gap: 16px;
}

.integration-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
}

.integration-list .material-symbols-outlined {
  color: var(--primary-container);
}

@keyframes swarmFloat {
  0%, 100% {
    transform: translate3d(0, 0, 0) scale(1);
  }
  50% {
    transform: translate3d(0, -11px, 0) scale(1.12);
  }
}

@keyframes swarmPulse {
  0%, 100% {
    opacity: 0.18;
    transform: scaleX(0.96);
  }
  50% {
    opacity: 0.72;
    transform: scaleX(1);
  }
}

@keyframes swarmNodeCorePulse {
  0%, 100% {
    opacity: 0.78;
    transform: scale(0.92);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes swarmCoreOuter {
  from {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(180deg) scale(1.04);
  }
  to {
    transform: rotate(360deg) scale(1);
  }
}

@keyframes swarmCoreInner {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes swarmSweep {
  0% {
    transform: translateX(-120%);
    opacity: 0;
  }
  12% {
    opacity: 0.22;
  }
  50% {
    opacity: 0.08;
  }
  100% {
    transform: translateX(120%);
    opacity: 0;
  }
}

@keyframes swarmSignalPulse {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.88;
  }
  50% {
    transform: translateY(-3px);
    opacity: 1;
  }
}

@keyframes swarmSignalSweep {
  0%, 100% {
    transform: translateX(-120%);
    opacity: 0;
  }
  30% {
    opacity: 0.55;
  }
  60% {
    opacity: 0.18;
  }
  100% {
    transform: translateX(120%);
    opacity: 0;
  }
}

@keyframes swarmLabelPulse {
  0%, 100% {
    opacity: 0.82;
    transform: scale(0.98);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes swarmOutputLift {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.94;
  }
  50% {
    transform: translateY(-4px);
    opacity: 1;
  }
}

@keyframes swarmOutputLine {
  0%, 100% {
    opacity: 0.45;
    transform: scaleX(0.94);
  }
  50% {
    opacity: 1;
    transform: scaleX(1);
  }
}

.section-title-centered {
  text-align: center;
  font-size: 3rem;
  margin: 0 0 48px;
}

.stack-card {
  background:
    linear-gradient(180deg, rgba(40, 42, 46, 0.74), rgba(30, 32, 36, 0.9)),
    rgba(30, 32, 36, 0.78);
  border-radius: var(--radius-surface);
  border: 1px solid rgba(59, 73, 75, 0.14);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02);
}

.launch-layout {
  grid-template-columns: minmax(0, 1.65fr) minmax(340px, 0.8fr);
  align-items: start;
}

.launch-panel {
  position: sticky;
  top: 108px;
}

.selected-outcomes {
  display: grid;
  gap: 14px;
  margin-bottom: 22px;
}

.selected-market-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.selected-market-stat {
  padding: 14px;
  border-radius: var(--radius-surface);
  background: rgba(17, 19, 24, 0.56);
  box-shadow: inset 0 0 0 1px rgba(59, 73, 75, 0.12);
}

.prompt-field {
  display: grid;
  gap: 10px;
}

.prompt-field span {
  font-family: 'Montech', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.74rem;
  color: var(--on-surface-variant);
}

.prompt-field textarea {
  width: 100%;
  min-height: 220px;
  resize: vertical;
  border-radius: var(--radius-surface);
  border: 1px solid transparent;
  background:
    linear-gradient(180deg, rgba(12, 14, 18, 0.98), rgba(26, 28, 32, 0.96)),
    rgba(17, 19, 24, 0.92);
  color: var(--on-surface);
  padding: 18px;
  font: inherit;
  line-height: 1.65;
  box-shadow:
    inset 0 0 0 1px rgba(59, 73, 75, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.02);
  outline: none;
}

.prompt-field textarea:focus {
  border-color: rgba(219, 252, 255, 0.18);
  box-shadow:
    inset 0 0 0 1px rgba(0, 240, 255, 0.2),
    inset 0 0 18px rgba(0, 240, 255, 0.08),
    0 0 0 1px rgba(0, 240, 255, 0.06);
}

.prompt-presets {
  display: grid;
  gap: 12px;
  margin-top: 18px;
}

.prompt-presets-head span {
  display: block;
  font-family: 'Montech', sans-serif;
  font-size: 0.78rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--on-surface-variant);
  margin-bottom: 4px;
}

.prompt-presets-head p {
  color: var(--on-surface-variant);
  font-size: 0.88rem;
}

.prompt-preset {
  border-radius: var(--radius-control);
  text-align: left;
}

.wizard-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding-top: 8px;
}

.wizard-footer-summary {
  min-width: 0;
  flex: 1 1 320px;
}

.wizard-footer-label,
.review-label {
  display: block;
  margin-bottom: 8px;
  color: var(--on-surface-variant);
  font-size: 0.76rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.review-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.review-card {
  padding: 20px;
  border-radius: var(--radius-surface);
  background: rgba(17, 19, 24, 0.56);
  box-shadow: inset 0 0 0 1px rgba(59, 73, 75, 0.12);
}

.review-stats-grid {
  margin-top: 16px;
  margin-bottom: 0;
}

.review-brief {
  margin: 0;
  white-space: pre-wrap;
  font: inherit;
  color: var(--on-surface);
  line-height: 1.7;
}

.market-list-actions {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

.proof-grid {
  gap: 56px;
}

.proof-stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 28px;
}

.proof-stat strong {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 3rem;
  color: var(--primary-container);
  margin-bottom: 6px;
}

.proof-stat span {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--on-surface-variant);
}

.proof-quote blockquote {
  font-size: 1.8rem;
  line-height: 1.5;
  margin: 0 0 28px;
  color: white;
}

.proof-attribution {
  display: flex;
  align-items: center;
  gap: 16px;
}

.proof-attribution strong {
  display: block;
  margin-bottom: 4px;
}

.avatar-shell {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-pill);
  overflow: hidden;
  background: rgba(51, 53, 57, 0.85);
  box-shadow: inset 0 0 0 1px rgba(59, 73, 75, 0.18);
}

.avatar-shell img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.footer {
  position: relative;
  z-index: 1;
  background: linear-gradient(180deg, rgba(17, 19, 24, 0), rgba(26, 28, 32, 0.78));
  box-shadow: inset 0 1px 0 rgba(59, 73, 75, 0.12);
  padding: 18px 0 40px;
  margin-top: 32px;
}

.footer-copy {
  margin-top: 6px;
  color: #a1a1aa;
  font-size: 0.9rem;
}

.state-box.error {
  color: #ffb4ab;
}

.state-box.success {
  color: var(--on-surface);
}

@media (max-width: 1100px) {
  .hero-grid,
  .integration-layout,
  .launch-layout,
  .proof-grid {
    grid-template-columns: 1fr;
  }

  .three-up,
  .four-up {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .section-head,
  .launch-head,
  .topbar-inner,
  .footer-inner {
    flex-direction: column;
    align-items: start;
  }

  .browser-head-tight,
  .wizard-panel-head,
  .market-filter-row {
    flex-direction: column;
    align-items: stretch;
  }

  .wizard-steps,
  .market-control-bar {
    grid-template-columns: 1fr;
  }

  .review-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .hero-section,
  .content-section,
  .topbar-inner,
  .footer-inner {
    padding-left: 18px;
    padding-right: 18px;
  }

  .topbar-links {
    display: none;
  }

  .brand-logo {
    width: 38px;
    height: 38px;
    border-radius: 12px;
  }

  .hero-brand-pill {
    width: 100%;
    max-width: 360px;
    padding-right: 14px;
  }

  .hero-brand-logo {
    width: 46px;
    height: 46px;
    border-radius: 15px;
  }

  .hero-copy h1,
  .section-head h2,
  .section-title-centered,
  .integration-copy h2 {
    font-size: 2.4rem;
  }

  .three-up,
  .four-up,
  .proof-stats {
    grid-template-columns: 1fr;
  }

  .market-results-meta {
    flex-direction: column;
    align-items: start;
    white-space: normal;
  }

  .selected-market-grid {
    grid-template-columns: 1fr;
  }

  .wizard-footer {
    align-items: stretch;
  }
}
</style>
