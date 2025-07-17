<template>
  <header class="app-header">
    <div class="header-content">
      <div class="logo-section">
        <img 
          src="../assets/castor_evolucion_digital_logo.png" 
          alt="Castor Evolución Digital" 
          class="logo"
        />
        <h1 class="app-title">Castor Challenge</h1>
      </div>
      
      <nav class="main-nav">
        <router-link 
          v-for="item in visibleNavItems" 
          :key="item.path"
          :to="item.path" 
          class="nav-link"
          :class="{ active: $route.path === item.path }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-text">{{ item.name }}</span>
        </router-link>
      </nav>
      
      <div class="user-section">
        <div v-if="authStore.isAuthenticated" class="user-info">
          <span class="user-name">{{ authStore.user?.name || 'Usuario' }}</span>
          <button @click="handleLogout" class="logout-btn">
            <span class="logout-icon">🚪</span>
            <span class="logout-text">Salir</span>
          </button>
        </div>
        <div v-else class="auth-buttons">
          <router-link to="/login" class="auth-btn login-btn">
            Iniciar Sesión
          </router-link>
          <router-link to="/register" class="auth-btn register-btn">
            Registrarse
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'AppHeader',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    // Volver a agregar Tendencias al menú
    const navItems = [
      { path: '/', name: 'Dashboard', icon: '🏠', requiresAuth: true },
      { path: '/favorites', name: 'Favoritos', icon: '❤️', requiresAuth: true },
      { path: '/trends', name: 'Tendencias', icon: '📊', requiresAuth: true },
      { path: '/recommendations', name: 'Recomendaciones', icon: '🎯', requiresAuth: true },
      { path: '/users', name: 'Usuarios', icon: '👥', requiresAuth: true },
      { path: '/guide', name: 'Guía', icon: '📖', requiresAuth: false }
    ]
    
    const visibleNavItems = computed(() => {
      if (authStore.isAuthenticated) {
        // Solo muestra secciones privadas si está logueado
        return navItems
      } else {
        // Solo muestra públicas
        return navItems.filter(item => !item.requiresAuth)
      }
    })
    
    const handleLogout = async () => {
      try {
        authStore.logout()
        router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    
    return {
      authStore,
      visibleNavItems,
      handleLogout
    }
  }
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  height: 40px;
  width: auto;
  filter: brightness(0) invert(1);
}

.app-title {
  font-size: 1.1rem; /* Reducido */
  font-weight: 600;
  margin: 0;
  margin-right: 2.5rem; /* Más espacio a la derecha */
  white-space: nowrap;
}

.main-nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.nav-icon {
  font-size: 1.2rem;
}

.nav-text {
  font-size: 0.9rem;
}

.user-section {
  display: flex;
  align-items: center;
  margin-left: 1.5rem; /* Separación extra del menú */
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  font-weight: 500;
  color: white;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.logout-icon {
  font-size: 1rem;
}

.logout-text {
  font-weight: 500;
}

.auth-buttons {
  display: flex;
  gap: 0.5rem;
}

.auth-btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.login-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.register-btn {
  background: white;
  color: #667eea;
  border: 1px solid white;
}

.register-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .main-nav {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .nav-text {
    display: none;
  }
  
  .nav-link {
    padding: 0.5rem;
  }
  
  .user-section {
    width: 100%;
    justify-content: center;
  }
  
  .user-info {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .auth-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .auth-btn {
    text-align: center;
  }
}
</style> 