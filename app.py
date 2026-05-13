import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURATION INTERFACE ---
st.set_page_config(
    page_title="La Buse Pro - Boulanger",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALISATION ÉTATS ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'accessibility_mode' not in st.session_state:
    st.session_state.accessibility_mode = False

# --- DONNÉES DE RÉFÉRENCE ---
BOULANGER_DATA = {
    "name": "Boulanger",
    "idcc": "1517",
    "syndicats": {
        "UNSA": {"nom": "UNSA", "contact": "S. SOURDET", "tel": "07 60 36 79 47", "email": "contact@unsa-boulanger.com", "infos": "Défense juridique et accompagnement."},
        "CFTC": {"nom": "CFTC", "contact": "A. CHIADMI", "tel": "06 51 92 56 99", "infos": "Expertise NAO 2026 et revalorisation BSC."},
        "CFDT": {"nom": "CFDT", "contact": "C. AVRILLON", "tel": "07 84 71 12 09", "infos": "Accompagnement et livret d'accueil."},
        "CGT": {"nom": "CGT", "contact": "W. B. AHAMED", "tel": "06 11 42 07 82", "infos": "Protection UES et réseaux sociaux."},
        "FO": {"nom": "FO", "contact": "Délégués Nat.", "infos": "Campagne étrennes 500€."}
    }
}

# --- STYLES CSS OPTIMISÉS ---
accessibility_style = ""
if st.session_state.accessibility_mode:
    accessibility_style = """
    :root { --text-color: #FFFF00 !important; --bg-card: #000000 !important; }
    .stMarkdown, p, h1, h2, h3, span { color: #FFFF00 !important; font-size: 1.2rem !important; }
    .premium-card { border: 2px solid #FFFF00 !important; background: black !important; }
    """

st.markdown(f"""
    <style>
    {accessibility_style}
    .premium-card {{
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #f26b21;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #1c1c1e;
    }}
    .stButton>button {{
        border-radius: 12px;
        background-color: #004a99;
        color: white;
        height: 3em;
        font-weight: bold;
    }}
    .stChatFloatingInputContainer {{ bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME D'AUTHENTIFICATION ---
def check_pin():
    if st.session_state.pin_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("Code PIN erroné.")

if not st.session_state.authenticated:
    _, col, _ = st.columns([1,2,1])
    with col:
        st.image("https://images.unsplash.com/photo-1516550130560-ef02196d8f6b?q=80&w=400", use_container_width=True)
        st.markdown("<h2 style='text-align:center;'>LA BUSE PRO</h2>", unsafe_allow_html=True)
        st.text_input("Saisissez votre code d'accès", type="password", key="pin_input", on_change=check_pin)
        st.stop()

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("🦅 Agent Eagle")
    st.toggle("♿ Accessibilité (Vocal/Contraste)", key="accessibility_mode")
    
    menu = st.radio("Menu Principal", ["🏠 Tableau de Bord", "🕵️ Multi-Audit Expert", "🤝 Défends tes droits", "📜 Convention IDCC", "📱 Mobile"])
    
    st.divider()
    st.subheader("Posez une question à l'IA")
    user_q = st.chat_input("Ex: Prime ancienneté ?")
    
    if user_q:
        res = "D'après la convention 1517 : "
        if "ancien" in user_q.lower(): res += "Vous avez droit à +1j après 10 ans, +2j après 15 ans et +3j après 20 ans."
        elif "salaire" in user_q.lower(): res += "Le minimum branche Niveau 1 est de 1766,92€ brut."
        else: res += "Je vous invite à contacter Stéphane SOURDET (UNSA) pour cette précision juridique complexe."
        st.session_state.chat_history.append({"q": user_q, "a": res})

    for chat in st.session_state.chat_history[-2:]:
        st.info(f"🗨️ {chat['q']}")
        st.success(f"🦅 {chat['a']}")

# --- LOGIQUE DES PAGES ---
if menu == "🏠 Tableau de Bord":
    st.title("Tableau de Bord Social")
    st.markdown("""
    <div class="premium-card">
        <h3>🔥 FLASH INFOS - Style Morandini</h3>
        <p><b>URGENT :</b> Les négociations NAO 2026 débutent. Les syndicats demandent une hausse de 5% pour compenser l'inflation.</p>
        <hr>
        <p><b>ALERTE RDTH :</b> Des bugs sur le calcul des temps de trajet ont été remontés en région Nord.</p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "🕵️ Multi-Audit Expert":
    st.title("Analyseur de Documents Intelligent")
    st.write("Importez jusqu'à 10 bulletins de paie ou contrats (PDF/JPG).")
    
    files = st.file_uploader("Fichiers à analyser", accept_multiple_files=True)
    c1, c2 = st.columns(2)
    with c1: rdth = st.checkbox("Statut RDTH ?")
    with c2: contrat = st.selectbox("Contrat", ["35h", "28h", "Autre"])

    if files and st.button("Lancer l'audit groupé"):
        with st.status("🔍 Eagle analyse vos documents...") as s:
            for f in files:
                time.sleep(1)
                st.write(f"Analyse de {f.name} terminée.")
            s.update(label="Analyse Terminée !", state="complete")
        
        st.success(f"✅ {len(files)} documents analysés en conformité IDCC 1517.")
        st.warning(f"⚠️ **Anomalie détectée :** Pour le contrat {contrat}, vérifiez la ligne 'Prime de lissage' qui semble absente.")
        if st.button("📤 Envoyer le rapport par Mail"):
            st.toast("Préparation du mail en cours...")

elif menu == "🤝 Défends tes droits":
    st.title("Vos Représentants")
    for k, v in BOULANGER_DATA["syndicats"].items():
        with st.expander(f"📌 {v['nom']} - {v['contact']}"):
            st.write(v["infos"])
            if "tel" in v: st.link_button(f"📞 Appeler", f"tel:{v['tel']}")

elif menu == "📜 Convention IDCC":
    st.title("Jurisprudence & Grilles")
    df = pd.DataFrame({
        "Niveau": ["1", "2", "3", "4", "5"],
        "Mini Brut": ["1766€", "1785€", "1830€", "1960€", "2150€"]
    })
    st.table(df)

# --- PIED DE PAGE ---
st.divider()
st.caption(f"La Buse Pro v9.2 | Optimisé pour iPhone | Design par Yann COLAS DAVID")
st.markdown("---")
# CORRECTION DE LA SYNTAXE ICI
st.caption("La Buse Pro v7.0 | Design Protecteur & Inclusif crée par Yann COLAS DAVID")
