# Configuración de YouTube Data API v3

## Pasos para obtener la API Key

### 1. Crear un proyecto en Google Cloud Console
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la facturación para el proyecto (requerido para YouTube Data API)

### 2. Habilitar YouTube Data API v3
1. En la consola de Google Cloud, ve a "APIs & Services" > "Library"
2. Busca "YouTube Data API v3"
3. Haz clic en "Enable"

### 3. Crear credenciales
1. Ve a "APIs & Services" > "Credentials"
2. Haz clic en "Create Credentials" > "API Key"
3. Copia la API key generada

### 4. Configurar la API Key en la aplicación
1. Abre el archivo `backend/env`
2. Reemplaza `your_youtube_api_key_here` con tu API key real:
   ```
   YOUTUBE_API_KEY=TU_API_KEY_AQUI
   ```

### 5. Configurar restricciones (opcional pero recomendado)
1. En Google Cloud Console, ve a "APIs & Services" > "Credentials"
2. Haz clic en tu API key
3. En "Application restrictions", selecciona "HTTP referrers"
4. Agrega tu dominio: `http://localhost:3000/*`
5. En "API restrictions", selecciona "Restrict key"
6. Selecciona "YouTube Data API v3"

## Verificación

Para verificar que la API está funcionando:

1. Reinicia el servidor Flask
2. Ve a la página de tendencias en el frontend
3. Deberías ver videos reales de YouTube en lugar de datos mock

## Límites de la API

- **Cuota gratuita**: 10,000 unidades por día
- **Cada búsqueda**: 100 unidades
- **Cada video trending**: 1 unidad
- **Cada categoría**: 1 unidad

## Solución de problemas

### Error: "YouTube API key not configured"
- Verifica que la variable `YOUTUBE_API_KEY` esté configurada en el archivo `env`
- Asegúrate de que el archivo `env` esté en la carpeta `backend/`

### Error: "API key not valid"
- Verifica que la API key sea correcta
- Asegúrate de que YouTube Data API v3 esté habilitada en tu proyecto

### Error: "Quota exceeded"
- Has excedido el límite diario de la API
- Considera actualizar a un plan de pago o esperar hasta el siguiente día

### Fallback a datos mock
- Si la API falla, la aplicación automáticamente usa datos mock
- Revisa los logs del servidor para ver el error específico 