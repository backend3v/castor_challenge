<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard</h1>
      <p class="subtitle">Bienvenido a Castor Challenge - Gestión de Videos de YouTube</p>
    </div>

    <div class="grid grid-3">
      <!-- Status Card -->
      <div class="card status-card">
        <h3>🔄 Estado del Sistema</h3>
        <div v-if="loading" class="loading">Verificando conexión...</div>
        <div v-else-if="error" class="error-message">{{ error }}</div>
        <div v-else class="status-success">
          <p>✅ Backend conectado</p>
          <p>✅ Base de datos operativa</p>
        </div>
        <button @click="checkStatus" class="btn btn-secondary" :disabled="loading">
          {{ loading ? 'Verificando...' : 'Verificar Estado' }}
        </button>
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <h3>⚡ Acciones Rápidas</h3>
        <div class="quick-actions">
          <router-link to="/favorites" class="btn btn-primary">
            ❤️ Ver Favoritos
          </router-link>
          <router-link to="/trends" class="btn btn-primary">
            📊 Ver Tendencias
          </router-link>
          <router-link to="/recommendations" class="btn btn-primary">
            🎯 Ver Recomendaciones
          </router-link>
        </div>
      </div>

      <!-- User Management -->
      <div class="card">
        <h3>👥 Gestión de Usuarios</h3>
        <div class="user-form">
          <div class="form-group">
            <label class="form-label">Nombre</label>
            <input 
              v-model="newUser.name" 
              type="text" 
              class="form-input" 
              :class="{ 'error': errors.name }"
              placeholder="Nombre del usuario"
              @blur="validateName"
              @input="clearError('name')"
              maxlength="100"
              required
            >
            <span v-if="errors.name" class="error-message">{{ errors.name }}</span>
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input 
              v-model="newUser.email" 
              type="email" 
              class="form-input" 
              :class="{ 'error': errors.email }"
              placeholder="email@ejemplo.com"
              @blur="validateEmail"
              @input="clearError('email')"
              maxlength="255"
              required
            >
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          </div>
          <button @click="createUser" class="btn btn-primary" :disabled="creatingUser || hasErrors">
            {{ creatingUser ? 'Creando...' : 'Crear Usuario' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Features Overview -->
    <div class="card">
      <h2>🚀 Funcionalidades Disponibles</h2>
      <div class="grid grid-2">
        <div class="feature-item">
          <h4>❤️ Gestión de Favoritos</h4>
          <p>Guarda y organiza tus videos favoritos de YouTube con metadatos completos.</p>
          <ul>
            <li>Agregar videos a favoritos</li>
            <li>Organizar por etiquetas</li>
            <li>Buscar y filtrar</li>
          </ul>
        </div>
        
        <div class="feature-item">
          <h4>📊 Análisis de Tendencias</h4>
          <p>Explora videos trending y obtén análisis detallados de tendencias.</p>
          <ul>
            <li>Videos trending por región</li>
            <li>Análisis de categorías</li>
            <li>Métricas de engagement</li>
          </ul>
        </div>
        
        <div class="feature-item">
          <h4>🎯 Sistema de Recomendaciones</h4>
          <p>Recibe recomendaciones personalizadas basadas en tus preferencias.</p>
          <ul>
            <li>Recomendaciones inteligentes</li>
            <li>Preferencias personalizables</li>
            <li>Historial de visualización</li>
          </ul>
        </div>
        
        <div class="feature-item">
          <h4>👥 Gestión de Usuarios</h4>
          <p>Administra usuarios y sus preferencias de manera eficiente.</p>
          <ul>
            <li>Crear y gestionar usuarios</li>
            <li>Configurar preferencias</li>
            <li>Historial de actividad</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      loading: false,
      error: null,
      creatingUser: false,
      newUser: {
        name: '',
        email: ''
      },
      errors: {
        name: '',
        email: ''
      }
    }
  },
  computed: {
    hasErrors() {
      return Object.values(this.errors).some(error => error !== '');
    }
  },
  mounted() {
    this.checkStatus()
  },
  methods: {
    async checkStatus() {
      this.loading = true
      this.error = null
      
      try {
        await apiService.testConnection()
        await apiService.testDatabase()
      } catch (err) {
        this.error = 'Error de conexión: ' + (err.response?.data?.message || err.message)
      } finally {
        this.loading = false
      }
    },
    
    async createUser() {
      if (!this.newUser.name || !this.newUser.email) {
        alert('Por favor completa todos los campos')
        return
      }
      
      this.creatingUser = true
      
      try {
        const response = await apiService.createUser(this.newUser)
        alert('Usuario creado exitosamente!')
        this.newUser = { name: '', email: '' }
      } catch (err) {
        alert('Error al crear usuario: ' + (err.response?.data?.message || err.message))
      } finally {
        this.creatingUser = false
      }
    },
    validateName() {
      if (!this.newUser.name) {
        this.errors.name = 'El nombre es requerido';
      } else {
        this.errors.name = '';
      }
    },
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.newUser.email) {
        this.errors.email = 'El email es requerido';
      } else if (!emailRegex.test(this.newUser.email)) {
        this.errors.email = 'Email inválido';
      } else {
        this.errors.email = '';
      }
    },
    clearError(field) {
      this.errors[field] = '';
    }
  }
}
</script>

<style scoped>
.dashboard-header {
  text-align: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: bold;
}

.subtitle {
  font-size: 1.1rem;
  color: #6c757d;
  margin: 0;
}

.status-card {
  text-align: center;
}

.status-success p {
  margin: 0.5rem 0;
  color: #28a745;
  font-weight: 500;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #f5c6cb;
  margin-bottom: 1rem;
  font-weight: 500;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.user-form {
  text-align: left;
}

.feature-item {
  padding: 1rem;
  border-left: 4px solid #667eea;
  background: #f8f9fa;
  border-radius: 0 8px 8px 0;
}

.feature-item h4 {
  margin: 0 0 0.5rem 0;
  color: #495057;
}

.feature-item p {
  margin: 0 0 1rem 0;
  color: #6c757d;
}

.feature-item ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #495057;
}

.feature-item li {
  margin-bottom: 0.25rem;
}

.form-input.error {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}
</style> 