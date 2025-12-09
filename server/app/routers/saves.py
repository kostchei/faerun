"""
Path: server/app/routers/saves.py
Purpose: Game save/load endpoints
Logic:
  - GET /: List all saved games
  - POST /: Create new save with name and character info
  - GET /{save_id}: Retrieve specific save by ID
  - DELETE /{save_id}: Delete save by ID
  - In-memory list for demo (replace with DB later)
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class SaveGame(BaseModel):
    id: str
    name: str
    created_at: datetime
    character_name: str
    level: int


# In-memory saves for demo
saves_db: list[SaveGame] = []


@router.get("/")
async def list_saves():
    """List all saved games."""
    return {"saves": saves_db}


@router.post("/")
async def create_save(name: str, character_name: str = "Hero", level: int = 1):
    """Create a new save."""
    save = SaveGame(
        id=f"save_{len(saves_db) + 1}",
        name=name,
        created_at=datetime.now(),
        character_name=character_name,
        level=level
    )
    saves_db.append(save)
    return {"status": "saved", "save": save}


@router.get("/{save_id}")
async def get_save(save_id: str):
    """Get a specific save."""
    for save in saves_db:
        if save.id == save_id:
            return save
    return {"error": "Save not found"}


@router.delete("/{save_id}")
async def delete_save(save_id: str):
    """Delete a save."""
    global saves_db
    saves_db = [s for s in saves_db if s.id != save_id]
    return {"status": "deleted"}
