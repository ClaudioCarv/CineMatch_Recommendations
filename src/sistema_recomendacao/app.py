import streamlit as st
import requests
import os
import sys
import html

# Garante importação do main.py independentemente do diretório de execução
try:
    from src.sistema_recomendacao.main import buscar_info_filme
except ImportError:
    try:
        from main import buscar_info_filme
    except ImportError:
        sys.path.append(os.path.dirname(__file__))
        from main import buscar_info_filme

# Configuração da página
st.set_page_config(
    page_title="CineMatch | Sistema de Recomendação de Filmes",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Endpoint da API
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000')

# Inicialização de session_state
if "filme_escolhido" not in st.session_state:
    st.session_state.filme_escolhido = ""

if "filme_fixado" not in st.session_state:
    st.session_state.filme_fixado = None  

if "recomendacoes" not in st.session_state:
    st.session_state.recomendacoes = None 

if "pagina" not in st.session_state:
    st.session_state.pagina = 0

# Pôster SVG fallback caso o TMDB não forneça imagem
POSTER_FALLBACK_SVG = (
    "data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22300%22%20height%3D%22450%22%20viewBox%3D%220%200%20300%20450%22%3E%3Crect%20fill%3D%22%23161b26%22%20width%3D%22300%22%20height%3D%22450%22%20rx%3D%2212%22%2F%3E%3Cg%20fill%3D%22none%22%20stroke%3D%22%23e50914%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%20transform%3D%22translate(110%2C%20150)%20scale(3.2)%22%3E%3Crect%20x%3D%222%22%20y%3D%222%22%20width%3D%2220%22%20height%3D%2220%22%20rx%3D%222.18%22%20ry%3D%222.18%22%2F%3E%3Cline%20x1%3D%227%22%20y1%3D%222%22%20x2%3D%227%22%20y2%3D%2222%22%2F%3E%3Cline%20x1%3D%2217%22%20y1%3D%222%22%20x2%3D%2217%22%20y2%3D%2222%22%2F%3E%3Cline%20x1%3D%222%22%20y1%3D%2212%22%20x2%3D%2222%22%20y2%3D%2212%22%2F%3E%3Cline%20x1%3D%222%22%20y1%3D%227%22%20x2%3D%227%22%20y2%3D%227%22%2F%3E%3Cline%20x1%3D%222%22%20y1%3D%2217%22%20x2%3D%227%22%20y2%3D%2217%22%2F%3E%3Cline%20x1%3D%2217%22%20y1%3D%2217%22%20x2%3D%2222%22%20y2%3D%2217%22%2F%3E%3Cline%20x1%3D%2217%22%20y1%3D%227%22%20x2%3D%2222%22%20y2%3D%227%22%2F%3E%3C%2Fg%3E%3Ctext%20fill%3D%22%2394a3b8%22%20font-family%3D%22sans-serif%22%20font-size%3D%2218%22%20font-weight%3D%22bold%22%20x%3D%2250%25%22%20y%3D%22270%22%20text-anchor%3D%22middle%22%3EP%C3%B4ster%20Indispon%C3%ADvel%3C%2Ftext%3E%3Ctext%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2213%22%20x%3D%2250%25%22%20y%3D%22300%22%20text-anchor%3D%22middle%22%3E(Dados%20n%C3%A3o%20encontrados)%3C%2Ftext%3E%3C%2Fsvg%3E"
)

# Estilização CSS Moderna
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hero Section */
.hero-container {
    text-align: center;
    padding: 1.8rem 1rem 1.8rem 1rem;
    margin-bottom: 1.5rem;
    background: radial-gradient(circle at 50% 0%, rgba(229, 9, 20, 0.16) 0%, rgba(15, 23, 42, 0) 70%);
    border-radius: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 0.4rem;
    background: linear-gradient(135deg, #ffffff 40%, #ff4d58 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    max-width: 650px;
    margin: 0 auto 1.2rem auto;
    line-height: 1.5;
}
.tags-row {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    flex-wrap: wrap;
}
.hero-tag {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.3rem 0.85rem;
    border-radius: 20px;
}

/* Inputs de Texto */
div[data-testid="stTextInput"] input {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 1.02rem !important;
    color: #f8fafc !important;
    transition: all 0.25s ease !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.25) !important;
}

/* Estilo dos Botões */
div.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.58rem 1.2rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Botão Primário */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #e50914 0%, #b20710 100%) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(229, 9, 20, 0.35) !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #ff1e2b 0%, #c40812 100%) !important;
    box-shadow: 0 6px 20px rgba(229, 9, 20, 0.55) !important;
    transform: translateY(-2px);
}

/* Botão Secundário */
div.stButton > button[kind="secondary"] {
    background-color: rgba(255, 255, 255, 0.06) !important;
    color: #f1f5f9 !important;
}
div.stButton > button[kind="secondary"]:hover {
    background-color: rgba(255, 255, 255, 0.13) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    transform: translateY(-2px);
}

/* Banner de Filme Fixado */
.pinned-banner {
    display: flex;
    align-items: center;
    background: linear-gradient(90deg, rgba(229, 9, 20, 0.14) 0%, rgba(30, 41, 59, 0.35) 100%);
    border: 1px solid rgba(229, 9, 20, 0.35);
    border-radius: 12px;
    padding: 0.75rem 1.1rem;
    margin: 0.6rem 0;
    color: #f8fafc;
}

/* Card de Filme Recomendado */
.movie-card {
    display: flex;
    flex-direction: row;
    gap: 1.5rem;
    background: rgba(24, 28, 40, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.3rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.movie-card:hover {
    transform: translateY(-4px);
    border-color: rgba(229, 9, 20, 0.4);
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.5), 0 0 20px rgba(229, 9, 20, 0.15);
}
.poster-container {
    position: relative;
    flex-shrink: 0;
    width: 175px;
    border-radius: 12px;
    overflow: hidden;
    background-color: #0b0f19;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}
.movie-poster {
    width: 100%;
    height: 255px;
    object-fit: cover;
    display: block;
    transition: transform 0.3s ease;
}
.movie-card:hover .movie-poster {
    transform: scale(1.03);
}
.score-badge {
    position: absolute;
    bottom: 8px;
    left: 8px;
    right: 8px;
    background: rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #38bdf8;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 4px 6px;
    border-radius: 6px;
    text-align: center;
}
.movie-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 0.65rem;
    min-width: 0;
}
.movie-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
}
.movie-title {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.3;
}
.badges-row {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    flex-wrap: wrap;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.82rem;
    padding: 4px 10px;
    border-radius: 8px;
    font-weight: 600;
}
.badge-year {
    background: rgba(148, 163, 184, 0.12);
    color: #cbd5e1;
    border: 1px solid rgba(148, 163, 184, 0.2);
}
.badge-rating {
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}
.badge-affinity {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
.progress-container {
    margin: 0.15rem 0;
}
.progress-bar-bg {
    background-color: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    height: 8px;
    width: 100%;
    overflow: hidden;
}
.progress-bar-fill {
    background: linear-gradient(90deg, #e50914 0%, #ff5e62 100%);
    height: 8px;
    border-radius: 999px;
    transition: width 0.6s ease;
}
.movie-synopsis {
    margin: 0;
    font-size: 0.93rem;
    color: #94a3b8;
    line-height: 1.55;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Empty State / Boas-vindas */
.empty-state {
    text-align: center;
    padding: 3rem 1.5rem;
    background: rgba(255, 255, 255, 0.02);
    border: 1px dashed rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    margin: 2rem 0;
}
.empty-icon {
    font-size: 3.2rem;
    margin-bottom: 0.8rem;
}
.empty-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
}
.empty-desc {
    color: #64748b;
    font-size: 0.96rem;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Paginação */
.pagination-info {
    text-align: center;
    font-weight: 600;
    color: #94a3b8;
    font-size: 0.95rem;
}

/* Sidebar Customizada */
.sidebar-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1.2rem;
}
.sidebar-metric {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 0.88rem;
    color: #cbd5e1;
}

/* Responsividade Mobile */
@media (max-width: 768px) {
    .movie-card {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .poster-container {
        width: 180px;
    }
    .badges-row {
        justify-content: center;
    }
    .movie-header {
        justify-content: center;
    }
}
</style>
""", unsafe_allow_html=True)

# Barra Lateral (Sidebar)
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 0 1.2rem 0;">
        <span style="font-size: 2.8rem;">🍿</span>
        <h2 style="margin: 0.4rem 0 0.1rem 0; font-weight: 800; color: #ffffff;">CineMatch</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 0.85rem;">Sistema Inteligente de Recomendação</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Dataset & Motor")
    st.markdown("""
    <div class="sidebar-box">
        <div class="sidebar-metric">📁 <strong>+5.000</strong> Filmes catalogados</div>
        <div class="sidebar-metric">🧠 <strong>TF-IDF</strong> Vetorização de texto</div>
        <div class="sidebar-metric">📐 <strong>Cosseno</strong> Similaridade matemática</div>
        <div class="sidebar-metric">🌐 <strong>TMDB API</strong> Metadados em tempo real</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎬 Como funciona?")
    st.markdown("""
    O sistema analisa **gêneros**, **sinopses** e **palavras-chave** dos filmes. Com **TF-IDF**, cada produção vira um vetor numérico e a **Similaridade por Cosseno** encontra as obras mais próximas no espaço vetorial.
    """)

    st.markdown("### 💡 Dicas de uso")
    st.markdown("""
    - Digite pelo menos **2 letras** para sugestões automáticas.
    - O catálogo possui títulos em **inglês** (*ex: The Dark Knight, Inception*).
    - Clique em uma sugestão para **fixar** e recomendar na hora.
    - Use o **Surpreenda-me** quando estiver indeciso!
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 5px 0;">
        Desenvolvido com 🐍 <strong>Python</strong>, ⚡ <strong>FastAPI</strong> & 🎈 <strong>Streamlit</strong>
    </div>
    """, unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🎬 CineMatch Recommendations</div>
    <div class="hero-subtitle">Descubra novos filmes com base na similaridade de roteiro, gênero e temática utilizando Inteligência Artificial.</div>
    <div class="tags-row">
        <span class="hero-tag">✨ TF-IDF Vectorizer</span>
        <span class="hero-tag">⚡ Cosine Similarity</span>
        <span class="hero-tag">🍿 +5.000 Títulos</span>
        <span class="hero-tag">🎯 Recomendações Precisas</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Seção de Busca e Ações
col_input, col_btn_recomendar, col_btn_surpresa = st.columns([4.2, 1.4, 1.4], vertical_alignment="bottom")

with col_input:
    filme = st.text_input(
        "Qual filme você assistiu e gostou?",
        value=st.session_state.filme_escolhido,
        placeholder="Digite o título em inglês (ex: Interstellar, The Matrix, Gladiator...)",
        key="input_filme"
    )

with col_btn_recomendar:
    btn_recomendar = st.button("🔍 Recomendar", type="primary", use_container_width=True)

with col_btn_surpresa:
    btn_surpresa = st.button("🎲 Surpreenda-me!", type="secondary", use_container_width=True)

# Ação: Surpreenda-me!
if btn_surpresa:
    with st.spinner("Sorteando um filme excelente..."):
        try:
            resposta = requests.get(f"{API_URL}/aleatorio", timeout=6)
            filme_aleatorio = resposta.json()['titulo']
            st.session_state.filme_escolhido = filme_aleatorio
            st.session_state.filme_fixado = filme_aleatorio
            st.session_state.pagina = 0
            resposta_rec = requests.get(f"{API_URL}/recomendacoes?filme={filme_aleatorio}", timeout=10)
            st.session_state.recomendacoes = resposta_rec.json()
            st.rerun()
        except Exception:
            st.error("Erro ao buscar filme aleatório. Certifique-se de que a API FastAPI está em execução.")

# Exibição do filme fixado com botão elegante de desafixar
if st.session_state.filme_fixado:
    col_fix_info, col_fix_btn = st.columns([5, 1.2], vertical_alignment="center")
    with col_fix_info:
        st.markdown(
            f"""
            <div class="pinned-banner">
                <span style="font-size: 1.2rem; margin-right: 8px;">📌</span>
                <span style="color: #cbd5e1; font-size: 0.95rem;">Filme fixado:</span>
                <strong style="color: #ffffff; font-size: 1.05rem; margin-left: 6px;">{html.escape(st.session_state.filme_fixado)}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_fix_btn:
        if st.button("❌ Desafixar", type="secondary", use_container_width=True):
            st.session_state.filme_fixado = None
            st.session_state.recomendacoes = None
            st.session_state.filme_escolhido = ""
            st.rerun()

# Busca de Sugestões em tempo real
sugestoes = []
if filme and len(filme) >= 2 and filme != st.session_state.filme_escolhido:
    try:
        resposta = requests.get(f"{API_URL}/sugestoes?filme={filme}", timeout=4)
        sugestoes = resposta.json()
    except Exception:
        sugestoes = []

    if sugestoes:
        st.markdown(
            "<p style='font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 14px; margin-bottom: 6px;'>💡 Sugestões encontradas (clique para fixar e recomendar):</p>",
            unsafe_allow_html=True
        )
        
        cols_sug = st.columns(min(len(sugestoes), 5))
        for idx, sug in enumerate(sugestoes):
            col = cols_sug[idx % len(cols_sug)]
            with col:
                is_fixed = (st.session_state.filme_fixado == sug)
                label = f"📌 {sug}" if is_fixed else f"🎬 {sug}"

                if st.button(label, key=f"sug_{sug}", use_container_width=True, type="primary" if is_fixed else "secondary"):
                    if is_fixed:
                        st.session_state.filme_fixado = None
                        st.session_state.recomendacoes = None
                        st.session_state.filme_escolhido = ""
                        st.rerun()
                    else:
                        st.session_state.filme_fixado = sug
                        st.session_state.filme_escolhido = sug
                        st.session_state.pagina = 0

                        try:
                            resposta = requests.get(f"{API_URL}/recomendacoes?filme={sug}", timeout=10)
                            st.session_state.recomendacoes = resposta.json()
                        except Exception:
                            st.session_state.recomendacoes = None

                        st.rerun()

# Ação: Recomendar
filme_busca = st.session_state.filme_fixado or st.session_state.filme_escolhido or filme

if btn_recomendar:
    if filme_busca:
        st.session_state.pagina = 0
        with st.spinner("Calculando similaridade e buscando recomendações..."):
            try:
                resposta = requests.get(f'{API_URL}/recomendacoes?filme={filme_busca}', timeout=10)
                st.session_state.pagina = 0
                st.session_state.recomendacoes = resposta.json()
                st.rerun()
            except requests.exceptions.RequestException:
                st.error('Erro ao conectar com a API. Verifique se o servidor FastAPI está ativo na porta 8000.')
                st.stop()
    else:
        st.warning('Por favor, digite o nome de um filme antes de buscar!')

# Renderização dos Resultados
if st.session_state.recomendacoes:
    dados = st.session_state.recomendacoes

    if not isinstance(dados, dict):
        st.error("Resposta inválida da API.")
        st.stop()

    if 'erro' in dados:
        st.warning(f"⚠️ {dados['erro']}")
        st.info("💡 **Dica:** Tente títulos originais em inglês (ex: *The Dark Knight*, *Pulp Fiction*, *Inception*).")
        st.stop()

    filme_base = dados.get('base', filme_busca)
    todos = dados.get('recomendacoes', [])

    if not todos:
        st.info("Nenhuma recomendação encontrada para este filme.")
        st.stop()

    # Cabeçalho da seção de resultados
    col_res_header, col_res_count = st.columns([3, 1], vertical_alignment="center")
    with col_res_header:
        st.markdown(
            f"### 🍿 Recomendações para: <span style='color: #ff4d58;'>{html.escape(filme_base)}</span>",
            unsafe_allow_html=True
        )
    with col_res_count:
        st.markdown(
            f"<div style='text-align: right; color: #94a3b8; font-size: 0.92rem; font-weight: 500;'>Total: <strong>{len(todos)}</strong> filmes</div>",
            unsafe_allow_html=True
        )

    # Paginação
    por_pagina = 5
    total_paginas = (len(todos) - 1) // por_pagina
    inicio = st.session_state.pagina * por_pagina
    fim = inicio + por_pagina
    pagina_atual = todos[inicio:fim]

    # Exibição dos cards
    for item in pagina_atual:
        info = buscar_info_filme(item['titulo'])

        poster = info['poster'] if (info and info.get('poster')) else POSTER_FALLBACK_SVG
        ano = info.get('ano', '') if info else ''
        nota = f"{info['nota']:.1f}/10" if (info and info.get('nota')) else 'N/A'
        sinopse = info.get('sinopse', 'Sinopse não disponível para esta produção.') if info else 'Sinopse não disponível para esta produção.'

        titulo_safe = html.escape(item['titulo'])
        sinopse_safe = html.escape(sinopse)
        score_val = float(item.get('score', 0))
        score_pct = int(round(score_val * 100))

        # Montagem do Card HTML
        ano_badge = f"<span class='badge badge-year'>📅 {ano}</span>" if ano else ""
        card_html = f"""
        <div class="movie-card">
            <div class="poster-container">
                <img src="{poster}" alt="{titulo_safe}" class="movie-poster" loading="lazy" />
                <div class="score-badge">🎯 {score_pct}% Afinidade</div>
            </div>
            <div class="movie-details">
                <div class="movie-header">
                    <h3 class="movie-title">🎬 {titulo_safe}</h3>
                    {ano_badge}
                </div>
                <div class="badges-row">
                    <span class="badge badge-rating">⭐ TMDB: <strong>{nota}</strong></span>
                    <span class="badge badge-affinity">🔥 Score: <strong>{score_val:.2f}</strong></span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {min(max(score_pct, 5), 100)}%;"></div>
                    </div>
                </div>
                <p class="movie-synopsis">{sinopse_safe}</p>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # Navegação de Páginas
    st.markdown("<br>", unsafe_allow_html=True)
    col_ant, col_info, col_prox = st.columns([1.2, 2, 1.2], vertical_alignment="center")

    with col_ant:
        if st.session_state.pagina > 0:
            if st.button("⬅️ Anterior", type="secondary", use_container_width=True):
                st.session_state.pagina -= 1
                st.rerun()

    with col_info:
        st.markdown(
            f"<div class='pagination-info'>Página <strong>{st.session_state.pagina + 1}</strong> de <strong>{total_paginas + 1}</strong></div>",
            unsafe_allow_html=True
        )

    with col_prox:
        if st.session_state.pagina < total_paginas:
            if st.button("Próximos ➡️", type="primary", use_container_width=True):
                st.session_state.pagina += 1
                st.rerun()

    st.divider()

else:
    # Estado inicial / Boas-vindas quando nenhuma busca foi realizada
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🍿</div>
        <div class="empty-title">Pronto para encontrar sua próxima maratona?</div>
        <div class="empty-desc">
            Digite o nome de uma produção que você curte no campo acima ou clique em uma das sugestões populares abaixo para ver a IA em ação:
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; font-weight: 600; color: #94a3b8; margin-bottom: 12px;'>✨ Recomendações instantâneas populares:</p>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    filmes_demo = ["Inception", "The Dark Knight", "Avatar", "Pulp Fiction", "Interstellar"]
    
    for col, demo_filme in zip([col1, col2, col3, col4, col5], filmes_demo):
        with col:
            if st.button(f"🎬 {demo_filme}", key=f"demo_{demo_filme}", use_container_width=True):
                st.session_state.filme_escolhido = demo_filme
                st.session_state.filme_fixado = demo_filme
                st.session_state.pagina = 0
                with st.spinner(f"Buscando recomendações para {demo_filme}..."):
                    try:
                        resp = requests.get(f"{API_URL}/recomendacoes?filme={demo_filme}", timeout=10)
                        st.session_state.recomendacoes = resp.json()
                    except Exception:
                        st.session_state.recomendacoes = None
                st.rerun()
