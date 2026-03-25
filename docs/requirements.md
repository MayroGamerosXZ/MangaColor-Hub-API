# Requisitos y Backlog del MVP

El proyecto se gestiona mediante metodología ágil utilizando Trello.

## Historias de Usuario (Priorización MoSCoW)

* **[Must]** Como administrador, quiero registrar un nuevo capítulo en el sistema para asignarlo al equipo de coloreo.
    * *Given* que tengo los datos válidos de un nuevo capítulo.
    * *When* envío una petición POST a la API.
    * *Then* el sistema guarda el capítulo y crea una tarjeta en la lista "To Do".
* **[Must]** Como colorista, quiero actualizar el estado de un capítulo para reflejar mi progreso.
    * *Given* que un capítulo existe en estado pendiente.
    * *When* envío una petición PATCH con estado "in_progress".
    * *Then* el sistema actualiza su estado y mueve la tarjeta en el tablero.
* **[Must]** Como usuario, quiero buscar un capítulo por su ID.
* **[Must]** Como usuario, quiero ver la lista completa de capítulos registrados.
* **[Should]** Como administrador, quiero validación para que no existan IDs de capítulos duplicados (Error 400).
* **[Should]** Como usuario, quiero recibir un error claro (404) si busco un capítulo inexistente.
* **[Could]** Como usuario, quiero filtrar la lista de capítulos por estado.
* **[Won't]** Como colorista, quiero subir las páginas coloreadas al servidor (Fuera del scope del MVP).
