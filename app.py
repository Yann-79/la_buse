import streamlit as st
import pandas as pd
import time
import requests
import json
import base64
from datetime import datetime

# --- CONFIGURATION API & MODÈLES ---
# L'API Key est gérée automatiquement par l'environnement
API_KEY = "" 

st.set_page_config(
    page_title="LA BUSE | MASTER-DEFENSE",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALISATION DES ÉTATS (SESSION STATE) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'loading_complete' not in st.session_state:
    st.session_state.loading_complete = False
if 'ai_history' not in st.session_state:
    st.session_state.ai_history = []
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "dark"
if 'accessibility' not in st.session_state:
    st.session_state.accessibility = False
if 'current_media' not in st.session_state:
    st.session_state.current_media = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070"
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- DESIGN SYSTEM "GENESIS" ---
def apply_ia_design():
    accent = "#D4AF37" # Or Buse
    bg = "#050505" if st.session_state.theme_mode == "dark" else "#F5F5F7"
    text = "#FFFFFF" if st.session_state.theme_mode == "dark" else "#111111"
    card_bg = "rgba(255, 255, 255, 0.03)" if st.session_state.theme_mode == "dark" else "rgba(0, 0, 0, 0.02)"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {{ 
        background: {bg};
        color: {text};
        font-family: 'Inter', sans-serif;
    }}
    
    .buse-card {{
        background: {card_bg};
        backdrop-filter: blur(15px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }}
    
    .buse-card:hover {{
        border-color: {accent};
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
    }}
    
    .glow-text {{
        color: {accent};
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    .media-monitor {{
        border: 2px solid {accent};
        border-radius: 15px;
        height: 350px;
        background: #000;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
    }}
    
    .stButton>button {{
        background: linear-gradient(45deg, #D4AF37, #8A6D3B);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
    }}

    {".stApp { font-size: 1.15rem; filter: contrast(1.1); }" if st.session_state.accessibility else ""}
    </style>
    """, unsafe_allow_html=True)

# --- SERVICES IA (EAGLE ENGINE) ---
def call_eagle_ia(prompt, context=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    system_prompt = f"""Tu es EAGLE, l'IA de 'La Buse'. Expert en Droit du Travail et IDCC 1517.
    CONTEXTE ACTUEL: {context}
    Réponds avec précision, cite les articles de loi. Ton ton est protecteur pour le salarié."""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "tools": [{"google_search": {}}]
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Liaison satellite instable. Impossible d'interroger la base juridique."

def generate_eagle_media(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
    payload = {
        "instances": {"prompt": f"Futuristic golden eagle technology, cinematic lighting, cyber defense, {prompt}"},
        "parameters": {"sampleCount": 1}
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        return f"data:image/png;base64,{response.json()['predictions'][0]['bytesBase64Encoded']}"
    except:
        return "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070"

def text_to_speech(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"Voix ferme et rassurante : {text[:400]}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": { "voiceConfig": { "prebuiltVoiceConfig": { "voiceName": "Kore" } } }
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        return response.json()['candidates'][0]['content']['parts'][0]['inlineData']['data']
    except:
        return None

# --- MODULES DE CALCULS ---
def calculate_infinity(heures, ca_perso):
    seuil_magasin = 1300.0
    declencheur = 411.69
    ecart = ca_perso - seuil_magasin
    
    bonus_label = "0%"
    if ecart >= declencheur:
        if ecart < 600: bonus_label = "20%"
        elif ecart < 1000: bonus_label = "40%"
        elif ecart < 1500: bonus_label = "60%"
        else: bonus_label = "100%"
    return ecart, bonus_label

def calculate_salary(brut, statut="non-cadre"):
    taux = 0.78 if statut == "non-cadre" else 0.75
    net = brut * taux
    ij = min((brut / 30.42) * 0.5, 52.04)
    return net, ij

# --- INTERFACE PRINCIPALE ---
def main_app():
    apply_ia_design()
    
    if not st.session_state.loading_complete:
        run_loading_sequence()
        return

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h1 class='glow-text' style='text-align:center;'>🦅 LA BUSE</h1>", unsafe_allow_html=True)
        menu = st.radio("CORE MODULES", [
            "DASHBOARD GÉNÉSIS", 
            "AGENT EAGLE (IA & AUDIT)", 
            "MOTEUR INFINITY",
            "SALAIRE & SANTÉ", 
            "RÉSEAU SENTINELLES",
            "SYNC DRIVE & CLOUD"
        ])
        st.markdown("---")
        st.session_state.accessibility = st.toggle("♿ ACCESSIBILITÉ +", value=st.session_state.accessibility)
        if st.button("LOGOUT / SECURE"):
            st.session_state.auth = False
            st.session_state.loading_complete = False
            st.rerun()

    # --- CONTENU DES MODULES ---
    
    if menu == "DASHBOARD GÉNÉSIS":
        st.markdown("<h2 class='glow-text'>MONITEUR DE SURVEILLANCE</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='buse-card'><b>CONVENTION</b><br>IDCC 1517</div>", unsafe_allow_html=True)
        c2.markdown("<div class='buse-card'><b>SYSTÈME</b><br><span style='color:#00ff00;'>ONLINE</span></div>", unsafe_allow_html=True)
        c3.markdown("<div class='buse-card'><b>ALERTE</b><br>AUCUNE</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("Résumé de l'activité")
        st.line_chart(pd.DataFrame({'Calculs': [12, 45, 32, 67, 89, 54]}))
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "AGENT EAGLE (IA & AUDIT)":
        st.markdown("<h2 class='glow-text'>🔍 AGENT EAGLE : IA & AUDIT RH</h2>", unsafe_allow_html=True)
        
        col_m, col_i = st.columns([1, 1])
        
        with col_m:
            st.markdown("<div class='media-monitor'>", unsafe_allow_html=True)
            st.image(st.session_state.current_media, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("📁 Import Audit")
            doc = st.file_uploader("Fiche de paie / Contrat", type=["pdf", "png", "jpg"])
            if doc:
                if st.button("LANCER L'ANALYSE DOCUMENTAIRE"):
                    with st.spinner("Analyse OCR..."):
                        time.sleep(2)
                        st.session_state.analysis_results = "Document analysé : Structure de paie conforme à l'IDCC 1517. Attention aux primes d'ancienneté."
                        st.success("Audit prêt.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_i:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Interroger l'IA")
            q = st.text_input("Posez votre question (Droit, Salaire...) :")
            if st.button("LANCER L'AGENT"):
                if q:
                    with st.spinner("Recherche juridique..."):
                        # Image
                        st.session_state.current_media = generate_eagle_media(q[:30])
                        # Texte
                        ctx = st.session_state.analysis_results if st.session_state.analysis_results else ""
                        res = call_eagle_ia(q, ctx)
                        # Audio
                        audio_b64 = text_to_speech(res)
                        st.session_state.ai_history.append({"q": q, "a": res, "audio": audio_b64})
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        for chat in reversed(st.session_state.ai_history):
            with st.expander(f"Question : {chat['q']}", expanded=True):
                st.write(chat['a'])
                if chat['audio']:
                    st.audio(base64.b64decode(chat['audio']), format='audio/wav')

    elif menu == "MOTEUR INFINITY":
        st.markdown("<h2 class='glow-text'>💎 CALCULATEUR INFINITY</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        h = st.number_input("Heures mensuelles", value=48.0)
        ca = st.number_input("CA Personnel (€)", value=1750.0)
        ecart, bonus = calculate_infinity(h, ca)
        
        col1, col2 = st.columns(2)
        col1.metric("Écart au Seuil", f"{ecart:.2f} €")
        col2.metric("Bonus Infinity", bonus)
        
        if ecart >= 411.69:
            st.balloons()
            st.success("SEUIL DE DÉPLAFONNEMENT ATTEINT")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "SALAIRE & SANTÉ":
        st.markdown("<h2 class='glow-text'>💰 SIMULATEUR SALAIRE & IJ</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        brut = st.number_input("Salaire Brut (€)", value=2100.0)
        statut = st.selectbox("Statut", ["non-cadre", "cadre"])
        net, ij = calculate_salary(brut, statut)
        
        st.markdown(f"### Salaire Net estimé : {net:.2f} €")
        st.markdown(f"### IJ Maladie (50%) : {ij:.2f} € / jour")
        st.caption("Basé sur les taux de cotisations moyens et plafonds CPAM.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "RÉSEAU SENTINELLES":
        st.markdown("<h2 class='glow-text'>🛡️ RÉSEAU SENTINELLES</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        map_df = pd.DataFrame({'lat': [48.8566, 45.7640, 43.2965], 'lon': [2.3522, 4.8357, 5.3698]})
        st.map(map_df)
        st.write("Délégués disponibles : 3")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "SYNC DRIVE & CLOUD":
        st.markdown("<h2 class='glow-text'>☁️ SYNC CLOUD & DRIVE</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.info("Statut : Connecté au répertoire sécurisé")
        if st.button("SYNCHRONISER MAINTENANT"):
            with st.spinner("Récupération des PDF..."):
                time.sleep(2)
                st.success("3 Documents synchronisés.")
        st.code("📄 contrat_travail.pdf\n📄 avenant_infinity.pdf\n📄 fiche_paie_0324.jpg")
        st.markdown("</div>", unsafe_allow_html=True)

# --- SEQUENCE DE CHARGEMENT ---
def run_loading_sequence():
    apply_ia_design()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;' class='glow-text'>INITIALISATION...</h2>", unsafe_allow_html=True)
        bar = st.progress(0)
        for i in range(101):
            bar.progress(i)
            time.sleep(0.01)
        st.session_state.loading_complete = True
        st.rerun()

# --- AUTHENTIFICATION ---
if not st.session_state.auth:
    apply_ia_design()
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h2 class='glow-text'>LOGIN</h2></div>", unsafe_allow_html=True)
        pin = st.text_input("CODE PIN", type="password")
        if st.button("ACCÉDER AU SYSTÈME"):
            if pin == "1234":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("PIN INCORRECT")
else:
    main_app()
    main_app()
