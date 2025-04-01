from fastapi import FastAPI, status, Depends
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from webscrapping import coletar_dados_do_site
from pydantic import BaseModel

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware (
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 3

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int =100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

class ColetarResponse(BaseModel):
    message: str
    dados: List[dict]

@app.get("/coletar", response_model=ColetarResponse, status_code=status.HTTP_200_OK)
async def coletar_dados(db: Session = Depends(get_db)):
    try:
        dados_coletados = coletar_dados_do_site()

        for dado in dados_coletados:
            novo_item = model.Model_Menu(menuNav=dado["menuNav"], link=dado["link"])
            db.add(novo_item)

        db.commit()
        return {"message": "Dados coletados e armazenados com sucesso!", "dados": dados_coletados}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
