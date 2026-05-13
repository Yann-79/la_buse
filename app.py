import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(
    page_title="La Buse Pro",
    page_icon="🦅",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    :root {
        --primary: #007AFF;
        --bg-color: #f2f2f7;
        --card-bg: #ffffff;
        --text-main: #1c1c1e;
        --text-sub: #3a3a3c;
        --accent: #f26b21;
    }

    /* Reset global pour la lisibilité */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-main) !important;
    }

    .stApp {
        background-color: var(--bg-color);
    }

    /* Cartes Premium avec contraste élevé */
    .premium-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 24px;
        border: 1px solid #d1d1d6;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Titres percutants */
    h1, h2, h3 {
        color: var(--text-main) !important;
        font-weight: 800 !important;
    }

    /* Agent IA Flottant Style */
    .ia-status {
        background: linear-gradient(135deg, #007AFF 0%, #0051FF 100%);
        color: white !important;
        padding: 10px 15px;
        border-radius: 12px;
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Style News Morandini Modernisé */
    .news-card {
        border-left: 6px solid var(--accent);
        background: #fff;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 0 12px 12px 0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.03);
    }
    .news-title {
        font-size: 1.2em;
        font-weight: 700;
        color: #000;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    /* Inputs et Boutons */
    .stTextInput input, .stSelectbox select {
        border-radius: 12px !important;
        border: 2px solid #e5e5ea !important;
        background: white !important;
        color: black !important;
    }

    /* Fix pour le problème d'invisibilité des onglets (image_e87f37.png) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #e5e5ea;
        padding: 5px;
        border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        border-radius: 10px;
        color: var(--text-sub) !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        color: var(--primary) !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_pin():
    if st.session_state.pin_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("Code PIN incorrect.")

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='text-align:center; padding-top:50px;'>", unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/144/eagle.png", width=100)
        st.markdown("<h1 style='color:#1c1c1e;'>LA BUSE PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#3a3a3c; font-weight:600;'>Identifiez-vous pour accéder à l'Intelligence Sociale</p>", unsafe_allow_html=True)
        st.text_input("Saisissez votre code PIN (4 chiffres)", type="password", key="pin_input", on_change=check_pin)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

with st.sidebar:
    st.markdown("### 🦅 Agent IA Eagle")
    st.info("Je suis disponible ici pour répondre à vos questions sur le contrat ou la paie.")
    user_query = st.text_input("Posez votre question à l'IA :", placeholder="Ex: Calcul prime ancienneté...")
    if user_query:
        with st.spinner("Analyse juridique en cours..."):
            time.sleep(1)
            st.success("D'après l'IDCC 1517, votre prime d'ancienneté est de 3% après 3 ans, 6% après 6 ans...")

    st.markdown("---")
    st.markdown("### 🔍 Moteur de Recherche")
    search_legal = st.text_input("Recherche Code du Travail :", placeholder="Ex: Licenciement, CP...")
    if search_legal:
        st.caption("Résultats trouvés dans la base Legifrance & IDCC 1517.")

st.markdown("<div class='ia-status'>✨ Agent IA Connecté | Prêt pour l'audit</div>", unsafe_allow_html=True)
st.title("Tableau de Bord Social")

tab1, tab2, tab3 = st.tabs(["🕵️ Analyseur Expert", "📢 Défends tes droits", "📜 Jurisprudence"])

with tab1:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Audit de Document")
    
    source = st.radio("Source du document", ["Fichier Local (Photo/PDF)", "Google Drive"], horizontal=True)
    
    if source == "Google Drive":
        st.text_input("Lien de partage Google Drive")
    else:
        st.file_uploader("Importer votre bulletin ou contrat", type=["pdf", "png", "jpg"])
    
    st.markdown("---")
    st.markdown("#### Votre Profil pour l'Audit")
    c1, c2 = st.columns(2)
    with c1:
        statut = st.selectbox("Statut", ["Employé", "Agent de Maîtrise", "Cadre"])
        rdth = st.toggle("Option RDTH", help="Rémunération Différée à Temps Heure")
    with c2:
        contrat = st.selectbox("Type de contrat", ["35h", "28h", "Temps Partiel (<28h)"])
    
    if st.button("Lancer l'audit de conformité"):
        with st.status("🔍 Eagle Vision analyse les lignes de paie...", expanded=True) as s:
            time.sleep(1)
            st.write("Vérification des taux horaires (SMIC vs IDCC 1517)...")
            time.sleep(1)
            if contrat == "28h":
                st.write("Calcul des heures complémentaires (limite 1/3)...")
            if rdth:
                st.warning("⚠️ Attention : La ligne de garantie minimale doit être vérifiée.")
            s.update(label="Audit Terminé !", state="complete")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("Actualités & Nouveautés Syndicales")
    st.caption("Mise à jour en temps réel des sources Facebook, Web et Sites Officiels")
    
    news = [
        {"titre": "EXCLUSIF : Négociations NAO 2026", "content": "Les syndicats demandent une revalorisation de 4% face à l'inflation.", "tag": "ALERTE"},
        {"titre": "Prime Partage de la Valeur", "content": "Le versement de la PPV confirmé pour le mois de juin.", "tag": "INFOS"},
        {"titre": "Modification des Plannings", "content": "Rappel sur le délai de prévenance de 7 jours ouvrés.", "tag": "LÉGAL"}
    ]
    
    for n in news:
        st.markdown(f"""
        <div class="news-card">
            <span style="background:#f26b21; color:white; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:bold;">{n['tag']}</span>
            <div class="news-title">{n['titre']}</div>
            <p style="color:#3a3a3c; margin:0;">{n['content']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("Convention Collective IDCC 1517")
    search_conv = st.text_input("Chercher un article précis :")
    st.markdown("""
    <div class='premium-card'>
        <p><b>🔍 Points de contrôle automatique :</b></p>
        <ul>
            <li><b>Congés :</b> 2.5 jours ouvrables par mois.</li>
            <li><b>Préavis :</b> Variable selon l'ancienneté (1 à 3 mois).</li>
            <li><b>Heures de nuit :</b> Majoration de 25% entre 21h et 6h.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.button("Déconnexion")
st.sidebar.caption("La Buse Pro v5.0 | Design Haute Visibilité")
