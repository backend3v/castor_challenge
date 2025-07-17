<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Iniciar Sesión</h1>
        <p>Accede a tu cuenta para continuar</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            :class="{ 'error': errors.email }"
            placeholder="tu@email.com"
            required
          />
          <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">Contraseña</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-input"
            :class="{ 'error': errors.password }"
            placeholder="Tu contraseña"
            required
          />
          <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
        </div>
        
        <div v-if="error" class="error-message global-error">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary login-btn" :disabled="loading">
          <span v-if="loading">Iniciando sesión...</span>
          <span v-else>Iniciar Sesión</span>
        </button>
      </form>
      
      <div class="login-footer">
        <p>¿No tienes cuenta? <router-link to="/register" class="link">Regístrate aquí</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const loading = ref(false)
    const error = ref('')
    
    const form = reactive({
      email: '',
      password: ''
    })
    
    const errors = reactive({
      email: '',
      password: ''
    })
    
    const validateForm = () => {
      errors.email = ''
      errors.password = ''
      
      if (!form.email) {
        errors.email = 'El email es requerido'
        return false
      }
      
      if (!form.email.includes('@')) {
        errors.email = 'El email debe ser válido'
        return false
      }
      
      if (!form.password) {
        errors.password = 'La contraseña es requerida'
        return false
      }
      
      if (form.password.length < 6) {
        errors.password = 'La contraseña debe tener al menos 6 caracteres'
        return false
      }
      
      return true
    }
    
    const handleLogin = async () => {
      if (!validateForm()) return
      
      loading.value = true
      error.value = ''
      
      try {
        const result = await authStore.login(form.email, form.password)
        
        if (result.success) {
          // Redirect to dashboard or intended page
          router.push('/')
        } else {
          error.value = result.error || 'Error al iniciar sesión'
        }
      } catch (err) {
        error.value = 'Error de conexión. Intenta de nuevo.'
        console.error('Login error:', err)
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      errors,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 2rem;
  font-weight: 600;
}

.login-header p {
  color: #666;
  margin: 0;
}

.login-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input.error {
  border-color: #dc3545;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.global-error {
  background: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #f5c6cb;
  margin-bottom: 1rem;
}

.login-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 1rem;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e1e5e9;
}

.login-footer p {
  margin: 0;
  color: #666;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-container {
    padding: 1rem;
  }
  
  .login-card {
    padding: 2rem;
  }
  
  .login-header h1 {
    font-size: 1.75rem;
  }
}
</style> 