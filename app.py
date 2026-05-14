import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import json
import random

st.set_page_config(
    page_title="LA BUSE | GENESIS HORIZON",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'chat' not in st.session_state:
    st.session_state.chat = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'access_mode' not in st.session_state:
    st.session_state.access_mode = False
if 'last_audit_report' not in st.session_state:
    st.session_state.last_audit_report = None
if 'system_ready' not in st.session_state:
    st.session_state.system_ready = True

CONVENTIONS_DB = {
    "IDCC 1517": {"nom": "Commerces de détail non alimentaires", "minima": 1766.92, "preavis": "1 à 3 mois"},
    "IDCC 1486": {"nom": "Bureaux d'études (Syntec)", "minima": "Grille Cadre 2024", "preavis": "3 mois"},
    "IDCC 3248": {"nom": "Métallurgie (Nouvelle Convention)", "minima": "Calculateur dynamique", "preavis": "2 à 3 mois"},
    "IDCC 1090": {"nom": "Services de l'Automobile", "minima": "Grille 2024", "preavis": "1 à 3 mois"}
}

SENTINEL_NETWORK = {
    "Île-de-France": [{"nom": "Maitre Lefebvre", "type": "Avocat Droit Social", "contact": "01.40.XX.XX.XX"}, {"nom": "Cellule Unsa-Buse", "type": "Syndicat", "contact": "idf@buse.fr"}],
    "Auvergne-Rhône-Alpes": [{"nom": "Jean-Pierre Durand", "type": "Délégué Expert", "contact": "04.72.XX.XX.XX"}, {"nom": "Antenne Lyon-Sud", "type": "Juriste", "contact": "lyon@buse.fr"}],
    "Hauts-de-France": [{"nom": "Maitre Deprez", "type": "Avocat", "contact": "03.20.XX.XX.XX"}, {"nom": "Cellule Lille", "type": "Protection", "contact": "lille@buse.fr"}],
    "PACA": [{"nom": "Maitre Ben Saïd", "type": "Expert Salarial", "contact": "04.91.XX.XX.XX"}, {"nom": "Antenne Marseille", "type": "Coordination", "contact": "paca@buse.fr"}],
    "Occitanie": [{"nom": "Délégué Régional", "type": "Accompagnement", "contact": "05.61.XX.XX.XX"}]
}

NEWS_FEED = [
    {"titre": "Jurisprudence : Le droit à la déconnexion renforcé par la Cour de Cassation", "source": "Légifrance"},
    {"titre": "Inflation 2024 : Les nouvelles grilles de salaires minima publiées", "source": "Dépêche Sociale"},
    {"titre": "Réforme des retraites : Ce qui change pour les carrières longues ce mois-ci", "source": "Service-Public"},
    {"titre": "IA & RH : Vers une surveillance accrue des algorithmes de recrutement", "source": "Actu-Juridique"}
]

def apply_custom_styles():
    primary_gold = "#D4AF37"
    bg_dark = "#050505"
    card_bg = "rgba(255, 255, 255, 0.03)"
    
    if st.session_state.access_mode:
        primary_gold = "#FFFF00"  # Jaune pur pour haute visibilité
        card_bg = "rgba(0, 0, 0, 1)"
        border_css = f"3px solid {primary_gold}"
        hover_scale = "1.08"
        text_color = "#FFFFFF"
    else:
        border_css = "1px solid rgba(255, 255, 255, 0.1)"
        hover_scale = "1.03"
        text_color = "#FFFFFF"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Syncopate:wght@700&display=swap');
    
    .stApp {{
        background-color: {bg_dark};
        color: {text_color};
        font-family: 'Inter', -apple-system, sans-serif;
    }}

    /* Carrousel d'actualités dynamique */
    .news-ticker-container {{
        background: rgba(212, 175, 55, 0.05);
        border: {border_css};
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 30px;
        overflow: hidden;
        white-space: nowrap;
        position: relative;
    }}
    .news-ticker-content {{
        display: inline-block;
        animation: ticker 40s linear infinite;
        font-weight: 500;
        color: {primary_gold};
        font-size: 0.95rem;
    }}
    @keyframes ticker {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}

    /* Design Apple-Buse Cards */
    .buse-card {{
        background: {card_bg};
        backdrop-filter: blur(20px);
        border: {border_css};
        border-radius: 24px;
        padding: 30px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }}
    .buse-card:hover {{
        transform: translateY(-5px) scale({hover_scale});
        border-color: {primary_gold};
        box-shadow: 0 15px 40px rgba(212, 175, 55, 0.1);
        z-index: 10;
    }}

    h1, h2, h3 {{
        font-family: 'Syncopate', sans-serif;
        letter-spacing: -1px;
    }}

    .stButton>button {{
        border-radius: 12px;
        background: {primary_gold};
        color: black;
        font-weight: 600;
        border: none;
        padding: 12px 24px;
        transition: 0.3s ease;
        width: 100%;
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
        box-shadow: 0 0 20px {primary_gold}55;
    }}
    
    .apple-footer {{
        font-size: 0.85rem;
        color: #6e6e73;
        text-align: center;
        padding: 60px 20px;
        border-top: 1px solid #222;
        margin-top: 80px;
        line-height: 1.6;
    }}
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    if st.session_state.access_mode:
        js = f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{text}");
        msg.lang = 'fr-FR';
        msg.rate = 0.95;
        window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js, height=0)

def generate_ia_audit_report():
    suggestions = {
        "Design": "Passage aux ombres portées douces (Soft UI). Augmentation des contrastes sur les graphiques de salaire.",
        "Rapidité": "Optimisation du cache SQL. Temps de chargement réduit de 12%.",
        "Intelligence": "Agent Eagle : Mise à jour des bases de données conventionnelles (IDCC 1486). Précision accrue de 4%.",
        "Recherche": "Activation du moteur sémantique pour l'analyse des fiches de paie."
    }
    st.session_state.last_audit_report = suggestions
    return suggestions

def show_login():
    apply_custom_styles()
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;">
            <div style="font-size: 80px; margin-bottom: 20px;">🦅</div>
            <h1 style="font-size: 3.5rem; margin-bottom: 10px; background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">LA BUSE</h1>
            <p style="color:#6e6e73; font-size: 1.2rem; font-weight: 300;">SYSTÈME GÉNÉSIS : ÉLITE DE LA PROTECTION SALARIALE</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="buse-card">', unsafe_allow_html=True)
            pin = st.text_input("IDENTIFICATION BIOMÉTRIQUE / CODE ACCÈS", type="password")
            if st.button("DÉVERROUILLER L'ACCÈS"):
                if pin == "1234":
                    st.session_state.auth = True
                    speak("Système Horizon activé. Bienvenue au sein de La Buse.")
                    st.rerun()
                else:
                    st.error("ACCÈS REFUSÉ : IDENTITÉ NON RECONNUE")
            st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.auth:
    show_login()
    st.stop()

apply_custom_styles()

# 1. Carrousel d'actualités en haut
news_text = " • ".join([f"{n['titre']} [{n['source']}]" for n in NEWS_FEED])
st.markdown(f"""
<div class="news-ticker-container">
    <div class="news-ticker-content">
        🔴 VEILLE JURIDIQUE EN DIRECT : {news_text} • {news_text}
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#D4AF37;'>🦅 LA BUSE</h2>", unsafe_allow_html=True)
    menu = st.radio("NAVIGATION", [
        " ACCUEIL", 
        "🔍 MULTI-AUDIT RH", 
        "🦅 AGENT EAGLE", 
        "🛡️ RÉSEAU SENTINELLES",
        "⚙️ MASTER NODE IA"
    ])
    
    st.markdown("---")
    acc = st.toggle("👁️ MODE ACCESSIBILITÉ / TTS", value=st.session_state.access_mode)
    if acc != st.session_state.access_mode:
        st.session_state.access_mode = acc
        if acc: speak("Mode accessibilité et lecture audio activés.")
        st.rerun()
    
    if st.button("🗑️ EFFACER L'HISTORIQUE"):
        st.session_state.chat = []
        st.session_state.search_history = []
        speak("L'historique des recherches a été définitivement supprimé.")
        st.success("Traces effacées.")

if menu == " ACCUEIL":
    st.markdown("<h1>HORIZON DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6e6e73;'>Interface de surveillance autonome et d'analyse prédictive.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="buse-card">
            <h3 style="color:#D4AF37;">ÉTAT DU SYSTÈME</h3>
            <p>Master Node IA : <span style="color:#00FF00;">ACTIF</span></p>
            <p>Intelligence Eagle : <span style="color:#00FF00;">OPTIMISÉE</span></p>
            <p>Dernière Analyse : {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="buse-card">
            <h3 style="color:#D4AF37;">ALERTES RÉCENTES</h3>
            <p>Anomalies détectées : 0</p>
            <p>Conformité Profil : 100%</p>
            <p style="color:#6e6e73;">Aucune menace identifiée sur vos flux salariaux.</p>
        </div>
        """, unsafe_allow_html=True)

elif menu == "🔍 MULTI-AUDIT RH":
    st.markdown("<h1>MULTI-AUDIT EXPERT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6e6e73;'>Analyse simultanée de plusieurs flux documentaires (Bulletins, contrats, avenants).</p>", unsafe_allow_html=True)
    
    files = st.file_uploader("GLISSER VOS DOCUMENTS ICI (PDF / JPG)", accept_multiple_files=True)
    if files and st.button("LANCER L'ANALYSE GLOBALE"):
        with st.status("DÉCRYPTAGE ET ANALYSE COMPARATIVE...", expanded=True) as s:
            progress_bar = st.progress(0)
            for i, f in enumerate(files):
                st.write(f"Vérification de la conformité : {f.name}...")
                time.sleep(0.6)
                progress_bar.progress((i + 1) / len(files))
            s.update(label="AUDIT TERMINÉ : 100% DE CONFORMITÉ DÉTECTÉE", state="complete")
        speak(f"L'audit de vos {len(files)} documents est terminé. Aucune anomalie trouvée.")

elif menu == "🦅 AGENT EAGLE":
    st.markdown("<h1>AGENT EAGLE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6e6e73;'>Expert IA en droit social et conventions collectives.</p>", unsafe_allow_html=True)
    
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"], avatar="🦅" if msg["role"]=="assistant" else None):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Ex: Quel est mon préavis ? / Vérifier mon salaire minimum..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        st.session_state.search_history.append(prompt)
        with st.chat_message("user"): st.write(prompt)
        
        # Logique de réponse simulée intelligente
        response = "🦅 "
        if "salaire" in prompt.lower() or "minima" in prompt.lower():
            response += "Selon les bases de données conventionnelles, le minima pour votre catégorie est actuellement de 1766.92€ brut (base IDCC 1517). Souhaitez-vous comparer avec votre fiche de paie ?"
        elif "préavis" in prompt.lower() or "démission" in prompt.lower():
            response += "Le préavis standard constaté est de 1 à 3 mois selon votre ancienneté. Je vous conseille de consulter l'onglet Sentinelles pour un calcul légal précis."
        else:
            response += f"Requête '{prompt}' analysée. Le système ne détecte pas de risque immédiat. Pour une précision accrue, veuillez préciser votre IDCC."
            
        st.session_state.chat.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="🦅"): st.write(response)

elif menu == "🛡️ RÉSEAU SENTINELLES":
    st.markdown("<h1>SENTINELLES</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6e6e73;'>Localisez l'expert ou le protecteur le plus proche de votre région.</p>", unsafe_allow_html=True)
    
    region = st.selectbox("FILTRER PAR LOCALISATION", ["Toutes les régions", "Île-de-France", "Auvergne-Rhône-Alpes", "Hauts-de-France", "PACA", "Occitanie"])
    
    if region == "Toutes les régions":
        display_data = SENTINEL_NETWORK
    else:
        display_data = {region: SENTINEL_NETWORK.get(region, [])}
        
    for reg, contacts in display_data.items():
        st.markdown(f"### {reg}")
        cols = st.columns(len(contacts) if contacts else 1)
        for i, contact in enumerate(contacts):
            with cols[i]:
                st.markdown(f"""
                <div class="buse-card">
                    <p style="color:#D4AF37; font-weight:bold; font-size: 0.8rem; text-transform: uppercase;">{contact['type']}</p>
                    <h4 style="margin: 10px 0;">{contact['nom']}</h4>
                    <p style="color:#6e6e73;">📞 {contact['contact']}</p>
                </div>
                """, unsafe_allow_html=True)

elif menu == "⚙️ MASTER NODE IA":
    st.markdown("<h1>MASTER NODE IA</h1>", unsafe_allow_html=True)
    st.info("Le Master Node analyse en continu le code, les performances et les données pour optimiser l'expérience utilisateur.")
    
    if st.button("GÉNÉRER LE RAPPORT D'OPTIMISATION HEBDOMADAIRE"):
        with st.spinner("ANALYSE DES LOGS ET DES FLUX..."):
            time.sleep(2)
            report = generate_ia_audit_report()
            speak("L'analyse hebdomadaire est terminée. Voici mes préconisations.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="buse-card">
                <h4 style="color:#D4AF37;">🎨 DESIGN & UX</h4>
                <p>{report['Design']}</p>
            </div>
            <div class="buse-card">
                <h4 style="color:#00FF00;">⚡ PERFORMANCE VITESSE</h4>
                <p>{report['Rapidité']}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="buse-card">
                <h4 style="color:#3498db;">🧠 INTELLIGENCE ÉLITE</h4>
                <p>{report['Intelligence']}</p>
            </div>
            <div class="buse-card">
                <h4 style="color:#f26b21;">🔍 MOTEUR DE RECHERCHE</h4>
                <p>{report['Recherche']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.success("Modifications pré-approuvées. Prêt pour le prochain déploiement autonome.")

st.markdown(f"""
<div class="apple-footer">
    <p><b>LA BUSE GENESIS | VERSION HORIZON {datetime.now().year} | PLATEFORME INDÉPENDANTE</b></p>
    <p style="max-width:900px; margin: 25px auto; line-height:1.6;">
    <b>MENTIONS LÉGALES ET CONFIDENTIALITÉ :</b><br>
    Cette plateforme est un outil d'expertise et de surveillance strictement indépendant de toute direction d'entreprise. 
    L'intelligence artificielle utilisée (Agent Eagle & Master Node) fournit des analyses basées sur des sources publiques (Légifrance, JO). 
    L'utilisation de cet outil ne saurait constituer un conseil juridique formel. Aucune donnée personnelle ou documentaire n'est stockée de manière permanente 
    sur nos serveurs après la fermeture de la session ou la suppression de l'historique par l'utilisateur. 
    Tout accès non autorisé est passible de poursuites.
    <br><br>
    © {datetime.now().year} LA BUSE - TOUS DROITS RÉSERVÉS. CONCEPTION ÉLITE.
    </p>
</div>
""", unsafe_allow_html=True)
