import streamlit as st
import requests
import os

st.title('Sistema de recomendação de filmes')
st.sidebar.title("Sobre")
st.sidebar.write("Sistema de recomendação usando TF-IDF e Similaridade")
API_URL = os.getenv('API_URL')



if "filme_input" not in st.session_state:
    st.session_state.filme_input = ""

def atualizar_input():
    st.session_state.filme_input = st.session_state.input_filme

filme = st.text_input(
    'Digite aqui o filme: ',
    key="input_filme"
)

sugestoes = []


if filme and len(filme) >= 2:
    try:
        resposta = requests.get(f"{API_URL}/sugestoes?filme={filme}")
        sugestoes = resposta.json()
    except:
        sugestoes = []

    if sugestoes:
        st.markdown("### 🔍 Sugestões")

        for sug in sugestoes:
            if st.button(sug, key=f"sug_{sug}"):
                st.session_state.filme_input = sug
                st.rerun()

if st.button('Recomendar'):
    if filme:
        with st.spinner("Buscando recomendações..."):
            try:
                resposta = requests.get(f'{API_URL}/recomendacoes?filme={filme}')
                dados = resposta.json()
            except  requests.exceptions.RequestException:
                st.error('Erro ao conectar com a API')
                st.stop()

            if not isinstance(dados, dict):
                st.error("Resposta inválida da API")
                st.stop()
        

            if 'erro' in dados:
                st.warning(dados['erro'])
                st.info("💡 Dica: tente nomes em inglês ou mais curtos")
                st.stop()

        st.success(f"Filmes encontrados")
        st.subheader('Filmes recomendados')
        
        for item in dados['recomendacoes']:
            st.markdown(f"""### 🎬 {item['titulo']}""")
            st.write(f'⭐ Score: {item['score']}')
            st.progress(float(item['score']))

        
    else:
        st.warning('Digite um filme!')

