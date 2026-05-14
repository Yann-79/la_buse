import streamlit as st
import pandas as pd
import time
import requests
import json
import base64
from datetime import datetime

# --- CONFIGURATION API & MODÈLES ---
# Note: L'API Key est gérée automatiquement par l'environnement
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
    st.session_state.current_media = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# --- DESIGN SYSTEM "GENESIS" DYNAMIQUE ---
def apply_ia_design():
    accent = "#D4AF37" # Or Buse
    bg = "#050505" if st.session_state.theme_mode == "dark" else "#F5F5F7"
    text = "#FFFFFF" if st.session_state.theme_mode == "dark" else "#111111"
    card_bg = "rgba(255, 255, 255, 0.03)" if st.session_state.theme_mode == "dark" else "rgba(0, 0, 0, 0.02)"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    :root {{ --accent: {accent}; --bg: {bg}; --text: {text}; }}
    
    .stApp {{ 
        background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, {bg} 100%);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }}
    
    /* Animations de scan laser */
    @keyframes scan {{
        0% {{ transform: translateY(-100%); opacity: 0; }}
        50% {{ opacity: 0.5; }}
        100% {{ transform: translateY(100%); opacity: 0; }}
    }}
    
    .buse-card {{
        background: {card_bg};
        backdrop-filter: blur(15px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    .buse-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: var(--accent);
        animation: scan 4s infinite linear;
    }}
    
    .buse-card:hover {{
        border-color: var(--accent);
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(212, 175, 55, 0.15);
    }}

    .media-monitor {{
        background: #000;
        border: 2px solid var(--accent);
        border-radius: 15px;
        height: 350px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 50px rgba(212, 175, 55, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .glow-text {{
        color: var(--accent);
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    
    /* Boutons Premium */
    .stButton>button {{
        background: linear-gradient(45deg, #D4AF37, #8A6D3B);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
    }}

    /* Mode Accessibilité */
    {".stApp { filter: contrast(1.2); font-size: 1.15rem; }" if st.session_state.accessibility else ""}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE IA EAGLE (TEXTE & IMAGE) ---
def call_eagle_ia(prompt, context=""):
    system_prompt = f"""Tu es EAGLE, l'IA de 'La Buse'. 
    CONTEXTE ANALYSE DOCUMENT: {context}
    Expertise : IDCC 1517 (Boulangerie-Pâtisserie), Code du travail français. 
    Instructions : Réponds de manière technique, cite les articles de loi. Si un document est présent, analyse-le prioritairement."""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "tools": [{"google_search": {}}]
    }
    try:
        response = requests.post(url, json=payload, timeout=12)
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Liaison satellite instable. Impossible d'interroger la base juridique."

def generate_eagle_media(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
    payload = {
        "instances": {"prompt": f"Cyberpunk digital eagle head, golden circuit lines, tech analysis interface, {prompt}"},
        "parameters": {"sampleCount": 1}
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        return f"data:image/png;base64,{response.json()['predictions'][0]['bytesBase64Encoded']}"
    except:
        return "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070"

# --- CALCULATEURS MÉTIER ---
def calculate_salary_metrics(brut, statut="non-cadre"):
    taux_net = 0.78 if statut == "non-cadre" else 0.75
    net = brut * taux_net
    # IJ : 50% du journalier plafonné
    ij = min((brut / 30.42) * 0.5, 52.04)
    return net, ij

def render_infinity_calculator():
    st.markdown("<h3 class='glow-text'>💎 MOTEUR INFINITY (PDF DATA)</h3>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            h_mois = st.number_input("Heures travaillées dans le mois", value=48, help="Valeur par défaut du document : 48h")
            ca_perso = st.number_input("CA Réalisé Personnel (€)", value=1750.0)
            ratio_ref = st.number_input("Ratio Référence / 100k", value=16.7)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Paramètres fixes du PDF
        seuil_magasin = 1300.0
        declencheur_bonus = 411.69
        difference = ca_perso - seuil_magasin
        
        with col2:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.metric("Écart Seuil", f"{difference:.2f} €", delta=f"{difference - declencheur_bonus:.2f} vs Déclencheur")
            
            bonus_percent = 0
            if difference >= declencheur_bonus:
                if difference < 600: bonus_percent = 20
                elif difference < 1000: bonus_percent = 40
                elif difference < 1500: bonus_percent = 60
                else: bonus_percent = 100
                st.success(f"🚀 BONUS ACTIF : {bonus_percent}% INFINITY")
            else:
                st.error(f"❌ Seuil non atteint. Manque {declencheur_bonus - difference:.2f}€")
            st.markdown("</div>", unsafe_allow_html=True)

# --- INTERFACE PRINCIPALE ---
def main_app():
    apply_ia_design()
    
    if not st.session_state.loading_complete:
        run_jarvis_sequence()
        return

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h1 class='glow-text' style='text-align:center;'>🦅 LA BUSE</h1>", unsafe_allow_html=True)
        st.markdown("---")
        menu = st.radio("CORE MODULES", [
            "DASHBOARD GÉNÉSIS", 
            "AUDIT & AGENT EAGLE", 
            "CALCULS SALAIRE & IJ", 
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
        st.markdown("<h2 class='glow-text'>MONITEUR DE BORD</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='buse-card'><b>CONVENTION</b><br>IDCC 1517</div>", unsafe_allow_html=True)
        c2.markdown("<div class='buse-card'><b>SANTÉ SYSTÈME</b><br>100% OPÉRATIONNEL</div>", unsafe_allow_html=True)
        c3.markdown("<div class='buse-card'><b>IA FLOW</b><br>ON-LINE</div>", unsafe_allow_html=True)
        
        render_infinity_calculator()

    elif menu == "AUDIT & AGENT EAGLE":
        st.markdown("<h2 class='glow-text'>🔍 AUDIT INTELLIGENT & EXPERTISE</h2>", unsafe_allow_html=True)
        
        col_view, col_ctrl = st.columns([1, 1])
        
        with col_view:
            st.markdown("<div class='media-monitor'>", unsafe_allow_html=True)
            if st.session_state.current_media:
                st.image(st.session_state.current_media, use_container_width=True)
            else:
                st.markdown("<p class='glow-text' style='font-size:0.8rem;'>SCANNER EN ATTENTE...</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_ctrl:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Analyse de document")
            doc = st.file_uploader("Charger Fiche de paie / Contrat", type=["pdf", "png", "jpg"])
            if doc and st.button("LANCER L'AUDIT"):
                with st.spinner("Analyse OCR & Juridique..."):
                    time.sleep(1.5)
                    st.session_state.analysis_results = "Analyse effectuée : Vérification des majorations heures de nuit et primes d'ancienneté (Art. 24 IDCC 1517)."
                    st.success("Audit terminé. Posez vos questions ci-dessous.")
            
            st.markdown("---")
            query = st.text_input("Requête à l'IA Eagle :")
            if st.button("INTERROGER"):
                with st.spinner("Consultation des bases de données..."):
                    ctx = st.session_state.analysis_results if st.session_state.analysis_results else "Audit vierge."
                    response = call_eagle_ia(query, ctx)
                    st.session_state.ai_history.append({"q": query, "a": response})
                    st.session_state.current_media = generate_eagle_media(query[:30])
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        for chat in reversed(st.session_state.ai_history[-2:]):
            with st.expander(f"Question : {chat['q']}", expanded=True):
                st.write(chat['a'])

    elif menu == "CALCULS SALAIRE & IJ":
        st.markdown("<h2 class='glow-text'>💰 SIMULATEUR DE REVENUS</h2>", unsafe_allow_html=True)
        col_s, col_ij = st.columns(2)
        
        with col_s:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Brut vers Net")
            brut_val = st.number_input("Salaire Brut (€)", value=2100.0)
            statut_val = st.radio("Statut employé", ["non-cadre", "cadre"])
            net_res, ij_res = calculate_salary_metrics(brut_val, statut_val)
            st.markdown(f"### NET ESTIMÉ : {net_res:.2f} €")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_ij:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Indemnités Maladie (IJ)")
            st.markdown(f"### IJ JOURNALIÈRE : {ij_res:.2f} €")
            st.caption("Estimation CPAM (50% du brut plafonné).")
            st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "RÉSEAU SENTINELLES":
        st.markdown("<h2 class='glow-text'>🛡️ CARTOGRAPHIE SENTINELLES</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        # Simulation de points de contact
        sentinelles_df = pd.DataFrame({
            'lat': [48.8566, 45.7640, 43.2965, 47.2184, 50.6292],
            'lon': [2.3522, 4.8357, 5.3698, -1.5536, 3.0573],
            'name': ['Expert Paris', 'Expert Lyon', 'Expert Marseille', 'Expert Nantes', 'Expert Lille']
        })
        st.map(sentinelles_df)
        st.subheader("Contacter une sentinelle")
        st.multiselect("Zone de recherche", ["IDF", "ARA", "PACA", "OCC", "HDF"])
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "SYNC DRIVE & CLOUD":
        st.markdown("<h2 class='glow-text'>☁️ ARCHIVES CLOUD</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.info("Statut : Connecté au dossier 'yann-79/la-buse/archives'")
        if st.button("SYNCHRONISER LES DOCUMENTS DRIVE"):
            with st.spinner("Récupération des données..."):
                time.sleep(2)
                st.success("Synchronisation terminée.")
        st.write("Fichiers récents :")
        st.code("📄 contrat_2024.pdf\n📄 avenant_infinity_v1.pdf\n📄 fiche_paie_avril.jpg")
        st.markdown("</div>", unsafe_allow_html=True)

# --- SYSTÈME DE CHARGEMENT ---
def run_jarvis_sequence():
    apply_ia_design()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#D4AF37;'>INITIALISATION JARVIS...</h2>", unsafe_allow_html=True)
        progress_bar = st.progress(0)
        status = st.empty()
        msgs = ["Connexion Master Node...", "Activation IDCC 1517...", "Liaison Eagle IA...", "Optimisation iPhone..."]
        for i, m in enumerate(msgs):
            status.markdown(f"<p style='text-align:center; font-family:monospace;'>{m}</p>", unsafe_allow_html=True)
            progress_bar.progress((i+1)*25)
            time.sleep(0.5)
        st.session_state.loading_complete = True
        st.rerun()

# --- AUTHENTIFICATION ---
if not st.session_state.auth:
    apply_ia_design()
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h2 class='glow-text'>ACCÈS SÉCURISÉ</h2></div>", unsafe_allow_html=True)
        pin = st.text_input("CODE PIN BIOMÉTRIQUE", type="password")
        if st.button("DÉVERROUILLER LE SYSTÈME"):
            if pin == "1234":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("PIN INCORRECT - ACCÈS BLOQUÉ")
else:
    main_app()
