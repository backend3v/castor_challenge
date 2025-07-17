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
            placeholder="1"
            min="1"
          >
        </div>
        <button @click="getUser" class="btn btn-secondary" :disabled="loadingUser">
          {{ loadingUser ? 'Buscando...' : 'Buscar por ID' }}
        </button>
      </div>
      
      <!-- Search by name -->
      <div class="user-search">
        <div class="form-group">
          <label class="form-label">Nombre de Usuario</label>
          <input 
            v-model="searchUserName" 
            type="text" 
            class="form-input" 
            placeholder="Nombre completo o parcial"
            maxlength="100"
          >
        </div>
        <button @click="searchUserByName" class="btn btn-secondary" :disabled="searchingByName">
          {{ searchingByName ? 'Buscando...' : 'Buscar por Nombre' }}
        </button>
      </div>
      
      <!-- Get all users -->
      <div class="user-search get-all-users-section">
        <button @click="getAllUsers" class="btn btn-primary" :disabled="loadingAllUsers">
          {{ loadingAllUsers ? 'Cargando...' : '📋 Consultar Todos los Usuarios' }}
        </button>
      </div>
    </div>

    <!-- User Details -->
    <div v-if="userDetails && !Array.isArray(userDetails)" class="card">
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

    <!-- Multiple Users Results -->
    <div v-if="Array.isArray(userDetails) && userDetails.length > 0" class="card">
      <h3>👥 Resultados de Búsqueda ({{ userDetails.length }} usuarios)</h3>
      <div class="users-list">
        <div v-for="user in userDetails" :key="user.id" class="user-item">
          <div class="user-info">
            <div class="user-name">{{ user.name }}</div>
            <div class="user-email">{{ user.email }}</div>
            <div class="user-meta">
              <span class="user-id">ID: {{ user.id }}</span>
              <span :class="user.active ? 'status-active' : 'status-inactive'">
                {{ user.active ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Results Message -->
    <div v-if="Array.isArray(userDetails) && userDetails.length === 0" class="card">
      <h3>🔍 No se encontraron usuarios</h3>
      <p>No se encontraron usuarios que coincidan con tu búsqueda.</p>
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
      searchingByName: false,
      loadingAllUsers: false,
      searchUserId: '',
      searchUserName: '',
      userDetails: null,
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
        console.log('Buscando usuario con ID:', this.searchUserId)
        const response = await apiService.getUser(this.searchUserId)
        console.log('Respuesta del servidor:', response.data)
        this.userDetails = response.data.user
        if (!this.userDetails) {
          alert('No se encontró ningún usuario con ese ID.')
        }
      } catch (err) {
        console.error('Error al buscar usuario:', err)
        alert('Error al buscar usuario: ' + (err.response?.data?.message || err.message))
        this.userDetails = null
      } finally {
        this.loadingUser = false
      }
    },

    async searchUserByName() {
      if (!this.searchUserName) {
        alert('Por favor ingresa un nombre de usuario para buscar')
        return
      }

      this.searchingByName = true
      try {
        console.log('Buscando usuario con nombre:', this.searchUserName)
        const response = await apiService.searchUsers(this.searchUserName)
        console.log('Respuesta del servidor:', response.data)
        this.userDetails = response.data.users
        if (this.userDetails.length === 0) {
          alert('No se encontró ningún usuario con ese nombre.')
        }
      } catch (err) {
        console.error('Error al buscar usuario por nombre:', err)
        alert('Error al buscar usuario por nombre: ' + (err.response?.data?.message || err.message))
        this.userDetails = null
      } finally {
        this.searchingByName = false
      }
    },

    async getAllUsers() {
      this.loadingAllUsers = true
      try {
        console.log('Obteniendo todos los usuarios')
        const response = await apiService.getAllUsers()
        console.log('Respuesta del servidor:', response.data)
        this.userDetails = response.data.users
        if (this.userDetails.length === 0) {
          alert('No hay usuarios registrados en el sistema.')
        }
      } catch (err) {
        console.error('Error al obtener usuarios:', err)
        alert('Error al obtener usuarios: ' + (err.response?.data?.message || err.message))
        this.userDetails = null
      } finally {
        this.loadingAllUsers = false
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
  margin-bottom: 1rem;
}

.user-search.get-all-users-section {
  margin-top: 1rem;
  margin-bottom: 1.5rem;
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

.users-list {
  display: grid;
  gap: 1rem;
}

.user-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  transition: all 0.2s ease;
}

.user-item:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.user-info {
  display: grid;
  gap: 0.5rem;
}

.user-name {
  font-weight: bold;
  font-size: 1.1rem;
  color: #495057;
}

.user-email {
  color: #6c757d;
  font-size: 0.9rem;
}

.user-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
  font-size: 0.85rem;
}

.user-id {
  color: #6c757d;
  font-weight: 500;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style> 