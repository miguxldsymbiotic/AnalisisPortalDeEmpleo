# 🇨🇴 Vacantes Colombia — Inteligencia Laboral (BID Analytics)

Plataforma de análisis y visualización del mercado laboral colombiano,diseñada para transformar datos fragmentados en inteligencia estratégica.

---

##  Arquitectura y Estructura del Proyecto

###  Backend (Python 3.11 / FastAPI)
*   `backend/api/routers/`: Implementación de capas de transporte REST.
    *   `estadisticas.py`: Agregaciones analíticas (Territorial, Tendencias, Inclusión).
    *   `scraper.py`: Control de orquestación de ingesta completa/parcial.
*   `backend/scraper/`: Núcleo de procesamiento de datos.
    *   `client.py`: Cliente HTTP asíncrono con **Semáforo de Concurrencia** y **Exponential Back-off**.
    *   `parser.py`: Lógica de normalización y tipado de payloads del SPE.
    *   `runner.py`: Gestor de estado de sesión con persistencia en DB para reanudación de fallos.
*   `backend/db/`: Capa de persistencia.
    *   `models.py`: Esquema de datos PostgreSQL optimizado para analítica.
    *   `session.py`: Motor asíncrono SQLAlchemy (`asyncpg`).

### Scraper Pipeline (Motor de Ingesta)
Ubicado en `backend/scraper/`, gestiona el ciclo de los datos:
*   `client.py`: Cliente HTTP asíncrono 
*   `parser.py`: Lógica de normalización y tipado de payloads del SPE.
*   `runner.py`: Gestor de estado de sesión para reanudación automática tras fallos.
*   `scheduler.py`: Orquestador de tareas programadas para actualizaciones periódicas.

### Frontend (React 19 / Vite 6)
*   `frontend/src/components/`: Despliegue de visualizaciones.
    *   `ColombiaMap.jsx`: Renderizado de GeoJSON con mapeo de normalización de cadenas.
    *   `GapAnalysis.jsx`: Correlación multidimensional (Nivel-Salario-Experiencia).
*   `frontend/public/colombia.json`: GeoJSON optimizado para latencia cero.

---

##  Especificaciones Técnicas

1.  **Capa de Presentación**: SPA con **Tailwind CSS 4** para diseño determinista y **Recharts** para renderizado de series temporales de alta densidad.
2.  **Capa de Lógica**: **FastAPI** con gestión de ciclo de vida (`lifespan`) para el manejo del **APScheduler**.
3.  **Capa de Datos**: **PostgreSQL 15** con índices **GIN** en campos categóricos y **B-Tree** en campos temporales para auditorías rápidas.

---

## Guía de Ejecución

Para poner en marcha el sistema completo, ejecute los siguientes comandos directamente en su terminal desde la raíz del proyecto:

### 1. Infraestructura (Base de Datos)
```bash
docker-compose up -d
```

### 2. Backend (Servidor API)
```powershell
cd backend; .\venv\Scripts\activate; pip install -r requirements.txt; uvicorn api.main:app --reload
```

### 3. Frontend 
```bash
cd frontend; npm install; npm run dev
```

### 4. Activación del Scraper (Ingesta de Datos)
En una nueva terminal (en la raíz del proyecto):
```powershell
.\backend\venv\Scripts\activate; python backend/trigger_scraper.py
```

---

## Administración de Base de Datos (PostgreSQL)

Para Gestión de datos crudos:
```bash
# Docker
docker exec -it vacantes_db psql -U vacantes_user -d vacantes_colombia
```
*   **Host**: `localhost` | **Port**: `5432` | **User**: `vacantes_user`
*   **Mantenimiento**: Migraciones asíncronas vía **Alembic**.


### Consultas 

*   **Ver total de vacantes**:
    ```sql
    SELECT count(*) FROM vacantes;
    ```
*   **Listar las últimas 5 vacantes**:
    ```sql
    SELECT codigo_vacante, titulo_vacante, fecha_publicacion FROM vacantes ORDER BY fecha_publicacion DESC LIMIT 5;
    ```
*   **Conteo por Departamento**:
    ```sql
    SELECT departamento, count(*) FROM vacantes GROUP BY departamento ORDER BY count(*) DESC;
    ```
*   **Estado de las sesiones de Scraping**:
    ```sql
    SELECT id, fecha_inicio, estado, total_registros FROM scrape_sessions ORDER BY fecha_inicio DESC;
    ```