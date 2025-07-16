<template>
  <div class="favorites">
    <div class="page-header">
      <h1>❤️ Mis Favoritos</h1>
      <p>Gestiona tus videos favoritos de YouTube</p>
    </div>

    <!-- Add Favorite Form -->
    <div class="card">
      <h3>➕ Agregar Video Favorito</h3>
      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">ID de Usuario</label>
          <input v-model="newFavorite.user_id" type="number" class="form-input" placeholder="1">
        </div>
        <div class="form-group">
          <label class="form-label">ID del Video (YouTube)</label>
          <input v-model="newFavorite.video_id" type="text" class="form-input" placeholder="dQw4w9WgXcQ">
        </div>
        <div class="form-group">
          <label class="form-label">Título</label>
          <input v-model="newFavorite.title" type="text" class="form-input" placeholder="Título del video">
        </div>
        <div class="form-group">
          <label class="form-label">Descripción</label>
          <textarea v-model="newFavorite.description" class="form-input" placeholder="Descripción del video"></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">URL</label>
          <input v-model="newFavorite.url" type="url" class="form-input" placeholder="https://youtube.com/watch?v=...">
        </div>
        <div class="form-group">
          <label class="form-label">Thumbnail</label>
          <input v-model="newFavorite.thumbnail" type="url" class="form-input" placeholder="https://...">
        </div>
        <div class="form-group">
          <label class="form-label">Canal</label>
          <input v-model="newFavorite.channel" type="text" class="form-input" placeholder="Nombre del canal">
        </div>
        <div class="form-group">
          <label class="form-label">Duración</label>
          <input v-model="newFavorite.duration" type="text" class="form-input" placeholder="10:30">
        </div>
        <div class="form-group">
          <label class="form-label">Fecha de Publicación</label>
          <input v-model="newFavorite.published_at" type="datetime-local" class="form-input">
        </div>
        <div class="form-group">
          <label class="form-label">Notas</label>
          <textarea v-model="newFavorite.notes" class="form-input" placeholder="Notas personales"></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Etiquetas (separadas por comas)</label>
          <input v-model="newFavorite.tags" type="text" class="form-input" placeholder="música, entretenimiento, tutorial">
        </div>
      </div>
      <button @click="addFavorite" class="btn btn-primary" :disabled="addingFavorite">
        {{ addingFavorite ? 'Agregando...' : 'Agregar a Favoritos' }}
      </button>
    </div>

    <!-- User Selection -->
    <div class="card">
      <h3>👤 Seleccionar Usuario</h3>
      <div class="user-selection">
        <div class="form-group">
          <label class="form-label">ID de Usuario</label>
          <input v-model="selectedUserId" type="number" class="form-input" placeholder="1">
        </div>
        <button @click="loadFavorites" class="btn btn-secondary" :disabled="loading">
          {{ loading ? 'Cargando...' : 'Cargar Favoritos' }}
        </button>
      </div>
    </div>

    <!-- Favorites List -->
    <div v-if="favorites.length > 0" class="card">
      <h3>📋 Lista de Favoritos</h3>
      <div class="favorites-grid">
        <div v-for="favorite in favorites" :key="favorite.id" class="favorite-item">
          <div class="favorite-header">
            <h4>{{ favorite.title }}</h4>
            <button @click="removeFavorite(favorite.user_id, favorite.video_id)" class="btn btn-danger btn-sm">
              🗑️ Eliminar
            </button>
          </div>
          <div class="favorite-content">
            <img v-if="favorite.thumbnail" :src="favorite.thumbnail" :alt="favorite.title" class="favorite-thumbnail">
            <div class="favorite-details">
              <p><strong>Canal:</strong> {{ favorite.channel }}</p>
              <p><strong>Duración:</strong> {{ favorite.duration }}</p>
              <p><strong>Agregado:</strong> {{ formatDate(favorite.added_at) }}</p>
              <p v-if="favorite.notes"><strong>Notas:</strong> {{ favorite.notes }}</p>
              <div v-if="favorite.tags && favorite.tags.length > 0" class="tags">
                <span v-for="tag in favorite.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
          </div>
          <a :href="favorite.url" target="_blank" class="btn btn-secondary btn-sm">
            📺 Ver en YouTube
          </a>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading" class="card empty-state">
      <h3>📭 No hay favoritos</h3>
      <p>Agrega algunos videos a tus favoritos para verlos aquí.</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      Cargando favoritos...
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Favorites',
  data() {
    return {
      loading: false,
      addingFavorite: false,
      selectedUserId: 1,
      favorites: [],
      newFavorite: {
        user_id: 1,
        video_id: '',
        title: '',
        description: '',
        url: '',
        thumbnail: '',
        channel: '',
        duration: '',
        published_at: '',
        notes: '',
        tags: ''
      }
    }
  },
  mounted() {
    this.loadFavorites()
  },
  methods: {
    async loadFavorites() {
      if (!this.selectedUserId) return
      
      this.loading = true
      try {
        const response = await apiService.getFavorites(this.selectedUserId)
        this.favorites = response.data.favorites || []
      } catch (err) {
        console.error('Error loading favorites:', err)
        this.favorites = []
      } finally {
        this.loading = false
      }
    },

    async addFavorite() {
      if (!this.newFavorite.video_id || !this.newFavorite.title) {
        alert('Por favor completa al menos el ID del video y el título')
        return
      }

      this.addingFavorite = true
      try {
        const favoriteData = {
          ...this.newFavorite,
          tags: this.newFavorite.tags ? this.newFavorite.tags.split(',').map(tag => tag.trim()) : []
        }
        
        await apiService.addFavorite(favoriteData)
        alert('Video agregado a favoritos exitosamente!')
        this.resetForm()
        this.loadFavorites()
      } catch (err) {
        alert('Error al agregar favorito: ' + (err.response?.data?.message || err.message))
      } finally {
        this.addingFavorite = false
      }
    },

    async removeFavorite(userId, videoId) {
      if (!confirm('¿Estás seguro de que quieres eliminar este favorito?')) return

      try {
        await apiService.removeFavorite(userId, videoId)
        alert('Favorito eliminado exitosamente!')
        this.loadFavorites()
      } catch (err) {
        alert('Error al eliminar favorito: ' + (err.response?.data?.message || err.message))
      }
    },

    resetForm() {
      this.newFavorite = {
        user_id: this.selectedUserId,
        video_id: '',
        title: '',
        description: '',
        url: '',
        thumbnail: '',
        channel: '',
        duration: '',
        published_at: '',
        notes: '',
        tags: ''
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
</style> 