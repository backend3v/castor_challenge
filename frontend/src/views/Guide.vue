<template>
  <div class="guide">
    <div class="page-header">
      <h1>📖 Guía de Uso</h1>
      <p>Documentación completa de Castor Challenge</p>
    </div>

    <!-- Quick Start -->
    <div class="card">
      <h2>🚀 Inicio Rápido</h2>
      <div class="guide-section">
        <h3>1. Verificar Estado del Sistema</h3>
        <p>En el Dashboard, verifica que el backend y la base de datos estén funcionando correctamente.</p>
        
        <h3>2. Crear un Usuario</h3>
        <p>Ve a la sección "Usuarios" y crea un nuevo usuario para comenzar a usar las funcionalidades.</p>
        
        <h3>3. Iniciar Sesión</h3>
        <p>Inicia sesión con tu usuario registrado. Todas las funcionalidades requieren estar autenticado.</p>
        
        <h3>4. Explorar Funcionalidades</h3>
        <p>Navega por las diferentes secciones usando el menú superior. El sistema utiliza automáticamente tu usuario autenticado para todas las acciones, no es necesario ingresar el ID manualmente.</p>
      </div>
    </div>

    <!-- Features Guide -->
    <div class="card">
      <h2>🎯 Funcionalidades Principales</h2>
      
      <div class="feature-guide">
        <div class="feature-item">
          <h3>❤️ Gestión de Favoritos</h3>
          <div class="feature-content">
            <h4>¿Qué hace?</h4>
            <p>Permite guardar y organizar tus videos favoritos de YouTube con metadatos completos.</p>
            
            <h4>¿Cómo usar?</h4>
            <ol>
              <li>Ve a la sección "Favoritos"</li>
              <li>Completa el formulario con los datos del video</li>
              <li>Haz clic en "Agregar a Favoritos"</li>
              <li>Para ver tus favoritos, haz clic en "Cargar Favoritos"</li>
            </ol>
            
            <h4>Campos requeridos:</h4>
            <ul>
              <li><strong>ID del Video:</strong> El ID de YouTube (ej: dQw4w9WgXcQ)</li>
              <li><strong>Título:</strong> Nombre del video</li>
              <li><strong>URL:</strong> Enlace completo del video</li>
              <li><strong>Canal:</strong> Nombre del canal</li>
            </ul>
          </div>
        </div>

        <div class="feature-item">
          <h3>📊 Análisis de Tendencias</h3>
          <div class="feature-content">
            <h4>¿Qué hace?</h4>
            <p>Muestra videos trending de YouTube y proporciona análisis detallados de tendencias.</p>
            
            <h4>¿Cómo usar?</h4>
            <ol>
              <li>Ve a la sección "Tendencias"</li>
              <li>Selecciona la región (ej: US, ES, MX)</li>
              <li>Define el número máximo de resultados</li>
              <li>Haz clic en "Cargar Tendencias"</li>
              <li>Para análisis, configura los días y haz clic en "Obtener Análisis"</li>
            </ol>
            
            <h4>Funcionalidades:</h4>
            <ul>
              <li>Videos trending por región</li>
              <li>Métricas de engagement (vistas, likes, comentarios)</li>
              <li>Análisis de categorías más populares</li>
              <li>Ranking de canales más exitosos</li>
            </ul>
          </div>
        </div>

        <div class="feature-item">
          <h3>🎯 Sistema de Recomendaciones</h3>
          <div class="feature-content">
            <h4>¿Qué hace?</h4>
            <p>Proporciona recomendaciones personalizadas basadas en tus favoritos. Si no tienes favoritos, la lista estará vacía.</p>
            
            <h4>¿Cómo usar?</h4>
            <ol>
              <li>Ve a la sección "Recomendaciones"</li>
              <li>Configura tus preferencias (categorías, canales, duración)</li>
              <li>Haz clic en "Actualizar Preferencias"</li>
              <li>Obtén recomendaciones personalizadas</li>
            </ol>
            
            <h4>Configuración de preferencias:</h4>
            <ul>
              <li><strong>Categorías:</strong> IDs separados por comas (ej: 20,24,28)</li>
              <li><strong>Canales:</strong> Nombres separados por comas</li>
              <li><strong>Duración máxima:</strong> En minutos</li>
              <li><strong>Idioma:</strong> Español, Inglés, Francés</li>
            </ul>
          </div>
        </div>

        <div class="feature-item">
          <h3>👥 Gestión de Usuarios</h3>
          <div class="feature-content">
            <h4>¿Qué hace?</h4>
            <p>Permite crear y gestionar usuarios del sistema.</p>
            
            <h4>¿Cómo usar?</h4>
            <ol>
              <li>Ve a la sección "Usuarios"</li>
              <li>Para crear: Completa nombre y email, haz clic en "Crear Usuario"</li>
              <li>Para buscar: Ingresa el nombre o email del usuario, haz clic en "Buscar Usuario"</li>
            </ol>
          </div>
        </div>
      </div>
    </div>

    <!-- API Reference -->
    <div class="card">
      <h2>🔗 Referencia de API</h2>
      <div class="api-reference">
        <h3>Endpoints Principales</h3>
        
        <div class="endpoint-group">
          <h4>Usuarios</h4>
          <div class="endpoint">
            <code>POST /api/users</code> - Crear usuario
          </div>
          <div class="endpoint">
            <code>GET /api/users/{id}</code> - Obtener usuario
          </div>
          <div class="endpoint">
            <code>GET /api/users/search?name=</code> - Buscar usuario por nombre
          </div>
        </div>

        <div class="endpoint-group">
          <h4>Favoritos</h4>
          <div class="endpoint">
            <code>GET /api/favorites/{user_id}</code> - Obtener favoritos
          </div>
          <div class="endpoint">
            <code>POST /api/favorites</code> - Agregar favorito
          </div>
          <div class="endpoint">
            <code>DELETE /api/favorites/{user_id}/{video_id}</code> - Eliminar favorito
          </div>
        </div>

        <div class="endpoint-group">
          <h4>Tendencias</h4>
          <div class="endpoint">
            <code>GET /api/trends</code> - Obtener videos trending
          </div>
          <div class="endpoint">
            <code>GET /api/trends/analysis</code> - Análisis de tendencias
          </div>
        </div>

        <div class="endpoint-group">
          <h4>Recomendaciones</h4>
          <div class="endpoint">
            <code>GET /api/recommendations/{user_id}</code> - Obtener recomendaciones
          </div>
          <div class="endpoint">
            <code>POST /api/recommendations/preferences</code> - Actualizar preferencias
          </div>
          <div class="endpoint">
            <code>POST /api/recommendations/view</code> - Registrar visualización
          </div>
        </div>
      </div>
    </div>

    <!-- Tips and Tricks -->
    <div class="card">
      <h2>💡 Consejos y Trucos</h2>
      <div class="tips-section">
        <div class="tip-item">
          <h4>🎯 IDs de Categorías de YouTube</h4>
          <ul>
            <li><strong>20:</strong> Gaming</li>
            <li><strong>24:</strong> Entertainment</li>
            <li><strong>28:</strong> Science & Technology</li>
            <li><strong>10:</strong> Music</li>
            <li><strong>17:</strong> Sports</li>
            <li><strong>27:</strong> Education</li>
          </ul>
        </div>

        <div class="tip-item">
          <h4>🔍 Obtener ID de Video de YouTube</h4>
          <p>El ID es la parte después de <code>v=</code> en la URL:</p>
          <code>https://youtube.com/watch?v=<strong>dQw4w9WgXcQ</strong></code>
        </div>

        <div class="tip-item">
          <h4>⚡ Mejores Prácticas</h4>
          <ul>
            <li>Usa siempre el mismo ID de usuario para mantener consistencia</li>
            <li>Configura preferencias específicas para mejores recomendaciones</li>
            <li>Registra visualizaciones para mejorar el algoritmo</li>
            <li>Usa etiquetas descriptivas en tus favoritos</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Troubleshooting -->
    <div class="card">
      <h2>🔧 Solución de Problemas</h2>
      <div class="troubleshooting">
        <div class="problem-item">
          <h4>❌ Error de conexión</h4>
          <p><strong>Síntoma:</strong> "Error de conexión" en el Dashboard</p>
          <p><strong>Solución:</strong> Verifica que el backend esté ejecutándose en el puerto 5000</p>
        </div>

        <div class="problem-item">
          <h4>❌ Error de base de datos</h4>
          <p><strong>Síntoma:</strong> "Database connection failed"</p>
          <p><strong>Solución:</strong> Asegúrate de que MySQL esté corriendo en Docker</p>
        </div>

        <div class="problem-item">
          <h4>❌ No se cargan los datos</h4>
          <p><strong>Síntoma:</strong> Las listas aparecen vacías</p>
          <p><strong>Solución:</strong> Verifica que el ID de usuario sea correcto y que existan datos</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Guide'
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

.guide-section h3 {
  color: #495057;
  margin-bottom: 0.5rem;
}

.guide-section p {
  margin-bottom: 1rem;
  color: #6c757d;
}

.feature-guide {
  display: grid;
  gap: 2rem;
}

.feature-item {
  border-left: 4px solid #667eea;
  padding-left: 1rem;
}

.feature-item h3 {
  color: #495057;
  margin-bottom: 1rem;
}

.feature-content h4 {
  color: #667eea;
  margin: 1rem 0 0.5rem 0;
}

.feature-content p {
  color: #6c757d;
  margin-bottom: 1rem;
}

.feature-content ol, .feature-content ul {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.feature-content li {
  margin-bottom: 0.25rem;
  color: #495057;
}

.api-reference {
  display: grid;
  gap: 1.5rem;
}

.endpoint-group h4 {
  color: #495057;
  margin-bottom: 0.5rem;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 0.5rem;
}

.endpoint {
  background: #f8f9fa;
  padding: 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  font-family: 'Courier New', monospace;
}

.endpoint code {
  color: #667eea;
  font-weight: bold;
}

.tips-section {
  display: grid;
  gap: 1.5rem;
}

.tip-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #28a745;
}

.tip-item h4 {
  color: #495057;
  margin-bottom: 0.5rem;
}

.tip-item ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.tip-item li {
  margin-bottom: 0.25rem;
}

.tip-item code {
  background: #e9ecef;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
}

.troubleshooting {
  display: grid;
  gap: 1rem;
}

.problem-item {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  padding: 1rem;
  border-radius: 8px;
}

.problem-item h4 {
  color: #856404;
  margin-bottom: 0.5rem;
}

.problem-item p {
  margin: 0.25rem 0;
  color: #856404;
}

.problem-item strong {
  color: #495057;
}
</style> 