import streamlit as st
import requests
import os

st.title('Sistema de recomendação de filmes')
st.sidebar.title("Sobre")
st.sidebar.write("Sistema de recomendação usando TF-IDF e Similaridade")
API_URL = os.getenv('API_URL')



if "filme_input" not in st.session_state:
    st.session_state.filme_input = ""

filme = st.text_input(
    'Digite aqui o filme: ',
    value=st.session_state.filme_input,
    key="input_filme"
)

sugerir = []


if filme and len(filme) >= 2:
    try:
        resposta = requests.get(f"{API_URL}/sugerir?filme={filme}").json()
        sugerir = resposta.json()
    except:
        sugerir = []

    if sugerir:
        st.write('Sugestões: ')
        for sug in sugerir:
            if st.button(sug):
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
                st.warning(['erro'])
                st.info("💡 Dica: tente nomes em inglês ou mais curtos")
                st.stop()

        st.success(f"Filme base: {dados['base']}")
        st.subheader('Filmes recomendados')
        
        for item in dados['recomendacoes']:
            st.markdown(f"""### 🎬 {item['titulo']}""")
            st.write(f'⭐ Score: {item['score']}')
            st.progress(float(item['score']))

        
    else:
        st.warning('Digite um filme!')

