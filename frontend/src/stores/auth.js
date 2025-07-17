import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  const loading = ref(false)

  // Actions
  const setUser = (userData) => {
    user.value = userData
  }

  const login = async (email, password) => {
    try {
      loading.value = true
      const response = await apiService.post('/api/auth/login', { email, password })
      if (response.success) {
        setUser(response.user)
        return { success: true }
      } else {
        return { success: false, error: response.error }
      }
    } catch (error) {
      return { success: false, error: 'Error al iniciar sesión' }
    } finally {
      loading.value = false
    }
  }

  const register = async (name, email, password) => {
    try {
      loading.value = true
      const response = await apiService.post('/api/auth/register', { name, email, password })
      if (response.success) {
        return { success: true }
      } else {
        return { success: false, error: response.error }
      }
    } catch (error) {
      return { success: false, error: 'Error al crear la cuenta' }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    setUser(null)
  }

  return {
    user,
    isAuthenticated,
    loading,
    setUser,
    login,
    register,
    logout
  }
}) 