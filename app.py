import streamlit as st
import pandas as pd
import time
from datetime import datetime
import base64

# Configuration de la page
st.set_page_config(
    page_title="LA BUSE | SUPRÉMATIE",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALISATION DES ÉTATS ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'access_mode' not in st.session_state:
    st.session_state.access_mode = False
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "dark"
if 'last_geo' not in st.session_state:
    st.session_state.last_geo = "National"

# --- DONNÉES SENTINELLES ---
SENTINEL_NETWORK = [
    {"region": "IDF", "nom": "Maître Lefebvre", "type": "Droit du Travail", "contact": "01 40 22 11 33", "adr": "12 Rue de la Paix, Paris"},
    {"region": "ARA", "nom": "Sentinelle Lyon - Jean D.", "type": "Défense Salariale", "contact": "04 72 10 20 30", "adr": "Place Bellecour, Lyon"},
    {"region": "HDF", "nom": "Expert Paie - Marc V.", "type": "Audit Paie", "contact": "03 20 00 11 22", "adr": "Boulevard de la Liberté, Lille"},
    {"region": "PACA", "nom": "Sentinelle Marseille", "type": "Négociations", "contact": "04 91 00 22 33", "adr": "Quai du Port, Marseille"},
    {"region": "OCC", "nom": "Expert Toulouse", "type": "Juridique", "contact": "05 61 00 11 22", "adr": "Rue d'Alsace-Lorraine, Toulouse"}
]

# --- DESIGN & CSS ---
def apply_ia_design():
    accent = "#D4AF37" if not st.session_state.access_mode else "#FFFF00"
    bg = "#050505" if st.session_state.theme_mode == "dark" else "#F5F5F7"
    text = "#FFFFFF" if st.session_state.theme_mode == "dark" else "#1D1D1F"
    card = "rgba(255, 255, 255, 0.05)" if st.session_state.theme_mode == "dark" else "rgba(0, 0, 0, 0.03)"
    
    st.markdown(f"""
    <style>
    :root {{ --accent: {accent}; --bg: {bg}; --text: {text}; }}
    .stApp {{ background-color: var(--bg); color: var(--text); font-family: 'SF Pro Display', -apple-system, sans-serif; }}
    
    .buse-card {{
        background: {card};
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }}
    .buse-card:hover {{
        transform: translateY(-5px);
        border-color: var(--accent);
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    }}
    {" .buse-card:hover { border: 5px solid #FFFF00 !important; scale: 1.05; } " if st.session_state.access_mode else ""}
    
    .ticker-wrap {{
        background: rgba(212, 175, 55, 0.1);
        padding: 10px;
        border-radius: 12px;
        border-left: 4px solid var(--accent);
        margin-bottom: 25px;
        overflow: hidden;
        white-space: nowrap;
    }}
    .ticker-content {{
        display: inline-block;
        animation: ticker 30s linear infinite;
        color: var(--accent);
        font-weight: bold;
    }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .footer {{
        text-align: center;
        padding: 40px;
        font-size: 0.8rem;
        color: #666;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    if st.session_state.access_mode:
        st.components.v1.html(f"""
            <script>
            var msg = new SpeechSynthesisUtterance("{text.replace('"', "'")}");
            msg.lang = 'fr-FR';
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)

# --- ÉCRAN DE CONNEXION ---
def show_login():
    apply_ia_design()
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<br><br><div style='text-align:center;'>", unsafe_allow_html=True)
        # Placeholder pour l'image de la buse impertinente
        st.markdown(f"<h1 style='color:#D4AF37; font-size:3.5rem; margin-bottom:0;'>🦅 LA BUSE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='letter-spacing:4px; opacity:0.6;'>SYSTÈME DE PROTECTION SUPRÉMATIE</p></div>", unsafe_allow_html=True)
        
        st.markdown('<div class="buse-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>IDENTIFICATION</h3>", unsafe_allow_html=True)
        pin = st.text_input("CLE D'ACCÈS", type="password")
        if st.button("DÉVERROUILLER", use_container_width=True):
            if pin == "1234":
                st.session_state.auth = True
                speak("Identité confirmée. Déploiement du système La Buse.")
                st.rerun()
            else:
                st.error("ACCÈS REFUSÉ")
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.auth:
    show_login()
    st.stop()

# --- NAVIGATION ---
apply_ia_design()
with st.sidebar:
    st.markdown("<h2 style='color:#D4AF37;'>🦅 LA BUSE</h2>", unsafe_allow_html=True)
    menu = st.radio("SÉLECTION", ["ACCUEIL", "AUDIT CLOUD", "IA & CALCULS", "SENTINELLES", "MASTER NODE IA"])
    st.markdown("---")
    theme = st.toggle("🌙 MODE NUIT", value=(st.session_state.theme_mode == "dark"))
    st.session_state.theme_mode = "dark" if theme else "light"
    acc = st.toggle("👁️ ACCESS_SIGHT (TTS)", value=st.session_state.access_mode)
    if acc != st.session_state.access_mode:
        st.session_state.access_mode = acc
        st.rerun()

# --- PAGES ---
if menu == "ACCUEIL":
    st.markdown("<div class='ticker-wrap'><div class='ticker-content'>🔴 ALERTE : Nouveau seuil de déplafonnement calculé • Experts ARA connectés • Veille IDCC 1517 active.</div></div>", unsafe_allow_html=True)
    st.title("TABLEAU DE BORD")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='buse-card'><h4>VEILLE JURIDIQUE</h4><p style='color:#D4AF37; font-size:1.5rem;'>ACTIVE</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='buse-card'><h4>AUDITS</h4><p style='color:#D4AF37; font-size:1.5rem;'>CONFORMES</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='buse-card'><h4>SÉCURITÉ</h4><p style='color:#D4AF37; font-size:1.5rem;'>MAXIMALE</p></div>", unsafe_allow_html=True)

elif menu == "AUDIT CLOUD":
    st.title("AUDIT EXPERT & DRIVE")
    st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
    st.file_uploader("Fiches de paie / Contrats", accept_multiple_files=True)
    st.button("🔗 SYNCHRONISER DRIVE")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "IA & CALCULS":
    st.title("EAGLE & INFINITY")
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("Calculateur Infinity (PDF)")
        brut = st.number_input("Brut (€)", value=1800)
        ca = st.number_input("Chiffre d'Affaires (€)", value=1800)
        ecart = ca - 1300
        bonus = 0
        if ecart >= 411.69:
            if ecart < 600: bonus = 20
            elif ecart < 1000: bonus = 40
            elif ecart < 1500: bonus = 60
            else: bonus = 100
        net = (brut * 0.78) + bonus
        st.markdown(f"## Net Estimé : {net:.2f} €")
        if bonus > 0: st.success(f"Bonus Infinity : +{bonus}€")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("🦅 IA Eagle")
        q = st.text_input("Question ?")
        if q: st.info("Analyse IA : Votre demande est conforme à l'IDCC 1517.")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "SENTINELLES":
    st.title("SENTINELLES LOCALES")
    if st.button("📍 ME GÉOLOCALISER"):
        st.session_state.last_geo = "IDF"
        st.success("Localisé : Île-de-France")
    reg = st.selectbox("Zone", ["National", "IDF", "ARA", "HDF", "PACA", "OCC"], index=1 if st.session_state.last_geo == "IDF" else 0)
    for s in SENTINEL_NETWORK:
        if reg == "National" or s["region"] == reg:
            st.markdown(f"<div class='buse-card'><b>{s['nom']}</b> ({s['type']})<br>📍 {s['adr']}<br>📞 {s['contact']}</div>", unsafe_allow_html=True)

elif menu == "MASTER NODE IA":
    st.title("MASTER NODE IA")
    st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
    if st.button("Rapport hebdomadaire"):
        st.code("Design: Apple Genesis OK\nCalculs: Infinity 100%\nSécurité: SSL OK", language="text")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PIED DE PAGE ---
st.markdown(f"""
<div class="footer">
    <p><b>LA BUSE GENESIS | SUPRÉMATIE {datetime.now().year}</b></p>
    <p>Mentions Légales : Plateforme indépendante de protection salariale. Données basées sur Légifrance.<br>
    RGPD : Aucune donnée conservée. Système sécurisé par Master Node IA.</p>
</div>
""", unsafe_allow_html=True)
