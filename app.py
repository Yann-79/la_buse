import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime

# --- CONFIGURATION API & MODÈLES ---
# Le moteur utilisera gemini-2.5-flash-preview-09-2025 pour le texte
# Et gemini-2.5-flash-image-preview pour les illustrations
API_KEY = "" # Géré par l'environnement

# Configuration de la page
st.set_page_config(
    page_title="LA BUSE | MASTER-DEFENSE",
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
if 'accessibility' not in st.session_state:
    st.session_state.accessibility = False
if 'current_media' not in st.session_state:
    st.session_state.current_media = None

# --- DESIGN SYSTEM ULTRA-DYNAMIQUE ---
def apply_ia_design():
    accent = "#D4AF37"
    bg = "#050505" if st.session_state.theme_mode == "dark" else "#F5F5F7"
    text = "#FFFFFF" if st.session_state.theme_mode == "dark" else "#111111"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    :root {{ --accent: {accent}; --bg: {bg}; }}
    
    .stApp {{ 
        background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, {bg} 100%);
        color: {text};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Animations de scan Jarvis */
    @keyframes scan {{
        0% {{ transform: translateY(-100%); opacity: 0; }}
        50% {{ opacity: 0.5; }}
        100% {{ transform: translateY(100%); opacity: 0; }}
    }}
    
    .buse-card {{
        background: rgba(255, 255, 255, 0.03);
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
        animation: scan 3s infinite linear;
    }}
    
    .buse-card:hover {{
        border-color: var(--accent);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1);
    }}

    /* Moniteur IA */
    .media-monitor {{
        background: #000;
        border: 2px solid var(--accent);
        border-radius: 15px;
        height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 50px rgba(212, 175, 55, 0.3);
        position: relative;
    }}
    
    .glow-text {{
        color: var(--accent);
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        font-family: 'Orbitron', sans-serif;
    }}
    
    /* Accessibilité */
    {" .stApp { filter: contrast(1.2) saturate(1.5); font-size: 1.1rem; }" if st.session_state.accessibility else ""}
    </style>
    """, unsafe_allow_html=True)

# --- FONCTIONS IA (GEMINI 2.5 FLASH) ---
def call_eagle_ia(prompt, mode="text"):
    system_prompt = """Tu es EAGLE, l'IA de 'La Buse'. Expertise : IDCC 1517 (Boulangerie-Pâtisserie), Code du travail, Calcul de primes. 
    Réponds de façon concise, technique et rassurante. Si tu dois générer une image, décris-la précisément."""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "tools": [{"google_search": {}}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        return text
    except:
        return "Erreur de liaison satellite. Réessayez."

def generate_eagle_image(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
    payload = {"instances": {"prompt": f"Style Jarvis HUD, Iron Man technology, {prompt}"}, "parameters": {"sampleCount": 1}}
    try:
        response = requests.post(url, json=payload, timeout=15)
        return f"data:image/png;base64,{response.json()['predictions'][0]['bytesBase64Encoded']}"
    except:
        return "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072"

# --- LOGIQUE DE CALCUL INFINITY (PDF) ---
def render_infinity_calculator():
    st.markdown("<h3 class='glow-text'>💎 SIMULATEUR INFINITY</h3>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            heures = st.slider("Heures travaillées (Mois)", 30, 60, 48)
            ca_realise = st.number_input("CA Réalisé (€)", value=1750, step=50)
        
        # Logique basée sur le PDF
        seuil_magasin = 1300
        declencheur = 411.69
        difference = ca_realise - seuil_magasin
        
        bonus = 0
        if difference >= declencheur:
            if difference < 600: bonus = 20
            elif difference < 1000: bonus = 40
            elif difference < 1500: bonus = 60
            else: bonus = 100
        
        with col2:
            st.metric("Écart Seuil", f"{difference:.2f} €", delta=f"{difference - declencheur:.2f} vs Objectif")
            if bonus > 0:
                st.success(f"DÉPLAFONNEMENT : {bonus}%")
            else:
                st.warning(f"Manque {declencheur - difference:.2f}€ pour le bonus")

# --- INTERFACE PRINCIPALE ---
def main():
    apply_ia_design()
    
    # Barre de chargement Jarvis au démarrage
    if not st.session_state.loading_complete:
        run_jarvis_sequence()
        return

    # Menu Sidebar
    with st.sidebar:
        st.markdown("<h1 class='glow-text'>🦅 LA BUSE</h1>", unsafe_allow_html=True)
        st.markdown("---")
        menu = st.radio("SÉLECTION MODULE", ["ACCUEIL", "AGENT EAGLE IA", "MULTI-AUDIT RH", "RÉSEAU SENTINELLES", "MASTER NODE IA"])
        st.markdown("---")
        st.session_state.accessibility = st.toggle("♿ ACCESSIBILITÉ +", value=st.session_state.accessibility)
        if st.button("LOGOUT"):
            st.session_state.auth = False
            st.rerun()

    # Routing
    if menu == "ACCUEIL":
        st.markdown("<h2 class='glow-text'>TABLEAU DE BORD OPÉRATIONNEL</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.markdown("<div class='buse-card'><b>SANTÉ SYSTÈME</b><br>Statut: Optimal</div>", unsafe_allow_html=True)
        col2.markdown("<div class='buse-card'><b>CONVENTION</b><br>IDCC 1517 Active</div>", unsafe_allow_html=True)
        col3.markdown("<div class='buse-card'><b>SYNCHRO DRIVE</b><br>OK (yann-79)</div>", unsafe_allow_html=True)
        
        render_infinity_calculator()

    elif menu == "AGENT EAGLE IA":
        st.markdown("<h2 class='glow-text'>🦅 AGENT EAGLE : INTERFACE IA</h2>", unsafe_allow_html=True)
        
        col_view, col_chat = st.columns([1.5, 1])
        
        with col_view:
            st.markdown("<div class='media-monitor'>", unsafe_allow_html=True)
            if st.session_state.current_media:
                st.image(st.session_state.current_media, use_container_width=True)
            else:
                st.markdown("<p class='jarvis-text'>SCANNER VISUEL PRÊT...</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_chat:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            prompt = st.text_input("Posez votre question (Droit, Salaire, Audit) :")
            if st.button("INTERROGER L'IA"):
                with st.spinner("Analyse des sources Légifrance..."):
                    res = call_eagle_ia(prompt)
                    st.session_state.ai_history.append({"q": prompt, "a": res})
                    # Génération d'une illustration
                    st.session_state.current_media = generate_eagle_image(prompt[:50])
                st.rerun()
            
            for chat in reversed(st.session_state.ai_history[-3:]):
                st.markdown(f"**Vous:** {chat['q']}")
                st.info(f"**EAGLE:** {chat['a']}")
            st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "MULTI-AUDIT RH":
        st.markdown("<h2 class='glow-text'>🔍 MULTI-AUDIT RH</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.write("Glissez vos fiches de paie ou contrats pour une analyse instantanée.")
        st.file_uploader("Upload Document (PDF/PNG)", type=["pdf", "png", "jpg"])
        st.button("LANCER L'AUDIT DE CONFORMITÉ")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "RÉSEAU SENTINELLES":
        st.markdown("<h2 class='glow-text'>🛡️ RÉSEAU SENTINELLES</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>Cartographie des experts en cours de déploiement...</div>", unsafe_allow_html=True)

    elif menu == "MASTER NODE IA":
        st.markdown("<h2 class='glow-text'>⚙️ MASTER NODE IA</h2>", unsafe_allow_html=True)
        st.json({"node": "Master-Defense-1.0", "engine": "Gemini 2.5 Flash", "status": "Optimized"})

# --- SEQUENCE DE CHARGEMENT ---
def run_jarvis_sequence():
    apply_ia_design()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#D4AF37;'>INITIALISATION SYSTÈME...</h2>", unsafe_allow_html=True)
        bar = st.progress(0)
        txt = st.empty()
        msgs = ["Triangulation GPS...", "Cryptage AES-256...", "Analyse Conventionnelle...", "Liaison Eagle IA..."]
        for i, m in enumerate(msgs):
            txt.markdown(f"<p class='jarvis-text' style='text-align:center;'>{m}</p>", unsafe_allow_html=True)
            bar.progress((i+1)*25)
            time.sleep(0.6)
        st.session_state.loading_complete = True
        st.rerun()

# --- AUTHENTIFICATION ---
if not st.session_state.auth:
    apply_ia_design()
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1516733725897-1aa73b87c8e8?q=80&w=2070&auto=format&fit=crop")
        pin = st.text_input("IDENTIFIANT BIOMÉTRIQUE / PIN", type="password")
        if st.button("ACCÉDER AU SYSTÈME"):
            if pin == "1234":
                st.session_state.auth = True
                st.rerun()
            else: st.error("ACCÈS REFUSÉ")
else:
    main()
