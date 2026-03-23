# 🚀 Guía Maestra: Despliega tu Proyecto en Azure (Capa Gratuita)

¡Hola! Esta guía está diseñada para que, aunque sea tu primera vez en Azure, puedas subir tu proyecto de Vacantes Colombia sin errores y totalmente gratis.

---

## 📂 PASO 0: Antes de empezar (GitHub)
Azure funciona mejor si tu código está en GitHub.
1.  Sube tu carpeta `PROYECTO` a un repositorio en GitHub (puede ser privado).
2.  Asegúrate de que la carpeta `backend` tenga el [Dockerfile](file:///c:/Users/migux/Downloads/PROYECTO/backend/Dockerfile) que creamos y la carpeta `frontend` tenga el archivo [staticwebapp.config.json](file:///c:/Users/migux/Downloads/PROYECTO/frontend/staticwebapp.config.json).

---

## 🏗️ PASO 1: Crear el Grupo de Recursos (El "Contenedor")
En Azure, todo debe ir dentro de una "bolsa" llamada Grupo de Recursos.

1.  Entra al [Portal de Azure](https://portal.azure.com).
2.  En el buscador de arriba escribe **Grupos de recursos** (Resource Groups) y entra.
3.  Haz clic en **+ Crear**.
4.  **Suscripción**: Elige la tuya (ej: "Azure for Students" o "Free Trial").
5.  **Grupo de recursos**: Escribe `PROYECTO_VACANTES_RG`.
6.  **Región**: Elige `East US` (es la que suele tener más opciones gratis).
7.  Haz clic en **Revisar y crear** y luego en **Crear**.

---

## 💾 PASO 2: La Base de Datos (PostgreSQL)
Vamos a crear una base de datos que sea gratis por 12 meses.

1.  Busca **Azure Database for PostgreSQL (servidores flexibles)** en la barra superior.
2.  Haz clic en **+ Crear**.
3.  **Configuración Básica**:
    *   **Grupo de recursos**: Selecciona `PROYECTO_VACANTES_RG`.
    *   **Nombre del servidor**: Ponle algo único (ej: `vacantes-db-miguel`).
    *   **Región**: `East US`.
    *   **Versión de PostgreSQL**: `15`.
    *   **Tipo de carga de trabajo**: Elige **Desarrollo (Development)**.
    *   **Proceso y almacenamiento**: Haz clic en **Configurar servidor**. Selecciona el nivel **Burstable** y asegúrate de elegir **B1ms** (este es el gratis). Dale a "Guardar".
    *   **Nombre de usuario de administrador**: Escribe `admin_vacantes`.
    *   **Contraseña**: Pon una segura y **anótala**.
4.  **Redes (Networking) - MUY IMPORTANTE**:
    *   Marca la casilla: **Permitir acceso público desde cualquier servicio de Azure dentro de Azure a este servidor**. (Sin esto, el backend no podrá guardar datos).
    *   Haz clic en "Agregar dirección IP de cliente actual" (para que puedas entrar tú desde tu PC).
5.  Haz clic en **Revisar y crear** y luego en **Crear**. (Espera 5-10 minutos).

---

## 🐳 PASO 3: El Backend (Azure Container Apps)
Aquí subiremos tu código Dockerizado.

1.  Busca **Container Apps** y haz clic en **+ Crear**.
2.  **Básico**:
    *   Nombre: `vacantes-backend`.
    *   Entorno de Container Apps: Dale a "Crear nuevo" -> Ponle un nombre -> "Crear".
3.  **Contenedor**:
    *   Desmarca "Usar imagen de inicio rápido".
    *   **Origen de la imagen**: Elige **GitHub**.
    *   Sigue los pasos para autorizar tu cuenta de GitHub y elige tu repositorio.
    *   **Ruta del Dockerfile**: Escribe [backend/Dockerfile](file:///c:/Users/migux/Downloads/PROYECTO/backend/Dockerfile).
4.  **Entrada (Ingress)**:
    *   Habilita **Ingress**.
    *   Tráfico de destino: **Limited to Container Apps Environment** (o public si quieres acceder desde fuera).
    *   **Puerto de destino**: Escribe `8000`.
5.  **Configuración (Variables de Entorno)**:
    Una vez creada la app, busca en el menú de la izquierda **Configuración** -> **Variables de entorno**. Añade estas:
    *   `DATABASE_URL`: `postgresql+asyncpg://admin_vacantes:TU_CONTRASEÑA@tu-servidor.postgres.database.azure.com:5432/postgres`
    *   `SCRAPER_CRON_HOURS`: `720`
6.  **Copia la URL** de tu Container App (ej: `https://vacantes-backend.xxxx.eastus.azurecontainerapps.io`).

---

## 🖼️ PASO 4: El Frontend (Azure Static Web Apps)
Esto servirá tu página React.

1.  Busca **Static Web Apps** y haz clic en **+ Crear**.
2.  **Básico**:
    *   Nombre: `vacantes-frontend`.
    *   Plan: **Gratis (Free)**.
    *   Origen: **GitHub**. Elige tu repositorio.
3.  **Detalles de compilación**:
    *   **Ubicación de la aplicación**: `/frontend`
    *   **Ubicación de la API**: Déjalo vacío.
    *   **Ubicación de salida**: `dist`
4.  **Variables de entorno**:
    Cuando se cree, ve a **Configuración** y añade:
    *   `VITE_API_URL`: Pega la URL del backend que copiaste en el paso anterior.

---

## 🛡️ PASO 5: Configuración Final de Seguridad (CORS)
Sin este paso, la página se verá vacía porque el backend rechazará las conexiones del frontend.

1.  Entra a tu **Container App (vacantes-backend)**.
2.  En el menú de la izquierda busca **CORS**.
3.  En "Orígenes permitidos", añade la URL de tu **Static Web App (Frontend)**.
4.  Marca la casilla "Allow Credentials" y dale a **Guardar**.

---

## ✅ ¿Cómo verificar que todo está bien?

1.  Entra a la URL de tu Frontend. Deberías ver los gráficos.
2.  **Primer Scraping**: Como lo configuramos para ejecutarse cada 1 mes, puedes forzar el primero entrando manualmente a: `https://tu-backend.io/api/v1/scraper/iniciar-completo`.
3.  En el portal de Azure, dentro de tu base de datos, verás que el almacenamiento empieza a subir (¡significa que guarda datos!).
