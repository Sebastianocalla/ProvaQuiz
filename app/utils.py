# app/utils.py

from app.models import DomandaCreate

def carica_domande_da_file(file_path: str):
    domande = []
    with open(file_path, 'r') as file:
        for line in file:
            testo, opzione1, opzione2, opzione3, risposta_corretta = line.strip().split(';')
            domande.append(DomandaCreate(
                testo=testo,
                opzioni=[opzione1, opzione2, opzione3],
                risposta_corretta=int(risposta_corretta)
            ))
    return domande
