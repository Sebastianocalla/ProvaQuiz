# app/models.py

from pydantic import BaseModel
from typing import List

class DomandaBase(BaseModel):
    testo: str
    opzioni: List[str]
    risposta_corretta: int

class Domanda(DomandaBase):
    id: int

    class Config:
        from_attributes = True  # Cambia da orm_mode a from_attributes

class DomandaCreate(DomandaBase):
    pass

class DomandaUpdate(BaseModel):
    testo: str
    opzioni: List[str]
    risposta_corretta: int
