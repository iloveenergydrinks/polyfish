import service, { requestWithRetry } from './index'

export const getActiveMarkets = ({ limit = 24, offset = 0 } = {}) => {
  return requestWithRetry(() =>
    service.get('/api/markets/active', {
      params: { limit, offset }
    })
  )
}

export const lookupMarket = ({ slug, id } = {}) => {
  return requestWithRetry(() =>
    service.get('/api/markets/lookup', {
      params: { slug, id }
    })
  )
}

export const createProjectFromMarket = (data) => {
  return requestWithRetry(() => service.post('/api/markets/project', data), 3, 1000)
}
