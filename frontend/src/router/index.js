import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Favorites from '../views/Favorites.vue'
import Trends from '../views/Trends.vue'
import Recommendations from '../views/Recommendations.vue'
import Users from '../views/Users.vue'
import Guide from '../views/Guide.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: Favorites
  },
  {
    path: '/trends',
    name: 'Trends',
    component: Trends
  },
  {
    path: '/recommendations',
    name: 'Recommendations',
    component: Recommendations
  },
  {
    path: '/users',
    name: 'Users',
    component: Users
  },
  {
    path: '/guide',
    name: 'Guide',
    component: Guide
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 