# MangaColor Hub API

Sistema de gestión de backlog y flujo de trabajo para equipos de traducción y coloreo de manga, con integración automatizada a Trello.

## Problema
Los equipos de traducción y coloreo pierden el seguimiento de qué capítulo está pendiente, quién lo trabaja y cuáles están finalizados, generando desorganización, trabajo duplicado y cuellos de botella.

## Solución
MangaColor Hub centraliza la gestión de capítulos mediante una API REST y un panel visual interactivo (Frontend), sincronizando automáticamente los estados (To Do, In Progress, Done) con tableros de Trello.

## Flujo principal
Registrar capítulo → Crear tarjeta en Trello (Automático) → Consultar backlog → Actualizar estado → Mover tarjeta en Trello (Automático)

## Tecnologías
Python, FastAPI, Uvicorn, Streamlit, Requests, Trello API

---

## 🚀 Guía para ejecutar y probar el proyecto

**1. Descargar los archivos**
Descarga este repositorio en tu computadora (clonándolo o como archivo ZIP) y extrae los archivos. Asegúrate de tener en la misma carpeta los archivos principales: `main.py` y `dashboard.py`.

**2. Instalar dependencias**
Abre una terminal (CMD o PowerShell) navegando hasta la carpeta donde descargaste los archivos y ejecuta:
```bash
pip install fastapi uvicorn requests python-dotenv streamlit pandas
```
3. Configurar entorno (.env)
Para que la conexión con Trello funcione de manera segura, debes crear un archivo llamado exactamente .env en esa misma carpeta con tus credenciales:

```
TRELLO_KEY=tu_api_key
TRELLO_TOKEN=tu_token
TRELLO_LIST_TODO=id_lista_todo
TRELLO_LIST_IN_PROGRESS=id_lista_in_progress
TRELLO_LIST_DONE=id_lista_done
```

4. Abrir el Tablero de Trello (Para ver la automatización en vivo)
Abre el siguiente enlace en tu navegador web y mantenlo a la vista. Aquí aparecerán y se moverán las tarjetas automáticamente según las peticiones de la API:


  https://trello.com/b/GP8fkMRl/mangacolor-hub-fayri-tail-backlog  


5. Ejecutar la API (El Motor / Backend)
En la terminal que ya tienes abierta en la carpeta del proyecto, enciende el servidor ejecutando:

Bash
```
uvicorn main:app --reload
```

🏠 Mensaje de bienvenida: 

```
http://127.0.0.1:8000
```


📖 Documentación Swagger: 

```
http://127.0.0.1:8000/docs
```

6. Ejecutar la Interfaz Visual (Frontend)
No cierres la primera terminal. Abre una nueva terminal en esa misma carpeta y levanta la interfaz gráfica ejecutando:

Bash
```
streamlit run dashboard.py
```


🖥️ Panel interactivo: Se abrirá automáticamente en tu navegador en: 

```
http://localhost:8501.
```
