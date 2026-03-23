# Documento de Arquitectura — Plataforma BID Analytics 🏛️

Este documento detalla la arquitectura técnica, los flujos de datos y las decisiones de diseño tomadas para cumplir con los requerimientos del BID TDR.

## 1. Arquitectura de Alto Nivel
El sistema sigue una arquitectura moderna de **3 Capas (Three-Tier)** desacoplada:

1.  **Capa de Presentación (Frontend)**: Single Page Application (SPA) reactiva construida con React 19 y Vite 6. Utiliza un paradigma de "Tabbed Dashboard" para separar los dominios analíticos (Territorial, Tendencias, Inclusión, Brechas).
2.  **Capa de Lógica (Backend)**: Micro-servicio basado en FastAPI (Python 3.11) con soporte asíncrono nativo para manejar concurrencia en I/O.
3.  **Capa de Datos**: PostgreSQL 15, optimizado para consultas analíticas pesadas mediante índices Gin en vectores de búsqueda y tipos de datos JSON para metadatos flexibles del prestador.

---

## 2. Flujo de Datos del Scraper (Pipeline)

El proceso de ingesta de datos es el corazón del sistema:

1.  **Client (Httpx)**: Realiza peticiones asíncronas a la API del Gobierno de Colombia. Implementa un **Semáforo de Concurrencia** para garantizar que las peticiones sean secuenciales y un **Back-off exponencial** ante fallos de red.
2.  **Parser**: Transforma el JSON crudo (con llaves inconsistentes como `MESOS_EXPERIENCIA_CARGO`) en un diccionario normalizado que cumple con el esquema del BID.
3.  **Runner (Gestor de Estado)**: 
    *   Mantiene la persistencia de la **Sesión de Scrape**. Si el proceso se detiene (pérdida de luz/internet), retoma automáticamente desde la última página procesada.
    *   Registra KPIs de la sesión: nuevas vacantes, vacantes actualizadas y total registros reportados por la fuente.
4.  **Database (Upsert)**: Utiliza la cláusula `ON CONFLICT (codigo_vacante) DO UPDATE` de PostgreSQL para garantizar que no existan duplicados históricos, manteniendo la base de datos siempre actualizada.

---

## 3. Estrategia de Mapeo Territorial

Para lograr un mapa coroplético fiable del BID sin dependencias externas inestables:

*   **GeoJSON Local**: Servido directamente desde `/frontend/public/colombia.json`.
*   **Normalización de Nombres**: Se implementó una función de limpieza de strings que elimina tildes, mayúsculas/minúsculas y variaciones comunes (ej: "BOGOTÁ D.C." → "BOGOTA DC") para asegurar que los datos del backend se "iluminen" correctamente en los polígonos del mapa.

---

## 4. Metodología de Análisis de Brechas (Gap Analysis)

El endpoint `/estadisticas/brechas` implementa una lógica de correlación tridimensional:
*   **X**: Nivel de Estudios.
*   **Y**: Rango Salarial.
*   **Z (Peso)**: Experiencia Requerida.

Esto permite al BID identificar sectores donde las exigencias (estudios + experiencia) están desalineadas con la oferta salarial, facilitando diagnósticos de política pública sobre precariedad o escasez de talento.

---

## 5. Scheduler y Lifecycle

El sistema utiliza **APScheduler** integrado en el ciclo de vida de FastAPI (`lifespan`):
*   En el arranque (`startup`), el programador inicia un hilo de monitoreo.
*   Cada 24 horas (configurable), dispara la tarea `scrape_periodic_job`.
*   Esto garantiza que los consultores del BID siempre trabajen con datos del ciclo de mercado actual (análisis diario).

---

## 6. Seguridad y Rendimiento

*   **CORS**: Configurado estrictamente vía variables de entorno.
*   **Streaming de Datos**: Los endpoints de exportación (CSV/Excel) utilizan generadores de Python para no saturar la memoria RAM del servidor al manejar cientos de miles de registros.
*   **Indexación**: El campo `sector_economico` y `departamento` están indexados para que las gráficas del dashboard carguen en < 200ms incluso con > 250,000 registros.
