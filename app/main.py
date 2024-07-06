# app/main.py

from typing import List
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import Domanda, DomandaCreate, DomandaUpdate
from app.database import SessionLocal, get_all_domande, get_domanda_by_id, create_domanda, update_domanda, delete_domanda
from app.utils import carica_domande_da_file

app = FastAPI()

# Configura Jinja2 per i template
templates = Jinja2Templates(directory="templates")

# Carica le domande dal file all'avvio
domande_iniziali = carica_domande_da_file('data/domande.txt')
for domanda in domande_iniziali:
    with SessionLocal() as db:
        create_domanda(db, domanda)

# Crea una dipendenza per ottenere una sessione di database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints

@app.get("/domande/", response_model=List[Domanda])
def leggi_domande(db: Session = Depends(get_db)):
    return get_all_domande(db)

@app.get("/domande/{domanda_id}", response_model=Domanda)
def leggi_domanda(domanda_id: int, db: Session = Depends(get_db)):
    domanda = get_domanda_by_id(db, domanda_id)
    if domanda is None:
        raise HTTPException(status_code=404, detail="Domanda non trovata")
    return domanda

@app.post("/domande/", response_model=Domanda)
def aggiungi_domanda(domanda: DomandaCreate, db: Session = Depends(get_db)):
    return create_domanda(db, domanda)

@app.put("/domande/{domanda_id}", response_model=Domanda)
def modifica_domanda(domanda_id: int, domanda: DomandaUpdate, db: Session = Depends(get_db)):
    domanda_aggiornata = update_domanda(db, domanda_id, domanda)
    if domanda_aggiornata is None:
        raise HTTPException(status_code=404, detail="Domanda non trovata")
    return domanda_aggiornata

@app.delete("/domande/{domanda_id}", response_model=Domanda)
def rimuovi_domanda(domanda_id: int, db: Session = Depends(get_db)):
    domanda = delete_domanda(db, domanda_id)
    if domanda is None:
        raise HTTPException(status_code=404, detail="Domanda non trovata")
    return domanda

# Frontend Routes

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    domande = get_all_domande(db)
    return templates.TemplateResponse("index.html", {"request": request, "domande": domande})

@app.get("/quiz/{domanda_id}", response_class=HTMLResponse)
async def quiz(request: Request, domanda_id: int, db: Session = Depends(get_db)):
    domanda = get_domanda_by_id(db, domanda_id)
    if domanda is None:
        raise HTTPException(status_code=404, detail="Domanda non trovata")
    return templates.TemplateResponse("quiz.html", {"request": request, "domanda": domanda})

@app.post("/risposta/{domanda_id}", response_class=HTMLResponse)
async def risposta(request: Request, domanda_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    risposta_utente = int(form.get("risposta"))
    domanda = get_domanda_by_id(db, domanda_id)
    if domanda is None:
        raise HTTPException(status_code=404, detail="Domanda non trovata")
    is_correct = risposta_utente == domanda.risposta_corretta
    return templates.TemplateResponse("risultato.html", {"request": request, "domanda": domanda, "is_correct": is_correct})
