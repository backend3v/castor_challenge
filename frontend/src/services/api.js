import axios from 'axios'
import { useAuthStore } from '../stores/auth'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.token
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()
    
    // If error is 401 and we haven't tried to refresh token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        // Try to refresh the token
        const newToken = await authStore.refreshAccessToken()
        
        // Retry the original request with new token
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return api(originalRequest)
      } catch (refreshError) {
        // If refresh fails, redirect to login
        await authStore.logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

// API service methods
export const apiService = {
  // GET request
  get: async (url, config = {}) => {
    try {
      return await api.get(url, config)
    } catch (error) {
      throw error
    }
  },

  // POST request
  post: async (url, data = {}, config = {}) => {
    try {
      return await api.post(url, data, config)
    } catch (error) {
      throw error
    }
  },

  // PUT request
  put: async (url, data = {}, config = {}) => {
    try {
      return await api.put(url, data, config)
    } catch (error) {
      throw error
    }
  },

  // DELETE request
  delete: async (url, config = {}) => {
    try {
      return await api.delete(url, config)
    } catch (error) {
      throw error
    }
  },

  // PATCH request
  patch: async (url, data = {}, config = {}) => {
    try {
      return await api.patch(url, data, config)
    } catch (error) {
      throw error
    }
  },

  // Check backend health (system status)
  // Returns { healthy: true } if backend is up, or { healthy: false, error } if not.
  testConnection: async () => {
    try {
      await api.get('/test')
      return { healthy: true }
    } catch (error) {
      return { healthy: false, error: error.message || 'Unable to connect to backend.' }
    }
  },

  // Check database connection health
  // Returns { healthy: true } if DB is up, or { healthy: false, error } if not.
  testDatabase: async () => {
    try {
      const response = await api.get('/test_db')
      if (response.status === 'ok' || response.status === 'connected') {
        return { healthy: true }
      }
      return { healthy: false, error: response.message || 'Database not healthy.' }
    } catch (error) {
      return { healthy: false, error: error.message || 'Unable to connect to database.' }
    }
  }
}

// YouTube API service
export const youtubeService = {
  // Get trending videos
  getTrending: async (region = 'AR', maxResults = 10) => {
    try {
      const response = await apiService.get('/api/trends', {
        params: { region, max_results: maxResults }
      })
      return response
    } catch (error) {
      throw error
    }
  },

  // Search videos
  searchVideos: async (query, maxResults = 10) => {
    try {
      const response = await apiService.get('/api/v1/youtube/search', {
        params: { q: query, max_results: maxResults }
      })
      return response
    } catch (error) {
      throw error
    }
  },

  // Get video details
  getVideoDetails: async (videoId) => {
    try {
      const response = await apiService.get(`/api/v1/youtube/video/${videoId}`)
      return response
    } catch (error) {
      throw error
    }
  },

  // Get video categories
  getCategories: async (region = 'AR') => {
    try {
      const response = await apiService.get('/api/v1/youtube/categories', {
        params: { region }
      })
      return response
    } catch (error) {
      throw error
    }
  }
}

// Favorites service
export const favoritesService = {
  // Get user favorites
  getFavorites: async () => {
    const authStore = useAuthStore()
    const userId = authStore.user?.id
    if (!userId) throw new Error('No user logged in')
    try {
      const response = await apiService.get('/api/favorites', { params: { user_id: userId } })
      return response
    } catch (error) {
      throw error
    }
  },

  // Add to favorites
  addFavorite: async (videoData) => {
    const authStore = useAuthStore()
    const userId = authStore.user?.id
    if (!userId) throw new Error('No user logged in')
    try {
      const response = await apiService.post('/api/favorites', { ...videoData, user_id: userId })
      return response
    } catch (error) {
      throw error
    }
  },

  // Remove from favorites
  removeFavorite: async (videoId) => {
    const authStore = useAuthStore()
    const userId = authStore.user?.id
    if (!userId) throw new Error('No user logged in')
    try {
      const response = await apiService.delete(`/api/favorites/${videoId}`, { params: { user_id: userId } })
      return response
    } catch (error) {
      throw error
    }
  }
}

// Recommendations service
export const recommendationsService = {
  // Get user recommendations
  getRecommendations: async () => {
    const authStore = useAuthStore()
    const userId = authStore.user?.id
    if (!userId) throw new Error('No user logged in')
    try {
      const response = await apiService.get('/api/recommendations', { params: { user_id: userId } })
      return response
    } catch (error) {
      throw error
    }
  },

  // Update user preferences
  updatePreferences: async (preferences) => {
    const authStore = useAuthStore()
    const userId = authStore.user?.id
    if (!userId) throw new Error('No user logged in')
    try {
      const response = await apiService.post('/api/recommendations/preferences', { ...preferences, user_id: userId })
      return response
    } catch (error) {
      throw error
    }
  },

  // Record video view
  recordView: async (viewData) => {
    const authStore = useAuthStore()
    const userId = authStore.user?.id
    if (!userId) throw new Error('No user logged in')
    try {
      const response = await apiService.post('/api/recommendations/view', { ...viewData, user_id: userId })
      return response
    } catch (error) {
      throw error
    }
  }
}

// User service
export const userService = {
  // Get current user
  getCurrentUser: async () => {
    try {
      const response = await apiService.get('/api/auth/me')
      return response
    } catch (error) {
      throw error
    }
  },

  // Get all users (admin only)
  getAllUsers: async () => {
    try {
      const response = await apiService.get('/api/users')
      return response
    } catch (error) {
      throw error
    }
  },

  // Search users
  searchUsers: async (name) => {
    try {
      const response = await apiService.get('/api/users/search', {
        params: { name }
      })
      return response
    } catch (error) {
      throw error
    }
  }
}

export default apiService 
export const trendsService = {
  getTrends: async (region = 'AR', maxResults = 10) => {
    const authStore = useAuthStore()
    const userId = authStore.user?.id
    if (!userId) throw new Error('No user logged in')
    return await apiService.get('/api/trends', { params: { user_id: userId, region, max_results: maxResults } })
  }
}
