<template>
  <div class="interaction-panel">
    <div class="interaction-toolbar">
      <div class="toolbar-group">
        <button
          class="toolbar-btn"
          :class="{ active: activeTab === 'chat' && chatTarget === 'report_agent' }"
          @click="selectReportAgentChat"
        >
          Report Agent
        </button>
        <button
          class="toolbar-btn"
          :class="{ active: activeTab === 'chat' && chatTarget === 'agent' }"
          @click="toggleAgentDropdown"
        >
          Agent Chat
        </button>
        <button
          class="toolbar-btn"
          :class="{ active: activeTab === 'survey' }"
          @click="selectSurveyTab"
        >
          Survey
        </button>
      </div>

      <div v-if="showAgentDropdown" class="agent-dropdown">
        <button class="dropdown-item" @click="selectReportAgentChat">
          Report Agent
        </button>
        <button
          v-for="(agent, idx) in profiles"
          :key="`${agent.username || 'agent'}-${idx}`"
          class="dropdown-item"
          @click="selectAgent(agent, idx)"
        >
          {{ agent.username || `Agent ${idx + 1}` }}
        </button>
      </div>
    </div>

    <div v-if="activeTab === 'chat'" class="chat-shell">
      <div v-if="chatTarget === 'agent' && selectedAgent" class="agent-profile-card">
        <div class="profile-card-header">
          <div class="profile-card-avatar">{{ (selectedAgent.username || 'A')[0] }}</div>
          <div class="profile-card-info">
            <div class="profile-card-name">{{ selectedAgent.username }}</div>
            <div class="profile-card-meta">
              <span v-if="selectedAgent.name" class="profile-card-handle">@{{ selectedAgent.name }}</span>
              <span class="profile-card-profession">{{ selectedAgent.profession || 'Unknown profession' }}</span>
            </div>
          </div>
          <button class="profile-card-toggle" @click="showFullProfile = !showFullProfile">
            <svg :class="{ 'is-expanded': showFullProfile }" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </div>
        <div v-if="showFullProfile && selectedAgent.bio" class="profile-card-body">
          <div class="profile-card-bio">
            <div class="profile-card-label">Bio</div>
            <p>{{ selectedAgent.bio }}</p>
          </div>
        </div>
      </div>

      <div class="chat-messages" ref="chatMessages">
        <div v-if="chatHistory.length === 0" class="chat-empty">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
          </div>
          <p class="empty-text">
            {{ chatTarget === 'report_agent' ? 'Chat with Report Agent to explore the report in depth' : 'Chat with simulated individuals to understand their viewpoints' }}
          </p>
        </div>
        <div
          v-for="(msg, idx) in chatHistory"
          :key="idx"
          class="chat-message"
          :class="msg.role"
        >
          <div class="message-avatar">
            <span v-if="msg.role === 'user'">U</span>
            <span v-else>{{ msg.role === 'assistant' && chatTarget === 'report_agent' ? 'R' : (selectedAgent?.username?.[0] || 'A') }}</span>
          </div>
          <div class="message-content">
            <div class="message-header">
              <span class="sender-name">
                {{ msg.role === 'user' ? 'You' : (chatTarget === 'report_agent' ? 'Report Agent' : (selectedAgent?.username || 'Agent')) }}
              </span>
              <span class="message-time">{{ formatTime(msg.timestamp) }}</span>
            </div>
            <div class="message-text" v-html="renderMarkdown(msg.content)"></div>
          </div>
        </div>
        <div v-if="isSending" class="chat-message assistant">
          <div class="message-avatar">
            <span>{{ chatTarget === 'report_agent' ? 'R' : (selectedAgent?.username?.[0] || 'A') }}</span>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <textarea
          v-model="chatInput"
          class="chat-input"
          placeholder="Enter your question..."
          @keydown.enter.exact.prevent="sendMessage"
          :disabled="isSending || (!selectedAgent && chatTarget === 'agent')"
          rows="1"
          ref="chatInputRef"
        ></textarea>
        <button
          class="send-btn"
          @click="sendMessage"
          :disabled="!chatInput.trim() || isSending || (!selectedAgent && chatTarget === 'agent')"
        >
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>

    <div v-if="activeTab === 'survey'" class="survey-container">
      <div class="survey-setup">
        <div class="setup-section">
          <div class="section-header">
            <span class="section-title">Select Survey Targets</span>
            <span class="selection-count">Selected {{ selectedAgents.size }} / {{ profiles.length }}</span>
          </div>
          <div class="agents-grid">
            <label
              v-for="(agent, idx) in profiles"
              :key="idx"
              class="agent-checkbox"
              :class="{ checked: selectedAgents.has(idx) }"
            >
              <input
                type="checkbox"
                :checked="selectedAgents.has(idx)"
                @change="toggleAgentSelection(idx)"
              >
              <div class="checkbox-avatar">{{ (agent.username || 'A')[0] }}</div>
              <div class="checkbox-info">
                <span class="checkbox-name">{{ agent.username }}</span>
                <span class="checkbox-role">{{ agent.profession || 'Unknown profession' }}</span>
              </div>
              <div class="checkbox-indicator">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
            </label>
          </div>
          <div class="selection-actions">
            <button class="action-link" @click="selectAllAgents">Select all</button>
            <span class="action-divider">|</span>
            <button class="action-link" @click="clearAgentSelection">Clear</button>
          </div>
        </div>

        <div class="setup-section">
          <div class="section-header">
            <span class="section-title">Survey Question</span>
          </div>
          <textarea
            v-model="surveyQuestion"
            class="survey-input"
            placeholder="Enter the question you want to ask all selected targets..."
            rows="3"
          ></textarea>
        </div>

        <button
          class="survey-submit-btn"
          :disabled="selectedAgents.size === 0 || !surveyQuestion.trim() || isSurveying"
          @click="submitSurvey"
        >
          <span v-if="isSurveying" class="loading-spinner"></span>
          <span v-else>Send Survey</span>
        </button>
      </div>

      <div v-if="surveyResults.length > 0" class="survey-results">
        <div class="results-header">
          <span class="results-title">Survey Results</span>
          <span class="results-count">{{ surveyResults.length }} replies</span>
        </div>
        <div class="results-list">
          <div
            v-for="(result, idx) in surveyResults"
            :key="idx"
            class="result-card"
          >
            <div class="result-header">
              <div class="result-avatar">{{ (result.agent_name || 'A')[0] }}</div>
              <div class="result-info">
                <span class="result-name">{{ result.agent_name }}</span>
                <span class="result-role">{{ result.profession || 'Unknown profession' }}</span>
              </div>
            </div>
            <div class="result-question">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              <span>{{ result.question }}</span>
            </div>
            <div class="result-answer" v-html="renderMarkdown(result.answer)"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { chatWithReport, getReport, getAgentLog } from '../api/report'
import { interviewAgents, getSimulationProfilesRealtime } from '../api/simulation'

const props = defineProps({
  reportId: String,
  simulationId: String
})

const emit = defineEmits(['add-log', 'update-status'])

// State
const activeTab = ref('chat')
const chatTarget = ref('report_agent')
const showAgentDropdown = ref(false)
const selectedAgent = ref(null)
const selectedAgentIndex = ref(null)
const showFullProfile = ref(true)
const showToolsDetail = ref(true)

// Chat State
const chatInput = ref('')
const chatHistory = ref([])
const chatHistoryCache = ref({}) // Cache all chat histories: { 'report_agent': [], 'agent_0': [], 'agent_1': [], ... }
const isSending = ref(false)
const chatMessages = ref(null)
const chatInputRef = ref(null)

// Survey State
const selectedAgents = ref(new Set())
const surveyQuestion = ref('')
const surveyResults = ref([])
const isSurveying = ref(false)

// Report Data
const reportOutline = ref(null)
const generatedSections = ref({})
const collapsedSections = ref(new Set())
const currentSectionIndex = ref(null)
const profiles = ref([])

// Helper Methods
const isSectionCompleted = (sectionIndex) => {
  return !!generatedSections.value[sectionIndex]
}

// Refs
const leftPanel = ref(null)
const rightPanel = ref(null)

// Methods
const addLog = (msg) => {
  emit('add-log', msg)
}

const toggleSectionCollapse = (idx) => {
  if (!generatedSections.value[idx + 1]) return
  const newSet = new Set(collapsedSections.value)
  if (newSet.has(idx)) {
    newSet.delete(idx)
  } else {
    newSet.add(idx)
  }
  collapsedSections.value = newSet
}

const selectChatTarget = (target) => {
  chatTarget.value = target
  if (target === 'report_agent') {
    showAgentDropdown.value = false
  }
}

// Save the current chat history to cache
const saveChatHistory = () => {
  if (chatHistory.value.length === 0) return
  
  if (chatTarget.value === 'report_agent') {
    chatHistoryCache.value['report_agent'] = [...chatHistory.value]
  } else if (selectedAgentIndex.value !== null) {
    chatHistoryCache.value[`agent_${selectedAgentIndex.value}`] = [...chatHistory.value]
  }
}

const selectReportAgentChat = () => {
  // Save the current chat history
  saveChatHistory()
  
  activeTab.value = 'chat'
  chatTarget.value = 'report_agent'
  selectedAgent.value = null
  selectedAgentIndex.value = null
  showAgentDropdown.value = false
  
  // Restore Report Agent chat history
  chatHistory.value = chatHistoryCache.value['report_agent'] || []
}

const selectSurveyTab = () => {
  activeTab.value = 'survey'
  selectedAgent.value = null
  selectedAgentIndex.value = null
  showAgentDropdown.value = false
}

const toggleAgentDropdown = () => {
  showAgentDropdown.value = !showAgentDropdown.value
  if (showAgentDropdown.value) {
    activeTab.value = 'chat'
    chatTarget.value = 'agent'
  }
}

const selectAgent = (agent, idx) => {
  // Save the current chat history
  saveChatHistory()
  
  selectedAgent.value = agent
  selectedAgentIndex.value = idx
  chatTarget.value = 'agent'
  showAgentDropdown.value = false
  
  // Restore the selected agent's chat history
  chatHistory.value = chatHistoryCache.value[`agent_${idx}`] || []
  addLog(`Select a conversation target: ${agent.username}`)
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  try {
    return new Date(timestamp).toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit'
    })
  } catch {
    return ''
  }
}

const renderMarkdown = (content) => {
  if (!content) return ''
  
  let processedContent = content.replace(/^##\s+.+\n+/, '')
  let html = processedContent.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="code-block"><code>$2</code></pre>')
  html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
  html = html.replace(/^#### (.+)$/gm, '<h5 class="md-h5">$1</h5>')
  html = html.replace(/^### (.+)$/gm, '<h4 class="md-h4">$1</h4>')
  html = html.replace(/^## (.+)$/gm, '<h3 class="md-h3">$1</h3>')
  html = html.replace(/^# (.+)$/gm, '<h2 class="md-h2">$1</h2>')
  html = html.replace(/^> (.+)$/gm, '<blockquote class="md-quote">$1</blockquote>')
  
  // translated comment
  html = html.replace(/^(\s*)- (.+)$/gm, (match, indent, text) => {
    const level = Math.floor(indent.length / 2)
    return `<li class="md-li" data-level="${level}">${text}</li>`
  })
  html = html.replace(/^(\s*)(\d+)\. (.+)$/gm, (match, indent, num, text) => {
    const level = Math.floor(indent.length / 2)
    return `<li class="md-oli" data-level="${level}">${text}</li>`
  })
  
  // translated comment
  html = html.replace(/(<li class="md-li"[^>]*>.*?<\/li>\s*)+/g, '<ul class="md-ul">$&</ul>')
  // translated comment
  html = html.replace(/(<li class="md-oli"[^>]*>.*?<\/li>\s*)+/g, '<ol class="md-ol">$&</ol>')
  
  // translated comment
  html = html.replace(/<\/li>\s+<li/g, '</li><li')
  // translated comment
  html = html.replace(/<ul class="md-ul">\s+/g, '<ul class="md-ul">')
  html = html.replace(/<ol class="md-ol">\s+/g, '<ol class="md-ol">')
  // translated comment
  html = html.replace(/\s+<\/ul>/g, '</ul>')
  html = html.replace(/\s+<\/ol>/g, '</ol>')
  
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')
  html = html.replace(/_(.+?)_/g, '<em>$1</em>')
  html = html.replace(/^---$/gm, '<hr class="md-hr">')
  html = html.replace(/\n\n/g, '</p><p class="md-p">')
  html = html.replace(/\n/g, '<br>')
  html = '<p class="md-p">' + html + '</p>'
  html = html.replace(/<p class="md-p"><\/p>/g, '')
  html = html.replace(/<p class="md-p">(<h[2-5])/g, '$1')
  html = html.replace(/(<\/h[2-5]>)<\/p>/g, '$1')
  html = html.replace(/<p class="md-p">(<ul|<ol|<blockquote|<pre|<hr)/g, '$1')
  html = html.replace(/(<\/ul>|<\/ol>|<\/blockquote>|<\/pre>)<\/p>/g, '$1')
  // translated comment
  html = html.replace(/<br>\s*(<ul|<ol|<blockquote)/g, '$1')
  html = html.replace(/(<\/ul>|<\/ol>|<\/blockquote>)\s*<br>/g, '$1')
  // translated comment
  html = html.replace(/<p class="md-p">(<br>\s*)+(<ul|<ol|<blockquote|<pre|<hr)/g, '$2')
  // translated comment
  html = html.replace(/(<br>\s*){2,}/g, '<br>')
  // translated comment
  html = html.replace(/(<\/ol>|<\/ul>|<\/blockquote>)<br>(<p|<div)/g, '$1$2')

  // translated comment
  const tokens = html.split(/(<ol class="md-ol">(?:<li class="md-oli"[^>]*>[\s\S]*?<\/li>)+<\/ol>)/g)
  let olCounter = 0
  let inSequence = false
  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i].startsWith('<ol class="md-ol">')) {
      const liCount = (tokens[i].match(/<li class="md-oli"/g) || []).length
      if (liCount === 1) {
        olCounter++
        if (olCounter > 1) {
          tokens[i] = tokens[i].replace('<ol class="md-ol">', `<ol class="md-ol" start="${olCounter}">`)
        }
        inSequence = true
      } else {
        olCounter = 0
        inSequence = false
      }
    } else if (inSequence) {
      if (/<h[2-5]/.test(tokens[i])) {
        olCounter = 0
        inSequence = false
      }
    }
  }
  html = tokens.join('')

  return html
}

// Chat Methods
const sendMessage = async () => {
  if (!chatInput.value.trim() || isSending.value) return
  
  const message = chatInput.value.trim()
  chatInput.value = ''
  
  // Add user message
  chatHistory.value.push({
    role: 'user',
    content: message,
    timestamp: new Date().toISOString()
  })
  
  scrollToBottom()
  isSending.value = true
  
  try {
    if (chatTarget.value === 'report_agent') {
      await sendToReportAgent(message)
    } else {
      await sendToAgent(message)
    }
  } catch (err) {
    addLog(`Send failed: ${err.message}`)
    chatHistory.value.push({
      role: 'assistant',
      content: `Sorry, an error occurred: ${err.message}`,
      timestamp: new Date().toISOString()
    })
  } finally {
    isSending.value = false
    scrollToBottom()
    // Automatically save chat history to cache
    saveChatHistory()
  }
}

const sendToReportAgent = async (message) => {
  addLog(`Send to Report Agent: ${message.substring(0, 50)}...`)
  
  // Build chat history for API
  const historyForApi = chatHistory.value
    .filter(msg => msg.role !== 'user' || msg.content !== message)
    .slice(-10) // Keep last 10 messages
    .map(msg => ({
      role: msg.role,
      content: msg.content
    }))
  
  const res = await chatWithReport({
    simulation_id: props.simulationId,
    message: message,
    chat_history: historyForApi
  })
  
  if (res.success && res.data) {
    chatHistory.value.push({
      role: 'assistant',
      content: res.data.response || res.data.answer || 'No response',
      timestamp: new Date().toISOString()
    })
    addLog('Report Agent replied')
  } else {
    throw new Error(res.error || 'Request failed')
  }
}

const sendToAgent = async (message) => {
  if (!selectedAgent.value || selectedAgentIndex.value === null) {
    throw new Error('Please select a simulated individual first')
  }
  
  addLog(`Send to ${selectedAgent.value.username} Translated: ${message.substring(0, 50)}...`)
  
  // Build prompt with chat history
  let prompt = message
  if (chatHistory.value.length > 1) {
    const historyContext = chatHistory.value
      .filter(msg => msg.content !== message)
      .slice(-6)
      .map(msg => `${msg.role === 'user' ? 'Questioner' : 'You'}:${msg.content}`)
      .join('\n')
    prompt = `Translated:\n${historyContext}\n\nTranslated:${message}`
  }
  
  const res = await interviewAgents({
    simulation_id: props.simulationId,
    interviews: [{
      agent_id: selectedAgentIndex.value,
      prompt: prompt
    }]
  })
  
  if (res.success && res.data) {
    // Correct data path: res.data.result.results is an object map
    // Format: {"twitter_0": {...}, "reddit_0": {...}} or single-platform {"reddit_0": {...}}
    const resultData = res.data.result || res.data
    const resultsDict = resultData.results || resultData
    
    // Convert the object map to an array and prefer the Reddit response
    let responseContent = null
    const agentId = selectedAgentIndex.value
    
    if (typeof resultsDict === 'object' && !Array.isArray(resultsDict)) {
      // Prefer the Reddit response, then Twitter
      const redditKey = `reddit_${agentId}`
      const twitterKey = `twitter_${agentId}`
      const agentResult = resultsDict[redditKey] || resultsDict[twitterKey] || Object.values(resultsDict)[0]
      if (agentResult) {
        responseContent = agentResult.response || agentResult.answer
      }
    } else if (Array.isArray(resultsDict) && resultsDict.length > 0) {
      // Support array format
      responseContent = resultsDict[0].response || resultsDict[0].answer
    }
    
    if (responseContent) {
      chatHistory.value.push({
        role: 'assistant',
        content: responseContent,
        timestamp: new Date().toISOString()
      })
      addLog(`${selectedAgent.value.username} replied`)
    } else {
      throw new Error('No responseTranslated')
    }
  } else {
    throw new Error(res.error || 'Request failed')
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight
    }
  })
}

// Survey Methods
const toggleAgentSelection = (idx) => {
  const newSet = new Set(selectedAgents.value)
  if (newSet.has(idx)) {
    newSet.delete(idx)
  } else {
    newSet.add(idx)
  }
  selectedAgents.value = newSet
}

const selectAllAgents = () => {
  const newSet = new Set()
  profiles.value.forEach((_, idx) => newSet.add(idx))
  selectedAgents.value = newSet
}

const clearAgentSelection = () => {
  selectedAgents.value = new Set()
}

const submitSurvey = async () => {
  if (selectedAgents.value.size === 0 || !surveyQuestion.value.trim()) return
  
  isSurveying.value = true
  addLog(`Send SurveyTranslated ${selectedAgents.value.size} targets...`)
  
  try {
    const interviews = Array.from(selectedAgents.value).map(idx => ({
      agent_id: idx,
      prompt: surveyQuestion.value.trim()
    }))
    
    const res = await interviewAgents({
      simulation_id: props.simulationId,
      interviews: interviews
    })
    
    if (res.success && res.data) {
      // Correct data path: res.data.result.results is an object map
      // translated comment
      const resultData = res.data.result || res.data
      const resultsDict = resultData.results || resultData
      
      // Convert the object map to array format
      const surveyResultsList = []
      
      for (const interview of interviews) {
        const agentIdx = interview.agent_id
        const agent = profiles.value[agentIdx]
        
        // Prefer the Reddit response, then Twitter
        let responseContent = 'No response'
        
        if (typeof resultsDict === 'object' && !Array.isArray(resultsDict)) {
          const redditKey = `reddit_${agentIdx}`
          const twitterKey = `twitter_${agentIdx}`
          const agentResult = resultsDict[redditKey] || resultsDict[twitterKey]
          if (agentResult) {
            responseContent = agentResult.response || agentResult.answer || 'No response'
          }
        } else if (Array.isArray(resultsDict)) {
          // Support array format
          const matchedResult = resultsDict.find(r => r.agent_id === agentIdx)
          if (matchedResult) {
            responseContent = matchedResult.response || matchedResult.answer || 'No response'
          }
        }
        
        surveyResultsList.push({
          agent_id: agentIdx,
          agent_name: agent?.username || `Agent ${agentIdx}`,
          profession: agent?.profession,
          question: surveyQuestion.value.trim(),
          answer: responseContent
        })
      }
      
      surveyResults.value = surveyResultsList
      addLog(`Received ${surveyResults.value.length} replies`)
    } else {
      throw new Error(res.error || 'Request failed')
    }
  } catch (err) {
    addLog(`TranslatedSend failed: ${err.message}`)
  } finally {
    isSurveying.value = false
  }
}

// Load Report Data
const loadReportData = async () => {
  if (!props.reportId) return
  
  try {
    addLog(`Load report data: ${props.reportId}`)
    
    // Get report info
    const reportRes = await getReport(props.reportId)
    if (reportRes.success && reportRes.data) {
      // Load agent logs to get report outline and sections
      await loadAgentLogs()
    }
  } catch (err) {
    addLog(`Failed to load report: ${err.message}`)
  }
}

const loadAgentLogs = async () => {
  if (!props.reportId) return
  
  try {
    const res = await getAgentLog(props.reportId, 0)
    if (res.success && res.data) {
      const logs = res.data.logs || []
      
      logs.forEach(log => {
        if (log.action === 'planning_complete' && log.details?.outline) {
          reportOutline.value = log.details.outline
        }
        
        if (log.action === 'section_complete' && log.section_index < 100 && log.details?.content) {
          generatedSections.value[log.section_index] = log.details.content
        }
      })
      
      addLog('Report data loaded')
    }
  } catch (err) {
    addLog(`Failed to load report logs: ${err.message}`)
  }
}

const loadProfiles = async () => {
  if (!props.simulationId) return
  
  try {
    const res = await getSimulationProfilesRealtime(props.simulationId, 'reddit')
    if (res.success && res.data) {
      profiles.value = res.data.profiles || []
      addLog(`Loaded ${profiles.value.length} simulated individuals`)
    }
  } catch (err) {
    addLog(`Failed to load simulated individuals: ${err.message}`)
  }
}

// Click outside to close dropdown
const handleClickOutside = (e) => {
  const dropdown = document.querySelector('.agent-dropdown')
  if (dropdown && !dropdown.contains(e.target)) {
    showAgentDropdown.value = false
  }
}

// Lifecycle
onMounted(() => {
  addLog('Step 5 interactive analysis initialized')
  loadReportData()
  loadProfiles()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

watch(() => props.reportId, (newId) => {
  if (newId) {
    loadReportData()
  }
}, { immediate: true })

watch(() => props.simulationId, (newId) => {
  if (newId) {
    loadProfiles()
  }
}, { immediate: true })
</script>

<style scoped>
.interaction-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #F8F9FA;
  font-family: 'Montech', 'Noto Sans SC', system-ui, sans-serif;
  overflow: hidden;
}

.interaction-toolbar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 20px;
  background: #FFFFFF;
  border-bottom: 1px solid #E5E7EB;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-btn {
  border: 1px solid #E5E7EB;
  background: #FFFFFF;
  color: #111827;
  border-radius: 999px;
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.toolbar-btn.active {
  background: #111827;
  color: #FFFFFF;
  border-color: #111827;
}

.agent-dropdown {
  position: absolute;
  top: calc(100% - 8px);
  left: 20px;
  z-index: 10;
  min-width: 220px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  padding: 8px;
  display: grid;
  gap: 6px;
}

.dropdown-item {
  text-align: left;
  border: none;
  background: #FFFFFF;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 13px;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #F3F4F6;
}

.chat-shell,
.survey-container {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 16px;
}

.chat-messages,
.survey-results {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.chat-input-area {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.chat-input,
.survey-input {
  width: 100%;
  border: 1px solid #D1D5DB;
  border-radius: 12px;
  padding: 12px 14px;
  background: #FFFFFF;
  font: inherit;
  resize: vertical;
}

.send-btn,
.survey-submit-btn {
  border: none;
  border-radius: 12px;
  background: #111827;
  color: #FFFFFF;
  padding: 12px 14px;
  cursor: pointer;
}

/* translated comment */
.left-panel.report-style {
  width: 45%;
  min-width: 450px;
  background: #FFFFFF;
  border-right: 1px solid #E5E7EB;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 30px 50px 60px 50px;
}

.left-panel::-webkit-scrollbar {
  width: 6px;
}

.left-panel::-webkit-scrollbar-track {
  background: transparent;
}

.left-panel::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: 3px;
  transition: background 0.3s ease;
}

.left-panel:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
}

.left-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.25);
}

/* translated comment */
.message-text {
  counter-reset: list-counter;
}

.message-text :deep(.md-ol) {
  list-style: none;
  padding-left: 0;
  margin: 8px 0;
}

.message-text :deep(.md-oli) {
  counter-increment: list-counter;
  display: flex;
  gap: 8px;
  margin: 4px 0;
}

.message-text :deep(.md-oli)::before {
  content: counter(list-counter) ".";
  font-weight: 600;
  color: #374151;
  min-width: 20px;
  flex-shrink: 0;
}

/* translated comment */
.message-text :deep(.md-ul) {
  padding-left: 20px;
  margin: 8px 0;
}

.message-text :deep(.md-li) {
  margin: 4px 0;
}

/* translated comment */
.chat-messages :deep(.md-quote),
.result-answer :deep(.md-quote) {
  margin: 12px 0;
  padding: 12px 16px;
  background: #F9FAFB;
  border-left: 3px solid #1F2937;
  color: #4B5563;
}

:deep(.code-block) {
  margin: 12px 0;
  padding: 12px 16px;
  background: #1F2937;
  border-radius: 6px;
  overflow-x: auto;
}

:deep(.code-block code) {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: #E5E7EB;
}

:deep(.inline-code) {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  background: #F3F4F6;
  padding: 2px 6px;
  border-radius: 4px;
  color: #1F2937;
}

:deep(.md-hr) {
  border: none;
  border-top: 1px solid #E5E7EB;
  margin: 24px 0;
}
</style>
