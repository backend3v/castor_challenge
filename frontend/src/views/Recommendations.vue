<template>
  <div class="recommendations">
    <div class="page-header">
      <h1>🎯 Recomendaciones</h1>
      <p>Sistema de recomendaciones personalizadas</p>
    </div>

    <!-- User Selection -->
    <div class="card">
      <h3>👤 Seleccionar Usuario</h3>
      <div class="user-selection">
        <div class="form-group">
          <label class="form-label">ID de Usuario</label>
          <input v-model="selectedUserId" type="number" class="form-input" placeholder="1">
        </div>
        <button @click="loadRecommendations" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Cargando...' : 'Obtener Recomendaciones' }}
        </button>
      </div>
    </div>

    <!-- Preferences Management -->
    <div class="card">
      <h3>⚙️ Gestión de Preferencias</h3>
      <div class="preferences-form">
        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Categorías Preferidas (IDs separados por comas)</label>
            <input v-model="preferences.preferred_categories" type="text" class="form-input" placeholder="20,24,28">
          </div>
          <div class="form-group">
            <label class="form-label">Canales Preferidos (separados por comas)</label>
            <input v-model="preferences.preferred_channels" type="text" class="form-input" placeholder="channel1,channel2">
          </div>
          <div class="form-group">
            <label class="form-label">Duración Máxima (minutos)</label>
            <input v-model="preferences.max_duration_minutes" type="number" class="form-input" placeholder="30">
          </div>
          <div class="form-group">
            <label class="form-label">Idioma</label>
            <select v-model="preferences.language" class="form-input">
              <option value="es">Español</option>
              <option value="en">Inglés</option>
              <option value="fr">Francés</option>
            </select>
          </div>
        </div>
        <button @click="updatePreferences" class="btn btn-secondary" :disabled="updatingPreferences">
          {{ updatingPreferences ? 'Actualizando...' : 'Actualizar Preferencias' }}
        </button>
      </div>
    </div>

    <!-- Recommendations List -->
    <div v-if="recommendations.length > 0" class="card">
      <h3>🎯 Recomendaciones Personalizadas</h3>
      <div class="recommendations-grid">
        <div v-for="rec in recommendations" :key="rec.id" class="recommendation-item">
          <div class="recommendation-header">
            <h4>{{ rec.title }}</h4>
            <span class="score">Score: {{ (rec.score * 100).toFixed(1) }}%</span>
          </div>
          <div class="recommendation-content">
            <img v-if="rec.thumbnail_url" :src="rec.thumbnail_url" :alt="rec.title" class="rec-thumbnail">
            <div class="rec-details">
              <p><strong>Canal:</strong> {{ rec.channel_title }}</p>
              <p><strong>Publicado:</strong> {{ formatDate(rec.published_at) }}</p>
              <p><strong>Razón:</strong> {{ rec.reason }}</p>
            </div>
          </div>
          <div class="recommendation-actions">
            <a :href="`https://youtube.com/watch?v=${rec.video_id}`" target="_blank" class="btn btn-secondary btn-sm">
              📺 Ver en YouTube
            </a>
            <button @click="recordView(rec)" class="btn btn-primary btn-sm">
              👁️ Marcar como Visto
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Record View -->
    <div class="card">
      <h3>📝 Registrar Visualización</h3>
      <div class="view-form">
        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">ID de Usuario</label>
            <input v-model="viewData.user_id" type="number" class="form-input" placeholder="1">
          </div>
          <div class="form-group">
            <label class="form-label">ID del Video</label>
            <input v-model="viewData.video_id" type="text" class="form-input" placeholder="dQw4w9WgXcQ">
          </div>
          <div class="form-group">
            <label class="form-label">Título del Video</label>
            <input v-model="viewData.title" type="text" class="form-input" placeholder="Título del video">
          </div>
          <div class="form-group">
            <label class="form-label">Duración de Visualización (segundos)</label>
            <input v-model="viewData.watch_duration_seconds" type="number" class="form-input" placeholder="300">
          </div>
          <div class="form-group">
            <label class="form-label">¿Completado?</label>
            <select v-model="viewData.completed" class="form-input">
              <option :value="true">Sí</option>
              <option :value="false">No</option>
            </select>
          </div>
        </div>
        <button @click="recordViewData" class="btn btn-primary" :disabled="recordingView">
          {{ recordingView ? 'Registrando...' : 'Registrar Visualización' }}
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && recommendations.length === 0" class="card empty-state">
      <h3>📭 No hay recomendaciones</h3>
      <p>Configura tus preferencias y obtén recomendaciones personalizadas.</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      Generando recomendaciones...
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Recommendations',
  data() {
    return {
      loading: false,
      updatingPreferences: false,
      recordingView: false,
      selectedUserId: 1,
      recommendations: [],
      preferences: {
        user_id: 1,
        preferred_categories: '',
        preferred_channels: '',
        max_duration_minutes: 30,
        language: 'es'
      },
      viewData: {
        user_id: 1,
        video_id: '',
        title: '',
        watch_duration_seconds: 300,
        completed: true
      }
    }
  },
  mounted() {
    this.loadRecommendations()
  },
  methods: {
    async loadRecommendations() {
      if (!this.selectedUserId) return
      
      this.loading = true
      try {
        const response = await apiService.getRecommendations(this.selectedUserId, { max_results: 10 })
        this.recommendations = response.data.recommendations || []
      } catch (err) {
        console.error('Error loading recommendations:', err)
        this.recommendations = []
      } finally {
        this.loading = false
      }
    },

    async updatePreferences() {
      if (!this.preferences.user_id) {
        alert('Por favor ingresa un ID de usuario')
        return
      }

      this.updatingPreferences = true
      try {
        const preferencesData = {
          ...this.preferences,
          preferred_categories: this.preferences.preferred_categories ? 
            this.preferences.preferred_categories.split(',').map(id => parseInt(id.trim())) : [],
          preferred_channels: this.preferences.preferred_channels ? 
            this.preferences.preferred_channels.split(',').map(channel => channel.trim()) : []
        }
        
        await apiService.updatePreferences(preferencesData)
        alert('Preferencias actualizadas exitosamente!')
        this.loadRecommendations()
      } catch (err) {
        alert('Error al actualizar preferencias: ' + (err.response?.data?.message || err.message))
      } finally {
        this.updatingPreferences = false
      }
    },

    async recordView(recommendation) {
      const viewData = {
        user_id: this.selectedUserId,
        video_id: recommendation.video_id,
        title: recommendation.title,
        watch_duration_seconds: 300,
        completed: true
      }
      
      try {
        await apiService.recordView(viewData)
        alert('Visualización registrada exitosamente!')
      } catch (err) {
        alert('Error al registrar visualización: ' + (err.response?.data?.message || err.message))
      }
    },

    async recordViewData() {
      if (!this.viewData.user_id || !this.viewData.video_id || !this.viewData.title) {
        alert('Por favor completa todos los campos obligatorios')
        return
      }

      this.recordingView = true
      try {
        await apiService.recordView(this.viewData)
        alert('Visualización registrada exitosamente!')
        this.viewData = {
          user_id: this.selectedUserId,
          video_id: '',
          title: '',
          watch_duration_seconds: 300,
          completed: true
        }
      } catch (err) {
        alert('Error al registrar visualización: ' + (err.response?.data?.message || err.message))
      } finally {
        this.recordingView = false
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
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

.user-selection {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.recommendation-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  background: #f8f9fa;
}

.recommendation-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.recommendation-header h4 {
  margin: 0;
  color: #495057;
  font-size: 1.1rem;
  flex: 1;
}

.score {
  background: #28a745;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.recommendation-content {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.rec-thumbnail {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 4px;
}

.rec-details {
  flex: 1;
}

.rec-details p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

.recommendation-actions {
  display: flex;
  gap: 0.5rem;
}

.view-form {
  text-align: left;
}

.empty-state {
  text-align: center;
  color: #6c757d;
}

.empty-state h3 {
  margin-bottom: 0.5rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}
</style> 