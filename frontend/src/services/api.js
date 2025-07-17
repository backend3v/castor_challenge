import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// API methods
export const apiService = {
  // System endpoints
  testConnection: () => api.get('/test'),
  testDatabase: () => api.get('/test_db'),

  // Users
  createUser: (userData) => api.post('/api/users', userData),
  getUser: (userId) => api.get(`/api/users/${userId}`),
  getAllUsers: () => api.get('/api/users'),
  searchUsers: (name) => api.get('/api/users/search', { params: { name } }),

  // Favorites
  getFavorites: (userId) => api.get(`/api/favorites/${userId}`),
  addFavorite: (favoriteData) => api.post('/api/favorites', favoriteData),
  removeFavorite: (userId, videoId) => api.delete(`/api/favorites/${userId}/${videoId}`),

  // Trends
  getTrends: (params = {}) => api.get('/api/trends', { params }),
  getTrendAnalysis: (params = {}) => api.get('/api/trends/analysis', { params }),

  // Recommendations
  getRecommendations: (userId, params = {}) => api.get(`/api/recommendations/${userId}`, { params }),
  updatePreferences: (preferencesData) => api.post('/api/recommendations/preferences', preferencesData),
  recordView: (viewData) => api.post('/api/recommendations/view', viewData)
}

export default api 