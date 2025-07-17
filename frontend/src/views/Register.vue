<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1>Crear Cuenta</h1>
        <p>Únete a nuestra comunidad</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="name" class="form-label">Nombre</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            class="form-input"
            :class="{ 'error': errors.name }"
            placeholder="Tu nombre completo"
            required
          />
          <span v-if="errors.name" class="error-message">{{ errors.name }}</span>
        </div>
        
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
            placeholder="Mínimo 6 caracteres"
            required
          />
          <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword" class="form-label">Confirmar Contraseña</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            class="form-input"
            :class="{ 'error': errors.confirmPassword }"
            placeholder="Repite tu contraseña"
            required
          />
          <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
        </div>
        
        <div v-if="error" class="error-message global-error">
          {{ error }}
        </div>
        <div v-if="success" class="success-message global-success">
          ¡Registro exitoso! Redirigiendo al login...
        </div>
        
        <button type="submit" class="btn btn-primary register-btn" :disabled="loading">
          <span v-if="loading">Creando cuenta...</span>
          <span v-else>Crear Cuenta</span>
        </button>
      </form>
      
      <div class="register-footer">
        <p>¿Ya tienes cuenta? <router-link to="/login" class="link">Inicia sesión aquí</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const loading = ref(false)
    const error = ref('')
    const success = ref(false)
    
    const form = reactive({
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    
    const errors = reactive({
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    
    const validateForm = () => {
      errors.name = ''
      errors.email = ''
      errors.password = ''
      errors.confirmPassword = ''
      
      if (!form.name.trim()) {
        errors.name = 'El nombre es requerido'
        return false
      }
      
      if (form.name.trim().length < 2) {
        errors.name = 'El nombre debe tener al menos 2 caracteres'
        return false
      }
      
      if (!form.email) {
        errors.email = 'El email es requerido'
        return false
      }
      
      if (!form.email.includes('@') || !form.email.includes('.')) {
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
      
      if (!form.confirmPassword) {
        errors.confirmPassword = 'Confirma tu contraseña'
        return false
      }
      
      if (form.password !== form.confirmPassword) {
        errors.confirmPassword = 'Las contraseñas no coinciden'
        return false
      }
      
      return true
    }
    
    const handleRegister = async () => {
      if (!validateForm()) return
      
      loading.value = true
      error.value = ''
      success.value = false
      
      try {
        const result = await authStore.register(form.name, form.email, form.password)
        
        if (result.success) {
          success.value = true
          setTimeout(() => {
            router.push('/login')
          }, 1500)
        } else {
          error.value = result.error || 'Error al crear la cuenta'
        }
      } catch (err) {
        error.value = 'Error de conexión. Intenta de nuevo.'
        console.error('Register error:', err)
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      errors,
      loading,
      error,
      success,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 2rem;
  font-weight: 600;
}

.register-header p {
  color: #666;
  margin: 0;
}

.register-form {
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

.success-message.global-success {
  background: #d4edda;
  color: #155724;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #c3e6cb;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: bold;
}

.register-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 1rem;
}

.register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e1e5e9;
}

.register-footer p {
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
  .register-container {
    padding: 1rem;
  }
  
  .register-card {
    padding: 2rem;
  }
  
  .register-header h1 {
    font-size: 1.75rem;
  }
}
</style> 