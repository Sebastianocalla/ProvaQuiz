# app/database.py

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models import DomandaCreate

DATABASE_URL = "sqlite:///./test.db"

# Crea l'engine del database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crea una base di dichiarazione per i modelli
Base = declarative_base()

# Definisce il modello di Domanda
class DomandaDB(Base):
    __tablename__ = "domande"

    id = Column(Integer, primary_key=True, index=True)
    testo = Column(Text, index=True)
    opzione1 = Column(String, index=True)
    opzione2 = Column(String, index=True)
    opzione3 = Column(String, index=True)
    risposta_corretta = Column(Integer, index=True)

# Crea le tabelle nel database
Base.metadata.create_all(bind=engine)

# Crea una sessione del database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funzioni CRUD
def get_all_domande(db):
    return db.query(DomandaDB).all()

def get_domanda_by_id(db, domanda_id: int):
    return db.query(DomandaDB).filter(DomandaDB.id == domanda_id).first()

def create_domanda(db, domanda: DomandaCreate):
    db_domanda = DomandaDB(
        testo=domanda.testo,
        opzione1=domanda.opzioni[0],
        opzione2=domanda.opzioni[1],
        opzione3=domanda.opzioni[2],
        risposta_corretta=domanda.risposta_corretta,
    )
    db.add(db_domanda)
    db.commit()
    db.refresh(db_domanda)
    return db_domanda

def update_domanda(db, domanda_id: int, domanda: DomandaCreate):
    db_domanda = db.query(DomandaDB).filter(DomandaDB.id == domanda_id).first()
    if db_domanda:
        db_domanda.testo = domanda.testo
        db_domanda.opzione1 = domanda.opzioni[0]
        db_domanda.opzione2 = domanda.opzioni[1]
        db_domanda.opzione3 = domanda.opzioni[2]
        db_domanda.risposta_corretta = domanda.risposta_corretta
        db.commit()
        db.refresh(db_domanda)
        return db_domanda
    return None

def delete_domanda(db, domanda_id: int):
    db_domanda = db.query(DomandaDB).filter(DomandaDB.id == domanda_id).first()
    if db_domanda:
        db.delete(db_domanda)
        db.commit()
        return db_domanda
    return None
