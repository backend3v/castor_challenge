<template>
  <div class="users">
    <div class="page-header">
      <h1>👥 Usuarios</h1>
      <p>Gestión de usuarios del sistema</p>
    </div>

    <!-- Create User -->
    <div class="card">
      <h3>➕ Crear Nuevo Usuario</h3>
      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">Nombre</label>
          <input 
            v-model="newUser.name" 
            type="text" 
            class="form-input" 
            :class="{ 'error': errors.name }"
            placeholder="Nombre completo"
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
      </div>
      <button @click="createUser" class="btn btn-primary" :disabled="creatingUser || hasErrors">
        {{ creatingUser ? 'Creando...' : 'Crear Usuario' }}
      </button>
    </div>

    <!-- Get User -->
    <div class="card">
      <h3>🔍 Buscar Usuario</h3>
      <div class="user-search">
        <div class="form-group">
          <label class="form-label">ID de Usuario</label>
          <input 
            v-model="searchUserId" 
            type="number" 
            class="form-input" 
            :class="{ 'error': errors.userId }"
            placeholder="1"
            @blur="validateUserId"
            @input="clearError('userId')"
            min="1"
            required
          >
          <span v-if="errors.userId" class="error-message">{{ errors.userId }}</span>
        </div>
        <button @click="getUser" class="btn btn-secondary" :disabled="loadingUser || errors.userId">
          {{ loadingUser ? 'Buscando...' : 'Buscar Usuario' }}
        </button>
      </div>
    </div>

    <!-- User Details -->
    <div v-if="userDetails" class="card">
      <h3>👤 Detalles del Usuario</h3>
      <div class="user-details">
        <div class="detail-item">
          <strong>ID:</strong> {{ userDetails.id }}
        </div>
        <div class="detail-item">
          <strong>Nombre:</strong> {{ userDetails.name }}
        </div>
        <div class="detail-item">
          <strong>Email:</strong> {{ userDetails.email }}
        </div>
        <div class="detail-item">
          <strong>Creado:</strong> {{ formatDate(userDetails.created_at) }}
        </div>
        <div class="detail-item">
          <strong>Estado:</strong> 
          <span :class="userDetails.active ? 'status-active' : 'status-inactive'">
            {{ userDetails.active ? 'Activo' : 'Inactivo' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Sample Users -->
    <div class="card">
      <h3>📋 Usuarios de Prueba</h3>
      <p>Usa estos IDs para probar las funcionalidades:</p>
      <div class="sample-users">
        <div class="sample-user">
          <strong>ID: 1</strong> - Test User (test@example.com)
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Users',
  data() {
    return {
      creatingUser: false,
      loadingUser: false,
      searchUserId: '',
      userDetails: null,
      newUser: {
        name: '',
        email: ''
      },
      errors: {
        name: '',
        email: '',
        userId: ''
      }
    }
  },
  computed: {
    hasErrors() {
      return Object.values(this.errors).some(error => error !== '');
    }
  },
  methods: {
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
        this.userDetails = response.data.user
      } catch (err) {
        alert('Error al crear usuario: ' + (err.response?.data?.message || err.message))
      } finally {
        this.creatingUser = false
      }
    },

    async getUser() {
      if (!this.searchUserId) {
        alert('Por favor ingresa un ID de usuario')
        return
      }

      this.loadingUser = true
      try {
        const response = await apiService.getUser(this.searchUserId)
        this.userDetails = response.data.user
      } catch (err) {
        alert('Error al buscar usuario: ' + (err.response?.data?.message || err.message))
        this.userDetails = null
      } finally {
        this.loadingUser = false
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
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
    validateUserId() {
      if (!this.searchUserId) {
        this.errors.userId = 'El ID de usuario es requerido';
      } else if (isNaN(this.searchUserId) || parseInt(this.searchUserId) < 1) {
        this.errors.userId = 'El ID de usuario debe ser un número positivo';
      } else {
        this.errors.userId = '';
      }
    },
    clearError(field) {
      this.errors[field] = '';
    }
  }
}
</script>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: bold;
}

.page-header p {
  color: #6c757d;
  font-size: 1.1rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.user-search {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.user-details {
  display: grid;
  gap: 1rem;
}

.detail-item {
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.status-active {
  color: #28a745;
  font-weight: bold;
}

.status-inactive {
  color: #dc3545;
  font-weight: bold;
}

.sample-users {
  margin-top: 1rem;
}

.sample-user {
  padding: 0.75rem;
  background: #e9ecef;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style> 