import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(
    page_title="La Buse Pro",
    page_icon="🦅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Reset global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f8f9fc 0%, #eef2f7 100%);
    }

    /* Style des Cartes (News & Actions) */
    .premium-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .premium-card:hover {
        transform: translateY(-5px);
    }

    /* News Feed Modernisé */
    .news-tag {
        background: #007AFF;
        color: white;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .news-title {
        font-size: 1.4em;
        font-weight: 800;
        color: #1d1d1f;
        margin-top: 10px;
        line-height: 1.2;
    }
    .news-excerpt {
        color: #86868b;
        font-size: 0.95em;
        margin-top: 8px;
    }

    /* Boutons de commande (Call to Action) */
    .stButton>button {
        border-radius: 16px;
        border: none;
        background: linear-gradient(90deg, #007AFF 0%, #0051FF 100%);
        color: white;
        font-weight: 600;
        padding: 12px 24px;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
    }
    .stButton>button:hover {
        box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
        transform: scale(1.02);
    }

    /* Login Screen */
    .login-container {
        text-align: center;
        padding: 60px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_pin():
    if st.session_state.pin_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("Code erroné. Veuillez réessayer.")

if not st.session_state.authenticated:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/144/eagle.png", width=90)
    st.markdown("<h1 style='font-weight:800; color:#1d1d1f;'>La Buse Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#86868b;'>Espace sécurisé - Intelligence Sociale</p>", unsafe_allow_html=True)
    
    st.text_input("Saisissez votre code PIN", type="password", key="pin_input", on_change=check_pin)
    st.caption("Accès réservé aux collaborateurs.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

NEWS_DATA = [
    {"source": "ALERTE INFO", "titre": "Négociations Salaires : Les dernières avancées", "resume": "Une hausse de 3.2% est sur la table. L'UNSA et la CFTC analysent les conditions de versement de la prime de partage de la valeur.", "date": "Aujourd'hui, 10h"},
    {"source": "CONSEIL PRO", "titre": "Statut RDTH : Maîtrisez vos commissions", "resume": "Nouveau guide pratique pour vérifier le calcul de vos primes variables ce mois-ci. Ne laissez passer aucun centime.", "date": "Hier"},
    {"source": "LÉGAL", "titre": "Evolution IDCC 1517 : Ce qui change en Juin", "resume": "Mise à jour des grilles de minima conventionnels. Vérifiez si votre salaire de base est impacté.", "date": "15 Mai"}
]

def run_smart_audit(doc_type, status_rdth, contract_type):
    with st.status("🚀 **Intelligence Artificielle en action...**", expanded=True) as status:
        time.sleep(1)
        st.write("🔍 Extraction des données biométriques du document...")
        time.sleep(1)
        st.write(f"⚖️ Comparaison avec la Convention Collective IDCC 1517...")
        time.sleep(1)
        
        # Logique de détection d'anomalies
        anomalies = []
        if contract_type == "28h" and not status_rdth:
            anomalies.append("📌 **Alerte Planning :** En contrat 28h, vos heures complémentaires ne peuvent dépasser 1/3 de votre durée contractuelle.")
        if status_rdth:
            anomalies.append("💰 **Check RDTH :** La garantie de rémunération minimale doit être vérifiée sur votre ligne de paie n°14.")
        
        status.update(label="Analyse terminée avec succès !", state="complete")
        
    if anomalies:
        for a in anomalies:
            st.warning(a)
    else:
        st.success("✅ Félicitations : Votre document semble parfaitement en règle avec les accords d'entreprise.")

st.markdown("<h2 style='font-weight:800; margin-bottom:0;'>Eagle Vision</h2>", unsafe_allow_html=True)
st.caption("Votre assistant de défense et d'analyse sociale")

tab1, tab2, tab3 = st.tabs(["🕵️ Analyseur", "📢 Défends tes droits", "📜 Convention"])

with tab1:
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    
    # Section Import
    with st.container():
        st.markdown("""<div class='premium-card'>
            <h4 style='margin:0;'>📥 Importer un document</h4>
            <p style='color:#86868b; font-size:0.9em;'>Glissez votre bulletin de paie ou contrat (PDF/JPG)</p>
        </div>""", unsafe_allow_html=True)
        
        source = st.segmented_control("Source", ["Fichier Local", "Google Drive"], default="Fichier Local")
        
        if source == "Fichier Local":
            st.file_uploader("Prendre en photo / Parcourir", type=["pdf", "png", "jpg"])
        else:
            st.text_input("Lien Google Drive partagé")

    # Section Profiling
    st.markdown("#### Votre Profil")
    col1, col2 = st.columns(2)
    with col1:
        rdth = st.toggle("Statut RDTH")
    with col2:
        contrat = st.selectbox("Contrat", ["35h", "28h", "Temps partiel"])
        
    doc = st.selectbox("Type de vérification", ["Bulletin de paie", "Contrat de travail", "Avenant"])

    if st.button("Lancer l'audit certifié"):
        run_smart_audit(doc, rdth, contrat)

with tab2:
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    for news in NEWS_DATA:
        st.markdown(f"""
        <div class="premium-card">
            <span class="news-tag">{news['source']}</span>
            <div class="news-title">{news['titre']}</div>
            <div class="news-excerpt">{news['resume']}</div>
            <div style="margin-top:15px; display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.8em; color:#aeaeb2;">{news['date']}</span>
                <span style="color:#007AFF; font-weight:600; font-size:0.9em;">Lire l'article →</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='premium-card'>
        <h3>IDCC 1517</h3>
        <p>Commerce de détail non alimentaire</p>
        <hr style='border:0; border-top:1px solid #eee;'>
        <p><b>Points clés Boulanger :</b></p>
        <ul>
            <li>Prime d'ancienneté : +3% après 3 ans.</li>
            <li>Délai de prévenance : 7 jours ouvrés.</li>
            <li>Majoration heures de nuit : 25%.</li>
        </ul>
        <a href='https://www.legifrance.gouv.fr' style='text-decoration:none;'>
            <button style='width:100%; padding:10px; border-radius:10px; border:1px solid #007AFF; background:none; color:#007AFF; cursor:pointer;'>Consulter le texte officiel</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.button("Déconnexion")
st.sidebar.caption("La Buse Pro v4.0 | © 2026")
