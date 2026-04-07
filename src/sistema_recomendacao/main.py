import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import requests


API_KEY_TMD = os.getenv('API_TMD')


def buscar_poster(titulo):
    url = f'https://api.themoviedb.org/3/movie'
    params = {
        "api_key": API_KEY_TMD,
        "query": titulo,
        "language": "pt-BR"
    }
    resposta = requests.get(url, params=params).json()

    if resposta['results']:
        filme = resposta['results'][0]
        poster_path = filme.get('poster_path')

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    
    return None


#buscar o filme digitado e ver se tem ou não na lista

def recomendar(filme):
    filme = filme[:50]
    filtro = df[df['original_title'].str.contains(filme, case=False, na=False)].head(1)
    if not isinstance(filme, str) or len(filme) < 2:
        return {"erro": "Digite um nome válido"}
    if filtro.empty:
        return {"erro": "Filme não encontrado. Tente outro nome."}
    else:
        indice = filtro.index[0]
        sim = list(enumerate(similaridade[indice]))
        sim = sorted(sim, key=lambda x: x[1], reverse=True)
        resultados = []
        filme_base = df['original_title'][indice]
        for idx, valor in sim[1:6]:
            resultados.append({
                'base': filme_base,
                'titulo': df['original_title'][idx],
                'score': round(valor, 2)
            })
        return {
            'base': filme_base,
            'recomendacoes': resultados
        }

def sugerir(texto):
    filtro = df[df['original_title'].str.contains(texto, case=False, na=False)]
    resultados = filtro['original_title'].head(5).tolist()

    return resultados



df = pd.read_csv('dataset/movies.csv')

#Tratando os valores Null
df['homepage'] = df['homepage'].fillna(' ')
df['genres'] = df['genres'].fillna('Outro')
df['tagline'] = df['tagline'].fillna(' ')
df['cast'] = df['cast'].fillna(' ')
df['keywords'] = df['keywords'].fillna('Sem')
df['director'] = df['director'].fillna(' ')
df['release_date'] = df['release_date'].fillna('09/09/2009')
df['overview'] = df['overview'].fillna(' ')
df['runtime'] = df['runtime'].fillna('Sem')

#criando uma coluna nova "perfil"
df['perfil'] = df['genres'] + ' ' + df['overview'] + ' ' + df['keywords'] 
df['perfil'] = df['perfil'].str.lower()


#Transformando palavras em vetores para o entendimento da maquina

#ajustes no vetorizador
vectorizador = TfidfVectorizer(
    stop_words='english',
    max_features=5000,
    ngram_range=(1,2)
)

#indicando qual coluna deve ser vetorizada
tfidf_matrix = vectorizador.fit_transform(df['perfil'])


#procura similaridade entre os filmes
similaridade = cosine_similarity(tfidf_matrix)

#transformar a similaridade em lista, ordenar inversamente e ignorar o primeiro valor
listasimilaridade = list(enumerate(similaridade[0]))
listasimilaridade = sorted(listasimilaridade, key=lambda x: x[1], reverse=True)

#printar similaridade
if __name__ == "__main__":
    recomendar("avengers")





