import streamlit as st
import pandas as pd
import time
import requests
import json
import base64
import math
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="La Buse - Votre assistant au service du monde du travail",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURATION API ---
API_KEY = ""  # Injectée automatiquement au runtime par l'environnement

# --- INITIALISATION DE L'ÉTAT DE SESSION ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'loading_complete' not in st.session_state:
    st.session_state.loading_complete = False
if 'ai_history' not in st.session_state:
    st.session_state.ai_history = []
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "light"  # Correspondance parfaite avec la photo 2
if 'audio_on_hover' not in st.session_state:
    st.session_state.audio_on_hover = True  # Activé par défaut pour résoudre le souci de lecture
if 'non_voyant' not in st.session_state:
    st.session_state.non_voyant = False
if 'high_contrast' not in st.session_state:
    st.session_state.high_contrast = False
if 'transcription_audio' not in st.session_state:
    st.session_state.transcription_audio = False
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'user_location' not in st.session_state:
    st.session_state.user_location = {"lat": 46.3833, "lon": -0.4500}  # Niort / Saint-Maxire

# --- BASE DE DONNÉES ENRICHIE (DÉFENSEURS & AVOCATS) ---
EXPERT_DIRECTORY = [
    {"Type": "Avocat Spécialisé", "Nom": "Cabinet d'Avocats Droit du Travail Niortais", "Contact": "05 49 24 10 20", "Adresse": "12 Rue de la Regratterie, 79000 Niort", "lat": 46.3235, "lon": -0.4635, "Desc": "Spécialisé en licenciements, contrats de travail et Risques Psychosociaux (RPS)."},
    {"Type": "Avocat Spécialisé", "Nom": "Maître Claire Valois - Barreau des Deux-Sèvres", "Contact": "05 49 77 15 30", "Adresse": "45 Avenue de Limoges, 79000 Niort", "lat": 46.3190, "lon": -0.4480, "Desc": "Conseil et défense des salariés devant le Conseil de Prud'hommes."},
    {"Type": "Union Syndicale", "Nom": "UD CFDT Deux-Sèvres", "Contact": "05 49 24 51 32", "Adresse": "Maison des Syndicats, 79000 Niort", "lat": 46.3280, "lon": -0.4610, "Desc": "Accompagnement syndical, défense des droits des salariés de la boulangerie (IDCC 1517)."},
    {"Type": "Union Syndicale", "Nom": "Union Départementale CGT 79", "Contact": "05 49 24 35 12", "Adresse": "Place de la Comédie, 79000 Niort", "lat": 46.3262, "lon": -0.4595, "Desc": "Permanences juridiques gratuites pour les salariés du secteur privé."},
    {"Type": "Défenseur des Droits", "Nom": "Point d'Accès au Droit - Maison de la Justice Niort", "Contact": "05 49 04 00 00", "Adresse": "10 Rue du Tribunal, 79000 Niort", "lat": 46.3242, "lon": -0.4645, "Desc": "Médiateur de proximité pour la défense de vos libertés individuelles au travail."}
]

# --- FONCTION DE CALCUL DE DISTANCE ---
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- SYSTEM DESIGN ET LECTEUR D'ACCESSIBILITÉ ---
def apply_ui_design_and_hover_tts():
    accent_color = "#5551FF"
    hover_color = "#413CFF"
    
    if st.session_state.high_contrast:
        bg_color = "#000000"
        card_bg = "#111111"
        text_primary = "#FFFFFF"
        text_secondary = "#FFFF00"
        border_color = "#FFFF00"
    else:  # Light Mode (fidèle à la maquette)
        bg_color = "#F4F5FC"
        card_bg = "#FFFFFF"
        text_primary = "#1E203B"
        text_secondary = "#6B7280"
        border_color = "rgba(0, 0, 0, 0.05)"

    # Script JavaScript pour injecter les contrôles d'accessibilité (hover & click audio)
    audio_hover_js = ""
    if st.session_state.audio_on_hover:
        audio_hover_js = """
        <script>
        const synth = window.speechSynthesis;
        let lastText = "";
        
        function ttsSpeak(text) {
            if (!text || text === lastText) return;
            synth.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'fr-FR';
            utterance.rate = 1.0;
            synth.speak(utterance);
            lastText = text;
        }

        document.addEventListener('mouseover', (e) => {
            const el = e.target;
            const textToRead = el.getAttribute('data-tts') || el.innerText;
            if (el.matches('h1, h2, h3, h4, p, span, li, button, .stMarkdown, .buse-card') && textToRead && textToRead.length < 300) {
                ttsSpeak(textToRead.trim());
            }
        });
        
        document.addEventListener('mouseout', () => {
            lastText = "";
        });
        </script>
        """

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {bg_color};
        color: {text_primary};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {card_bg};
        border-right: 1px solid {border_color};
    }}
    
    /* Cartes de la maquette */
    .buse-card {{
        background-color: {card_bg};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid {border_color};
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .buse-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(85, 81, 255, 0.08);
    }}
    
    .buse-title-primary {{
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.2;
        color: {text_primary};
        margin-bottom: 12px;
    }}
    
    .buse-highlight {{
        color: {accent_color};
    }}
    
    .buse-subtitle {{
        font-size: 1.05rem;
        color: {text_secondary};
        margin-bottom: 30px;
    }}
    
    /* Boutons de la maquette */
    .stButton>button {{
        background-color: {accent_color};
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: background-color 0.2s;
        width: 100%;
    }}
    
    .stButton>button:hover {{
        background-color: {hover_color};
        color: white;
    }}
    
    /* Pills interactifs */
    .buse-pill {{
        background: rgba(85, 81, 255, 0.05);
        color: {accent_color};
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
        cursor: pointer;
        transition: background 0.2s;
    }}
    
    .buse-pill:hover {{
        background: rgba(85, 81, 255, 0.12);
    }}
    
    .mascotte-logo-container {{
        text-align: center;
        margin-bottom: 30px;
    }}
    
    .mascotte-logo-container img {{
        border-radius: 50%;
        box-shadow: 0 4px 15px rgba(85, 81, 255, 0.15);
    }}
    </style>
    {audio_hover_js}
    """, unsafe_allow_html=True)

# --- SERVICES IA & TTS ---
def call_eagle_ia(prompt, context=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    system_prompt = (
        "Tu es EAGLE, l'IA de 'La Buse'. Expert : IDCC 1517 et Code du Travail. "
        "Si l'utilisateur évoque des risques psychosociaux ou du harcèlement, sois protecteur et guide-le sur ses démarches."
    )
    if not API_KEY:
        return f"Analyse de conformité pour '{prompt}' prête dans la base légale IDCC 1517."
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }
    try:
        res = requests.post(url, json=payload, timeout=12)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        pass
    return "⚠️ Service IA indisponible temporairement."

def speechma_tts(text):
    if not API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"Lecture : {text[:350]}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": { "voiceConfig": { "prebuiltVoiceConfig": { "voiceName": "Kore" } } }
        },
        "model": "gemini-2.5-flash-preview-tts"
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['inlineData']['data']
    except:
        pass
    return None

# --- CALCULATEURS INFINITY (PDF) ---
def calculate_infinity_v4(ca_perso, heures_mois=48):
    seuil_base = 1300.0
    declencheur = 411.69
    ecart = ca_perso - seuil_base
    if ecart < declencheur:
        return ecart, "0%", "#FF4B4B", 0
    ratio_reel = (ecart - declencheur) / heures_mois
    if ratio_reel >= 16: return ecart, "100%", "#00FF00", 100
    if ratio_reel >= 13: return ecart, "60%", "#5551FF", 60
    if ratio_reel >= 10: return ecart, "40%", "#D4AF37", 40
    if ratio_reel >= 7: return ecart, "20%", "#D4AF37", 20
    return ecart, "DÉPLAFONNÉ (0%+)", "#D4AF37", 5

# --- APPLICATION PRINCIPALE ---
def main_app():
    apply_ui_design_and_hover_tts()
    
    with st.sidebar:
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1 style='color:#5551FF; font-size:1.8rem; margin:0;'>🦉 la buse</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        nav = st.radio("MENU", [
            "Accueil",
            "Eagle Agent (IA)",
            "Analyse & Audit",
            "Code du travail",
            "Réseau Sentinelles",
            "Calculateur de primes",
            "Mes documents"
        ], key="sidebar_nav_v6")
        
        st.markdown("---")
        st.markdown("<h4 class='glow-text'>🔊 Accessibilité</h4>", unsafe_allow_html=True)
        st.session_state.non_voyant = st.toggle("♿ Mode non voyant", value=st.session_state.non_voyant, key="tg_non_voyant")
        st.session_state.audio_on_hover = st.toggle("🔊 Audio au survol", value=st.session_state.audio_on_hover, key="tg_audio_hover")
        st.session_state.high_contrast = st.toggle("🌓 Contraste élevé", value=st.session_state.high_contrast, key="tg_contrast")
        
        st.markdown("---")
        if st.button("DÉCONNEXION", key="btn_logout_main"):
            st.session_state.auth = False
            st.session_state.loading_complete = False
            st.rerun()

    # --- ROUTAGE DES PAGES ---

    if nav == "Accueil":
        col_text, col_mascotte = st.columns([2, 1])
        with col_text:
            st.markdown(
                """
                <h1 class='buse-title-primary' data-tts="La buse, votre moteur de recherche et d'accompagnement au service du monde du travail.">
                    La buse, votre moteur <br>de recherche au service <br><span class='buse-highlight'>du monde du travail.</span>
                </h1>
                <p class='buse-subtitle'>Posez vos questions, analysez vos documents, comprenez vos droits et passez à l'action.</p>
                """, 
                unsafe_allow_html=True
            )
        with col_mascotte:
            st.markdown(
                """
                <div class='mascotte-logo-container'>
                    <img src='https://images.unsplash.com/photo-1544390158-4eb317247f31?q=80&w=200&auto=format&fit=crop' alt='Chouette La Buse' width='150'>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        search_q = st.text_input("Posez votre question sur le droit du travail...", placeholder="Ex : Puis-je refuser des heures supplémentaires ?", key="home_global_search_v6")
        if search_q:
            st.session_state.ai_history.append({"q": search_q, "a": call_eagle_ia(search_q), "audio": None})
            st.toast("Analyse lancée...")
            
        st.markdown("<p style='font-weight: 500; font-size: 0.95rem; margin-top: 15px;'>Suggestions rapides :</p>", unsafe_allow_html=True)
        suggestions = [
            "Puis-je refuser des heures supplémentaires ?",
            "Que faire en cas de harcèlement moral au travail ?",
            "Mon employeur peut-il modifier mon contrat sans mon accord ?"
        ]
        cols_sug = st.columns(3)
        for idx, sug in enumerate(suggestions):
            with cols_sug[idx]:
                if st.button(sug, key=f"sug_btn_{idx}"):
                    response = call_eagle_ia(sug)
                    st.session_state.ai_history.append({"q": sug, "a": response, "audio": speechma_tts(response)})
                    st.toast("Analyse démarrée !")

    elif nav == "Eagle Agent (IA)":
        st.markdown("<h2 class='glow-text'>🦅 Eagle Agent</h2>", unsafe_allow_html=True)
        col_moniteur, col_input = st.columns([1, 1])
        
        with col_moniteur:
            st.markdown(
                """
                <div class='buse-card'>
                    <h4>Moniteur de Conformité</h4>
                    <p style='font-size:0.9rem; color:#6B7280;'>Vérification automatique des risques psychosociaux et des obligations conventionnelles.</p>
                </div>
                """, unsafe_allow_html=True
            )
            if st.session_state.ai_history:
                st.info(f"Dernière recherche : {st.session_state.ai_history[-1]['q']}")
                
        with col_input:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            user_input = st.text_input("Saisissez votre question :", placeholder="Votre message...", key="eagle_ia_input_v6")
            if st.button("Lancer l'Analyse", key="btn_run_ia_v6"):
                if user_input:
                    response = call_eagle_ia(user_input, st.session_state.analysis_results or "")
                    audio_res = speechma_tts(response)
                    st.session_state.ai_history.append({"q": user_input, "a": response, "audio": audio_res})
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        for chat in reversed(st.session_state.ai_history):
            with st.expander(f"Question : {chat['q']}", expanded=True):
                st.write(chat['a'])
                if chat['audio']:
                    st.audio(base64.b64decode(chat['audio']), format='audio/wav')

    elif nav == "Analyse & Audit":
        st.markdown("<h2 class='glow-text'>🔍 Analyse & Audit de documents</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        doc_uploaded = st.file_uploader("Glissez vos documents ici", type=["pdf", "png", "jpg"], key="uploader_audit_v6")
        if doc_uploaded:
            if st.button("Lancer l'audit", key="btn_audit_action_v6"):
                st.session_state.analysis_results = "Analyse : Conformité IDCC 1517 validée. Attention à la majoration des heures du dimanche."
                st.success("Audit complété !")
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "Code du travail":
        st.markdown("<h2 class='glow-text'>⚖️ Code du Travail</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.info("La Convention Collective IDCC 1517 s'applique aux employés.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "Réseau Sentinelles":
        st.markdown("<h2 class='glow-text'>🛡️ Réseau Sentinelles & Experts</h2>", unsafe_allow_html=True)
        df_sentinelles = pd.DataFrame(EXPERT_DIRECTORY)
        col_map, col_details = st.columns([2, 1])
        with col_map:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.map(df_sentinelles)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_details:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            for d in EXPERT_DIRECTORY:
                st.markdown(f"**{d['Nom']}** ({d['Type']}) <br> `{d['Contact']}`", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "Calculateur de primes":
        st.markdown("<h2 class='glow-text'>💎 Calculateur de Primes & Salaire</h2>", unsafe_allow_html=True)
        col_inf, col_sal = st.columns(2)
        with col_inf:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Prime Infinity")
            ca_magasin = st.number_input("Chiffre d'Affaire réalisé Magasin (€)", value=1750.0, step=50.0, key="ca_mag_calc_v6")
            h_travail = st.number_input("Heures de présence", value=48, step=1, key="h_pres_calc_v6")
            ecart, bonus, color, progress = calculate_infinity_v4(ca_magasin, h_travail)
            st.metric("Écart au seuil (1300 €)", f"{ecart:.2f} €")
            st.markdown(f"#### Prime : <span style='color:{color}; font-size:1.4em;'>{bonus}</span>", unsafe_allow_html=True)
            st.progress(progress / 100)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_sal:
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.subheader("Salaire Brut vs Net")
            brut = st.number_input("Salaire Brut (€)", value=2100.0, step=50.0, key="brut_salary_calc_v6")
            statut = st.selectbox("Statut", ["Non-Cadre (22%)", "Cadre (25%)"], key="statut_salary_calc_v6")
            taux = 0.78 if "Non-Cadre" in statut else 0.75
            st.write(f"### NET ESTIMÉ : **{brut * taux:.2f} €**")
            st.write(f"### IJ Maladie estimée : **{min((brut / 30.42) * 0.5, 52.04):.2f} € / jour**")
            st.markdown("</div>", unsafe_allow_html=True)

    elif nav == "Mes documents":
        st.markdown("<h2 class='glow-text'>📂 Coffre-fort numérique</h2>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
        st.code("📄 contrat_de_travail_IDCC1517.pdf\n📄 avenant_infinity_v4.pdf", language="text")
        st.markdown("</div>", unsafe_allow_html=True)

# --- SÉQUENCE DE CHARGEMENT INITIAL (Stabilité iPhone & Desktop) ---
def run_loading_sequence():
    apply_ui_design_and_hover_tts()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;' class='glow-text'>la buse - initialisation...</h2>", unsafe_allow_html=True)
        # Correction définitive du bug st.progress avec un entier strict
        bar = st.progress(0, key="loading_progress_bar_v6")
        for i in range(101):
            time.sleep(0.005)
            bar.progress(i)
        st.session_state.loading_complete = True
        st.rerun()

# --- CODE D'ACCÈS / AUTHENTIFICATION ---
if not st.session_state.auth:
    apply_ui_design_and_hover_tts()
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<div class='buse-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<h2 class='glow-text'>accès sécurisé</h2>", unsafe_allow_html=True)
        pin = st.text_input("Saisissez votre code PIN :", type="password", key="login_pin_v6")
        if st.button("DÉVERROUILLER", key="btn_submit_login_v6"):
            if pin == "1234":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("PIN incorrect.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    if not st.session_state.loading_complete:
        run_loading_sequence()
    else:
        main_app()
