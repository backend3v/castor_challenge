<template>
  <div class="favorites">
    <div class="page-header">
      <h1 class="favorites-title">❤️ Favoritos</h1>
      <p class="favorites-subtitle">Lista de tus videos favoritos</p>
    </div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="loading" class="loading">Cargando favoritos...</div>
    <div v-else>
      <div v-if="favorites.length === 0" class="empty-message">No tienes videos favoritos aún.</div>
      <div v-else class="favorites-list">
        <div v-for="fav in favorites" :key="fav.id" class="favorite-item">
          <h3 class="favorite-title">{{ fav.title }}</h3>
          <p>{{ fav.description }}</p>
          <a :href="fav.url" target="_blank">Ver en YouTube</a>
          <button @click="removeFavorite(fav.video_id)" class="btn btn-danger btn-sm">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { favoritesService } from '../services/api'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Favorites',
  data() {
    return {
      loading: false,
      favorites: [],
      error: ''
    }
  },
  mounted() {
    this.loadFavorites()
  },
  methods: {
    async loadFavorites() {
      this.loading = true
      try {
        const response = await favoritesService.getFavorites()
        this.favorites = response.favorites || []
      } catch (err) {
        this.error = 'Error al cargar favoritos.'
        this.favorites = []
      } finally {
        this.loading = false
      }
    },
    async removeFavorite(videoId) {
      try {
        await favoritesService.removeFavorite(videoId)
        this.loadFavorites()
      } catch (err) {
        alert('Error al eliminar favorito')
      }
    }
  }
}
</script>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 2rem;
}
.favorites-title {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: bold;
}
.favorites-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
}
.favorite-title {
  font-weight: bold;
  color: #495057;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.user-selection {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.favorite-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  background: #f8f9fa;
}

.favorite-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.favorite-header h4 {
  margin: 0;
  color: #495057;
  font-size: 1.1rem;
}

.favorite-content {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.favorite-thumbnail {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 4px;
}

.favorite-details {
  flex: 1;
}

.favorite-details p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tag {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  color: #6c757d;
}

.empty-state h3 {
  margin-bottom: 0.5rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}
</style> 