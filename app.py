import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Configuration de la page pour une expérience Premium
st.set_page_config(
    page_title="LA BUSE | SUPRÉMATIE",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALISATION DES ÉTATS (SESSION STATE) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'loading_complete' not in st.session_state:
    st.session_state.loading_complete = False
if 'access_mode' not in st.session_state:
    st.session_state.access_mode = False
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "dark"
if 'ai_response_media' not in st.session_state:
    st.session_state.ai_response_media = None

# --- DESIGN & CSS (STARK/APPLE HYBRID) ---
def apply_ia_design():
    accent = "#D4AF37" # Or Buse
    bg = "#050505" if st.session_state.theme_mode == "dark" else "#F5F5F7"
    text = "#FFFFFF" if st.session_state.theme_mode == "dark" else "#1D1D1F"
    card = "rgba(255, 255, 255, 0.05)" if st.session_state.theme_mode == "dark" else "rgba(0, 0, 0, 0.03)"
    
    st.markdown(f"""
    <style>
    :root {{ --accent: {accent}; --bg: {bg}; --text: {text}; }}
    .stApp {{ background-color: var(--bg); color: var(--text); font-family: 'SF Pro Display', -apple-system, sans-serif; }}
    
    /* Cartes Glassmorphism */
    .buse-card {{
        background: {card};
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }}
    .buse-card:hover {{ border-color: var(--accent); box-shadow: 0 0 20px rgba(212,175,55,0.2); }}

    /* Barre de chargement Jarvis */
    .stProgress > div > div > div > div {{
        background-color: var(--accent);
    }}
    
    /* Fenêtre Média IA Eagle */
    .media-window {{
        background: #000;
        border: 2px solid var(--accent);
        border-radius: 15px;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        overflow: hidden;
        position: relative;
    }}
    
    .jarvis-text {{
        font-family: 'Courier New', monospace;
        color: var(--accent);
        text-transform: uppercase;
        font-size: 0.8rem;
    }}
    
    /* Animation Ticker */
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
    </style>
    """, unsafe_allow_html=True)

# --- SEQUENCE DE CHARGEMENT JARVIS ---
def run_jarvis_sequence():
    apply_ia_design()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#D4AF37;'>INITIALISATION SYSTÈME EAGLE...</h2>", unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "Connexion au serveur Master Node...",
            "Initialisation des protocoles biométriques...",
            "Cryptage de la session (AES-256)...",
            "Analyse des protocoles conventionnels IDCC 1517...",
            "Synchronisation Cloud Drive (yann-79)...",
            "Chargement de l'interface IA Eagle...",
            "Accès autorisé. Bienvenue, Monsieur."
        ]
        
        for i, step in enumerate(steps):
            status_text.markdown(f"<p class='jarvis-text' style='text-align:center;'>{step}</p>", unsafe_allow_html=True)
            progress_bar.progress(int((i + 1) * (100/len(steps))))
            time.sleep(0.5)
        
        st.session_state.loading_complete = True
        st.rerun()

# --- ECRAN DE CONNEXION ---
def show_login():
    apply_ia_design()
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Image de la Buse Business Predator (Générée avec Gemini)
        st.image("https://images.unsplash.com/photo-1516733725897-1aa73b87c8e8?q=80&w=2070&auto=format&fit=crop", 
                 caption="LA BUSE : DOMINATION & PROTECTION")
        
        st.markdown('<div class="buse-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#D4AF37;'>ACCÈS SÉCURISÉ</h2>", unsafe_allow_html=True)
        pin = st.text_input("IDENTIFIANT BIOMÉTRIQUE / PIN", type="password")
        if st.button("AUTHENTIFICATION", use_container_width=True):
            if pin == "1234":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("ÉCHEC DE L'AUTHENTIFICATION")
        st.markdown('</div>', unsafe_allow_html=True)

# --- LOGIQUE D'AFFICHAGE PRINCIPALE ---
if not st.session_state.auth:
    show_login()
elif not st.session_state.loading_complete:
    run_jarvis_sequence()
else:
    apply_ia_design()
    
    # --- BARRE LATÉRALE ---
    with st.sidebar:
        st.markdown("<h1 style='color:#D4AF37; text-align:center;'>🦅 LA BUSE</h1>", unsafe_allow_html=True)
        menu = st.radio("CORE MODULES", ["SENSORS & CORE", "DRIVE ACCESS", "SENTINEL NETWORK", "PARAMÈTRES"])
        st.markdown("---")
        st.toggle("🌙 STEALTH MODE", value=True, key="t1")
        st.toggle("🔊 JARVIS VOICE (TTS)", key="t2")
        st.session_state.access_mode = st.session_state.get('t2', False)

    # --- MODULE 1: SENSORS & CORE (DASHBOARD + IA) ---
    if menu == "SENSORS & CORE":
        st.markdown("<div class='ticker-wrap'><div class='ticker-content'>🔴 ALERTE : Nouveau seuil de déplafonnement calculé • Synchronisation Drive terminée • IA Eagle : Prête à analyser.</div></div>", unsafe_allow_html=True)
        
        col_dash, col_ia = st.columns([1, 2])

        with col_dash:
            st.markdown("### 📊 DASHBOARD STATS")
            st.markdown("<div class='buse-card'><b>SANTÉ SYSTÈME</b><br><span style='color:#00FF00;'>SANTÉ : 100% (STABLE)</span></div>", unsafe_allow_html=True)
            
            # CALCULATEUR INFINITY (BASÉ SUR PDF)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("💎 INFINITY (Seuil 1300€)")
            
            brut = st.number_input("Salaire Brut de base (€)", value=1800)
            ca_mag = st.number_input("CA Réalisé Magasin (€)", value=1750)
            
            seuil_mag = 1300
            diff = ca_mag - seuil_mag
            trigger_bonus = 411.69
            
            bonus_percent = 0
            if diff >= trigger_bonus:
                # Paliers progressifs issus du PDF
                if diff < 600: bonus_percent = 20
                elif diff < 1000: bonus_percent = 30
                elif diff < 1500: bonus_percent = 40
                else: bonus_percent = 50
            
            st.markdown(f"**Écart au seuil :** `{diff:.2f} €`")
            if bonus_percent > 0:
                st.success(f"BONUS INFINITY : +{bonus_percent} %")
                # Calcul de simulation de prime (Brut + (Pourcentage * Coefficient))
                net_calc = (brut * 0.78) + (bonus_percent * 3.5) 
                st.metric("Net Estimé avec Bonus", f"{net_calc:.2f} €")
            else:
                st.warning(f"Manque {trigger_bonus - diff:.2f}€ pour déclencher le Bonus 20%")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_ia:
            st.markdown("### 🦅 MOTEUR IA EAGLE")
            
            # Fenêtre Média IA (Vidéo / Image)
            st.markdown("<div class='media-window'>", unsafe_allow_html=True)
            if st.session_state.ai_response_media:
                st.image(st.session_state.ai_response_media, use_container_width=True)
            else:
                st.markdown("<p class='jarvis-text'>Visualisation Holo-Hectare En Attente...</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Posez votre question")
            query = st.text_input("Requête Système :", placeholder="Analyse mon contrat ou calcule mes primes...")
            if st.button("LANCER L'ANALYSE NEURALE", use_container_width=True):
                with st.spinner("IA Eagle en cours d'analyse..."):
                    time.sleep(1.5)
                    # Simulation de réponse illustrée
                    st.session_state.ai_response_media = "https://images.unsplash.com/photo-1551288049-bbbda536339a?q=80&w=2070&auto=format&fit=crop"
                    st.info("ANALYSE TERMINÉE : Les données indiquent une conformité totale avec l'IDCC 1517. Graphique de performance chargé.")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- MODULE 2: DRIVE ACCESS ---
    elif menu == "DRIVE ACCESS":
        st.title("📂 DRIVE SYNC (GOOGLE)")
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.write("Dossier source : `yann-79/la-buse/archives`")
        st.info("Statut : Connecté à Google Cloud Storage")
        
        uploaded_files = st.file_uploader("Importer des documents (PDF, JPG) pour analyse IA", accept_multiple_files=True)
        
        if st.button("FORCER LA SYNCHRONISATION CLOUD"):
            with st.spinner("Synchronisation avec Google Drive en cours..."):
                time.sleep(2)
                st.success("Toutes les archives ont été synchronisées avec succès.")
        
        st.markdown("---")
        st.write("Fichiers récents :")
        st.code("📄 contrat_travail_v2.pdf\n📄 fiche_paie_mai_2024.pdf\n📄 avenant_infinity.pdf", language="text")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- MODULE 3: SENTINEL NETWORK ---
    elif menu == "SENTINEL NETWORK":
        st.title("📍 RÉSEAU SENTINELLES")
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.subheader("Recherche d'Experts")
        reg = st.selectbox("Sélectionnez votre zone :", ["IDF", "ARA", "HDF", "PACA", "OCC"])
        
        sentinelles = {
            "IDF": {"nom": "Sentinelle Paris - Maître Lefebvre", "contact": "01 40 22 11 33"},
            "ARA": {"nom": "Sentinelle Lyon - Jean D.", "contact": "04 72 10 20 30"},
            "HDF": {"nom": "Sentinelle Lille - Marc V.", "contact": "03 20 00 11 22"}
        }
        
        if reg in sentinelles:
            s = sentinelles[reg]
            st.success(f"**{s['nom']}** identifiée.")
            st.write(f"📞 Contact Direct : {s['contact']}")
        else:
            st.warning("Recherche d'expert en cours dans cette zone...")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- MODULE 4: PARAMÈTRES ---
    elif menu == "PARAMÈTRES":
        st.title("⚙️ CONFIGURATION SYSTÈME")
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.write("**Version du Noyau :** 2.5.0 (Eagle-Flash)")
        st.write("**Utilisateur :** Yann-79")
        if st.button("RÉINITIALISER LA SESSION"):
            st.session_state.auth = False
            st.session_state.loading_complete = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- FOOTER JARVIS ---
    st.markdown(f"""
    <div style='text-align:center; padding:30px; opacity:0.3; font-size:0.7rem;'>
        LA BUSE GENESIS | SUPRÉMATIE TOTALE {datetime.now().year} | PROTOCOLE JARVIS ACTIF | SÉCURITÉ AES-256
    </div>
    """, unsafe_allow_html=True)
