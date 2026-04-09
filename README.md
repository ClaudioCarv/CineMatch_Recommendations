# Sistema de Recomendação de Filmes

Sistema de recomendação de filmes construído com **Python**, **FastAPI** e **Streamlit**, utilizando **TF-IDF** e **Similaridade por Cosseno** para encontrar filmes parecidos com o que você pesquisar. Integrado com a **API do TMDB** para exibir pôsteres, notas, sinopses e ano de lançamento.

---

## Demo

**[Acesse o sistema aqui](https://recomendacaofilmes.streamlit.app/)**

---

## Funcionalidades

- 🔍 **Busca inteligente** com sugestões em tempo real enquanto você digita
- 📌 **Filme fixado** — clique numa sugestão para fixar e recomendar com base nela
- 🎬 **Recomendações** baseadas em gênero, sinopse e palavras-chave do filme
- 🖼️ **Pôsteres** dos filmes via API do TMDB
- 📅 **Informações extras** — ano de lançamento, nota do TMDB e sinopse
- 📄 **Paginação** — navegue entre páginas de recomendações
- 📊 **Barra de similaridade** — visualize o quão similar cada filme é

---

## Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| FastAPI | API REST para recomendações e sugestões |
| Uvicorn | Servidor ASGI para rodar a API |
| Streamlit | Interface web do sistema |
| Scikit-learn | TF-IDF e Similaridade por Cosseno |
| Pandas | Manipulação do dataset |
| TMDB API | Pôsteres, notas e sinopses |
| Requests | Chamadas HTTP |

---

## Estrutura do projeto

```
SISTEMA_RECOMENDACAO/
├── dataset/
│   └── movies.csv               # Dataset com os filmes
├── src/
│   └── sistema_recomendacao/
│       ├── __init__.py
│       ├── api.py               # Rotas da API (FastAPI)
│       ├── app.py               # Interface web (Streamlit)
│       ├── main.py              # Lógica de recomendação e TMDB
│       └── notebook.ipynb       # Exploração e testes
├── tests/
│   └── __init__.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Como funciona

### 1. Preparação dos dados
O dataset `movies.csv` é carregado e tratado. Uma coluna `perfil` é criada combinando gênero, sinopse e palavras-chave de cada filme:

```python
df['perfil'] = df['genres'] + ' ' + df['overview'] + ' ' + df['keywords']
```

### 2. Vetorização com TF-IDF
O texto do `perfil` é transformado em vetores numéricos usando o `TfidfVectorizer`:

```python
vectorizador = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1,2))
tfidf_matrix = vectorizador.fit_transform(df['perfil'])
```

### 3. Similaridade por Cosseno
A similaridade entre todos os filmes é calculada:

```python
similaridade = cosine_similarity(tfidf_matrix)
```

### 4. Recomendação
Ao buscar um filme, o sistema encontra os filmes com maior similaridade e retorna os top 20.

---

## 🚀 Como rodar localmente

### Pré-requisitos
- Python 3.13+
- Conta na [TMDB](https://www.themoviedb.org/) para obter a API Key

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/recomendacao-filmes.git
cd recomendacao-filmes
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
API_URL=http://localhost:8000
API_KEY_TMD=sua_chave_tmdb_aqui
```

### 5. Rode a API

```bash
uvicorn src.sistema_recomendacao.api:app --reload
```

### 6. Rode o Streamlit

Em outro terminal:

```bash
streamlit run src/sistema_recomendacao/app.py
```
---

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/recomendacoes?filme={titulo}` | Retorna 10 filmes recomendados |
| GET | `/sugestoes?filme={texto}` | Retorna sugestões de filmes |


```json
{
  "base": "The Avengers",
  "recomendacoes": [
    { "base": "The Avengers", "titulo": "Iron Man 2", "score": 0.4 },
    { "base": "The Avengers", "titulo": "Thor", "score": 0.38 }
  ]
}
```

## 📊 Dataset

O dataset `movies.csv` contém informações de filmes como:

| Coluna | Descrição |
|---|---|
| `original_title` | Título original do filme |
| `genres` | Gêneros do filme |
| `overview` | Sinopse |
| `keywords` | Palavras-chave |
| `cast` | Elenco principal |
| `director` | Diretor |
| `release_date` | Data de lançamento |
| `runtime` | Duração |

---

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'feat: minha nova feature'`
4. Push para a branch: `git push origin minha-feature`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Feito com Python e uma ajudinha de IA.
