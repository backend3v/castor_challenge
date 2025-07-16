# 🎥 Guía de Configuración de YouTube Data API v3

## 📋 Requisitos Previos

1. **Cuenta de Google**: Necesitas una cuenta de Google activa
2. **Proyecto de Google Cloud**: Para acceder a las APIs de Google
3. **Facturación habilitada**: La API de YouTube tiene cuotas gratuitas pero requiere facturación

## 🚀 Pasos para Configurar la API

### 1. Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Anota el **Project ID** - lo necesitarás más adelante

### 2. Habilitar YouTube Data API v3

1. En la consola de Google Cloud, ve a **APIs & Services** > **Library**
2. Busca "YouTube Data API v3"
3. Haz clic en la API y luego en **Enable**

### 3. Configurar Facturación

1. Ve a **Billing** en el menú lateral
2. Vincula tu proyecto con una cuenta de facturación
3. **Importante**: La API tiene cuota gratuita de 10,000 unidades por día

### 4. Crear Credenciales

1. Ve a **APIs & Services** > **Credentials**
2. Haz clic en **Create Credentials** > **API Key**
3. Se generará una clave de API - **¡Guárdala de forma segura!**

### 5. Restringir la Clave de API (Recomendado)

1. Haz clic en la clave de API creada
2. En **Application restrictions**, selecciona **HTTP referrers** o **IP addresses**
3. En **API restrictions**, selecciona **Restrict key** y elige **YouTube Data API v3**
4. Guarda los cambios

## 🔧 Configuración en el Proyecto

### 1. Agregar la Clave al Archivo .env

En tu archivo `backend/.env`, agrega:

```env
YOUTUBE_API_KEY=tu_clave_de_api_aqui
```

### 2. Verificar la Configuración

Ejecuta el backend y prueba el endpoint:

```bash
curl "http://localhost:5000/api/v1/youtube/search?q=python&max_results=5"
```

## 📊 Cuotas y Límites

### Cuota Gratuita Diaria
- **10,000 unidades por día**
- **Costos por operación**:
  - Search: 100 unidades
  - Video details: 1 unidad
  - Trending videos: 1 unidad
  - Categories: 1 unidad

### Ejemplos de Uso
- 100 búsquedas = 10,000 unidades
- 10,000 detalles de video = 10,000 unidades
- 100 búsquedas + 9,000 detalles = 19,000 unidades (excede cuota)

## 🛡️ Mejores Prácticas de Seguridad

### 1. Protección de la Clave
- **Nunca** subas la clave al repositorio
- Usa variables de entorno
- Restringe la clave por IP/dominio

### 2. Manejo de Errores
```python
try:
    videos = youtube_service.search_videos(query)
except Exception as e:
    # Manejar error de cuota excedida
    if "quota" in str(e).lower():
        return {"error": "API quota exceeded"}
```

### 3. Caché de Respuestas
- Implementa caché para reducir llamadas a la API
- Usa Redis o similar para almacenar resultados

## 🔍 Endpoints Disponibles

### Búsqueda de Videos
```
GET /api/v1/youtube/search?q=query&max_results=10
```

### Detalles de Video
```
GET /api/v1/youtube/video/{video_id}
```

### Videos en Tendencia
```
GET /api/v1/youtube/trending?region=US&max_results=20
```

### Categorías de Video
```
GET /api/v1/youtube/categories?region=US
```

## 🚨 Solución de Problemas

### Error: "API key not valid"
- Verifica que la clave esté correcta en el .env
- Asegúrate de que la API esté habilitada
- Revisa las restricciones de la clave

### Error: "Quota exceeded"
- Revisa tu uso diario en Google Cloud Console
- Implementa caché para reducir llamadas
- Considera aumentar la cuota (costo adicional)

### Error: "API not enabled"
- Ve a Google Cloud Console
- Habilita YouTube Data API v3
- Espera unos minutos para que se active

## 📈 Monitoreo y Análisis

### Google Cloud Console
1. Ve a **APIs & Services** > **Dashboard**
2. Selecciona YouTube Data API v3
3. Revisa métricas de uso y errores

### Logs Recomendados
```python
import logging

logging.info(f"YouTube API call: {endpoint} - Quota used: {quota_used}")
```

## 💡 Consejos Adicionales

1. **Desarrollo**: Usa cuota gratuita para desarrollo
2. **Producción**: Monitorea el uso y considera aumentar cuota
3. **Backup**: Ten un plan para cuando se agote la cuota
4. **Caché**: Implementa caché para mejorar rendimiento
5. **Rate Limiting**: Respeta los límites de la API

## 🔗 Enlaces Útiles

- [YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [API Quotas](https://developers.google.com/youtube/v3/getting-started#quota)
- [API Reference](https://developers.google.com/youtube/v3/docs/)

---

**⚠️ Importante**: Esta guía es para configuración local. En producción, usa variables de entorno seguras y considera usar un servicio de gestión de secretos. 