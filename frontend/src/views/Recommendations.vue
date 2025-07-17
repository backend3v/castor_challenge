<template>
  <div class="recommendations">
    <div class="page-header">
      <h1 class="recommendations-title">🎯 Recomendaciones</h1>
      <p class="recommendations-subtitle">Videos recomendados para ti</p>
    </div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="loading" class="loading">Cargando recomendaciones...</div>
    <div v-else>
      <div v-if="recommendations.length === 0" class="empty-message">No hay recomendaciones disponibles.</div>
      <div v-else class="recommendations-list">
        <div v-for="rec in recommendations" :key="rec.id" class="recommendation-item">
          <h3 class="recommendation-title">{{ rec.title }}</h3>
          <p>{{ rec.description }}</p>
          <a :href="rec.url" target="_blank">Ver en YouTube</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { recommendationsService } from '../services/api'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Recommendations',
  data() {
    return {
      loading: false,
      recommendations: [],
      error: ''
    }
  },
  mounted() {
    this.loadRecommendations()
  },
  methods: {
    async loadRecommendations() {
      this.loading = true
      try {
        const response = await recommendationsService.getRecommendations()
        this.recommendations = response.recommendations || []
      } catch (err) {
        this.error = 'Error al cargar recomendaciones.'
        this.recommendations = []
      } finally {
        this.loading = false
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
.recommendations-title {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: bold;
}
.recommendations-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
}
.recommendation-title {
  font-weight: bold;
  color: #495057;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
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

.error-message {
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}
</style> 