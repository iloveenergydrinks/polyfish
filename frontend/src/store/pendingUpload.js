/**
 * Temporarily store the market and requirement pending launch
 * Used to jump from the home page immediately and perform the API call in Process
 */
import { reactive } from 'vue'

const state = reactive({
  market: null,
  simulationRequirement: '',
  isPending: false
})

export function setPendingUpload(market, requirement) {
  state.market = market
  state.simulationRequirement = requirement
  state.isPending = true
}

export function getPendingUpload() {
  return {
    market: state.market,
    simulationRequirement: state.simulationRequirement,
    isPending: state.isPending
  }
}

export function clearPendingUpload() {
  state.market = null
  state.simulationRequirement = ''
  state.isPending = false
}

export default state
