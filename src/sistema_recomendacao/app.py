import streamlit as st
import requests
import os
from main import buscar_info_filme

st.title('Sistema de recomendação de filmes')
st.sidebar.title("🎬 Sistema de Recomendação")
st.sidebar.markdown("---")
st.sidebar.markdown("""
### Como funciona?
Digite o nome de um filme e o sistema encontra os mais similares usando **TF-IDF** e **Similaridade por Cosseno**.

### Dicas de uso
- Digite pelo menos 2 letras para ver sugestões
- Clique numa sugestão para **fixar** o filme
- Clique no filme fixado para **desmarcar**
- Use nomes em **inglês** para melhores resultados

### Tecnologias
- Python
- FastAPI
- Streamlit
- Scikit-learn
- TMDB API

### Dataset
+5000 filmes catalogados

---
Feito com Python
""")
API_URL = os.getenv('API_URL')

# session_state
if "filme_escolhido" not in st.session_state:
    st.session_state.filme_escolhido = ""

if "filme_fixado" not in st.session_state:
    st.session_state.filme_fixado = None  

if "recomendacoes" not in st.session_state:
    st.session_state.recomendacoes = None 

if "pagina" not in st.session_state:
    st.session_state.pagina = 0


st.markdown("""
    <style>
    /* botão recomendar — selecionado pelo texto */
    div.stButton > button[kind="primary"] {
        background-color: #0068C9 !important;
        color: white !important;
    }
    div.stButton > button:hover[kind="primary"] {
        background-color: #003f7a !important;
        color: white !important;
    }

    /* todos os botões por padrão — sugestões */
    div.stButton > button {
        background-color: #FFC300 !important;
        color: black !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }

    div.stButton > button:hover {
        background-color: #e0a800 !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

#input filme
filme = st.text_input(
    'Digite aqui o filme: ',
    value=st.session_state.filme_escolhido,
    key="input_filme"
)

#botão surpreenda-me
if st.button("Surpreenda-me!"):
    try:
        resposta = requests.get(f"{API_URL}/aleatorio")
        filme_aleatorio = resposta.json()['titulo']
        st.session_state.filme_escolhido = filme_aleatorio
        st.session_state.filme_fixado = filme_aleatorio
        st.session_state.pagina = 0
        resposta_rec = requests.get(f"{API_URL}/recomendacoes?filme={filme_aleatorio}")
        st.session_state.recomendacoes = resposta_rec.json()
        st.rerun()
    except:
        st.error("Erro ao buscar filme aleatório")

#mostra o filme fixado
if st.session_state.filme_fixado:
    st.info(f"📌 Filme fixado: **{st.session_state.filme_fixado}**")

    if st.button("❌ Desafixar", type="primary"): 
        st.session_state.filme_fixado = None
        st.session_state.recomendacoes = None
        st.session_state.filme_escolhido = ""
        st.rerun()


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
            #mostra se estiver fixado
            label = f"✅ {sug}" if st.session_state.filme_fixado == sug else sug

            if st.button(label, key=f"sug_{sug}"):
                if st.session_state.filme_fixado == sug:
                    #clicou no fixado desmarca
                    st.session_state.filme_fixado = None
                    st.session_state.recomendacoes = None
                    st.session_state.filme_escolhido = ""
                    st.rerun()
                else:
                    #clicou numa sugestão fixa e ja busca recomendações
                    st.session_state.filme_fixado = sug
                    st.session_state.filme_escolhido = sug

                    try:
                        resposta = requests.get(f"{API_URL}/recomendacoes?filme={sug}")
                        st.session_state.recomendacoes = resposta.json()
                    except:
                        st.session_state.recomendacoes = None

                st.rerun()



#prioridade: fixado > digitado
filme_busca = st.session_state.filme_fixado or st.session_state.filme_escolhido or filme


if st.button('Recomendar', type="primary"):
    if filme_busca:
        st.session_state.pagina = 0
        with st.spinner("Buscando recomendações..."):
            try:
                resposta = requests.get(f'{API_URL}/recomendacoes?filme={filme_busca}')
                st.session_state.pagina = 0
                st.session_state.recomendacoes = resposta.json()
            except requests.exceptions.RequestException:
                st.error('Erro ao conectar com a API')
                st.stop()
    else:
        st.warning('Digite um filme!')

#exibe recomendações (vindas do botão OU do clique na sugestão)
if st.session_state.recomendacoes:
    dados = st.session_state.recomendacoes

    if not isinstance(dados, dict):
        st.error("Resposta inválida da API")
        st.stop()

    if 'erro' in dados:
        st.warning(dados['erro'])
        st.info("💡 Dica: tente nomes em inglês ou mais curtos")
        st.stop()

    st.success("Filmes encontrados")
    st.subheader('Filmes recomendados')

    #paginação
    todos = dados['recomendacoes']
    por_pagina = 5
    total_paginas = (len(todos) - 1) // por_pagina
    inicio = st.session_state.pagina * por_pagina
    fim = inicio + por_pagina
    pagina_atual = todos[inicio:fim]


    for item in pagina_atual:
        info = buscar_info_filme(item['titulo'])

        poster = info['poster'] if info and info['poster'] else "https://via.placeholder.com/150x220?text=Sem+Imagem"
        ano = info['ano'] if info else ''
        nota = f"{info['nota']:.1f}/10" if info else 'N/A'
        sinopse = info['sinopse'] if info else 'Sem sinopse'
        sinopse = (sinopse
            .replace('&', '&amp;')
            .replace('"', '&quot;')
            .replace("'", '&#39;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
        )
        titulo = item['titulo'].replace('"', '&quot;').replace("'", '&#39;')

        # 👇 monta o HTML numa variável ANTES do st.markdown
        html = "<div style='display:flex; gap:20px; padding:16px; border-radius:12px; background-color:#1e1e1e; margin-bottom:16px; align-items:stretch;'>"
        html += f"<img src='{poster}' style='width:200px; min-height:300px; object-fit:cover; border-radius:8px; flex-shrink:0; align-self:stretch;'>"
        html += "<div style='flex:1; display:flex; flex-direction:column; gap:8px;'>"
        html += f"<h3 style='margin:0;'>🎬 {titulo}</h3>"
        html += f"<p style='margin:0;'>📅 {ano}</p>"
        html += f"<p style='margin:0;'>⭐ Nota TMDB: {nota}</p>"
        html += f"<p style='margin:0; font-size:14px; color:#aaa;'>{sinopse}</p>"
        html += f"<p style='margin:0;'>🎯 Score: {item['score']}</p>"
        html += f"<div style='background-color:#333; border-radius:8px; height:10px; width:100%;'>"
        html += f"<div style='background-color:#0068C9; border-radius:8px; height:10px; width:{item['score']*100}%;'></div>"
        html += "</div>"
        html += "</div></div>"

        st.markdown(html, unsafe_allow_html=True)

            # 👇 navegação entre páginas
    st.markdown("<br>", unsafe_allow_html=True)
    col_esq, col_meio, col_dir = st.columns([1, 2, 1])

    with col_esq:
        if st.session_state.pagina > 0:
            if st.button("Anteriores", type="primary"):
                st.session_state.pagina -= 1
                st.rerun()

    with col_meio:
        st.markdown(f"<p style='text-align:center; color:#aaa;'>Página {st.session_state.pagina + 1} de {total_paginas + 1}</p>", unsafe_allow_html=True)

    with col_dir:
        if st.session_state.pagina < total_paginas:
            if st.button("Próximos", type="primary"):
                st.session_state.pagina += 1
                st.rerun()

        
    st.divider()