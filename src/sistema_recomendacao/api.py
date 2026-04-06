from fastapi import FastAPI
from src.sistema_recomendacao.main import recomendar
from src.sistema_recomendacao.main import sugerir_texto

app = FastAPI()

@app.get('/recomendacoes')
def recomendar_api(filme: str):
    return recomendar(filme)


@app.get('/sugerir')
def sugerir(filme:str):
    return sugerir_texto(filme)
