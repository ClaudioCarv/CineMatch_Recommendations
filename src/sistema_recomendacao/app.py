import streamlit as st
import requests
import os
from main import buscar_poster


st.title('Sistema de recomendação de filmes')
st.sidebar.title("Sobre")
st.sidebar.write("Sistema de recomendação usando TF-IDF e Similaridade")
API_URL = os.getenv('API_URL')



if "filme_escolhido" not in st.session_state:
    st.session_state.filme_escolhido = ""

filme = st.text_input(
    'Digite aqui o filme: ',
    value=st.session_state.filme_escolhido,
    key="input_filme"
)

sugestoes = []


if filme and len(filme) >= 2 and filme != st.session_state.filme_escolhido:
    try:
        resposta = requests.get(f"{API_URL}/sugestoes?filme={filme}")
        sugestoes = resposta.json()
    except:
        sugestoes = []

    if sugestoes:
        st.markdown("### 🔍 Sugestões")

        for sug in sugestoes:
            if st.button(sug, key=f"sug_{sug}"):
                st.session_state.filme_escolhido = sug
                st.rerun()                              

filme_busca = st.session_state.filme_escolhido or filme




st.markdown("""
    <style>
    div.stButton > button {
        background-color: #0068C9;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #0051a0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

if st.button('Recomendar'):
    if filme_busca:
        with st.spinner("Buscando recomendações..."):
            try:
                resposta = requests.get(f'{API_URL}/recomendacoes?filme={filme_busca}')
                dados = resposta.json()
                
            except requests.exceptions.RequestException:
                st.error('Erro ao conectar com a API')
                st.stop()

            if not isinstance(dados, dict):
                st.error("Resposta inválida da API")
                st.stop()

            if 'erro' in dados:
                st.warning(dados['erro'])
                st.info("💡 Dica: tente nomes em inglês ou mais curtos")
                st.stop()

        st.success("Filmes encontrados")
        st.subheader('Filmes recomendados')

        for item in dados['recomendacoes']:
            st.markdown(f"### 🎬 {item['titulo']}")

            poster_url = buscar_poster(item['titulo'])
            col_poster, col_info = st.columns([1, 3])

            with col_poster:
                if poster_url:
                    st.image(poster_url, width=150)
                else:
                    st.write("🎬 Sem imagem")
    
            with col_info:
                st.markdown(f"### 🎬 {item['titulo']}")
                st.write(f"⭐ Score: {item['score']}")
                st.progress(float(item['score']))
            
            st.divider()  
    else:
        st.warning('Digite um filme!')