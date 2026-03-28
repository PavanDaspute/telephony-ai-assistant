/**
 * api.js — Centralised Axios instance for calling the Django REST API.
 * Base URL defaults to the Vite dev proxy (/api) so no CORS issues in dev.
 */

import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10_000,
})

/**
 * Fetch all property listings.
 * @param {object} params - Optional query params (search, ordering, page).
 * @returns {Promise<AxiosResponse>}
 */
export const fetchProperties = (params = {}) => api.get('/properties/', { params })

/**
 * Fetch a single property by ID.
 * @param {number} id
 * @returns {Promise<AxiosResponse>}
 */
export const fetchProperty = (id) => api.get(`/properties/${id}/`)

export default api
