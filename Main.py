from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
from dotenv import load_dotenv

# Cargar credenciales ocultas
load_dotenv()
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
LIST_TODO = os.getenv("TRELLO_LIST_TODO")
LIST_IN_PROGRESS = os.getenv("TRELLO_LIST_IN_PROGRESS")
LIST_DONE = os.getenv("TRELLO_LIST_DONE")

app = FastAPI(
    title="MangaColor Hub API",
    description="API MVP que gestiona capítulos y automatiza tarjetas en Trello.",
    version="1.0.0"
)

# Añadimos un campo para guardar el ID que Trello le asigne a la tarjeta
class Chapter(BaseModel):
    id: int
    title: str
    chapter_number: float
    status: str = "pending"
    trello_card_id: Optional[str] = None

db_chapters: List[Chapter] = []

@app.post("/chapters", response_model=Chapter, status_code=201)
def create_chapter(chapter: Chapter):
    for existing in db_chapters:
        if existing.id == chapter.id:
            raise HTTPException(status_code=400, detail="El capítulo ya existe.")

    # 1. Crear tarjeta en Trello en la columna 'To Do'
    url = f"https://api.trello.com/1/cards"
    query = {
        'idList': LIST_TODO,
        'key': TRELLO_KEY,
        'token': TRELLO_TOKEN,
        'name': f"Capítulo {chapter.chapter_number}: {chapter.title}"
    }
    response = requests.post(url, params=query)

    # 2. Guardar el ID de Trello y registrar en memoria
    if response.status_code == 200:
        chapter.trello_card_id = response.json()["id"]

    db_chapters.append(chapter)
    return chapter

@app.get("/chapters")
def get_all_chapters():
    return db_chapters

@app.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: int):
    for chapter in db_chapters:
        if chapter.id == chapter_id:
            return chapter
    raise HTTPException(status_code=404, detail="Capítulo no encontrado.")

@app.patch("/chapters/{chapter_id}/status")
def update_chapter_status(chapter_id: int, new_status: str):
    if new_status not in ["pending", "in_progress", "done"]:
        raise HTTPException(status_code=400, detail="Estado no válido.")

    for chapter in db_chapters:
        if chapter.id == chapter_id:
            chapter.status = new_status

            # 1. Elegir a qué columna de Trello se va a mover
            target_list = LIST_IN_PROGRESS if new_status == "in_progress" else LIST_DONE
            if new_status == "pending": target_list = LIST_TODO

            # 2. Mover la tarjeta en Trello
            if chapter.trello_card_id:
                url = f"https://api.trello.com/1/cards/{chapter.trello_card_id}"
                query = {'idList': target_list, 'key': TRELLO_KEY, 'token': TRELLO_TOKEN}
                requests.put(url, params=query)

            return {"message": "Estado actualizado y tarjeta movida en Trello", "chapter": chapter}

    raise HTTPException(status_code=404, detail="Capítulo no encontrado.")