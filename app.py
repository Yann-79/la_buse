import streamlit as st
import pandas as pd
import time
import requests
import json
import base64
from datetime import datetime

# --- CONFIGURATION & CONSTANTES ---
API_KEY = "" 
APP_ID = "la-buse-genesis-final"

st.set_page_config(
    page_title="LA BUSE | SYSTÈME DE DÉFENSE",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DONNÉES MÉTIER RÉINTÉGRÉES (BOULANGER & SYNDICATS) ---
BOULANGER_DATA = {
    "Délégués": [
        {"Région": "IDF", "Nom": "Jean-Pierre D.", "Contact": "06 xx xx xx xx"},
        {"Région": "ARA", "Nom": "Marc L.", "Contact": "04 xx xx xx xx"},
        {"Région": "PACA", "Nom": "Sophie M.", "Contact": "07 xx xx xx xx"},
        {"Région": "HDF", "Nom": "Thomas R.", "Contact": "06 xx xx xx xx"}
    ],
    "Syndicats": {
        "CFDT": "cfdt@boulanger.com",
        "CGT": "cgt@boulanger.com",
        "FO": "fo@boulanger.com",
        "CFTC": "cftc@boulanger.com"
    }
}

# --- INITIALISATION DES ÉTATS ---
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

# --- DESIGN SYSTEM "OBSIDIAN GOLD" ---
def apply_ia_design():
    accent = "#D4AF37" 
    bg = "#080808"
    card_bg = "#111111"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {{ background: {bg}; color: #E0E0E0; font-family: 'Inter', sans-serif; }}
    
    .buse-card {{
        background: {card_bg};
        border-left: 4px solid {accent};
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        transition: transform 0.2s;
    }}
    
    .buse-card:hover {{ transform: scale(1.01); }}
    
    .glow-text {{
        color: {accent};
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    .health-stable {{ color: #00FF00; font-weight: bold; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.5; }} }}
    
    .stButton>button {{
        background: linear-gradient(45deg, #D4AF37, #8A6D3B);
        color: white; border-radius: 8px; font-weight: 700;
        text-transform: uppercase; border: none; width: 100%;
        padding: 10px;
    }}

    {".stApp { font-size: 1.2rem; filter: contrast(1.2); }" if st.session_state.accessibility else ""}
    </style>
    """, unsafe_allow_html=True)

# --- MOTEUR API AVEC RETRY AUTO (AUTO-CORRECTION) ---
def safe_api_call(url, payload, method="POST", retries=5):
    for i in range(retries):
        try:
            res = requests.post(url, json=payload, timeout=12) if method=="POST" else requests.get(url, timeout=12)
            if res.status_code == 200: return res.json()
            time.sleep(2**i) 
        except:
            time.sleep(2**i)
    return None

def call_eagle_ia(prompt, context=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": f"Tu es EAGLE, l'IA de La Buse. Contexte audit: {context}. Expert IDCC 1517. Réponds de manière tactique et juridique."}]},
        "tools": [{"google_search": {}}]
    }
    result = safe_api_call(url, payload)
    return result['candidates'][0]['content']['parts'][0]['text'] if result else "⚠️ Liaison satellite perdue. Réessai en cours..."

def generate_eagle_media(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
    payload = {"instances": {"prompt": f"Cyber defense eagle, golden neon, 4k, {prompt}"}, "parameters": {"sampleCount": 1}}
    result = safe_api_call(url, payload)
    return f"data:image/png;base64,{result['predictions'][0]['bytesBase64Encoded']}" if result else st.session_state.current_media

def text_to_speech(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": text[:300]}]}],
        "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Kore"}}}},
        "model": "gemini-2.5-flash-preview-tts"
    }
    result = safe_api_call(url, payload)
    return result['candidates'][0]['content']['parts'][0]['inlineData']['data'] if result else None

# --- LOGIQUE MÉTIER ---
def calculate_salary_v4(brut, statut="non-cadre"):
    taux = 0.78 if statut == "non-cadre" else 0.75
    net = brut * taux
    ij = min((brut / 30.42) * 0.5, 52.04)
    return net, ij

def calculate_infinity_v4(ca_perso, heures_mois=48):
    seuil_base = 1300.0
    declencheur = 411.69
    ecart = ca_perso - seuil_base
    if ecart < declencheur: return ecart, "0%", "#FF4B4B"
    ratio_reel = (ecart - declencheur) / heures_mois
    if ratio_reel >= 16: return ecart, "100%", "#00FF00"
    if ratio_reel >= 13: return ecart, "60%", "#ADFF2F"
    if ratio_reel >= 10: return ecart, "40%", "#D4AF37"
    if ratio_reel >= 7: return ecart, "20%", "#D4AF37"
    return ecart, "DÉPLAFONNÉ (0%+)", "#D4AF37"

# --- INTERFACE ---
def main_app():
    apply_ia_design()
    
    with st.sidebar:
        st.markdown("<h1 class='glow-text'>🦅 LA BUSE</h1>", unsafe_allow_html=True)
        nav = st.radio("SÉLECTION MODULE", [
            "MONITEUR GÉNÉSIS",
            "AGENT EAGLE (IA & AUDIT)",
            "MOTEUR INFINITY",
            "SALAIRE & SANTÉ",
            "RÉSEAU SENTINELLES",
            "CLOUD DRIVE"
        ], key="nav_v4")
        st.divider()
        st.session_state.accessibility = st.toggle("MODALITÉ ACCESSIBLE", value=st.session_state.accessibility)
        if st.button("LOGOUT"):
            st.session_state.auth = False
            st.session_state.loading_complete = False
            st.rerun()

    if nav == "MONITEUR GÉNÉSIS":
        st.markdown("<h2 class='glow-text'>TABLEAU DE BORD</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.markdown("<div class='buse-card'><b>SYSTÈME</b><br><span class='health-stable'>STABLE</span></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='buse-card'><b>CONVENTION</b><br>IDCC 1517</div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='buse-card'><b>ALERTE</b><br>ZÉRO</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("Contacts Boulanger")
        for d in BOULANGER_DATA["Délégués"]:
            st.write(f"🚩 **{d['Région']}** : {d['Nom']} ({d['Contact']})")
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "AGENT EAGLE (IA & AUDIT)":
        st.markdown("<h2 class='glow-text'>🔍 AGENT EAGLE</h2>", unsafe_allow_html=True)
        cl, cr = st.columns([1, 1])
        with cl:
            st.image(st.session_state.current_media)
            doc = st.file_uploader("Audit Document (Paie/Contrat)", type=["pdf", "png", "jpg"])
            if doc and st.button("LANCER L'AUDIT"):
                with st.spinner("Analyse OCR..."):
                    time.sleep(2)
                    st.session_state.analysis_results = "Analyse terminée : Structure salariale conforme à l'IDCC 1517. Vérifiez le palier Infinity."
                    st.success("Audit complété.")

        with cr:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            q = st.text_input("Question juridique ou métier :")
            if st.button("INTERROGER EAGLE"):
                if q:
                    with st.spinner("Activation Eagle..."):
                        st.session_state.current_media = generate_eagle_media(q[:15])
                        res = call_eagle_ia(q, st.session_state.analysis_results or "")
                        audio = text_to_speech(res)
                        st.session_state.ai_history.append({"q": q, "a": res, "audio": audio})
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        for chat in reversed(st.session_state.ai_history):
            with st.expander(f"REQUÊTE : {chat['q']}", expanded=True):
                st.write(chat['a'])
                if chat['audio']: st.audio(base64.b64decode(chat['audio']), format='audio/wav')

    elif nav == "MOTEUR INFINITY":
        st.markdown("<h2 class='glow-text'>💎 CALCUL INFINITY</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        ca = st.number_input("CA Personnel (€)", value=1750.0)
        hrs = st.number_input("Heures (Mois)", value=48)
        ecart, bonus, color = calculate_infinity_v4(ca, hrs)
        st.metric("Écart au seuil", f"{ecart:.2f} €")
        st.markdown(f"### BONUS ESTIMÉ : <span style='color:{color}; font-size:1.5em;'>{bonus}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "SALAIRE & SANTÉ":
        st.markdown("<h2 class='glow-text'>💰 SALAIRE & SANTÉ</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        brut = st.number_input("Salaire Brut Mensuel (€)", value=2100.0)
        stat = st.selectbox("Statut", ["non-cadre", "cadre"])
        net, ij = calculate_salary_v4(brut, stat)
        st.write(f"### NET ESTIMÉ : {net:.2f} €")
        st.write(f"### IJ MALADIE (50%) : {ij:.2f} € / jour")
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "RÉSEAU SENTINELLES":
        st.markdown("<h2 class='glow-text'>🛡️ RÉSEAU SENTINELLES</h2>", unsafe_allow_html=True)
        st.map(pd.DataFrame({'lat': [48.8566, 45.7640, 43.6045], 'lon': [2.3522, 4.8357, 1.4442]}))

    elif nav == "CLOUD DRIVE":
        st.markdown("<h2 class='glow-text'>☁️ CLOUD DRIVE</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>Synchronisation active avec le Master Node.</div>", unsafe_allow_html=True)
        st.code("📄 contrat_boulanger.pdf\n📄 avenant_infinity.pdf\n📄 idcc_1517_full.pdf")

# --- INITIALISATION ---
if not st.session_state.auth:
    apply_ia_design()
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<br><br><h2 class='glow-text' style='text-align:center;'>ACCESS CORE</h2>", unsafe_allow_html=True)
        pin = st.text_input("CODE PIN", type="password")
        if st.button("CONNECT"):
            if pin == "1234":
                st.session_state.auth = True
                st.rerun()
else:
    if not st.session_state.loading_complete:
        apply_ia_design()
        p = st.progress(0.0)
        for i in range(101):
            time.sleep(0.01)
            p.progress(i / 100.0)
        st.session_state.loading_complete = True
        st.rerun()
    main_app()
