# MangaColor-Hub-API
Repositorio de Documentacion S5 
# MangaColor Hub API - MVP

## Descripción
Este es el MVP técnico funcional para MangaColor Hub, un sistema diseñado para gestionar y coordinar el flujo de trabajo de equipos de traducción y coloreo de manga. 

La API RESTful gestiona el registro de capítulos y la actualización de sus estados (pending, in_progress, done), automatizando el movimiento de tarjetas mediante integración con la API de Trello.

## Cómo ejecutar localmente
1. Clonar el repositorio.
2. Instalar dependencias: `pip install fastapi uvicorn pydantic requests python-dotenv`
3. Crear un archivo `.env` con las credenciales de Trello.
4. Ejecutar el servidor: `uvicorn main:app --reload`
5. Acceder a Swagger UI en: `http://127.0.0.1:8000/docs`
