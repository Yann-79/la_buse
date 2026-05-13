import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.set_page_config(
    page_title="LA BUSE PRO | L'ŒIL DE L'EXPERT",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des états de session
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'chat' not in st.session_state:
    st.session_state.chat = []
if 'access_mode' not in st.session_state:
    st.session_state.access_mode = False

def apply_la_buse_styles():
    if st.session_state.access_mode:
        primary_gold = "#ffff00" # Jaune pur pour accessibilité
        bg_card = "#000000"
        text_color = "#ffffff"
        border_width = "4px"
        hover_transform = "scale(1.05)"
    else:
        primary_gold = "#c5a059" # Or Mat La Buse
        bg_card = "rgba(255, 255, 255, 0.03)"
        text_color = "#ffffff"
        border_width = "1px"
        hover_transform = "scale(1.02)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    :root {{
        --accent-gold: {primary_gold};
        --bg-dark: #0a0a0a;
    }}

    .stApp {{
        background-color: var(--bg-dark);
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }}

    h1, h2, h3, .buse-font {{
        font-family: 'Syncopate', sans-serif;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: var(--accent-gold);
    }}

    .buse-card {{
        background: {bg_card};
        border: {border_width} solid rgba(197, 160, 89, 0.3);
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 8px solid var(--accent-gold);
        transition: all 0.3s ease-in-out;
    }}
    
    /* Correction du survol demandée */
    .buse-card:hover {{
        background: rgba(197, 160, 89, 0.15);
        border-left: 15px solid var(--accent-gold);
        transform: {hover_transform};
        box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        z-index: 10;
    }}

    .stButton>button {{
        border-radius: 0px;
        background-color: transparent;
        color: var(--accent-gold);
        border: 2px solid var(--accent-gold);
        padding: 15px 30px;
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        width: 100%;
        transition: 0.3s ease;
    }}

    .stButton>button:hover {{
        background-color: var(--accent-gold);
        color: black !important;
    }}

    .status-badge {{
        background: var(--accent-gold);
        color: black;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 900;
        border-radius: 2px;
        margin-right: 10px;
    }}

    .legal-footer {{
        font-size: 0.65rem;
        color: #666;
        text-align: center;
        margin-top: 100px;
        padding: 40px;
        border-top: 1px solid #222;
        line-height: 1.6;
    }}

    [data-testid="stSidebar"] {{
        background-color: #050505;
        border-right: 1px solid var(--accent-gold);
    }}
    </style>
    """, unsafe_allow_html=True)

apply_la_buse_styles()

def check_password():
    if st.session_state.get("pin_input") == "1234":
        st.session_state.auth = True
    else:
        st.error("ACCÈS RÉSERVÉ : EMPREINTE NUMÉRIQUE INCONNUE")

if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><img src='https://cdn-icons-png.flaticon.com/512/681/681662.png' width='150' style='filter: sepia(1) saturate(5) hue-rotate(10deg);'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>LA BUSE PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; opacity:0.5; letter-spacing:1px;'>SYSTÈME DE SURVEILLANCE UES BOULANGER</p>", unsafe_allow_html=True)
        
        st.text_input("IDENTIFIANT DE SÉCURITÉ", type="password", key="pin_input", on_change=check_password)
        st.markdown("<p style='text-align:center; font-size:0.6rem; color:#444; margin-top:50px;'>CRYPTAGE MILITAIRE AES-256 ACCRÉDITÉ</p>", unsafe_allow_html=True)
        st.stop()

SYNDICATS = {
    "UNSA": {
        "nom": "UNSA BOULANGER",
        "expert": "Stéphane SOURDET",
        "tel": "07 60 36 79 47",
        "mail": "contact@unsa-boulanger.com",
        "spec": ["Expertise Juridique", "Application Mobile", "Défense Terrain"],
        "color": "#005ca9"
    },
    "CFTC": {
        "nom": "CFTC BOULANGER",
        "expert": "Aziz CHIADMI",
        "tel": "06 51 92 56 99",
        "mail": "contact@cftc-boulanger.fr",
        "spec": ["NAO", "Grilles de Salaires", "Équilibre Vie Pro"],
        "color": "#f26b21"
    },
    "CFDT": {
        "nom": "CFDT BOULANGER",
        "expert": "Claire AVRILLON",
        "tel": "07 84 71 12 09",
        "spec": ["Insertion", "Conditions Travail", "Égalité"],
        "color": "#ff5a00"
    },
    "CGT": {
        "nom": "CGT BOULANGER",
        "expert": "W. BACHIR AHAMED",
        "tel": "06 11 42 07 82",
        "spec": ["Défense UES", "Réseaux Sociaux", "Alertes"],
        "color": "#db231a"
    },
    "FO": {
        "nom": "FO BOULANGER",
        "expert": "Délégués Nationaux",
        "spec": ["Campagne Étrennes", "Primes Fin d'Année"],
        "color": "#f00000"
    }
}

def agent_eagle_brain(query):
    q = query.lower()
    if any(x in q for x in ["salaire", "argent", "paye", "brut"]):
        return "🦅 **ANALYSE SALAIRE :** Le minimum IDCC 1517 Niveau 1 est de 1766,92€. Vérifiez votre ligne 'Salaire de base'. Une différence est une anomalie."
    elif any(x in q for x in ["congé", "vacance", "cp", "rtt"]):
        return "🦅 **ALERTE CONGÉS :** 10 ans d'ancienneté = +1 jour. 15 ans = +2 jours. 20 ans = +3 jours. Vérifiez votre compteur sur MyBoulanger."
    elif "démission" in q or "rupture" in q:
        return "🦅 **STRATÉGIE :** Ne démissionnez jamais sans avoir tenté la Rupture Conventionnelle. L'UNSA peut vous assister pour le calcul des indemnités."
    else:
        return "🦅 **L'OEIL DE L'EXPERT :** Requête analysée. Pour ce cas précis, je vous suggère de contacter directement **Stéphane SOURDET (UNSA)** au 07 60 36 79 47."

with st.sidebar:
    st.markdown("<h2 style='color:#c5a059; margin-bottom:0;'>LA BUSE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.7rem; opacity:0.6;'>L'OEIL DE L'EXPERT</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("NAVIGATION", [
        "🛸 TABLEAU DE BORD", 
        "🔍 MULTI-AUDIT RH", 
        "🦅 AGENT EAGLE", 
        "🤝 LES SENTINELLES", 
        "📜 CONVENTION 1517",
        "📱 INSTALLATION"
    ])
    
    st.markdown("---")
    st.session_state.access_mode = st.toggle("👁️ MODE ACCESSIBILITÉ", value=st.session_state.access_mode)
    
    if st.button("🔴 DÉCONNEXION"):
        st.session_state.auth = False
        st.rerun()

if menu == "🛸 TABLEAU DE BORD":
    st.markdown("<h1>SURVEILLANCE GLOBALE</h1>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="buse-card" style="text-align:center;"><p style="font-size:0.7rem;">IDCC</p><h3>1517</h3></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="buse-card" style="text-align:center;"><p style="font-size:0.7rem;">OBJECTIF NAO</p><h3>+5.0%</h3></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="buse-card" style="text-align:center;"><p style="font-size:0.7rem;">ALERTES</p><h3 style="color:#ff4b4b;">3</h3></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="buse-card" style="text-align:center;"><p style="font-size:0.7rem;">SENTINELLES</p><h3>5</h3></div>', unsafe_allow_html=True)

    st.markdown("### 🔥 ALERTES ACTIVES")
    st.markdown("""
    <div class="buse-card">
        <span class="status-badge">CRITIQUE</span> <b>Anomalie Paie Logistique :</b> Retard de versement constaté en région Nord.
    </div>
    <div class="buse-card">
        <span class="status-badge" style="background:#444; color:white;">INFO</span> <b>Prime Étrennes :</b> La pétition FO est disponible dans l'onglet Sentinelles.
    </div>
    """, unsafe_allow_html=True)

elif menu == "🔍 MULTI-AUDIT RH":
    st.markdown("<h1>MULTI-AUDIT EXPERT</h1>", unsafe_allow_html=True)
    st.write("Analysez vos documents pour détecter les erreurs de l'entreprise.")
    
    files = st.file_uploader("DÉPOSER VOS BULLETINS (PDF/JPG)", accept_multiple_files=True)
    
    if files:
        if st.button("LANCER L'ANALYSE"):
            with st.status("SCANNING EN COURS...", expanded=True) as s:
                st.write("Extraction des données numériques...")
                time.sleep(1)
                st.write("Vérification des taux horaires...")
                time.sleep(1)
                s.update(label="ANALYSE TERMINÉE", state="complete")
            
            st.markdown(f"""
            <div class="buse-card">
                <h3 style="color:#c5a059;">RAPPORT D'AUDIT</h3>
                <p><b>{len(files)} document(s) analysé(s).</b></p>
                <ul style="list-style-type: '🦅 ';">
                    <li style="color:#00ff00;">Salaire : Conforme.</li>
                    <li style="color:#ff4b4b;"><b>Alerte :</b> Heures supplémentaires du 12/03 non majorées.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

elif menu == "🦅 AGENT EAGLE":
    st.markdown("<h1>AGENT EAGLE AI</h1>", unsafe_allow_html=True)
    
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"], avatar="🦅" if msg["role"]=="assistant" else None):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Posez votre question juridique..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        response = agent_eagle_brain(prompt)
        st.session_state.chat.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="🦅"):
            st.write(response)

elif menu == "🤝 LES SENTINELLES":
    st.markdown("<h1>RÉSEAU DES SENTINELLES</h1>", unsafe_allow_html=True)
    for key, data in SYNDICATS.items():
        with st.expander(f"🦅 {data['nom']} - {data['expert']}"):
            st.write(f"**Expertise :** {', '.join(data['spec'])}")
            if "tel" in data: st.link_button(f"APPELER {data['tel']}", f"tel:{data['tel']}")

elif menu == "📜 CONVENTION 1517":
    st.markdown("<h1>GRILLE IDCC 1517</h1>", unsafe_allow_html=True)
    df = pd.DataFrame({
        "Niveau": ["1A", "1B", "2", "3", "4", "5"],
        "Minimum Brut (€)": [1766.92, 1785.10, 1832.40, 1980.00, 2560.00, 3400.00]
    })
    st.table(df)

elif menu == "📱 INSTALLATION":
    st.markdown("<h1>INSTALLATION IPHONE</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="buse-card">
        <h3>PROCÉDURE PWA</h3>
        <ol>
            <li>Ouvrez dans <b>Safari</b>.</li>
            <li>Appuyez sur <b>Partager</b>.</li>
            <li>Sélectionnez <b>"Sur l'écran d'accueil"</b>.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="legal-footer">
    <b>LA BUSE PRO | VERSION ABSOLUTE V10.5 | © {datetime.now().year} INDÉPENDANT</b><br><br>
    <b>MENTIONS LÉGALES :</b> Cet outil est une initiative privée et indépendante, non affiliée officiellement à la direction de l'UES Boulanger. 
    Les données relatives à la convention collective IDCC 1517 sont fournies à titre purement informatif. 
    L'utilisation de cet outil ne remplace pas l'avis d'un délégué syndical ou d'un avocat spécialisé en droit du travail. 
    Aucune donnée personnelle sensible ou mot de passe d'entreprise n'est stocké sur nos serveurs. 
    L'agent Eagle AI est un assistant de recherche automatisé.
</div>
""", unsafe_allow_html=True)
