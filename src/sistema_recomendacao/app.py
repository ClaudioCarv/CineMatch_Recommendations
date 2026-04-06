import streamlit as st
import requests
import os

st.title('Sistema de recomendação de filmes')
st.sidebar.title("Sobre")
st.sidebar.write("Sistema de recomendação usando TF-IDF e Similaridade")
API_URL = os.getenv('API_URL')



filme = st.text_input('Digite aqui um filme:', placeholder="Ex: Avengers, Batman...")

if filme and len >= 2:
    try:
        sugerir = requests.get(f"{API_URL}/sugerir?filme={filme}").json()
    except:
        sugerir = []

    if sugerir:
        filme = st.selectbox('Sugestões: ', sugerir)


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

