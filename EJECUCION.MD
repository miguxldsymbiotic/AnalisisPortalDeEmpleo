# Guía de Ejecución Técnica — Vacantes Colombia

Este documento detalla los pasos exactos realizados para poner en marcha el sistema, incluyendo las soluciones a problemas de dependencias encontrados.

---

## 1. Infraestructura (Base de Datos)
Se inició el contenedor de PostgreSQL para la persistencia de datos.

```bash
docker-compose up -d
```
*   **Estado**: El contenedor `vacantes_db` quedó en ejecución en el puerto `5432`.

## 2. Backend (API FastAPI)
Se configuró el entorno de Python y se inició el servidor de la API.

```powershell
cd backend
# Activar entorno virtual
.\venv\Scripts\activate
# Instalar dependencias
pip install -r requirements.txt
# Iniciar servidor con recarga automática
uvicorn api.main:app --reload
```
*   **Nota**: El backend se conecta automáticamente a la base de datos usando las credenciales del archivo `.env`.

## 3. Frontend (Interfaz React + Vite)
Se configuró el entorno de Node.js. Se detectó un conflicto de versiones en las dependencias de mapas, por lo que se usó un flag específico.

```powershell
cd frontend
# Instalación con soporte para dependencias de versiones previas
npm install --legacy-peer-deps
# Iniciar servidor de desarrollo
npm run dev
```
*   **Acceso**: La interfaz queda disponible en [http://localhost:5173](http://localhost:5173).

## 4. Activación del Scraper (Ingesta)
Se activó el proceso de carga de datos desde el Servicio Público de Empleo (SPE).

```powershell
cd backend
.\venv\Scripts\activate
python trigger_scraper.py
```
*   **Funcionalidad**: Este script envía una señal al API para que comience a recorrer las páginas de vacantes y las guarde en la base de datos.

---

## Verificación de Logs
Para confirmar que todo funciona, puedes revisar la terminal del backend, donde deberías ver mensajes como:
`Page X processed. Added/Updated: 50 vacantes.`
