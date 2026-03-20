<template>
  <div class="report-panel">
    <div class="report-toolbar">
      <div>
        <p class="eyebrow">Report Agent</p>
        <h2 class="report-title">Final Thesis</h2>
      </div>

      <div class="toolbar-actions">
        <span class="status-badge" :class="statusTone">{{ statusLabel }}</span>
        <button class="ghost-btn" @click="refreshAll" :disabled="isRefreshing">
          {{ isRefreshing ? 'Refreshing...' : 'Refresh' }}
        </button>
        <button
          v-if="isComplete"
          class="primary-btn"
          @click="goToInteraction"
        >
          Open Interaction
        </button>
      </div>
    </div>

    <div class="report-grid">
      <section class="panel-card report-meta">
        <div class="meta-item">
          <span class="meta-label">Report ID</span>
          <span class="meta-value">{{ report?.report_id || props.reportId }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Simulation</span>
          <span class="meta-value">{{ report?.simulation_id || props.simulationId || 'Unknown' }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Created</span>
          <span class="meta-value">{{ formatDate(report?.created_at) }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Completed</span>
          <span class="meta-value">{{ formatDate(report?.completed_at) }}</span>
        </div>
      </section>

      <section class="panel-card outline-card">
        <div class="card-header">
          <h3>Outline</h3>
          <span class="card-count">{{ sections.length }} sections</span>
        </div>
        <p v-if="report?.outline?.summary" class="outline-summary">
          {{ report.outline.summary }}
        </p>
        <ul v-if="sections.length > 0" class="outline-list">
          <li v-for="(section, idx) in sections" :key="`${section.title}-${idx}`">
            <span class="section-index">{{ String(idx + 1).padStart(2, '0') }}</span>
            <span>{{ section.title }}</span>
          </li>
        </ul>
        <p v-else class="empty-copy">Outline is not available yet.</p>
      </section>
    </div>

    <section class="panel-card thesis-card">
      <div class="card-header">
        <h3>Written Thesis</h3>
        <span v-if="isComplete" class="card-count">Ready</span>
        <span v-else class="card-count">In progress</span>
      </div>

      <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>

      <div v-if="renderedReport" class="report-content markdown-body" v-html="renderedReport"></div>
      <div v-else class="empty-state">
        <div class="empty-state-title">Report content is not ready yet</div>
        <p class="empty-state-copy">
          The agent logs below are still useful while generation is running.
        </p>
      </div>
    </section>

    <div class="log-grid">
      <section class="panel-card log-card">
        <div class="card-header">
          <h3>Agent Timeline</h3>
          <span class="card-count">{{ agentLogs.length }} events</span>
        </div>

        <div v-if="agentLogs.length === 0" class="empty-copy">No structured agent events yet.</div>
        <div v-else class="timeline-list">
          <article
            v-for="(log, idx) in agentLogs"
            :key="`${log.timestamp || 'log'}-${idx}`"
            class="timeline-item"
          >
            <div class="timeline-dot"></div>
            <div class="timeline-body">
              <div class="timeline-row">
                <span class="timeline-action">{{ humanizeAction(log.action) }}</span>
                <span class="timeline-time">{{ formatTime(log.timestamp) }}</span>
              </div>
              <p v-if="log.section_title" class="timeline-section">{{ log.section_title }}</p>
              <p v-if="describeAgentLog(log)" class="timeline-detail">{{ describeAgentLog(log) }}</p>
            </div>
          </article>
        </div>
      </section>

      <section class="panel-card log-card">
        <div class="card-header">
          <h3>Console Log</h3>
          <span class="card-count">{{ consoleLogs.length }} lines</span>
        </div>

        <div v-if="consoleLogs.length === 0" class="empty-copy">No console output yet.</div>
        <pre v-else class="console-block">{{ consoleLogs.join('\n') }}</pre>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getAgentLog, getConsoleLog, getReport } from '../api/report'

const props = defineProps({
  reportId: String,
  simulationId: String,
  systemLogs: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['add-log', 'update-status'])

const router = useRouter()

const report = ref(null)
const agentLogs = ref([])
const consoleLogs = ref([])
const agentLogLine = ref(0)
const consoleLogLine = ref(0)
const errorMessage = ref('')
const isRefreshing = ref(false)
const pollingHandle = ref(null)

const sections = computed(() => report.value?.outline?.sections || [])
const isComplete = computed(() => report.value?.status === 'completed')
const statusLabel = computed(() => {
  if (report.value?.status) return report.value.status
  return errorMessage.value ? 'error' : 'loading'
})

const statusTone = computed(() => {
  if (errorMessage.value || report.value?.status === 'failed') return 'is-error'
  if (report.value?.status === 'completed') return 'is-complete'
  return 'is-processing'
})

const renderedReport = computed(() => renderMarkdown(report.value?.markdown_content || ''))

const addLog = (message) => {
  emit('add-log', message)
}

const emitStatus = (status) => {
  emit('update-status', status)
}

const formatDate = (value) => {
  if (!value) return 'Pending'

  try {
    return new Date(value).toLocaleString('en-US', {
      hour12: false,
      year: 'numeric',
      month: 'short',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return value
  }
}

const formatTime = (value) => {
  if (!value) return ''

  try {
    return new Date(value).toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch {
    return ''
  }
}

const humanizeAction = (action) => {
  if (!action) return 'Event'

  return action
    .replace(/_/g, ' ')
    .replace(/\b\w/g, char => char.toUpperCase())
}

const describeAgentLog = (log) => {
  if (!log?.details) return ''

  if (log.details.message) return log.details.message
  if (log.details.tool_name) return `Tool: ${log.details.tool_name}`
  if (log.details.error) return log.details.error
  if (log.details.response) return String(log.details.response).slice(0, 220)

  return ''
}

const escapeHtml = (content) => {
  return content
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

const renderMarkdown = (content) => {
  if (!content) return ''

  let html = escapeHtml(content.trim())

  html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre class="code-block"><code>$2</code></pre>')
  html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
  html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>')
  html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^# (.+)$/gm, '<h2>$1</h2>')
  html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
  html = html.replace(/^\s*[-*] (.+)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
  html = html.replace(/<\/li>\n<li>/g, '</li><li>')
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')
  html = html.replace(/\n{2,}/g, '</p><p>')
  html = html.replace(/\n/g, '<br>')
  html = `<p>${html}</p>`
  html = html.replace(/<p><h/g, '<h')
  html = html.replace(/<\/h([2-4])><\/p>/g, '</h$1>')
  html = html.replace(/<p><blockquote>/g, '<blockquote>')
  html = html.replace(/<\/blockquote><\/p>/g, '</blockquote>')
  html = html.replace(/<p><pre/g, '<pre')
  html = html.replace(/<\/pre><\/p>/g, '</pre>')
  html = html.replace(/<p><ul>/g, '<ul>')
  html = html.replace(/<\/ul><\/p>/g, '</ul>')

  return html
}

const fetchReport = async () => {
  if (!props.reportId) return

  try {
    const res = await getReport(props.reportId)
    if (res.success && res.data) {
      report.value = res.data
      errorMessage.value = res.data.error || ''

      if (res.data.status === 'failed') {
        emitStatus('error')
        addLog(`Report failed: ${errorMessage.value || 'Unknown error'}`)
      } else if (res.data.status === 'completed') {
        emitStatus('completed')
      } else {
        emitStatus('processing')
      }
    }
  } catch (error) {
    errorMessage.value = error.message || 'Failed to load report'
    emitStatus('error')
  }
}

const fetchAgentLogs = async () => {
  if (!props.reportId) return

  try {
    const res = await getAgentLog(props.reportId, agentLogLine.value)
    if (res.success && res.data) {
      const newLogs = res.data.logs || []
      if (newLogs.length > 0) {
        agentLogs.value = [...agentLogs.value, ...newLogs]
        agentLogLine.value = res.data.total_lines || agentLogLine.value + newLogs.length
      }
    }
  } catch (error) {
    errorMessage.value = error.message || 'Failed to load agent logs'
  }
}

const fetchConsoleLogs = async () => {
  if (!props.reportId) return

  try {
    const res = await getConsoleLog(props.reportId, consoleLogLine.value)
    if (res.success && res.data) {
      const newLogs = res.data.logs || []
      if (newLogs.length > 0) {
        consoleLogs.value = [...consoleLogs.value, ...newLogs]
        consoleLogLine.value = res.data.total_lines || consoleLogLine.value + newLogs.length
      }
    }
  } catch (error) {
    errorMessage.value = error.message || 'Failed to load console logs'
  }
}

const refreshAll = async () => {
  if (!props.reportId || isRefreshing.value) return

  isRefreshing.value = true
  try {
    await Promise.all([fetchReport(), fetchAgentLogs(), fetchConsoleLogs()])
  } finally {
    isRefreshing.value = false
  }
}

const stopPolling = () => {
  if (pollingHandle.value) {
    clearInterval(pollingHandle.value)
    pollingHandle.value = null
  }
}

const startPolling = () => {
  stopPolling()

  pollingHandle.value = setInterval(async () => {
    await refreshAll()
    if (isComplete.value || report.value?.status === 'failed') {
      stopPolling()
    }
  }, 3000)
}

const resetState = () => {
  report.value = null
  agentLogs.value = []
  consoleLogs.value = []
  agentLogLine.value = 0
  consoleLogLine.value = 0
  errorMessage.value = ''
}

const initialize = async () => {
  if (!props.reportId) return

  resetState()
  addLog(`Report panel initialized: ${props.reportId}`)
  emitStatus('processing')
  await refreshAll()

  if (!isComplete.value && report.value?.status !== 'failed') {
    startPolling()
  }
}

const goToInteraction = () => {
  if (!props.reportId) return
  router.push({ name: 'Interaction', params: { reportId: props.reportId } })
}

watch(() => props.reportId, async (newReportId) => {
  if (!newReportId) return
  await initialize()
}, { immediate: true })

onMounted(() => {
  if (props.reportId && !pollingHandle.value) {
    startPolling()
  }
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.report-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  background: #f7f7f4;
  color: #121212;
  overflow: auto;
}

.report-toolbar,
.report-grid,
.log-grid {
  display: grid;
  gap: 16px;
}

.report-toolbar {
  grid-template-columns: 1fr auto;
  align-items: start;
}

.toolbar-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.eyebrow {
  margin: 0 0 6px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #6b6b63;
}

.report-title {
  margin: 0;
  font-size: 28px;
  line-height: 1;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  height: 36px;
  padding: 0 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.status-badge.is-processing {
  background: #efe8c8;
  color: #6f5700;
}

.status-badge.is-complete {
  background: #dbf1dd;
  color: #1c6b2d;
}

.status-badge.is-error {
  background: #f8dddd;
  color: #8d1f1f;
}

.ghost-btn,
.primary-btn {
  height: 36px;
  padding: 0 14px;
  border-radius: 10px;
  border: 1px solid #d4d2ca;
  background: #fff;
  color: #121212;
  font-weight: 600;
  cursor: pointer;
}

.primary-btn {
  border-color: #121212;
  background: #121212;
  color: #fff;
}

.ghost-btn:disabled,
.primary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.report-grid,
.log-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.panel-card {
  background: #fff;
  border: 1px solid #e5e2d8;
  border-radius: 20px;
  padding: 18px;
  box-shadow: 0 10px 30px rgba(18, 18, 18, 0.04);
}

.report-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-label,
.card-count {
  font-size: 12px;
  color: #6b6b63;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.meta-value {
  font-size: 14px;
  font-weight: 600;
  word-break: break-word;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
}

.outline-summary,
.empty-copy,
.empty-state-copy,
.timeline-detail,
.timeline-section {
  margin: 0;
  color: #505048;
}

.outline-list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.outline-list li {
  display: flex;
  gap: 12px;
  align-items: center;
  font-weight: 600;
}

.section-index {
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #f1efe6;
  color: #6b6b63;
  font-size: 12px;
}

.thesis-card {
  min-height: 260px;
}

.error-banner {
  margin: 0 0 14px;
  padding: 12px 14px;
  border-radius: 12px;
  background: #f8dddd;
  color: #8d1f1f;
}

.empty-state {
  border: 1px dashed #d8d5ca;
  border-radius: 16px;
  padding: 20px;
  background: #faf9f5;
}

.empty-state-title {
  margin-bottom: 6px;
  font-weight: 700;
}

.report-content {
  line-height: 1.65;
}

.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
  margin: 1.2em 0 0.5em;
  line-height: 1.2;
}

.markdown-body :deep(p) {
  margin: 0.8em 0;
}

.markdown-body :deep(ul) {
  margin: 0.8em 0;
  padding-left: 1.25rem;
}

.markdown-body :deep(blockquote) {
  margin: 1em 0;
  padding-left: 14px;
  border-left: 3px solid #d4d2ca;
  color: #505048;
}

.markdown-body :deep(.inline-code),
.markdown-body :deep(code) {
  padding: 0.1rem 0.35rem;
  border-radius: 6px;
  background: #f1efe6;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.92em;
}

.markdown-body :deep(pre) {
  overflow: auto;
  padding: 14px;
  border-radius: 12px;
  background: #161616;
  color: #f4f0e6;
}

.log-card {
  min-height: 280px;
}

.timeline-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.timeline-item {
  display: flex;
  gap: 12px;
  align-items: start;
}

.timeline-dot {
  width: 10px;
  height: 10px;
  margin-top: 6px;
  border-radius: 999px;
  background: #121212;
  flex: none;
}

.timeline-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.timeline-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.timeline-action {
  font-weight: 700;
}

.timeline-time {
  font-size: 12px;
  color: #6b6b63;
}

.timeline-section {
  font-weight: 600;
}

.console-block {
  margin: 0;
  padding: 14px;
  border-radius: 14px;
  background: #151515;
  color: #e9e6dc;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  line-height: 1.6;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

@media (max-width: 1100px) {
  .report-grid,
  .log-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .report-panel {
    padding: 14px;
  }

  .report-toolbar {
    grid-template-columns: 1fr;
  }

  .toolbar-actions {
    flex-wrap: wrap;
  }

  .report-meta {
    grid-template-columns: 1fr;
  }
}
</style>
