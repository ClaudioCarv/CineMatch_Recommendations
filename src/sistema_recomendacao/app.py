import streamlit as st
import requests
import os

st.title('Sistema de recomendação de filmes')
st.sidebar.title("Sobre")
st.sidebar.write("Sistema de recomendação usando TF-IDF e Similaridade")
API_URL = os.getenv('API_URL')



filme = st.text_input('Digite aqui um filme:', placeholder="Ex: Avengers, Batman...")

if filme:
    sugestoes = requests.get(f"{API_URL}/sugestoes?filme={filme}").json()

    if sugestoes:
        opcao = st.selectbox("Você quis dizer:", sugestoes)
        filme = opcao


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
        

            if isinstance(dados, dict) and 'erro' in dados:
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

