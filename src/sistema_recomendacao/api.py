from fastapi import FastAPI
from src.sistema_recomendacao.main import recomendar
from src.sistema_recomendacao.main import sugerir

app = FastAPI()

@app.get('/recomendacoes')
def recomendar_api(filme: str):
    return recomendar(filme)


@app.get('/sugestoes')
def sugerir_api(filme: str):
    return sugerir(filme)
