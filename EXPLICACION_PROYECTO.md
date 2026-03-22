# 📘 Explicación Técnica: Migración y Configuración (Backend + Aiven)

Este documento explica las decisiones técnicas tomadas para el despliegue y la migración masiva de datos del proyecto "Análisis Portal de Empleo".

## 1. ¿Por qué elegimos Aiven Cloud?

Aiven fue seleccionado sobre otras alternativas (como Neon o Supabase) por las siguientes razones:
- **PostgreSQL Gestionado**: Ofrece un entorno PostgreSQL 15+ puro, ideal para el tipo de datos complejo (TSVECTOR, JSONB) que maneja este proyecto.
- **Fiabilidad en Render**: Aiven tiene una latencia mínima con los centros de datos de Render, lo que asegura que la API responda rápido.
- **Panel de Control Robusto**: Permite monitorear métricas, conexiones y logs de forma clara, facilitando el diagnóstico de errores.

## 2. Metodología de Migración (Sincronización de Datos)

El mayor reto fue subir **266,234 registros** sin volver a ejecutar el scraping (lo cual tardaría semanas).

### Desafíos Superados:
1. **Incompatibilidad de Drivers**: Los drivers estándar de Python a veces fallan al enviar fechas o decimales complejos a través de conexiones SSL estrictas como las de Aiven.
2. **Límites de Conexión**: La capa gratuita de Aiven tiene un límite de conexiones simultáneas. Ejecutar muchos scripts a la vez causa errores "TooManyConnections".

### Solución Implementada (`migrate_definitive.py`):
- **Adaptación Manual de Tipos**: Usamos una función llamada `adapt_value` que convierte automáticamente:
  - `datetime` y `date` -> a strings en formato ISO (YYYY-MM-DD).
  - `Decimal` -> a flotantes de Python.
  - `dict` y `list` (columna `detalles_prestador`) -> a strings JSON.
- **Inserción por Lotes (Chunks)**: En lugar de subir registro por registro (lento) o todos de golpe (falla por tamaño), los subimos en grupos de 500.
- **Manejo de Conflictos**: Usando `ON CONFLICT (codigo_vacante) DO NOTHING`, el script puede re-ejecutarse sin duplicar datos y sin dar errores de "ID ya existe".

## 3. Archivos de Configuración Clave

- **`.env`**:
  - `DATABASE_URL`: Versión `asyncpg` para la API de Render.
  - El script de migración la convierte automáticamente a la versión `psycopg2` para mayor estabilidad en la carga masiva.
- **`db/session.py`**: Configurado para forzar `sslmode=require` en Aiven, garantizando seguridad en la transmisión.
- **`api/main.py`**: Configurado para funcionar con el prefijo `/api/v1` en Render.

## 4. Cómo Correr el Scraping de Nuevo

### Opción A: Local (Para Pruebas)
1. Asegúrate de que tu `.env` apunte a tu base de datos local o la de Aiven (según prefieras).
2. Abre una terminal en la carpeta `backend`.
3. Ejecuta: `.\venv\Scripts\uvicorn.exe api.main:app --reload`.
4. Ve a `localhost:8000/docs` y usa el botón **Execute** en el endpoint de "iniciar".

### Opción B: En la Nube (Recomendado)
El scraper ya está desplegado en Render. Usarlo desde allí es mejor porque el servidor de Render no sufre de las limitaciones de conexión/SSL que tiene una PC personal.
1. Ve a: [https://vacantes-backend-migux.onrender.com/docs](https://vacantes-backend-migux.onrender.com/docs)
2. Busca `POST /api/v1/scraper/iniciar-completo`.
3. Haz clic en **Execute**.

## 🏁 Estado Final y Bloqueo de Aiven

Tras agotar todos los métodos de sincronización, hemos llegado al límite físico de tu base de datos actual:

- **Registros Totales en la Nube**: 121,123.
- **Estado de Aiven**: **READ-ONLY (Solo Lectura)**. 
- **Razón**: Aiven pone las bases de datos en modo "Solo Lectura" cuando detecta que se ha superado el límite de almacenamiento o de operaciones permitidas para el plan gratuito.

---
*Este documento fue generado para documentar el estado final del despliegue en Marzo 2026.*
