import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Dashboard from '../views/Dashboard.vue'
import Favorites from '../views/Favorites.vue'
import Trends from '../views/Trends.vue'
import Recommendations from '../views/Recommendations.vue'
import Users from '../views/Users.vue'
import Guide from '../views/Guide.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: Favorites,
    meta: { requiresAuth: true }
  },
  {
    path: '/trends',
    name: 'Trends',
    component: Trends,
    meta: { requiresAuth: true } // Si decides reactivar la sección
  },
  {
    path: '/recommendations',
    name: 'Recommendations',
    component: Recommendations,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
    meta: { requiresAuth: true }
  },
  {
    path: '/guide',
    name: 'Guide',
    component: Guide,
    meta: { requiresAuth: false } // Pública
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false, guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false, guestOnly: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  // Rutas privadas
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  // Rutas solo para invitados
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next('/')
    return
  }
  next()
})

export default router 