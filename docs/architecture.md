# Arquitectura - MangaColor Hub API

## Descripción
El sistema utiliza una arquitectura Cliente-Servidor. La API expone endpoints para gestionar capítulos de manga y actúa como cliente consumiendo la API de Trello para automatizar el movimiento de tarjetas en el tablero.

## Decisiones Arquitectónicas
* **Framework:** Python + FastAPI con la librería `requests`. Elegido por su auto-documentación y facilidad de validación.
* **Seguridad:** Uso de variables de entorno (`.env` local) para proteger credenciales.
* **Almacenamiento:** En memoria temporal para cumplir con el MVP de manera local.

## Diagrama de Flujo Principal
```mermaid
sequenceDiagram
    participant Cliente
    participant FastAPI
    participant TrelloAPI
    participant Memoria

    Cliente->>FastAPI: POST /chapters
    FastAPI->>TrelloAPI: Petición POST para crear tarjeta
    TrelloAPI-->>FastAPI: Devuelve Trello Card ID
    FastAPI->>Memoria: Guarda capítulo + Card ID
    FastAPI-->>Cliente: 201 Created
    
    Cliente->>FastAPI: PATCH /chapters/{id}/status
    FastAPI->>TrelloAPI: Petición PUT para mover tarjeta
    TrelloAPI-->>FastAPI: 200 OK
    FastAPI->>Memoria: Actualiza estado local
    FastAPI-->>Cliente: 200 OK
