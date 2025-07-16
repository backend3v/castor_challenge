<template>
  <div class="trends">
    <div class="page-header">
      <h1>📊 Tendencias</h1>
      <p>Explora videos trending y análisis de tendencias</p>
    </div>

    <!-- Filters -->
    <div class="card">
      <h3>🔍 Filtros</h3>
      <div class="filters">
        <div class="form-group">
          <label class="form-label">Región</label>
          <select v-model="filters.region_code" class="form-input">
            <option value="US">Estados Unidos</option>
            <option value="ES">España</option>
            <option value="MX">México</option>
            <option value="AR">Argentina</option>
            <option value="CO">Colombia</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Máximo de resultados</label>
          <input v-model="filters.max_results" type="number" class="form-input" min="1" max="50">
        </div>
        <button @click="loadTrends" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Cargando...' : 'Cargar Tendencias' }}
        </button>
      </div>
    </div>

    <!-- Trends List -->
    <div v-if="trends.length > 0" class="card">
      <h3>🔥 Videos Trending</h3>
      <div class="trends-grid">
        <div v-for="trend in trends" :key="trend.id" class="trend-item">
          <div class="trend-header">
            <h4>{{ trend.title }}</h4>
            <span class="trend-category">{{ getCategoryName(trend.category_id) }}</span>
          </div>
          <div class="trend-content">
            <img v-if="trend.thumbnail_url" :src="trend.thumbnail_url" :alt="trend.title" class="trend-thumbnail">
            <div class="trend-details">
              <p><strong>Canal:</strong> {{ trend.channel_title }}</p>
              <p><strong>Vistas:</strong> {{ formatNumber(trend.view_count) }}</p>
              <p><strong>Likes:</strong> {{ formatNumber(trend.like_count) }}</p>
              <p><strong>Comentarios:</strong> {{ formatNumber(trend.comment_count) }}</p>
              <p><strong>Publicado:</strong> {{ formatDate(trend.published_at) }}</p>
            </div>
          </div>
          <div class="trend-actions">
            <a :href="`https://youtube.com/watch?v=${trend.video_id}`" target="_blank" class="btn btn-secondary btn-sm">
              📺 Ver en YouTube
            </a>
            <button @click="addToFavorites(trend)" class="btn btn-primary btn-sm">
              ❤️ Agregar a Favoritos
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Analysis -->
    <div class="card">
      <h3>📈 Análisis de Tendencias</h3>
      <div class="analysis-controls">
        <div class="form-group">
          <label class="form-label">Días hacia atrás</label>
          <input v-model="analysisFilters.days_back" type="number" class="form-input" min="1" max="30">
        </div>
        <button @click="loadAnalysis" class="btn btn-secondary" :disabled="loadingAnalysis">
          {{ loadingAnalysis ? 'Analizando...' : 'Obtener Análisis' }}
        </button>
      </div>

      <div v-if="analysis" class="analysis-results">
        <div class="stats-grid">
          <div class="stat-card">
            <h4>📊 Total de Videos</h4>
            <p class="stat-number">{{ analysis.total_videos }}</p>
          </div>
          <div class="stat-card">
            <h4>👀 Total de Vistas</h4>
            <p class="stat-number">{{ formatNumber(analysis.total_views) }}</p>
          </div>
          <div class="stat-card">
            <h4>📈 Promedio de Vistas</h4>
            <p class="stat-number">{{ formatNumber(analysis.avg_views) }}</p>
          </div>
        </div>

        <div v-if="analysis.top_categories" class="analysis-section">
          <h4>🏆 Categorías Más Populares</h4>
          <div class="categories-list">
            <div v-for="category in analysis.top_categories" :key="category.category_id" class="category-item">
              <span class="category-name">{{ category.name }}</span>
              <span class="category-count">{{ category.count }} videos</span>
            </div>
          </div>
        </div>

        <div v-if="analysis.top_channels" class="analysis-section">
          <h4>🎬 Canales Más Populares</h4>
          <div class="channels-list">
            <div v-for="channel in analysis.top_channels" :key="channel.channel" class="channel-item">
              <span class="channel-name">{{ channel.channel }}</span>
              <span class="channel-stats">{{ channel.videos }} videos, {{ formatNumber(channel.total_views) }} vistas</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      Cargando tendencias...
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Trends',
  data() {
    return {
      loading: false,
      loadingAnalysis: false,
      trends: [],
      analysis: null,
      filters: {
        region_code: 'US',
        max_results: 10
      },
      analysisFilters: {
        days_back: 7
      },
      categories: {
        1: 'Film & Animation',
        2: 'Autos & Vehicles',
        10: 'Music',
        15: 'Pets & Animals',
        17: 'Sports',
        19: 'Travel & Events',
        20: 'Gaming',
        22: 'People & Blogs',
        23: 'Comedy',
        24: 'Entertainment',
        25: 'News & Politics',
        26: 'Howto & Style',
        27: 'Education',
        28: 'Science & Technology',
        29: 'Nonprofits & Activism'
      }
    }
  },
  mounted() {
    this.loadTrends()
  },
  methods: {
    async loadTrends() {
      this.loading = true
      try {
        const response = await apiService.getTrends(this.filters)
        this.trends = response.data.trends || []
      } catch (err) {
        console.error('Error loading trends:', err)
        this.trends = []
      } finally {
        this.loading = false
      }
    },

    async loadAnalysis() {
      this.loadingAnalysis = true
      try {
        const response = await apiService.getTrendAnalysis({
          ...this.filters,
          ...this.analysisFilters
        })
        this.analysis = response.data.analysis
      } catch (err) {
        console.error('Error loading analysis:', err)
        this.analysis = null
      } finally {
        this.loadingAnalysis = false
      }
    },

    async addToFavorites(trend) {
      const userId = prompt('Ingresa el ID del usuario:')
      if (!userId) return

      try {
        const favoriteData = {
          user_id: parseInt(userId),
          video_id: trend.video_id,
          title: trend.title,
          description: trend.description || '',
          url: `https://youtube.com/watch?v=${trend.video_id}`,
          thumbnail: trend.thumbnail_url,
          channel: trend.channel_title,
          duration: '',
          published_at: trend.published_at
        }
        
        await apiService.addFavorite(favoriteData)
        alert('Video agregado a favoritos exitosamente!')
      } catch (err) {
        alert('Error al agregar a favoritos: ' + (err.response?.data?.message || err.message))
      }
    },

    getCategoryName(categoryId) {
      return this.categories[categoryId] || 'Sin categoría'
    },

    formatNumber(num) {
      if (!num) return '0'
      return new Intl.NumberFormat('es-ES').format(num)
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

.filters {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.trends-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.trend-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  background: #f8f9fa;
}

.trend-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.trend-header h4 {
  margin: 0;
  color: #495057;
  font-size: 1.1rem;
  flex: 1;
}

.trend-category {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  white-space: nowrap;
}

.trend-content {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.trend-thumbnail {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 4px;
}

.trend-details {
  flex: 1;
}

.trend-details p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

.trend-actions {
  display: flex;
  gap: 0.5rem;
}

.analysis-controls {
  display: flex;
  gap: 1rem;
  align-items: end;
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.stat-card h4 {
  margin: 0 0 0.5rem 0;
  color: #495057;
  font-size: 1rem;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  margin: 0;
}

.analysis-section {
  margin-bottom: 2rem;
}

.analysis-section h4 {
  margin-bottom: 1rem;
  color: #495057;
}

.categories-list, .channels-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-item, .channel-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.category-name, .channel-name {
  font-weight: 500;
}

.category-count, .channel-stats {
  color: #6c757d;
  font-size: 0.9rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}
</style> 