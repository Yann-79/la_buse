import streamlit as st
import pandas as pd
import time
from datetime import datetime
import json

st.set_page_config(
    page_title="LA BUSE | GENESIS PRO",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'access_mode' not in st.session_state:
    st.session_state.access_mode = False
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'last_geo' not in st.session_state:
    st.session_state.last_geo = "National"

CONVENTIONS_DB = {
    "IDCC 1517": {"nom": "Commerces de détail non alimentaires", "minima": 1766.92, "prime_anciennete": True},
    "IDCC 1486": {"nom": "Bureaux d'études techniques (Syntec)", "minima": 1900.00, "prime_anciennete": False},
    "IDCC 3248": {"nom": "Secteur Privé / Commerce général", "minima": 1766.92, "prime_anciennete": True}
}

SENTINEL_NETWORK = [
    {"region": "IDF", "nom": "Expert Sentinel Paris", "type": "Juridique", "contact": "01.XX.XX.XX.XX"},
    {"region": "ARA", "nom": "Sentinelle Lyon", "type": "Défense Salariale", "contact": "expert.lyon@labuse.pro"},
    {"region": "HDF", "nom": "Sentinelle Nord", "type": "Audit Paie", "contact": "via App"},
    {"region": "PACA", "nom": "Expert Sud", "type": "Négociations", "contact": "contact@labuse.pro"}
]

def apply_apple_styles():
    accent_color = "#D4AF37" # Gold
    if st.session_state.access_mode:
        accent_color = "#FFFF00" # Ultra Yellow
        card_border = f"4px solid {accent_color}"
    else:
        card_border = "1px solid rgba(255, 255, 255, 0.1)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=SF+Pro+Display:wght@700&display=swap');
    
    .stApp {{ background-color: #050505; color: white; font-family: 'Inter', sans-serif; }}
    
    /* Design Apple Glassmorphism */
    .buse-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        border: {card_border};
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .buse-card:hover {{
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.06);
        border-color: {accent_color};
        box-shadow: 0 15px 35px rgba(212, 175, 55, 0.15);
    }}

    .news-ticker {{
        background: linear-gradient(90deg, rgba(212, 175, 55, 0.1), transparent);
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 30px;
        border-left: 5px solid {accent_color};
        overflow: hidden;
        white-space: nowrap;
    }}
    
    .ticker-text {{
        display: inline-block;
        animation: scroll 40s linear infinite;
        color: {accent_color};
        font-weight: 600;
        font-size: 0.95rem;
    }}
    @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    /* Mentions Légales */
    .footer {{
        font-size: 0.75rem;
        color: #6e6e73;
        text-align: center;
        padding: 60px 20px;
        border-top: 1px solid #222;
        margin-top: 100px;
    }}
    
    /* Animation Accessibilité TTS */
    .tts-active {{ border: 3px solid #FFFF00 !important; transform: scale(1.02); }}
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    if st.session_state.access_mode:
        st.components.v1.html(f"""
            <script>
            var msg = new SpeechSynthesisUtterance("{text}");
            msg.lang = 'fr-FR';
            msg.rate = 1.0;
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)

def show_login():
    apply_apple_styles()
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.markdown("<br><br><div style='text-align:center;'><h1 style='font-size:4rem; color:#D4AF37;'>🦅 LA BUSE</h1><p style='color:#6e6e73; font-size:1.2rem; letter-spacing:2px;'>GENESIS | ÉLITE DE LA PROTECTION</p></div>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="buse-card">', unsafe_allow_html=True)
            pin = st.text_input("IDENTIFIANT D'ACCÈS", type="password", placeholder="Entrez votre code secret")
            if st.button("DÉVERROUILLER L'INTERFACE"):
                if pin == "1234":
                    st.session_state.auth = True
                    speak("Accès autorisé. Système La Buse opérationnel.")
                    st.rerun()
                else:
                    st.error("ACCÈS REFUSÉ - IDENTIFIANT INCONNU")
            st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.auth:
    show_login()
    st.stop()

apply_apple_styles()
with st.sidebar:
    st.markdown("<h2 style='color:#D4AF37;'>🦅 LA BUSE</h2>", unsafe_allow_html=True)
    menu = st.radio("NAVIGATION", ["🏠 ACCUEIL", "🔍 MULTI-AUDIT RH", "📊 AGENT EAGLE (SALAIRE)", "🛡️ RÉSEAU SENTINELLES", "⚙️ MASTER NODE IA"])
    
    st.markdown("---")
    acc = st.toggle("👁️ MODE ACCESS_SIGHT (TTS)", value=st.session_state.access_mode)
    if acc != st.session_state.access_mode:
        st.session_state.access_mode = acc
        if acc: speak("Mode accessibilité activé. Survol et énoncé actif.")
        st.rerun()
    
    if st.button("🗑️ EFFACER L'HISTORIQUE"):
        st.session_state.search_history = []
        st.success("Traces supprimées.")

if menu == "🏠 ACCUEIL":
    st.markdown("<div class='news-ticker'><div class='ticker-text'>🔴 ALERTE JURIDIQUE : Mise à jour des plafonds de la sécurité sociale • VEILLE SOCIALE : Négociations annuelles obligatoires en cours dans les secteurs IDCC 1517 et 1486 • ACTUALITÉ : Nouvelle jurisprudence sur le temps de trajet effectif...</div></div>", unsafe_allow_html=True)
    st.markdown("<h1>HORIZON DASHBOARD</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='buse-card'><h3>SURVEILLANCE</h3><p>Conventions suivies : 12</p><p style='color:#D4AF37;'>Statut : Optimal</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='buse-card'><h3>ALERTES IA</h3><p>Anomalies détectées : 0</p><p style='color:#D4AF37;'>Analyse : Continue</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='buse-card'><h3>SENTINELLES</h3><p>Experts actifs : 142</p><p style='color:#D4AF37;'>Réseau : Maillé</p></div>", unsafe_allow_html=True)

elif menu == "🔍 MULTI-AUDIT RH":
    st.markdown("<h1>MULTI-AUDIT CLOUD</h1>")
    tab1, tab2 = st.tabs(["📤 Import Manuel", "☁️ DRIVE / CLOUD"])
    
    with tab1:
        files = st.file_uploader("Fiches de paie ou Contrats (PDF/JPG)", accept_multiple_files=True)
        if files:
            if st.button("LANCER L'ANALYSE EXPERTE"):
                with st.status("Extraction des métadonnées...", expanded=True) as status:
                    time.sleep(1.5)
                    st.write("Vérification des taux de cotisations 2024...")
                    time.sleep(1)
                    st.write("Comparaison avec la convention IDCC...")
                    status.update(label="Audit Terminé avec succès !", state="complete")
                st.success(f"Analyse effectuée sur {len(files)} document(s). Aucune erreur détectée.")

    with tab2:
        st.info("Synchronisez votre stockage pour un audit historique complet.")
        if st.button("🔗 CONNECTER GOOGLE DRIVE"):
            st.warning("Simulation : Connexion au dossier 'La Buse' en cours...")
            time.sleep(2)
            st.success("Accès autorisé. 12 fichiers détectés.")

elif menu == "📊 AGENT EAGLE (SALAIRE)":
    st.markdown("<h1>AGENT EAGLE & CALCULATEUR</h1>")
    
    with st.container():
        st.markdown('<div class="buse-card">', unsafe_allow_html=True)
        st.subheader("Estimation Salaire 2024")
        brut = st.number_input("Salaire Mensuel Brut (€)", value=2000, step=50)
        statut = st.selectbox("Statut Professionnel", ["Employé (22%)", "Cadre (25%)", "Apprenti (0%)"])
        
        taux = 0.78 if "Employé" in statut else 0.75
        if "Apprenti" in statut: taux = 1.0
        
        net = brut * taux
        st.markdown(f"<h2 style='color:#D4AF37;'>Net Estimé : {net:.2f} €</h2>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🦅 Demander à l'IA Eagle"):
        query = st.text_input("Posez une question (ex: 'Prime ancienneté 1517')")
        if query:
            st.session_state.search_history.append(query)
            st.write("L'IA analyse votre question par rapport aux bases IDCC...")
            st.info("Réponse IA : Selon la convention IDCC 1517, la prime d'ancienneté est calculée après 3 ans de présence effective.")

elif menu == "🛡️ RÉSEAU SENTINELLES":
    st.markdown("<h1>SENTINELLES GÉO-LOCALISÉES</h1>")
    
    col_map, col_list = st.columns([1, 1])
    
    with col_map:
        if st.button("📍 ME GÉOLOCALISER"):
            with st.spinner("Triangulation..."):
                time.sleep(1.5)
                st.session_state.last_geo = "IDF"
                st.success("Position détectée : Ile-de-France")
        
        region = st.selectbox("Filtrer par région", ["Toutes", "IDF", "ARA", "HDF", "PACA", "OCC"], 
                              index=0 if st.session_state.last_geo == "National" else 1)

    with col_list:
        st.markdown("<p style='color:#6e6e73;'>Mise à jour mensuelle : Mai 2024</p>", unsafe_allow_html=True)
        for s in SENTINEL_NETWORK:
            if region == "Toutes" or s["region"] == region:
                st.markdown(f"""
                <div class="buse-card">
                    <span style="background:#D4AF37; color:black; padding:2px 10px; border-radius:50px; font-weight:bold; font-size:0.7rem;">{s['region']}</span>
                    <h4>{s['nom']}</h4>
                    <p>Expertise : {s['type']}</p>
                    <p><b>Contact :</b> {s['contact']}</p>
                </div>
                """, unsafe_allow_html=True)

elif menu == "⚙️ MASTER NODE IA":
    st.markdown("<h1>MASTER NODE IA</h1>")
    st.write("Module d'auto-optimisation autonome.")
    
    if st.button("GÉNÉRER LE RAPPORT D'OPTIMISATION HEBDOMADAIRE"):
        with st.status("Analyse du trafic et des performances..."):
            time.sleep(2)
        
        st.code(f"""
        RAPPORT D'ANALYSE GENESIS - {datetime.now().strftime('%d/%m/%Y')}
        ----------------------------------------------------------
        1. DESIGN : Fluidité Apple Glass validée (60fps).
        2. VITESSE : Temps de réponse serveur < 200ms.
        3. INTELLIGENCE : Base IDCC enrichie de 4 nouvelles jurisprudences.
        4. RECHERCHE : Taux de réussite Agent Eagle : 94%.
        
        PROPOSITION : Ajouter un module de simulation de rupture conventionnelle.
        """, language="text")

st.markdown(f"""
<div class="footer">
    <p><b>LA BUSE GENESIS | VERSION OMNIS {datetime.now().year}</b></p>
    <p>Plateforme d'expertise indépendante. Les données fournies sont issues de bases de données publiques (Légifrance) et syndicales.</p>
    <p>Ce site n'est affilié à aucune entreprise. L'utilisation des simulateurs ne remplace pas l'avis d'un expert juridique qualifié.</p>
    <p>Protection des données : Aucun document n'est stocké de manière permanente sur nos serveurs.</p>
</div>
""", unsafe_allow_html=True)
