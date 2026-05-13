import streamlit as st
import pandas as pd
from datetime import datetime
import time
import urllib.parse
import json
import base64
import struct

# Configuration de la page
st.set_page_config(
    page_title="La Buse Pro - Social Intelligence",
    page_icon="🦅",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialisation des états
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'last_audit' not in st.session_state:
    st.session_state.last_audit = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'accessibility_mode' not in st.session_state:
    st.session_state.accessibility_mode = False

def pcm_to_wav(pcm_data, sample_rate=24000):
    """Convertit les données PCM brutes de l'API Gemini en fichier WAV valide."""
    num_channels = 1
    sample_width = 2  # 16-bit
    
    header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF', 36 + len(pcm_data), b'WAVE',
        b'fmt ', 16, 1, num_channels, sample_rate,
        sample_rate * num_channels * sample_width,
        num_channels * sample_width, sample_width * 8,
        b'data', len(pcm_data)
    )
    return header + pcm_data

def speak_text(text, voice_name="Sadachbia"):
    """Appelle l'API Gemini TTS pour générer une voix de synthèse."""
    try:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=" # API Key auto-filled by UI
        payload = {
            "contents": [{"parts": [{"text": f"Lis ce contenu de manière claire et posée : {text}"}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {"voiceName": voice_name}
                    }
                }
            }
        }
        
        # Note: Dans un environnement réel, on utiliserait st.secrets pour la clé
        response = st.session_state.get('last_tts_response', None)
        
        import requests
        res = requests.post(api_url, json=payload)
        if res.status_code == 200:
            data = res.json()
            audio_base64 = data['candidates'][0]['content']['parts'][0]['inlineData']['data']
            pcm_bytes = base64.b64decode(audio_base64)
            wav_bytes = pcm_to_wav(pcm_bytes)
            return wav_bytes
    except Exception as e:
        st.error(f"Erreur audio : {e}")
    return None

# CSS avec support du Mode Accessibilité
accessibility_css = ""
if st.session_state.accessibility_mode:
    accessibility_css = """
    :root {
        --bg-color: #000000 !important;
        --card-bg: #1a1a1a !important;
        --text-main: #FFFF00 !important; /* Jaune sur noir pour contraste max */
        --text-sub: #FFFFFF !important;
        --primary: #FFFF00 !important;
        --border-color: #FFFF00 !important;
    }
    html, body, [class*="css"] {
        font-size: 1.2rem !important; /* Texte plus grand */
        line-height: 1.6 !important;
    }
    .stButton>button {
        border: 3px solid #FFFF00 !important;
        font-size: 1.3rem !important;
        height: auto !important;
        padding: 15px !important;
    }
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    :root {{
        --primary: #007AFF;
        --accent: #f26b21;
        --bg-color: #f2f2f7;
        --card-bg: #ffffff;
        --text-main: #1c1c1e;
        --text-sub: #636366;
        --border-color: #d1d1d6;
    }}

    @media (prefers-color-scheme: dark) {{
        :root {{
            --bg-color: #000000;
            --card-bg: #1c1c1e;
            --text-main: #ffffff;
            --text-sub: #aeaeb2;
            --border-color: #3a3a3c;
        }}
    }}

    {accessibility_css}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: var(--text-main) !important;
    }}

    .stApp {{ background-color: var(--bg-color); }}

    label, .stMarkdown p, .stCaption {{
        color: var(--text-main) !important;
        font-weight: 600 !important;
    }}

    .premium-card {{
        background: var(--card-bg);
        border-radius: 20px;
        padding: 24px;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }}

    .news-card {{
        border-left: 6px solid var(--accent);
        background: var(--card-bg);
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 0 12px 12px 0;
    }}
    
    .audio-btn {{
        background: none;
        border: 1px solid var(--primary);
        color: var(--primary);
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.8em;
        cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)

def check_pin():
    if st.session_state.pin_input == "1234":
        st.session_state.authenticated = True
    else:
        st.error("Code PIN incorrect.")

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='text-align:center; padding-top:50px;'>", unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/144/eagle.png", width=100)
        st.markdown("<h1>LA BUSE PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight:700;'>Identifiez-vous</p>", unsafe_allow_html=True)
        st.text_input("Code PIN (1234)", type="password", key="pin_input", on_change=check_pin)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

with st.sidebar:
    st.markdown("### 🛠️ Paramètres")
    st.toggle("♿ Mode Accessibilité (Contrast+)", key="accessibility_mode")
    
    st.markdown("---")
    st.markdown("### 🦅 Agent IA Eagle")
    
    if st.button("🔊 Lire le résumé du site"):
        with st.spinner("Génération de l'audio..."):
            audio = speak_text("Bienvenue sur La Buse Pro. Ce tableau de bord vous permet d'analyser vos bulletins de paie, de consulter vos droits et les actualités syndicales de Boulanger. Je suis Eagle, votre assistant juridique.")
            if audio:
                st.audio(audio, format="audio/wav", autoplay=True)
    
    chat_input = st.chat_input("Votre question...")
    if chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        time.sleep(1)
        response = "D'après l'analyse, l'anomalie sur la prime d'ancienneté est confirmée."
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history[-2:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

st.title("Tableau de Bord Social")
tab1, tab2, tab3, tab4 = st.tabs(["🕵️ Expert", "📊 Rapports", "📢 Défends-toi", "📜 Jurisprudence"])

with tab1:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Audit Multi-Documents")
    files = st.file_uploader("Glissez vos bulletins (PDF/JPG)", accept_multiple_files=True)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        statut = st.selectbox("Statut", ["Employé", "Agent de Maîtrise", "Cadre"])
    with c2:
        contrat = st.selectbox("Contrat", ["35h", "28h", "Temps Partiel"])
    
    if st.button("Lancer l'audit de masse"):
        if files:
            with st.status("🔍 Analyse en cours...", expanded=True) as s:
                time.sleep(1.5)
                st.session_state.last_audit = {
                    "date": datetime.now().strftime("%d/%m/%Y"),
                    "anomalies": ["Erreur de calcul sur la prime d'ancienneté (Code 4.2).", "Absence de majoration sur les heures du dimanche."],
                    "statut": statut
                }
                s.update(label="Audit Terminé !", state="complete")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    if st.session_state.last_audit:
        audit = st.session_state.last_audit
        st.subheader(f"Rapport du {audit['date']}")
        
        col_title, col_audio = st.columns([0.8, 0.2])
        with col_audio:
            if st.button("🔊 Écouter"):
                txt = "Voici votre rapport d'audit. " + " ".join(audit['anomalies'])
                audio = speak_text(txt)
                if audio: st.audio(audio, format="audio/wav", autoplay=True)
        
        for ano in audit['anomalies']:
            st.markdown(f"<div class='anomalie-box' style='background:rgba(255,59,48,0.1); padding:10px; border-radius:10px; margin-bottom:10px;'>⚠️ {ano}</div>", unsafe_allow_html=True)
    else:
        st.info("Utilisez l'onglet Expert pour générer un rapport.")

with tab3:
    st.subheader("Actualités Syndicales")
    news_items = [
        {"titre": "NAO 2026 : Progrès en cours", "desc": "Les négociations sur les salaires ont débuté."},
        {"titre": "Prime PPV", "desc": "Versement prévu sur la paie de juin."}
    ]
    
    for i, n in enumerate(news_items):
        with st.container():
            st.markdown(f"""
            <div class="news-card">
                <strong>{n['titre']}</strong><br>
                <small>{n['desc']}</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 Lire l'actu {i+1}", key=f"news_{i}"):
                audio = speak_text(f"{n['titre']}. {n['desc']}")
                if audio: st.audio(audio, format="audio/wav", autoplay=True)

with tab4:
    st.subheader("Convention IDCC 1517")
    st.info("Focus Ancienneté : 3% après 3 ans, 6% après 6 ans.")
    if st.button("🔊 Lire les règles d'ancienneté"):
        audio = speak_text("L'ancienneté dans la convention collective 1517 prévoit une majoration de salaire de 3 pourcent après 3 ans de présence, 6 pourcent après 6 ans, et 9 pourcent après 9 ans.")
        if audio: st.audio(audio, format="audio/wav", autoplay=True)

st.sidebar.caption("La Buse Pro v6.5 | Mode Accessibilité Actif")
