import streamlit as st
import pandas as pd
from datetime import datetime
import time
import base64
import struct
import json

# Configuration de la page
st.set_page_config(
    page_title="La Buse Pro - Protection Sociale",
    page_icon="🦅",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialisation des états
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'last_audit' not in st.session_state:
    st.session_state.last_audit = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'accessibility_mode' not in st.session_state:
    st.session_state.accessibility_mode = False

def speak_text(text):
    """Utilise l'API Web Speech du navigateur pour une lecture immédiate."""
    # Cette fonction génère un petit script JS pour forcer la lecture
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text.replace('"', "'")}");
    msg.lang = 'fr-FR';
    window.speechSynthesis.speak(msg);
    </script>
    """
    return js_code

# CSS pour le design et l'accessibilité
accessibility_css = ""
hover_js = ""

if st.session_state.accessibility_mode:
    accessibility_css = """
    :root {
        --bg-color: #000000 !important;
        --card-bg: #1a1a1a !important;
        --text-main: #FFFF00 !important;
        --text-sub: #FFFFFF !important;
        --primary: #FFFF00 !important;
        --border-color: #FFFF00 !important;
    }
    html, body, [class*="css"] {
        font-size: 1.25rem !important;
    }
    .stButton>button {
        border: 3px solid #FFFF00 !important;
        font-size: 1.4rem !important;
        color: #FFFF00 !important;
    }
    """
    # Script JS pour la lecture au survol
    hover_js = """
    <script>
    document.querySelectorAll('p, h1, h2, h3, span, li, .stMarkdown').forEach(item => {
        item.addEventListener('mouseenter', event => {
            var msg = new SpeechSynthesisUtterance(event.target.innerText);
            msg.lang = 'fr-FR';
            window.speechSynthesis.speak(msg);
        });
        item.addEventListener('mouseleave', event => {
            window.speechSynthesis.cancel();
        });
    });
    </script>
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    :root {{
        --primary: #007AFF;
        --accent: #f26b21;
        --bg-color: #f8f9fa;
        --card-bg: #ffffff;
        --text-main: #1c1c1e;
        --text-sub: #636366;
        --border-color: #e5e5ea;
    }}

    {accessibility_css}

    .stApp {{ background-color: var(--bg-color); }}
    
    .premium-card {{
        background: var(--card-bg);
        border-radius: 20px;
        padding: 24px;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }}

    .eagle-banner {{
        width: 100%;
        border-radius: 25px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }}
    </style>
    """, unsafe_allow_html=True)

# Injection du script de survol si mode actif
if st.session_state.accessibility_mode:
    st.components.v1.html(hover_js, height=0)

def check_pin():
    if st.session_state.pin_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("Code PIN incorrect.")

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Image de buse majestueuse et protectrice
    st.image("https://images.unsplash.com/photo-1535136128062-8e3676c8c77f?q=80&w=1000&auto=format&fit=crop", 
             caption="La Buse Pro - Votre Vigilance Sociale", use_container_width=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>ESPACE SÉCURISÉ</h1>", unsafe_allow_html=True)
        st.text_input("Code PIN d'accès (1234)", type="password", key="pin_input", on_change=check_pin)
    st.stop()

with st.sidebar:
    st.markdown("## 🦅 Agent Eagle")
    st.image("https://img.icons8.com/fluency/96/eagle.png", width=60)
    
    st.toggle("♿ Mode Accessibilité (Contrast+)", key="accessibility_mode")
    
    if st.session_state.accessibility_mode:
        if st.button("🔊 Lire le résumé du site"):
            st.components.v1.html(speak_text("Bienvenue sur votre tableau de bord La Buse Pro. Ce site vous permet de chercher dans le code du travail, d'analyser vos bulletins et de suivre les actualités de Boulanger."), height=0)
    
    st.markdown("---")
    chat_input = st.chat_input("Posez une question à Eagle...")
    if chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        # Simulation réponse IA
        response = "D'après la convention 1517, vous avez droit à une pause de 20 minutes après 6h de travail."
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history[-2:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

st.title("Tableau de Bord Social")

# Moteur de recherche juridique (Toujours visible)
search_query = st.text_input("🔍 Recherche Intelligente (Code du Travail / Convention 1517)", placeholder="Ex: Prime d'ancienneté, rupture conventionnelle...")
if search_query:
    st.info(f"Résultat pour '{search_query}' : L'Article L1234-1 précise les modalités de préavis...")

tab1, tab2, tab3, tab4 = st.tabs(["🕵️ Audit Expert", "📊 Rapports", "📢 Défends tes droits", "📜 Jurisprudence"])

with tab1:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Analyse Multi-Documents")
    files = st.file_uploader("Glissez vos documents (PDF/JPG)", accept_multiple_files=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: statut = st.selectbox("Statut", ["Employé", "Maîtrise", "Cadre"])
    with c2: contrat = st.selectbox("Contrat", ["35h", "28h", "Autre"])
    with c3: rdth = st.toggle("Option RDTH")
    
    if st.button("Lancer l'audit massif"):
        if files:
            with st.status("🔍 la buse cherche sa proie...") as s:
                time.sleep(2)
                st.session_state.last_audit = {
                    "date": datetime.now().strftime("%d/%m/%Y"),
                    "anomalies": ["Erreur de majoration dimanche (ligne 14).", "Anomalie calcul prime RDTH confirmée."],
                    "nb_fichiers": len(files)
                }
                s.update(label="Audit Terminé !", state="complete")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    if st.session_state.last_audit:
        audit = st.session_state.last_audit
        st.subheader(f"Rapport d'anomalies - {audit['nb_fichiers']} fichiers")
        for ano in audit['anomalies']:
            st.error(f"⚠️ {ano}")
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1: st.button("📥 Imprimer le rapport")
        with col_ex2: st.button("📧 Envoyer aux délégués")
    else:
        st.info("Aucun audit en cours. Utilisez l'onglet Audit Expert.")

with tab3:
    st.markdown("### 📰 Actualités Syndicales Boulanger")
    news = [
        {"t": "NAO 2026 : LA DIRECTION BLOQUE !", "d": "Les syndicats appellent à la vigilance sur les salaires."},
        {"t": "PRIME PPV : 500€ POUR LES LUTINS", "d": "Victoire syndicale sur le versement de juin."}
    ]
    for n in news:
        st.markdown(f"""
        <div style='border-left:5px solid red; padding:15px; background:white; margin-bottom:10px; border-radius:0 10px 10px 0;'>
            <h4 style='color:black; margin:0;'>{n['t']}</h4>
            <p style='color:#333; margin:5px 0 0 0;'>{n['d']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("Convention Collective 1517")
    st.markdown("""
    - **Ancienneté :** 3% à 3 ans, 6% à 6 ans, 9% à 9 ans...
    - **Heures Supplémentaires :** Majoration de 25% pour les 8 premières heures.
    - **Travail du Dimanche :** Majoration de 100% du salaire horaire.
    """)

st.markdown("---")
st.caption("La Buse Pro v7.0 | Design Protecteur & Inclusif" crée par Yann COLAS DAVID )

st.sidebar.caption("La Buse Pro v6.5 | Mode Accessibilité Actif")
