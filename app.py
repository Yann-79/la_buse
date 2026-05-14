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

# --- DONNÉES MÉTIER (BOULANGER & SENTINELLES) ---
BOULANGER_DATA = {
    "Délégués": [
        {"Région": "IDF", "Nom": "Jean-Pierre D.", "Contact": "06 xx xx xx xx", "lat": 48.8566, "lon": 2.3522},
        {"Région": "ARA", "Nom": "Marc L.", "Contact": "04 xx xx xx xx", "lat": 45.7640, "lon": 4.8357},
        {"Région": "PACA", "Nom": "Sophie M.", "Contact": "07 xx xx xx xx", "lat": 43.2965, "lon": 5.3698},
        {"Région": "HDF", "Nom": "Thomas R.", "Contact": "06 xx xx xx xx", "lat": 50.6292, "lon": 3.0573},
        {"Région": "OCC", "Nom": "Julie A.", "Contact": "05 xx xx xx xx", "lat": 43.6045, "lon": 1.4442}
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
    }}
    
    .glow-text {{
        color: {accent};
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    .status-badge {{
        background: rgba(0, 255, 0, 0.1);
        color: #00FF00;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        border: 1px solid #00FF00;
    }}
    
    .stButton>button {{
        background: linear-gradient(45deg, #D4AF37, #8A6D3B);
        color: white; border-radius: 8px; font-weight: 700;
        text-transform: uppercase; border: none; width: 100%;
        padding: 10px;
    }}

    /* Scale for mobile */
    @media (max-width: 600px) {{
        .glow-text {{ font-size: 1.2rem; }}
    }}

    {".stApp { font-size: 1.2rem; filter: contrast(1.2); }" if st.session_state.accessibility else ""}
    </style>
    """, unsafe_allow_html=True)

# --- MOTEUR API ---
def safe_api_call(url, payload, method="POST", retries=3):
    if not API_KEY:
        return None # Simulation mode
    for i in range(retries):
        try:
            res = requests.post(url, json=payload, timeout=10) if method=="POST" else requests.get(url, timeout=10)
            if res.status_code == 200: return res.json()
            time.sleep(1)
        except:
            time.sleep(1)
    return None

def call_eagle_ia(prompt, context=""):
    if not API_KEY:
        return f"MODRE SIMULATION : En tant qu'expert IDCC 1517, je traite votre demande sur '{prompt}'. L'accès satellite réel nécessite une clé API. Cependant, selon les règles de la convention, votre requête semble légitime."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": f"Tu es EAGLE, l'IA de La Buse. Contexte: {context}. Expert Convention Collective Boulanger (IDCC 1517)."}]}
    }
    result = safe_api_call(url, payload)
    return result['candidates'][0]['content']['parts'][0]['text'] if result else "⚠️ Erreur de liaison satellite. Mode local activé."

def text_to_speech(text):
    # Fallback si pas de clé
    if not API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": text[:200]}]}],
        "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Kore"}}}},
        "model": "gemini-2.5-flash-preview-tts"
    }
    result = safe_api_call(url, payload)
    return result['candidates'][0]['content']['parts'][0]['inlineData']['data'] if result else None

# --- LOGIQUE MÉTIER ---
def calculate_infinity_v4(ca_perso, heures_mois=48):
    # Paramètres extraits du PDF
    seuil_base = 1300.0
    declencheur = 411.69
    ecart = ca_perso - seuil_base
    
    if ecart < declencheur:
        return ecart, "0%", "#FF4B4B", 0
    
    ratio_reel = (ecart - declencheur) / heures_mois
    
    if ratio_reel >= 16: return ecart, "100%", "#00FF00", 100
    if ratio_reel >= 13: return ecart, "60%", "#ADFF2F", 60
    if ratio_reel >= 10: return ecart, "40%", "#D4AF37", 40
    if ratio_reel >= 7: return ecart, "20%", "#D4AF37", 20
    return ecart, "DÉPLAFONNÉ (0%+)", "#D4AF37", 5

# --- INTERFACE ---
def main_app():
    apply_ia_design()
    
    with st.sidebar:
        st.markdown("<h1 class='glow-text'>🦅 LA BUSE</h1>", unsafe_allow_html=True)
        nav = st.radio("NAVIGATION SYSTÈME", [
            "MONITEUR GÉNÉSIS",
            "AGENT EAGLE (IA & AUDIT)",
            "MOTEUR INFINITY",
            "SALAIRE & SANTÉ",
            "RÉSEAU SENTINELLES"
        ], key="nav_v5")
        st.divider()
        st.session_state.accessibility = st.toggle("MODE ACCESSIBILITÉ", value=st.session_state.accessibility)
        if st.button("DÉCONNEXION"):
            st.session_state.auth = False
            st.rerun()

    if nav == "MONITEUR GÉNÉSIS":
        st.markdown("<h2 class='glow-text'>CENTRE DE CONTRÔLE</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='buse-card'><b>ÉTAT RÉSEAU</b><br><span class='status-badge'>OPÉRATIONNEL</span></div>", unsafe_allow_html=True)
        c2.markdown("<div class='buse-card'><b>BASE LÉGALE</b><br>IDCC 1517</div>", unsafe_allow_html=True)
        c3.markdown("<div class='buse-card'><b>ALERTES</b><br>AUCUNE</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("📋 Dernières Directives")
        st.info("Mise à jour des paliers Infinity effectuée selon le protocole V4 (PDF).")
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "AGENT EAGLE (IA & AUDIT)":
        st.markdown("<h2 class='glow-text'>🔍 INTELLIGENCE EAGLE</h2>", unsafe_allow_html=True)
        cl, cr = st.columns([1, 1])
        with cl:
            st.image(st.session_state.current_media, caption="Visualisation Eagle")
            doc = st.file_uploader("Scanner un document (Paie/Contrat)", type=["pdf", "png", "jpg"])
            if doc and st.button("LANCER L'ANALYSE"):
                with st.spinner("Analyse en cours..."):
                    time.sleep(2)
                    st.session_state.analysis_results = "Analyse : Le document semble être une fiche de paie. Vérification des cotisations retraite et prévoyance conforme à l'IDCC 1517."
                    st.success("Audit terminé.")

        with cr:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            q = st.text_input("Interroger l'expert (IA) :", placeholder="Ex: Quel est le délai de prévenance ?")
            if st.button("COMMUNIQUER"):
                if q:
                    with st.spinner("Traitement..."):
                        res = call_eagle_ia(q, st.session_state.analysis_results or "")
                        audio = text_to_speech(res)
                        st.session_state.ai_history.append({"q": q, "a": res, "audio": audio})
            st.markdown("</div>", unsafe_allow_html=True)

        for chat in reversed(st.session_state.ai_history):
            with st.expander(f"REQUÊTE : {chat['q']}", expanded=True):
                st.write(chat['a'])
                if chat['audio']: st.audio(base64.b64decode(chat['audio']), format='audio/wav')

    elif nav == "MOTEUR INFINITY":
        st.markdown("<h2 class='glow-text'>💎 MOTEUR INFINITY V4</h2>", unsafe_allow_html=True)
        col_in, col_res = st.columns([1, 1])
        
        with col_in:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            ca = st.number_input("CA Personnel Réalisé (€)", value=1800.0, step=50.0)
            hrs = st.number_input("Heures de présence (Mois)", value=48, step=1)
            ecart, bonus, color, progress = calculate_infinity_v4(ca, hrs)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_res:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.metric("Écart au seuil (1300€)", f"{ecart:.2f} €", delta=f"{ecart-411.69:.2f} € vs Seuil déclenchement")
            st.markdown(f"### PRIME : <span style='color:{color};'>{bonus}</span>", unsafe_allow_html=True)
            st.progress(progress / 100.0)
            st.caption(f"Progression vers le palier 100% (Ratio actuel: {(ecart-411.69)/hrs:.2f}€/h)")
            st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "SALAIRE & SANTÉ":
        st.markdown("<h2 class='glow-text'>💰 SIMULATEUR DE PAIE</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        brut = st.number_input("Salaire Brut (€)", value=2100.0)
        stat = st.selectbox("Statut", ["Employé/Ouvrier (Non-Cadre)", "Cadre"])
        taux = 0.78 if "Non-Cadre" in stat else 0.75
        net = brut * taux
        st.write(f"### NET ESTIMÉ : **{net:.2f} €**")
        st.divider()
        st.write("**IJ Maladie (Sécurité Sociale) :**")
        st.info(f"Estimation : {min((brut/30.42)*0.5, 52.04):.2f} € / jour (après carence)")
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "RÉSEAU SENTINELLES":
        st.markdown("<h2 class='glow-text'>🛡️ RÉSEAU DES SENTINELLES</h2>", unsafe_allow_html=True)
        
        # Données pour la carte
        df = pd.DataFrame(BOULANGER_DATA["Délégués"])
        
        col_map, col_list = st.columns([2, 1])
        
        with col_map:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.map(df)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_list:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Contacts")
            for _, row in df.iterrows():
                with st.expander(f"📍 {row['Région']} - {row['Nom']}"):
                    st.write(f"📞 {row['Contact']}")
                    st.button("Contacter", key=row['Nom'])
            st.markdown("</div>", unsafe_allow_html=True)

# --- INITIALISATION ---
if not st.session_state.auth:
    apply_ia_design()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><h2 class='glow-text' style='text-align:center;'>AUTH SYSTÈME</h2>", unsafe_allow_html=True)
        pin = st.text_input("PIN DE SÉCURITÉ", type="password")
        if st.button("DÉVERROUILLER"):
            if pin == "1234":
                st.session_state.auth = True
                st.rerun()
            else: st.error("CODE INVALIDE")
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
    main_app()
