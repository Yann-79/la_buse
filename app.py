import streamlit as st
import pandas as pd
import time
import requests
import json
import base64
from datetime import datetime

# --- CONFIGURATION & CONSTANTES ---
API_KEY = "" 
APP_ID = "la-buse-v4"

st.set_page_config(
    page_title="LA BUSE | SYSTÈME DE DÉFENSE",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALISATION DES ÉTATS ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'loading_complete' not in st.session_state:
    st.session_state.loading_complete = False
if 'ai_history' not in st.session_state:
    st.session_state.ai_history = []
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "dark"
if 'current_media' not in st.session_state:
    st.session_state.current_media = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070"

# --- DESIGN SYSTEM "OBSIDIAN GOLD" ---
def apply_ia_design():
    accent = "#D4AF37" 
    bg = "#080808"
    card_bg = "#111111"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {{ 
        background: {bg};
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }}
    
    .buse-card {{
        background: {card_bg};
        border-left: 3px solid {accent};
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    
    .glow-text {{
        color: {accent};
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
    }}

    .status-box {{
        background: #181818;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #333;
        margin-bottom: 10px;
    }}

    .health-stable {{ color: #00FF00; font-weight: bold; }}
    
    .stButton>button {{
        background: #D4AF37;
        color: black;
        border-radius: 4px;
        font-weight: 700;
        text-transform: uppercase;
        border: none;
    }}

    /* Fix pour les sliders et inputs en mode dark */
    .stNumberInput input {{ background-color: #222 !important; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- MOTEUR API (EAGLE ENGINE) ---
def safe_api_call(url, payload, method="POST", retries=5):
    for i in range(retries):
        try:
            res = requests.post(url, json=payload, timeout=10) if method=="POST" else requests.get(url, timeout=10)
            if res.status_code == 200: return res.json()
            time.sleep(1 * (i + 1))
        except:
            time.sleep(1 * (i + 1))
    return None

def call_eagle_ia(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": "Tu es EAGLE. Expert Droit du Travail (IDCC 1517). Ton ton est cyber-industriel, précis et protecteur."}]},
        "tools": [{"google_search": {}}]
    }
    result = safe_api_call(url, payload)
    if result:
        return result['candidates'][0]['content']['parts'][0]['text']
    return "⚠️ Liaison satellite instable. Impossible d'interroger la base juridique."

# --- LOGIQUE MÉTIER (MISE À JOUR SELON VOS DOCUMENTS) ---
def calculate_infinity_v4(ca_perso, heures_mois=48):
    # Selon votre PDF : 48h -> Seuil 1300€ -> Déclencheur 411.69€
    seuil_base = 1300.0
    declencheur = 411.69
    
    ecart = ca_perso - seuil_base
    
    # Calcul des paliers basé sur le ratio horaire extrait du PDF
    # 7€/h -> 20%, 10€/h -> 40%, 13€/h -> 60%, 16€/h -> 100%
    if ecart < declencheur:
        return ecart, "0%", "#FF4B4B"
    
    ratio_reel = (ecart - declencheur) / heures_mois
    
    if ratio_reel >= 16: bonus, color = "100%", "#00FF00"
    elif ratio_reel >= 13: bonus, color = "60%", "#ADFF2F"
    elif ratio_reel >= 10: bonus, color = "40%", "#D4AF37"
    elif ratio_reel >= 7: bonus, color = "20%", "#D4AF37"
    else: bonus, color = "DÉPLAFONNÉ (0%+)", "#D4AF37"
    
    return ecart, bonus, color

# --- COMPOSANTS UI ---
def sidebar_navigation():
    with st.sidebar:
        st.markdown("<h1 class='glow-text'>🦅 LA BUSE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.8em; opacity:0.6;'>SÉCURITÉ SYSTÈME : ACTIVE</p>", unsafe_allow_html=True)
        
        nav = st.radio("NAVIGATION", [
            "TABLEAU DE BORD",
            "MOTEUR IA EAGLE",
            "CALCUL INFINITY",
            "SENTINELLES (MAP)"
        ])
        
        st.divider()
        if st.button("DÉCONNEXION"):
            st.session_state.auth = False
            st.rerun()
    return nav

def dashboard_view():
    st.markdown("<h2 class='glow-text'>DASHBOARD STATS</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("""
        <div class='buse-card'>
            <p>SANTÉ SYSTÈME</p>
            <p class='health-stable'>SANTÉ : 100% (STABLE)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("Raccourcis")
        st.button("Vérifier IDCC 1517")
        st.button("Export PDF")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("Activité Réseau")
        chart_data = pd.DataFrame({'Requêtes': [10, 25, 15, 40, 35, 50]})
        st.area_chart(chart_data, color="#D4AF37")
        st.markdown("</div>", unsafe_allow_html=True)

def eagle_view():
    st.markdown("<h2 class='glow-text'>MOTEUR IA EAGLE</h2>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.markdown(f"<div style='border:1px solid #D4AF37; border-radius:10px; overflow:hidden;'><img src='{st.session_state.current_media}' style='width:100%;'></div>", unsafe_allow_html=True)
    
    with col_r:
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        query = st.text_input("Posez votre question (Droit, Salaire, Audit) :")
        if st.button("INTERROGER L'IA"):
            if query:
                with st.spinner("Liaison en cours..."):
                    response = call_eagle_ia(query)
                    st.session_state.ai_history.append({"q": query, "a": response})
        st.markdown("</div>", unsafe_allow_html=True)

    for item in reversed(st.session_state.ai_history):
        with st.expander(f"REQUÊTE : {item['q']}", expanded=True):
            st.write(item['a'])

def infinity_view():
    st.markdown("<h2 class='glow-text'>💎 INFINITY (Seuil 1300€)</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        ca = st.number_input("CA Réalisé Magasin (€)", value=1750, step=10)
        heures = st.number_input("Heures travaillées (Mois)", value=48, step=1)
    
    ecart, bonus, color = calculate_infinity_v4(ca, heures)
    
    with c2:
        st.metric("Écart au seuil", f"{ecart:.2f} €", delta=f"{ecart-411.69:.2f} € vs Déclencheur")
        st.markdown(f"### BONUS : <span style='color:{color};'>{bonus}</span>", unsafe_allow_html=True)
    
    if bonus != "0%":
        st.success(f"Palier Infinity atteint ! Bonus estimé : {bonus}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- SÉQUENCE D'INITIALISATION ---
def run_initialization():
    apply_ia_design()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><h2 style='text-align:center;' class='glow-text'>INITIALISATION...</h2>", unsafe_allow_html=True)
        # Fix du bug st.progress (float 0.0 à 1.0)
        p_bar = st.progress(0.0)
        for i in range(101):
            time.sleep(0.01)
            p_bar.progress(i / 100.0)
        st.session_state.loading_complete = True
        st.rerun()

# --- POINT D'ENTRÉE ---
def main():
    apply_ia_design()
    
    if not st.session_state.auth:
        _, col, _ = st.columns([1, 1, 1])
        with col:
            st.markdown("<br><br><h2 class='glow-text' style='text-align:center;'>ACCÈS SYSTÈME</h2>", unsafe_allow_html=True)
            pin = st.text_input("CODE PIN", type="password")
            if st.button("ENTRER"):
                if pin == "1234":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("ACCÈS REFUSÉ")
        return

    if not st.session_state.loading_complete:
        run_initialization()
        return

    menu = sidebar_navigation()
    
    if menu == "TABLEAU DE BORD": dashboard_view()
    elif menu == "MOTEUR IA EAGLE": eagle_view()
    elif menu == "CALCUL INFINITY": infinity_view()
    elif menu == "SENTINELLES (MAP)":
        st.markdown("<h2 class='glow-text'>CARTE DES SENTINELLES</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.map(pd.DataFrame({'lat': [48.85, 45.76, 43.60], 'lon': [2.35, 4.83, 1.44]}))
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
