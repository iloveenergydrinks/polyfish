import service, { requestWithRetry } from './index'

/**
 * Generate the ontology from uploaded files and the simulation requirement
 * @param {Object} data - Includes files, simulation_requirement, project_name, and more
 * @returns {Promise}
 */
export function generateOntology(formData) {
  return requestWithRetry(() => 
    service({
      url: '/graph/ontology/generate',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  )
}

/**
 * Build the graph
 * @param {Object} data - Includes project_id, graph_name, and more
 * @returns {Promise}
 */
export function buildGraph(data) {
  return requestWithRetry(() =>
    service({
      url: '/graph/build',
      method: 'post',
      data
    })
  )
}

/**
 * Query task status
 * @param {String} taskId - Task ID
 * @returns {Promise}
 */
export function getTaskStatus(taskId) {
  return service({
    url: `/graph/task/${taskId}`,
    method: 'get'
  })
}

/**
 * Fetch graph data
 * @param {String} graphId - Graph ID
 * @returns {Promise}
 */
export function getGraphData(graphId) {
  return service({
    url: `/graph/data/${graphId}`,
    method: 'get'
  })
}

/**
 * Fetch project information
 * @param {String} projectId - Project ID
 * @returns {Promise}
 */
export function getProject(projectId) {
  return service({
    url: `/graph/project/${projectId}`,
    method: 'get'
  })
}
