import streamlit as st
import pandas as pd
from datetime import datetime
import time
import base64

# Configuration de la page
st.set_page_config(
    page_title="La Buse Pro - Protection Sociale",
    page_icon="🦅",
    layout="centered",
    initial_sidebar_state="expanded"
)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'last_audit' not in st.session_state:
    st.session_state.last_audit = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'accessibility_mode' not in st.session_state:
    st.session_state.accessibility_mode = False

def speak_text(text):
    """Génère un script JS pour forcer la lecture vocale immédiate."""
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text.replace('"', "'")}");
    msg.lang = 'fr-FR';
    window.speechSynthesis.speak(msg);
    </script>
    """
    return js_code

accessibility_css = ""
hover_js = ""

if st.session_state.accessibility_mode:
    # Thème Haute Visibilité (Noir et Jaune)
    accessibility_css = """
    :root {
        --bg-color: #000000 !important;
        --card-bg: #1a1a1a !important;
        --text-main: #FFFF00 !important;
        --text-sub: #FFFFFF !important;
        --primary: #FFFF00 !important;
        --border-color: #FFFF00 !important;
    }
    html, body, [class*="css"] {
        font-size: 1.3rem !important;
    }
    .stButton>button {
        border: 4px solid #FFFF00 !important;
        font-size: 1.5rem !important;
        color: #FFFF00 !important;
        background-color: black !important;
    }
    """
    # Script JS pour la lecture au survol de la souris
    hover_js = """
    <script>
    const synth = window.speechSynthesis;
    document.querySelectorAll('p, h1, h2, h3, span, li, .stMarkdown').forEach(item => {
        item.addEventListener('mouseenter', event => {
            synth.cancel();
            var msg = new SpeechSynthesisUtterance(event.target.innerText);
            msg.lang = 'fr-FR';
            synth.speak(msg);
        });
        item.addEventListener('mouseleave', event => {
            synth.cancel();
        });
    });
    </script>
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    :root {{
        --primary: #007AFF;
        --accent: #f26b21;
        --bg-color: #f8f9fa;
        --card-bg: #ffffff;
        --text-main: #1c1c1e;
        --text-sub: #636366;
        --border-color: #e5e5ea;
    }}

    {accessibility_css}

    .stApp {{ background-color: var(--bg-color); color: var(--text-main); }}
    
    .premium-card {{
        background: var(--card-bg);
        border-radius: 20px;
        padding: 24px;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }}

    h1, h2, h3 {{ color: var(--text-main) !important; }}
    p, span, label {{ color: var(--text-main) !important; }}
    </style>
    """, unsafe_allow_html=True)

# Activation du survol vocal si mode actif
if st.session_state.accessibility_mode:
    st.components.v1.html(hover_js, height=0)

def check_pin():
    if st.session_state.pin_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("Code PIN incorrect.")

if not st.session_state.authenticated:
    st.markdown("<br>", unsafe_allow_html=True)
    # IMAGE DE LA BUSE PROTECTRICE
    st.image("https://images.unsplash.com/photo-1516550130560-ef02196d8f6b?q=80&w=1500&auto=format&fit=crop", 
             caption="La Buse Pro - Votre Vigilance Sociale", use_container_width=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h2 style='text-align:center;'>ESPACE SÉCURISÉ</h2>", unsafe_allow_html=True)
        st.text_input("Saisissez votre code PIN (1234)", type="password", key="pin_input", on_change=check_pin)
    st.stop()

with st.sidebar:
    st.markdown("## 🦅 Agent IA Eagle")
    st.image("https://img.icons8.com/fluency/96/eagle.png", width=60)
    
    st.toggle("♿ Mode Accessibilité (Contrast+)", key="accessibility_mode")
    
    # Bouton de lecture conditionnel
    if st.session_state.accessibility_mode:
        if st.button("🔊 Lire le résumé du site"):
            st.components.v1.html(speak_text("Bienvenue sur La Buse Pro. Ce tableau de bord vous permet d'analyser vos bulletins de paie, de consulter la jurisprudence et de contacter vos délégués. Le mode accessibilité est activé, survolez les textes pour les entendre."), height=0)
    
    st.markdown("---")
    st.subheader("Chat avec Eagle")
    chat_input = st.chat_input("Une question sur vos droits ?")
    if chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        # Réponse simulée
        response = "D'après la convention 1517, votre prime d'ancienneté doit figurer sur une ligne distincte de votre salaire de base."
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history[-2:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

st.title("Tableau de Bord Social")

# MOTEUR DE RECHERCHE INTELLIGENT
search_query = st.text_input("🔍 Recherche Juridique (Code du Travail, Convention 1517...)", 
                            placeholder="Ex: Prime RDTH, Majorations dimanche, Temps de pause...")
if search_query:
    st.info(f"Résultat pour '{search_query}' : Selon l'IDCC 1517, l'article 4.2 encadre précisément ce point...")

tab1, tab2, tab3, tab4 = st.tabs(["🕵️ Audit Expert", "📊 Rapports", "📢 Défends tes droits", "📜 Jurisprudence"])

with tab1:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Analyse Multi-Documents")
    files = st.file_uploader("Glissez vos fiches de paie ou contrats (PDF/JPG)", accept_multiple_files=True)
    
    c1, c2 = st.columns(2)
    with c1: 
        statut = st.selectbox("Statut", ["Employé", "Maîtrise", "Cadre"])
        rdth = st.toggle("Option RDTH (Rémunération Différée)")
    with c2: 
        contrat = st.selectbox("Type de contrat", ["35h", "28h", "Forfait Jours", "Temps Partiel"])
    
    if st.button("Lancer l'audit massif"):
        if files:
            with st.status("🔍 Eagle examine vos documents...") as s:
                time.sleep(2)
                st.session_state.last_audit = {
                    "date": datetime.now().strftime("%d/%m/%Y"),
                    "anomalies": [
                        "⚠️ Erreur possible sur la majoration du dimanche.",
                        f"✅ Prime d'ancienneté conforme pour le profil {statut}.",
                        "⚠️ Absence de mention de la pause obligatoire de 20min."
                    ],
                    "nb_fichiers": len(files)
                }
                s.update(label="Audit Terminé !", state="complete")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    if st.session_state.last_audit:
        audit = st.session_state.last_audit
        st.subheader(f"Rapport d'anomalies - {audit['nb_fichiers']} fichiers")
        for ano in audit['anomalies']:
            st.warning(ano)
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1: st.button("📥 Imprimer le rapport (PDF)")
        with col_ex2: st.button("📧 Envoyer aux délégués")
    else:
        st.info("Aucun audit récent. Téléchargez vos documents dans l'onglet Audit Expert.")

with tab3:
    st.markdown("### 📰 Actualités Syndicales & Sociales")
    news = [
        {"t": "NAO 2026 : LA DIRECTION BLOQUE LES SALAIRES", "d": "Face à l'inflation, les syndicats demandent une revalorisation de 4%."},
        {"t": "PRIME PPV : VICTOIRE POUR LES SALARIÉS", "d": "Le versement de 500€ est confirmé pour le mois de juin."},
        {"t": "RDTH : ATTENTION AUX CALCULS", "d": "De nombreuses erreurs ont été signalées sur les nouveaux contrats."}
    ]
    for n in news:
        st.markdown(f"""
        <div style='border-left:5px solid #f26b21; padding:15px; background:white; margin-bottom:12px; border-radius:10px; color:black;'>
            <h4 style='color:#1c1c1e; margin:0;'>{n['t']}</h4>
            <p style='color:#444; margin:5px 0 0 0;'>{n['d']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("Convention Collective IDCC 1517")
    st.markdown("""
    - **Ancienneté :** 3% à 3 ans, 6% à 6 ans, 9% à 9 ans (Palier max 15%).
    - **Heures Sup :** 25% pour les 8 premières, 50% au-delà.
    - **Travail de nuit :** Majoration de 20% entre 21h et 6h.
    """)

st.markdown("---")
# CORRECTION DE LA SYNTAXE ICI
st.caption("La Buse Pro v7.0 | Design Protecteur & Inclusif crée par Yann COLAS DAVID")
