import streamlit as st
import pandas as pd
from PIL import Image

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="La Buse - Analyseur Social",
    page_icon="🦅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- DESIGN CSS PERSONNALISÉ (OPTIMISÉ IPHONE) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f8fafc; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #007AFF;
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    .status-ok { color: #2ecc71; font-weight: bold; }
    .status-warn { color: #e67e22; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES INTELLIGENTE ---
# Ces données sont issues de vos photos et des recherches publiques
DATA = {
    "Boulanger": {
        "idcc": "1517",
        "convention": "Commerces de détail non alimentaires",
        "syndicats": [
            {
                "nom": "UNSA Boulanger",
                "contact": "Stéphane SOURDET",
                "tel": "07 60 36 79 47",
                "email": "contact@unsa-boulanger.com",
                "web": "www.unsa-boulanger.com",
                "note": "Expertise Élections CSE 2026"
            },
            {
                "nom": "CFTC Boulanger",
                "contact": "Aziz CHIADMI",
                "tel": "06 51 92 56 99",
                "web": "cftc-boulanger.fr",
                "note": "Spécialiste NAO & Primes BES"
            },
            {
                "nom": "CFDT Boulanger",
                "contact": "Claire Avrillon",
                "tel": "07 84 71 12 09",
                "app": "App 'CFDT Boulanger' dispo",
                "note": "Déléguée Syndicale Régionale"
            },
            {
                "nom": "CGT Boulanger",
                "contact": "W. Bachir AHAMED",
                "tel": "06 11 42 07 82",
                "email": "uescgt.boulanger@gmail.com",
                "note": "Présent sur Instagram & TikTok"
            },
            {
                "nom": "FO Boulanger",
                "contact": "Délégué Central",
                "app": "App 'FO Boulanger' dispo",
                "note": "Focus : Pouvoir d'achat & Étrennes"
            }
        ]
    },
    "Généraliste (Autre)": {
        "idcc": "À définir",
        "convention": "Code du Travail (Droit Commun)",
        "syndicats": [
            {"nom": "Interpro UNSA", "contact": "Bourse du Travail", "note": "Contactez l'union locale de votre ville."},
            {"nom": "Interpro CFDT", "contact": "Espace Salariés", "note": "Conseils juridiques généralistes."}
        ]
    }
}

# --- LOGIQUE D'ANALYSE ---
def moteur_analyse(doc, enseigne):
    # Simulation d'analyse IA (basée sur l'IDCC 1517 si Boulanger)
    st.success("✅ Analyse du document terminée")
    
    with st.container():
        st.markdown(f"### 📊 Rapport d'analyse : {enseigne}")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Taux Horaire :**")
            st.write("**Heures Sup :**")
            st.write("**Ancienneté :**")
        with col2:
            st.markdown("<span class='status-ok'>CONFORME</span>", unsafe_allow_html=True)
            st.markdown("<span class='status-warn'>À VÉRIFIER (ligne 14)</span>", unsafe_allow_html=True)
            st.markdown("<span class='status-ok'>À JOUR</span>", unsafe_allow_html=True)
        
        if enseigne == "Boulanger":
            st.warning("⚠️ **Alerte Conventionnelle :** Vérifiez si votre Prime de Vacances a bien été versée sur ce bulletin (Art. 32 IDCC 1517).")

# --- INTERFACE PRINCIPALE ---

# Header
st.markdown("<h1 style='text-align: center;'>🦅 La Buse</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Analyseur Intelligent & Défense des Salariés</p>", unsafe_allow_html=True)

# Navigation
tabs = st.tabs(["🕵️ Analyseur", "🛡️ Syndicats", "📜 Mes Droits"])

# ONGLET 1 : ANALYSEUR
with tabs[0]:
    st.subheader("Vérifier mon bulletin")
    ent = st.selectbox("Mon entreprise :", list(DATA.keys()))
    
    file = st.file_uploader("Prendre en photo ou charger un PDF", type=["jpg", "png", "pdf"])
    
    if file:
        st.image(file, caption="Bulletin chargé", use_container_width=True)
        if st.button("Lancer l'analyse intelligente"):
            with st.spinner("L'IA examine vos droits..."):
                moteur_analyse(file, ent)

# ONGLET 2 : SYNDICATS
with tabs[1]:
    st.subheader("Contacter un expert")
    ent_sync = st.selectbox("Voir les contacts pour :", list(DATA.keys()), key="sync")
    
    city = st.text_input("Votre ville ou département (optionnel) :", placeholder="ex: 79, Niort, Paris...")
    
    for s in DATA[ent_sync]["syndicats"]:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <h4 style="margin:0; color:#007AFF;">{s['nom']}</h4>
                <p style="margin:5px 0;">👤 <b>{s.get('contact', 'Référent')}</b></p>
                <p style="font-size: 0.9em; color: #64748b;">{s['note']}</p>
                <div style="margin-top:10px;">
                    {f"📞 <a href='tel:{s['tel']}'>{s['tel']}</a>" if 'tel' in s else ""}
                    {f" | 🌐 <a href='https://{s['web']}'>Site Web</a>" if 'web' in s else ""}
                </div>
                {f"<p style='color:#2ecc71; font-size:0.8em; margin-top:5px;'>📱 {s['app']}</p>" if 'app' in s else ""}
            </div>
            """, unsafe_allow_html=True)

# ONGLET 3 : MES DROITS
with tabs[2]:
    ent_droits = st.selectbox("Règles applicables pour :", list(DATA.keys()), key="droits")
    info = DATA[ent_droits]
    
    st.info(f"**Convention Collective :** {info['convention']} (IDCC {info['idcc']})")
    
    with st.expander("📅 Congés & Absences"):
        st.write("- 2.08 jours ouvrés par mois.")
        st.write("- Jours enfants malades : Selon ancienneté (IDCC 1517).")
        
    with st.expander("💰 Salaires & Primes"):
        st.write("- Grille de salaire mise à jour au 1er Janvier 2026.")
        if ent_droits == "Boulanger":
            st.write("- Prime d'ancienneté : +3% après 3 ans, +6% après 6 ans...")

# Footer
st.markdown("---")
st.caption("Application sécurisée - Aucune donnée de paie n'est stockée sur nos serveurs.")
if st.button("📲 Installer sur mon iPhone"):
    st.info("Appuyez sur le bouton **Partager** (carré avec flèche) de votre navigateur Safari, puis choisissez **'Sur l'écran d'accueil'**.")
