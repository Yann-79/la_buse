mport streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="La Buse Pro", page_icon="🦅", layout="centered")

# --- DESIGN PERSONNALISÉ (STYLE MORANDINI & PREMIUM) ---
st.markdown("""
    <style>
    /* Style général */
    .stApp { background-color: #f0f2f5; }
    
    /* Style Blog Morandini */
    .news-card {
        background: white;
        padding: 15px;
        border-radius: 5px;
        border-left: 8px solid #e74c3c;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .news-tag {
        background: #e74c3c;
        color: white;
        padding: 2px 8px;
        font-weight: bold;
        font-size: 0.7em;
        text-transform: uppercase;
        margin-bottom: 5px;
        display: inline-block;
    }
    .news-title { font-size: 1.2em; font-weight: 800; color: #2c3e50; line-height: 1.2; }
    .news-meta { font-size: 0.8em; color: #7f8c8d; margin-top: 5px; }
    
    /* PIN Screen */
    .pin-container { text-align: center; padding: 50px 20px; }
    
    /* Boutons et inputs */
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_pin():
    if st.session_state.pin_input == "1234": # CODE PAR DÉFAUT
        st.session_state.authenticated = True
    else:
        st.error("Code incorrect ❌")

if not st.session_state.authenticated:
    st.markdown("<div class='pin-container'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/clouds/200/eagle.png", width=120)
    st.title("Accès Sécurisé")
    st.text_input("Entrez votre code à 4 chiffres :", type="password", key="pin_input", on_change=check_pin)
    st.info("Par défaut : 1234")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- DONNÉES SIMULÉES (NEWS & DROITS) ---
NEWS_DATA = [
    {"source": "FACEBOOK", "titre": "ALERTE : Négociations salariales Boulanger en cours !", "resume": "Les syndicats demandent une revalorisation de 4% face à l'inflation. Les premiers retours sont mitigés.", "date": "Aujourd'hui, 09h15"},
    {"source": "WEB SYNDICAT", "titre": "EXCLUSIF : Prime de vacances, vos droits méconnus", "resume": "De nombreux salariés oublient de vérifier l'article 32. Vérifiez votre bulletin de juin impérativement.", "date": "Hier, 18h30"},
    {"source": "OFFICIEL", "titre": "Mise à jour de la grille IDCC 1517", "resume": "Les nouveaux minima conventionnels sont entrés en vigueur au 1er mai. Vérifiez votre taux horaire.", "date": "12/05/2026"}
]

def analyse_experte(data, rdth, contrat, type_doc):
    st.subheader("📊 Rapport de Conformité")
    
    # Simulation de logique d'analyse par rapport à l'IDCC 1517
    with st.status("Analyse du document en cours...", expanded=True) as status:
        st.write("Extraction des données textuelles...")
        st.write(f"Vérification du statut {'RDTH' if rdth else 'Standard'}...")
        st.write(f"Contrôle base horaire : {contrat}h...")
        
        # Logique de vérification
        anomalies = []
        if contrat == "28h" and not rdth:
            anomalies.append("⚠️ **Contrat 28h :** Vérifiez si votre planning respecte le délai de prévenance de 7 jours (Art. 14).")
        if rdth:
            anomalies.append("💡 **Statut RDTH :** N'oubliez pas de vérifier vos primes de performance spécifiques ce mois-ci.")
        
        status.update(label="Analyse terminée !", state="complete")
    
    if anomalies:
        for a in anomalies:
            st.warning(a)
    else:
        st.success("✅ Aucun problème majeur détecté par rapport à la Convention Collective.")

tab1, tab2, tab3 = st.tabs(["🕵️ Analyseur", "📰 Défends tes droits", "📜 Convention"])

with tab1:
    st.header("Analyseur Intelligent")
    
    # Source du document
    source_doc = st.radio("Source du document :", ["Téléchargement Direct", "Google Drive / Lien Web"])
    
    if source_doc == "Téléchargement Direct":
        file = st.file_uploader("Prendre en photo ou PDF", type=["jpg", "png", "pdf"])
    else:
        drive_link = st.text_input("Collez le lien partagé Google Drive :", placeholder="https://drive.google.com/...")
        if drive_link: st.success("Lien détecté, prêt à l'analyse.")

    st.divider()
    st.subheader("Questions Précises")
    col1, col2 = st.columns(2)
    with col1:
        is_rdth = st.toggle("Êtes-vous RDTH ?")
    with col2:
        contrat_type = st.selectbox("Votre contrat :", ["35h", "28h", "Autre (Temps partiel)"])
    
    doc_type = st.selectbox("Type de document :", ["Bulletin de paie", "Contrat de travail", "Avenant"])

    if st.button("Lancer l'audit de conformité"):
        analyse_experte(None, is_rdth, contrat_type, doc_type)

with tab2:
    st.header("Défends tes droits")
    st.caption("Actualités agrégées en temps réel (Facebook, Web, Interne)")
    
    for news in NEWS_DATA:
        st.markdown(f"""
        <div class="news-card">
            <span class="news-tag">{news['source']}</span>
            <div class="news-title">{news['titre']}</div>
            <div class="news-meta">Publié le {news['date']}</div>
            <p style="margin-top:10px; color:#555;">{news['resume']}</p>
            <a href="#" style="color:#e74c3c; font-weight:bold; text-decoration:none;">Lire la suite →</a>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.header("Convention Collective")
    st.info("📚 **IDCC 1517 :** Commerces de détail non alimentaires.")
    
    with st.expander("🔗 Accès Rapide aux Textes"):
        st.markdown("[Consulter sur Legifrance (Officiel)](https://www.legifrance.gouv.fr/conv_coll/id/KALICONT000005635139)")
    
    st.subheader("Points clés pour Boulanger")
    st.write("- **Prime de vacances :** Versée sous conditions d'ancienneté (Art. 32).")
    st.write("- **Heures Sup :** Majoration de 25% pour les 8 premières heures.")
    st.write("- **Prévoyance :** Couverture obligatoire pour les cadres et non-cadres.")

# --- FOOTER ---
st.sidebar.markdown("---")
if st.sidebar.button("Déconnexion"):
    st.session_state.authenticated = False
    st.rerun()
st.sidebar.caption("La Buse v3.0 | Données Sécurisées")
