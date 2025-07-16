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
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path" 
          class="nav-link"
          :class="{ active: $route.path === item.path }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-text">{{ item.name }}</span>
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      navItems: [
        { path: '/', name: 'Dashboard', icon: '🏠' },
        { path: '/favorites', name: 'Favoritos', icon: '❤️' },
        { path: '/trends', name: 'Tendencias', icon: '📊' },
        { path: '/recommendations', name: 'Recomendaciones', icon: '🎯' },
        { path: '/users', name: 'Usuarios', icon: '👥' },
        { path: '/guide', name: 'Guía', icon: '📖' }
      ]
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
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
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
}
</style> 