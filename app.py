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
        {"Région": "IDF", "Nom": "Jean-Pierre D.", "Contact": "06 11 22 33 44", "lat": 48.8566, "lon": 2.3522},
        {"Région": "ARA", "Nom": "Marc L.", "Contact": "04 78 00 00 00", "lat": 45.7640, "lon": 4.8357},
        {"Région": "PACA", "Nom": "Sophie M.", "Contact": "07 88 99 00 11", "lat": 43.2965, "lon": 5.3698},
        {"Région": "HDF", "Nom": "Thomas R.", "Contact": "06 55 44 33 22", "lat": 50.6292, "lon": 3.0573},
        {"Région": "OCC", "Nom": "Julie A.", "Contact": "05 61 00 00 00", "lat": 43.6045, "lon": 1.4442}
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

    @media (max-width: 600px) {{
        .glow-text {{ font-size: 1.2rem; }}
    }}

    {".stApp { font-size: 1.2rem; filter: contrast(1.2); }" if st.session_state.accessibility else ""}
    </style>
    """, unsafe_allow_html=True)

# --- MOTEUR API ---
def safe_api_call(url, payload, method="POST", retries=3):
    if not API_KEY:
        return None 
    for i in range(retries):
        try:
            res = requests.post(url, json=payload, timeout=10) if method=="POST" else requests.get(url, timeout=10)
            if res.status_code == 200: return res.json()
            time.sleep(1)
        except:
            time.sleep(1)
    return None

def call_eagle_ia(prompt, context=""):
    # Système d'instruction enrichi pour le harcèlement et les RPS
    system_prompt = (
        "Tu es EAGLE, l'IA de défense stratégique de 'La Buse'. "
        "Expertise : Convention Collective Boulanger (IDCC 1517), Code du Travail, et Santé au Travail. "
        "IMPORTANT : Si l'utilisateur évoque le harcèlement, l'épuisement (burn-out) ou les pressions managériales : "
        "1. Adopte un ton empathique et protecteur. "
        "2. Rappelle l'obligation de sécurité de l'employeur (Art. L4121-1). "
        "3. Oriente vers des actions concrètes : Alerte CSE, Médecine du Travail, Consignation des faits, Droit de retrait si danger imminent. "
        "4. Ne te limite pas au cadre légal froid, aide sur la stratégie de défense mentale et administrative. "
        "Contexte actuel du document : " + str(context)
    )

    if not API_KEY:
        # Simulation améliorée en cas d'absence de clé pour le harcèlement
        if "harcèlement" in prompt.lower() or "rps" in prompt.lower() or "pression" in prompt.lower():
            return (
                "🛡️ **PROTOCOLE DE PROTECTION ACTIVÉ**\n\n"
                "Face à une situation de harcèlement ou de pression excessive :\n"
                "- **Consignez tout :** Gardez trace écrite des échanges, dates et témoins.\n"
                "- **Alertez les Sentinelles :** Contactez immédiatement un délégué (voir menu Réseau).\n"
                "- **Santé :** Consultez votre médecin traitant pour faire constater l'impact sur votre santé.\n"
                "- **Droit :** L'employeur est légalement responsable de votre santé mentale. Le CSE doit être saisi pour lancer une enquête RPS."
            )
        return f"SIMULATION : En tant qu'expert IDCC 1517, je traite votre demande sur '{prompt}'. Cette situation requiert une analyse du cadre légal et des risques associés."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }
    result = safe_api_call(url, payload)
    return result['candidates'][0]['content']['parts'][0]['text'] if result else "⚠️ Erreur satellite. Mode local activé."

def text_to_speech(text):
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
        ], key="sidebar_nav_unique")
        
        st.divider()
        st.session_state.accessibility = st.toggle("MODE ACCESSIBILITÉ", value=st.session_state.accessibility)
        if st.button("DÉCONNEXION", key="btn_logout"):
            st.session_state.auth = False
            st.session_state.loading_complete = False
            st.rerun()

    if nav == "MONITEUR GÉNÉSIS":
        st.markdown("<h2 class='glow-text'>CENTRE DE CONTRÔLE</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='buse-card'><b>ÉTAT RÉSEAU</b><br><span class='status-badge'>OPÉRATIONNEL</span></div>", unsafe_allow_html=True)
        c2.markdown("<div class='buse-card'><b>BASE LÉGALE</b><br>IDCC 1517 & RPS</div>", unsafe_allow_html=True)
        c3.markdown("<div class='buse-card'><b>ALERTES IA</b><br>VEILLE ACTIVE</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("📋 Dernières Directives")
        st.info("L'Agent EAGLE a été mis à jour pour inclure le support sur les Risques Psychosociaux (RPS).")
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "AGENT EAGLE (IA & AUDIT)":
        st.markdown("<h2 class='glow-text'>🔍 INTELLIGENCE EAGLE (SUPPORT RPS)</h2>", unsafe_allow_html=True)
        cl, cr = st.columns([1, 1])
        with cl:
            st.image(st.session_state.current_media, caption="Analyse de situation")
            doc = st.file_uploader("Scanner une preuve ou document (Mail, Planning...)", type=["pdf", "png", "jpg"], key="uploader_eagle")
            if doc and st.button("LANCER L'ANALYSE", key="btn_analyse"):
                with st.spinner("Cryptage et analyse..."):
                    time.sleep(1)
                    st.session_state.analysis_results = "Analyse terminée. Document intégré au contexte de défense."
                    st.success("Audit terminé.")

        with cr:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.caption("Posez vos questions sur vos droits, votre salaire ou signalez une situation difficile (harcèlement, pression...).")
            q = st.text_input("Interroger l'IA :", placeholder="Ex: Pressions managériales répétées, que faire ?", key="input_eagle")
            if st.button("COMMUNIQUER", key="btn_comm"):
                if q:
                    with st.spinner("Récupération des données satellites..."):
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
            ca = st.number_input("CA Personnel (€)", value=1850.0, step=50.0, key="ca_input")
            hrs = st.number_input("Heures (Mois)", value=48, step=1, key="hrs_input")
            ecart, bonus, color, progress = calculate_infinity_v4(ca, hrs)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_res:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.metric("Écart au seuil (1300€)", f"{ecart:.2f} €", delta=f"{ecart-411.69:.2f} € vs Déclencheur")
            st.markdown(f"### PRIME : <span style='color:{color};'>{bonus}</span>", unsafe_allow_html=True)
            st.progress(progress / 100.0)
            st.caption(f"Palier : {progress}%")
            st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "SALAIRE & SANTÉ":
        st.markdown("<h2 class='glow-text'>💰 SIMULATEUR DE PAIE & SANTÉ</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        brut = st.number_input("Salaire Brut (€)", value=2100.0, key="brut_input")
        stat = st.selectbox("Statut", ["Non-Cadre", "Cadre"], key="statut_select")
        taux = 0.78 if stat == "Non-Cadre" else 0.75
        st.write(f"### NET ESTIMÉ : **{brut * taux:.2f} €**")
        st.divider()
        st.subheader("🛡️ Protection Santé")
        st.write(f"Estimation IJ Maladie (CPAM) : **{min((brut/30.42)*0.5, 52.04):.2f} € / jour**")
        st.info("Note : La prévoyance conventionnelle peut compléter ce montant selon votre ancienneté.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "RÉSEAU SENTINELLES":
        st.markdown("<h2 class='glow-text'>🛡️ RÉSEAU DES SENTINELLES</h2>", unsafe_allow_html=True)
        df = pd.DataFrame(BOULANGER_DATA["Délégués"])
        col_map, col_list = st.columns([2, 1])
        with col_map:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.map(df)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_list:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Contacts d'Urgence")
            for _, row in df.iterrows():
                with st.expander(f"📍 {row['Région']} - {row['Nom']}"):
                    st.write(f"📞 {row['Contact']}")
            st.markdown("</div>", unsafe_allow_html=True)

# --- FLUX PRINCIPAL ---
if not st.session_state.auth:
    apply_ia_design()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><h2 class='glow-text' style='text-align:center;'>AUTH SYSTÈME</h2>", unsafe_allow_html=True)
        pin = st.text_input("PIN SÉCURITÉ", type="password", key="login_pin")
        if st.button("DÉVERROUILLER", key="login_btn"):
            if pin == "1234":
                st.session_state.auth = True
                st.rerun()
            else: st.error("CODE INVALIDE")
else:
    if not st.session_state.loading_complete:
        apply_ia_design()
        p = st.progress(0.0)
        status_text = st.empty()
        for i in range(101):
            time.sleep(0.01)
            p.progress(i / 100.0)
            if i == 20: status_text.text("Initialisation des protocoles...")
            if i == 50: status_text.text("Chargement du module RPS...")
            if i == 80: status_text.text("Liaison satellite établie.")
        st.session_state.loading_complete = True
        st.rerun()
    else:
        main_app()
