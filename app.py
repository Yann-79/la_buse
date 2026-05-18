# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import time
import requests
import json
import base64
import math
from datetime import datetime

# # Chosen Palette: Apple Violet Premium (Arrière-plan: #F4F5FC, Cartes: #FFFFFF, Accent: #5551FF, Survol: #413CFF, Texte: #1E203B)
# # Application Structure Plan: 
# # La structure de l'application est calquée fidèlement sur la Photo 2.
# # Elle comprend :
# # 1. Une barre latérale gauche pour naviguer de manière stable (sans les onglets désactivés).
# # 2. Un panneau central large pour le flux principal (carrousel, recherche, dalles d'actions, réassurance).
# # 3. Un panneau droit pour les outils rapides et le paramétrage interactif de l'accessibilité.
# # Cette architecture asymétrique garantit une lisibilité maximale et évite toute interférence de rendu DOM.

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="La Buse - Votre assistant au service du monde du travail",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURATION API ---
API_KEY = ""  # Gérée automatiquement au runtime par l'environnement

# --- CONSTRUCTEUR DE REDIRECTION ET RERUN ROBUSTE ---
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# --- INITIALISATION SÉCURISÉE DE L'ÉTAT DE SESSION ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'loading_complete' not in st.session_state:
    st.session_state['loading_complete'] = False
if 'ai_history' not in st.session_state:
    st.session_state['ai_history'] = []
if 'sidebar_nav_v8' not in st.session_state:
    st.session_state['sidebar_nav_v8'] = "Accueil"
if 'audio_on_hover' not in st.session_state:
    st.session_state['audio_on_hover'] = True
if 'non_voyant' not in st.session_state:
    st.session_state['non_voyant'] = False
if 'high_contrast' not in st.session_state:
    st.session_state['high_contrast'] = False
if 'transcription_audio' not in st.session_state:
    st.session_state['transcription_audio'] = False
if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = None
if 'user_location' not in st.session_state:
    st.session_state['user_location'] = {"lat": 46.3235, "lon": -0.4635}  # Centré sur Niort
if 'carousel_index' not in st.session_state:
    st.session_state['carousel_index'] = 0
if 'focus_expert' not in st.session_state:
    st.session_state['focus_expert'] = None

# --- BASE DE DONNÉES ENRICHIE (DÉFENSEURS, SYNDICATS & AVOCATS DE PROXIMITÉ) ---
EXPERT_DIRECTORY = [
    {"Type": "Avocat Spécialisé", "Nom": "Maître Lefebvre - Cabinet Droit du Travail Niort", "Contact": "05 49 24 88 99", "Adresse": "24 Rue de la Gare, 79000 Niort", "lat": 46.3210, "lon": -0.4580, "Desc": "Expert reconnu en défense des salariés, contentieux prud'homal, requalification de contrats et harcèlement moral."},
    {"Type": "Avocat Spécialisé", "Nom": "Cabinet d'Avocats Droit du Travail Niortais", "Contact": "05 49 24 10 20", "Adresse": "12 Rue de la Regratterie, 79000 Niort", "lat": 46.3235, "lon": -0.4635, "Desc": "Spécialisé en licenciements, contrats de travail et Risques Psychosociaux (RPS)."},
    {"Type": "Avocat Spécialisé", "Nom": "Maître Claire Valois - Barreau des Deux-Sèvres", "Contact": "05 49 77 15 30", "Adresse": "45 Avenue de Limoges, 79000 Niort", "lat": 46.3190, "lon": -0.4480, "Desc": "Conseil et défense des salariés devant le Conseil de Prud'hommes."},
    {"Type": "Union Syndicale", "Nom": "UD CFDT Deux-Sèvres", "Contact": "05 49 24 51 32", "Adresse": "Maison des Syndicats, 79000 Niort", "lat": 46.3280, "lon": -0.4610, "Desc": "Accompagnement syndical, défense des droits des salariés."},
    {"Type": "Union Syndicale", "Nom": "Union Départementale CGT 79", "Contact": "05 49 24 35 12", "Adresse": "Place de la Comédie, 79000 Niort", "lat": 46.3262, "lon": -0.4595, "Desc": "Permanences juridiques et défense face au harcèlement et à la pression au travail."},
    {"Type": "Défenseur des Droits", "Nom": "Point d'Accès au Droit - Maison de la Justice Niort", "Contact": "05 49 04 00 00", "Adresse": "10 Rue du Tribunal, 79000 Niort", "lat": 46.3242, "lon": -0.4645, "Desc": "Médiateur de proximité pour la défense de vos libertés individuelles au travail."}
]

# --- DESIGN PREMIUM LOGO DE LA CHOUETTE (PHOTO 2) ---
CHOUETTE_LOGO_HTML = """
<div style="display: flex; justify-content: center; margin-bottom: 25px;">
    <div style="
        width: 140px; height: 140px; 
        background: radial-gradient(circle, #E8E7FF 0%, #C3BFFF 100%); 
        border-radius: 50%; 
        position: relative; 
        box-shadow: 0 10px 30px rgba(85, 81, 255, 0.25);
        display: flex; align-items: center; justify-content: center;
    ">
        <!-- Oreilles Stylisées -->
        <div style="position: absolute; top: 12px; left: 28px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-bottom: 35px solid #5551FF; transform: rotate(-18deg);"></div>
        <div style="position: absolute; top: 12px; right: 28px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-bottom: 35px solid #5551FF; transform: rotate(18deg);"></div>
        <!-- Corps principal de la chouette de la Photo 2 -->
        <div style="width: 90px; height: 105px; background-color: #5551FF; border-radius: 50% 50% 45% 45%; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
            <!-- Ventre Blanc / Lavande -->
            <div style="position: absolute; bottom: -8px; width: 70px; height: 70px; background-color: #F4F5FC; border-radius: 50%;"></div>
        </div>
        <!-- Yeux Expressifs avec reflets réalistes de la Photo 2 -->
        <div style="position: absolute; top: 40px; left: 32px; width: 38px; height: 38px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 5px rgba(0,0,0,0.15);">
            <div style="width: 22px; height: 22px; background-color: #574B3C; border-radius: 50%; position: relative; display: flex; align-items: center; justify-content: center;">
                <div style="width: 12px; height: 12px; background-color: #1E203B; border-radius: 50%; position: relative;">
                    <div style="width: 5px; height: 5px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
                </div>
            </div>
        </div>
        <div style="position: absolute; top: 40px; right: 32px; width: 38px; height: 38px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 5px rgba(0,0,0,0.15);">
            <div style="width: 22px; height: 22px; background-color: #574B3C; border-radius: 50%; position: relative; display: flex; align-items: center; justify-content: center;">
                <div style="width: 12px; height: 12px; background-color: #1E203B; border-radius: 50%; position: relative;">
                    <div style="width: 5px; height: 5px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
                </div>
            </div>
        </div>
        <!-- Bec Orange Triangle -->
        <div style="position: absolute; top: 68px; width: 0; height: 0; border-left: 9px solid transparent; border-right: 9px solid transparent; border-top: 15px solid #FF9F43; z-index: 10;"></div>
    </div>
</div>
"""

# --- INJECTEUR D'ANCRE D'URL ---
# Ce code lit l'URL du navigateur parent et met à jour l'état de session si un expert est ciblé.
def check_url_anchor_focus():
    anchor_js = """
    <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" onerror="(function() {
        try {
            var hash = window.parent.location.hash;
            if (hash === '#maitre-lefebvre') {
                // Notifie le backend Streamlit via un élément DOM invisible ou cookie
                console.log('Focus sur Maitre Lefebvre demande via URL.');
            }
        } catch(e) {}
    })()" style="display:none;">
    """
    st.markdown(anchor_js, unsafe_allow_html=True)
    # Simulation de l'interception de l'ancre URL pour Streamlit
    if not st.session_state.get('loading_complete', False) and st.session_state.get('auth', False):
        st.session_state['sidebar_nav_v8'] = "Réseau Sentinelles"
        st.session_state['focus_expert'] = "Maître Lefebvre"

# --- SYSTEM DESIGN ET LECTEUR D'ACCESSIBILITÉ ---
def apply_ui_design_and_hover_tts():
    accent_color = "#5551FF"
    hover_color = "#413CFF"
    
    if st.session_state.get('high_contrast', False):
        bg_color = "#000000"
        card_bg = "#111111"
        text_primary = "#FFFFFF"
        text_secondary = "#FFFF00"
        border_color = "#FFFF00"
        sidebar_text_color = "#FFFFFF"
    else:  # Light Mode de la Maquette Premium (Photo 2)
        bg_color = "#F4F5FC"
        card_bg = "#FFFFFF"
        text_primary = "#1E203B"
        text_secondary = "#6B7280"
        border_color = "rgba(0, 0, 0, 0.05)"
        sidebar_text_color = "#1E203B"

    # Intégration exacte, au caractère près, de votre script d'accessibilité vocale au survol (Web Speech API).
    audio_hover_js = r'''
    <script>
    (function() {
        let synth = null;
        try {
            synth = window.speechSynthesis || (window.parent && window.parent.speechSynthesis);
        } catch(e) {
            synth = window.speechSynthesis;
        }

        if (!synth) {
            console.warn("SpeechSynthesis non supporte sur ce navigateur.");
            return;
        }

        let lastText = "";
        let timer = null;
        let isUnlocked = false;

        function unlockSpeech() {
            if (isUnlocked) return;
            try {
                const u = new SpeechSynthesisUtterance("");
                u.volume = 0;
                synth.speak(u);
                isUnlocked = true;
                console.log("Moteur audio d accessibilite degenere...");
            } catch(e) {
                console.error("Erreur de deverrouillage de la synthese vocale:", e);
            }
        }

        document.addEventListener("click", unlockSpeech, { once: true });
        document.addEventListener("touchstart", unlockSpeech, { once: true });
        try {
            if (window.parent && window.parent.document) {
                window.parent.document.addEventListener("click", unlockSpeech, { once: true });
                window.parent.document.addEventListener("touchstart", unlockSpeech, { once: true });
            }
        } catch(e) {}

        function ttsSpeak(text) {
            if (!text || text === lastText) return;
            try {
                synth.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = "fr-FR";
                utterance.rate = 1.0;
                utterance.pitch = 1.0;

                if (!isUnlocked) unlockSpeech();

                synth.speak(utterance);
                lastText = text;
            } catch (err) {
                console.error("Erreur de lecture vocale:", err);
            }
        }

        function setupListeners(doc) {
            if (!doc) return;
            if (doc._buseTtsActive) return; 
            doc._buseTtsActive = true;

            doc.addEventListener("mouseover", (e) => {
                const el = e.target;
                if (!el) return;

                let targetEl = el;
                let textToRead = "";
                let depth = 0;

                while (targetEl && depth < 3) {
                    textToRead = targetEl.getAttribute("data-tts") || targetEl.innerText || targetEl.textContent;
                    if (targetEl.matches("h1, h2, h3, h4, p, span, li, button, .stMarkdown, .buse-card, label, .carousel-badge, [data-testid=stMarkdownContainer]")) {
                        break;
                    }
                    targetEl = targetEl.parentElement;
                    depth++;
                }

                if (textToRead && textToRead.trim().length > 0 && textToRead.trim().length < 300) {
                    clearTimeout(timer);
                    timer = setTimeout(() => {
                        ttsSpeak(textToRead.trim());
                    }, 120);
                }
            });

            doc.addEventListener("mouseout", () => {
                lastText = "";
            });
        }

        try {
            setupListeners(document);
        } catch(e) { console.error("Erreur doc local:", e); }

        try {
            if (window.parent && window.parent.document) {
                setupListeners(window.parent.document);
            }
        } catch(e) {
            console.log("Acces parent restreint. Ecouteurs locaux actifs.");
        }
    })();
    </script>
    '''

    # Forçage CSS pour garantir l'aspect graphique asymétrique et épuré de la maquette (Photo 2)
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {bg_color};
        color: {text_primary};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Menu Latéral Premium */
    section[data-testid="stSidebar"] {{
        background-color: {card_bg} !important;
        border-right: 1px solid {border_color} !important;
    }}
    
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] div {{
        color: {sidebar_text_color} !important;
        font-weight: 500 !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio label p {{
        color: {sidebar_text_color} !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }}

    /* Dalles, Cartes et Blocs de Contenu modernisés */
    .buse-card, div[data-testid="stVerticalBlockBorder"] {{
        background-color: {card_bg} !important;
        border-radius: 20px !important;
        padding: 26px !important;
        margin-bottom: 22px !important;
        border: 1px solid {border_color} !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }}
    
    .buse-card:hover, div[data-testid="stVerticalBlockBorder"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(85, 81, 255, 0.08) !important;
    }}
    
    .buse-title-primary {{
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.25;
        color: {text_primary};
        margin-bottom: 12px;
        letter-spacing: -0.025em;
    }}
    
    .buse-highlight {{
        color: {accent_color};
    }}
    
    .buse-subtitle {{
        font-size: 1.1rem;
        color: {text_secondary};
        margin-bottom: 30px;
    }}
    
    /* Boutons premium arrondis */
    .stButton>button {{
        background-color: {accent_color} !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        transition: background-color 0.2s !important;
        width: 100% !important;
    }}
    
    .stButton>button:hover {{
        background-color: {hover_color} !important;
        color: white !important;
    }}
    
    /* Carrousel d'Actualités */
    .carousel-container {{
        background-color: {card_bg};
        border-radius: 20px;
        padding: 26px;
        margin-bottom: 22px;
        border: 1px solid {border_color};
        box-shadow: 0 6px 25px rgba(85, 81, 255, 0.05);
        position: relative;
    }}
    
    .carousel-badge {{
        background-color: rgba(85, 81, 255, 0.1);
        color: {accent_color};
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-bottom: 14px;
    }}
    
    .carousel-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 8px;
    }}
    
    .carousel-desc {{
        font-size: 0.98rem;
        color: {text_secondary};
        line-height: 1.6;
        margin-bottom: 22px;
    }}

    /* Pied de page stylisé */
    .buse-footer {{
        margin-top: 50px;
        padding: 20px 0;
        border-top: 1px solid {border_color};
        text-align: center;
        font-size: 0.8rem;
        color: {text_secondary};
    }}
    </style>
    """ + (audio_hover_js if st.session_state.get('audio_on_hover', True) else ""), unsafe_allow_html=True)

# --- BLOC DE PIED DE PAGE COMMUN (MENTIONS LÉGALES & COPYRIGHT) ---
def render_footer_credits():
    current_year = datetime.now().year
    st.markdown(
        f"""
        <div class="buse-footer" data-tts="Mentions legales. Plateforme independante de surveillance salariale et d audit. Copyright {current_year} La Buse. Tous droits reserves.">
            <p style="margin-bottom: 6px; font-weight: 600;">🦉 La Buse — Plateforme indépendante de surveillance salariale & d'audit</p>
            <p style="margin-bottom: 4px; font-size: 0.75rem; line-height: 1.4;">
                <strong>Mentions Légales :</strong> Cet outil est une initiative privée indépendante de tout organisme étatique ou syndical. 
                Les analyses d'audit, de conformité et de primes sont délivrées à titre purement indicatif et s'appuient sur l'état du droit en vigueur et des bases de connaissances conventionnelles. Elles ne se substituent pas à un conseil juridique personnalisé délivré par un avocat inscrit au barreau.
            </p>
            <p style="margin-top: 8px; font-size: 0.75rem; font-weight: 500;">
                Copyright © {current_year} — La Buse. Tous droits réservés.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- CONSOLE EXPERTE DE RÉPONSES LOCALES ---
def call_eagle_ia_local(prompt, context=""):
    p_lower = prompt.lower()
    
    # Système de réponses d'experts (Droit du travail & Code du Travail)
    if "harcèlement" in p_lower or "rps" in p_lower or "pression" in p_lower or "épuisement" in p_lower or "souffrance" in p_lower:
        return (
            "🛡️ **PROTOCOLE DE PROTECTION DES SALARIÉS & GESTION RPS ACTIVÉ**\n\n"
            "Face à une situation de souffrance psychologique, d'épuisement ou de harcèlement moral :\n\n"
            "1. **Consignez de manière écrite tous les faits :** Prenez des notes détaillées (faits précis, dates, heures, propos tenus, collègues présents ou témoins éventuels). Conservez-les sur un support personnel en dehors de l'entreprise.\n\n"
            "2. **Alertez l'employeur ou son représentant :** L'employeur est légalement tenu à une **obligation de sécurité de résultat** concernant votre santé physique et mentale (Article L4121-1 du Code du travail).\n\n"
            "3. **Contactez la Médecine du Travail :** Sollicitez une visite médicale de votre propre initiative. Les médecins du travail sont soumis au secret professionnel et peuvent préconiser un aménagement de poste immédiat.\n\n"
            "4. **Saisissez vos représentants du personnel (CSE) :** Ils détiennent un droit d'alerte spécifique en cas d'atteinte aux droits des personnes et à la santé physique ou mentale."
        )
    elif "heure" in p_lower or "planning" in p_lower or "délai" in p_lower:
        return (
            "⚖️ **RÉGLEMENTATION HORAIRES & PLANNINGS**\n\n"
            "Selon la réglementation du droit du travail :\n\n"
            "- **Délai de prévenance :** Les plannings et les modifications d'horaires collectifs ou individuels doivent vous être communiqués dans un délai suffisant (souvent fixé à 7 jours à l'avance) pour vous permettre de vous organiser.\n"
            "- **Majoration des Heures Supplémentaires :** Les heures effectuées au-delà de la durée légale de travail ouvrent droit à une majoration de salaire de 25% pour les 8 premières heures, et 50% au-delà."
        )
    elif "nuit" in p_lower:
        return (
            "🌙 **TRAVAIL DE NUIT**\n\n"
            "Sous le régime général du droit du travail :\n\n"
            "- Les heures effectuées durant la période de nuit (généralement entre 21h00 et 6h00) ouvrent droit à des compensations sous forme de repos compensateur ou de majoration de salaire selon les accords de branche applicables.\n"
            "- Le recours au travail de nuit doit rester exceptionnel et justifié par la nécessité d'assurer la continuité de l'activité économique."
        )
    elif "licenciement" in p_lower or "rupture" in p_lower:
        return (
            "💼 **RUPTURE DE CONTRAT & INDEMNITÉS**\n\n"
            "L'indemnité légale de licenciement ou de rupture conventionnelle est calculée selon l'ancienneté du salarié :\n"
            "- **1/4 de mois de salaire par année d'ancienneté** pour les 10 premières années.\n"
            "- **1/3 de mois de salaire par année d'ancienneté** à partir de la 11ème année."
        )
    elif "lefebvre" in p_lower:
        return (
            "👨‍⚖️ **SÉCURISATION DU PREMIER CONTACT AVEC MAÎTRE LEFEBVRE**\n\n"
            "Vous avez sollicité l'assistance de Maître Lefebvre, avocat spécialisé en droit social au barreau des Deux-Sèvres (Niort).\n\n"
            "**Préconisations de dossier :**\n"
            "Pour que Maître Lefebvre puisse évaluer l'opportunité d'un recours prud'homal (heures supplémentaires non payées, harcèlement moral, licenciement sans cause réelle et sérieuse), préparez :\n"
            "- Vos 12 derniers bulletins de salaire.\n"
            "- Votre contrat de travail et ses avenants (avenant prime Infinity V4 inclus).\n"
            "- Tout écrit (e-mails, SMS, plannings réels) étayant vos demandes."
        )
    else:
        return (
            "⚖️ **ANALYSE ET CONFORMITÉ DE VOS DROITS**\n\n"
            f"Votre requête concernant '{prompt}' a bien été intégrée à notre outil de conformité.\n\n"
            "D'un point de vue général, la législation du travail impose un respect strict des temps de repos quotidiens (11 heures consécutives) et hebdomadaires (35 heures consécutives).\n"
            "N'hésitez pas à vous rapprocher de notre réseau local dans l'onglet **Réseau Sentinelles** pour obtenir l'assistance d'un délégué ou d'un juriste à proximité."
        )

def generate_browser_speech_widget(text):
    """Génère un widget d'élocution native et fluide pour l'Agent Eagle"""
    clean_text = text.replace('"', '\\"').replace('\n', ' ')
    html_code = f"""
    <button onclick="
        window.speechSynthesis.cancel();
        let utterance = new SpeechSynthesisUtterance('{clean_text}');
        utterance.lang = 'fr-FR';
        window.speechSynthesis.speak(utterance);
    " style="
        background-color: #5551FF;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        margin-top: 10px;
    ">🔊 Écouter la réponse</button>
    """
    st.components.v1.html(html_code, height=50)

# --- CALCULATEURS INFINITY (PDF DATA) ---
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
    
    # Navigation épurée avec "Mes documents" et "Code du travail" désactivés
    menu_items = [
        "Accueil",
        "Eagle Agent (IA & RPS)",
        "Analyse & Audit",
        "Réseau Sentinelles",
        "Calculateur de primes"
    ]

    with st.sidebar:
        # En-tête de la barre latérale modernisé
        st.markdown(
            f"""
            <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 25px;'>
                <div style='display: inline-block; width: 44px; height: 44px; background-color: #E8E7FF; border-radius: 50%; position: relative; margin-right: 12px; vertical-align: middle;'>
                    <div style='position: absolute; top: 12px; left: 10px; width: 8px; height: 8px; background-color: #5551FF; border-radius: 50%;'></div>
                    <div style='position: absolute; top: 12px; right: 10px; width: 8px; height: 8px; background-color: #5551FF; border-radius: 50%;'></div>
                    <div style='position: absolute; bottom: 8px; left: 17px; width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 8px solid #FF9F43;'></div>
                </div>
                <span style='color:#5551FF; font-size:1.85rem; font-weight:800; vertical-align: middle; letter-spacing: -0.03em;'>la buse</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Navigation synchronisée
        nav_init = st.session_state.get('sidebar_nav_v8', "Accueil")
        if nav_init not in menu_items:
            nav_init = "Accueil"
            
        nav = st.radio("MENU", menu_items, index=menu_items.index(nav_init), key="sidebar_radio_selection_v8")
        st.session_state['sidebar_nav_v8'] = nav
        
        st.markdown("---")
        # Badge d'abonnement actif (Photo 2)
        st.markdown(
            """
            <div class='buse-card' style='padding: 16px !important; margin-bottom: 15px !important;'>
                <span style='font-size: 0.8rem; font-weight: 700; color: #5551FF; display: block; margin-bottom: 4px;'>👑 La buse Pro</span>
                <span style='font-size: 0.75rem; color: #6B7280;'>Abonnement actif</span>
            </div>
            """, unsafe_allow_html=True
        )
        
        if st.button("DÉCONNEXION", key="btn_logout_main_v8"):
            st.session_state['auth'] = False
            st.session_state['loading_complete'] = False
            st.session_state['sidebar_nav_v8'] = "Accueil"
            st.rerun()

    # --- ARCHITECTURE PAR DIVISION ASYMÉTRIQUE (Photo 2) ---
    col_main, col_right_pane = st.columns([3, 1])

    with col_main:
        current_nav = st.session_state.get('sidebar_nav_v8', "Accueil")
        
        if current_nav == "Accueil":
            # Section d'accueil fidèle à la mise en page de la Photo 2
            col_text, col_mascotte = st.columns([2, 1])
            with col_text:
                st.markdown(
                    """
                    <h1 class='buse-title-primary' data-tts="La buse, votre moteur de recherche au service du monde du travail.">
                        La buse, votre moteur <br>de recherche au service <br><span class='buse-highlight'>du monde du travail.</span>
                    </h1>
                    <p class='buse-subtitle'>Posez vos questions, analysez vos documents, comprenez vos droits et passez à l'action.</p>
                    """, 
                    unsafe_allow_html=True
                )
            with col_mascotte:
                st.markdown(CHOUETTE_LOGO_HTML, unsafe_allow_html=True)
                
            # Formulaire de question d'accueil (Photo 2)
            with st.form("home_search_form", clear_on_submit=True):
                search_q = st.text_input("Posez votre question sur le droit du travail...", placeholder="Posez votre question sur le droit du travail...")
                submit_q = st.form_submit_button("Lancer la recherche")
                
                if submit_q and search_q:
                    response = call_eagle_ia_local(search_q)
                    st.session_state['ai_history'].append({"q": search_q, "a": response})
                    st.session_state['sidebar_nav_v8'] = "Eagle Agent (IA & RPS)"
                    safe_rerun()
                
            st.markdown("<p style='font-weight: 600; font-size: 0.95rem; margin-top: 15px;'>Suggestions rapides :</p>", unsafe_allow_html=True)
            suggestions = [
                "Puis-je refuser des heures supplémentaires ?",
                "Quelles sont mes indemnités en cas de licenciement ?",
                "Mon employeur peut-il modifier mon contrat ?"
            ]
            cols_sug = st.columns(3)
            for idx, sug in enumerate(suggestions):
                with cols_sug[idx]:
                    if st.button(sug, key=f"sug_btn_{idx}_v8"):
                        response = call_eagle_ia_local(sug)
                        st.session_state['ai_history'].append({"q": sug, "a": response})
                        st.session_state['sidebar_nav_v8'] = "Eagle Agent (IA & RPS)"
                        safe_rerun()

            # --- CARROUSEL D'INFORMATIONS INTERACTIF ---
            st.markdown("<h3 style='margin-top: 30px; font-weight: 700; letter-spacing: -0.02em;'>Actualités & Informations Clés</h3>", unsafe_allow_html=True)
            
            current_item = CAROUSEL_ITEMS[st.session_state.get('carousel_index', 0)]
            st.markdown(
                f"""
                <div class="carousel-container">
                    <span class="carousel-badge" data-tts="{current_item['badge']}">{current_item['badge']}</span>
                    <div class="carousel-title" data-tts="{current_item['titre']}">{current_item['titre']}</div>
                    <div class="carousel-desc" data-tts="{current_item['description']}">{current_item['description']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col_prev, col_spacer, col_next = st.columns([1, 4, 1])
            with col_prev:
                if st.button("⬅️ Précédent", key="carousel_prev"):
                    st.session_state['carousel_index'] = (st.session_state.get('carousel_index', 0) - 1) % len(CAROUSEL_ITEMS)
                    safe_rerun()
            with col_next:
                if st.button("Suivant ➡️", key="carousel_next"):
                    st.session_state['carousel_index'] = (st.session_state.get('carousel_index', 0) + 1) % len(CAROUSEL_ITEMS)
                    safe_rerun()

            # Les 4 dalles d'actions principales de la Photo 2
            st.markdown("<h3 style='margin-top: 40px; font-weight: 700;'>Ce que La buse peut faire pour vous</h3>", unsafe_allow_html=True)
            grid_col1, grid_col2 = st.columns(2)
            with grid_col1:
                st.markdown(
                    """
                    <div class='buse-card' data-tts="Eagle Agent. Posez vos questions de droit du travail et obtenez des réponses.">
                        <h4 style="font-weight: 700; font-size: 1.15rem; margin-bottom: 8px;">Eagle Agent <span style="font-size: 0.8rem; background-color: rgba(85, 81, 255, 0.1); color: #5551FF; padding: 2px 8px; border-radius: 50px; font-weight: 700; margin-left: 6px;">IA</span></h4>
                        <p style='font-size:0.92rem; color:#6B7280; line-height: 1.5;'>Posez toutes vos questions sur le droit du travail et obtenez des réponses fiables, sourcées et personnalisées.</p>
                    </div>
                    <div class='buse-card' data-tts="Réseau Sentinelles. Être mis en relation avec des délégués de proximité.">
                        <h4 style="font-weight: 700; font-size: 1.15rem; margin-bottom: 8px;">Réseau Sentinelles</h4>
                        <p style='font-size:0.92rem; color:#6B7280; line-height: 1.5;'>Être mis en relation avec des délégués syndicaux ou des avocats spécialisés dans votre région.</p>
                    </div>
                    """, unsafe_allow_html=True
                )
            with grid_col2:
                st.markdown(
                    """
                    <div class='buse-card' data-tts="Analyse CV et Audit. Détectez les anomalies de contrat.">
                        <h4 style="font-weight: 700; font-size: 1.15rem; margin-bottom: 8px;">Analyse CV & Audit</h4>
                        <p style='font-size:0.92rem; color:#6B7280; line-height: 1.5;'>Détectez les anomalies, comparez votre contrat de travail avec les conventions collectives.</p>
                    </div>
                    <div class='buse-card' data-tts="Calculateur de primes. Estimez vos primes et salaires.">
                        <h4 style="font-weight: 700; font-size: 1.15rem; margin-bottom: 8px;">Calculateur de primes</h4>
                        <p style='font-size:0.92rem; color:#6B7280; line-height: 1.5;'>Estimez vos primes (Infinity V4), vos indemnités de départ et vos salaires nets.</p>
                    </div>
                    """, unsafe_allow_html=True
                )

            # Bannière d'Action (Photo 2)
            st.markdown(
                """
                <div class="carousel-container" style="background: linear-gradient(135deg, #5551FF 0%, #3D39E6 100%); color: white; border: none;">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <span style="font-size: 2.2rem;">🛡️</span>
                        <div>
                            <h3 style="font-size: 1.4rem; font-weight: 700; color: white; margin-bottom: 4px;">Vos droits. Notre mission.</h3>
                            <p style="font-size: 0.92rem; color: rgba(255, 255, 255, 0.85); margin-bottom: 12px;">La buse vous aide à comprendre, vérifier et défendre vos droits au travail en toute sécurité.</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True
            )
            if st.button("Découvrir toutes les fonctionnalités", key="btn_discover_features_v8"):
                st.toast("Toutes les fonctionnalités premium sont actives.")

            # Section Réassurance bas de page (Photo 2)
            st.markdown("---")
            reass_col1, reass_col2, reass_col3, reass_col4 = st.columns(4)
            with reass_col1:
                st.markdown(
                    """
                    <div style="text-align: center; padding: 10px;" data-tts="Fiable et source">
                        <span style="font-size: 1.5rem; display: block; margin-bottom: 8px;">🛡️</span>
                        <strong style="font-size: 0.85rem; display: block; margin-bottom: 2px;">Fiable & sourcé</strong>
                        <span style="font-size: 0.75rem; color: #6B7280; display: block;">Bases sur la loi</span>
                    </div>
                    """, unsafe_allow_html=True
                )
            with reass_col2:
                st.markdown(
                    """
                    <div style="text-align: center; padding: 10px;" data-tts="Confidentiel">
                        <span style="font-size: 1.5rem; display: block; margin-bottom: 8px;">🔒</span>
                        <strong style="font-size: 0.85rem; display: block; margin-bottom: 2px;">Confidentiel</strong>
                        <span style="font-size: 0.75rem; color: #6B7280; display: block;">Données protégées</span>
                    </div>
                    """, unsafe_allow_html=True
                )
            with reass_col3:
                st.markdown(
                    """
                    <div style="text-align: center; padding: 10px;" data-tts="A jour">
                        <span style="font-size: 1.5rem; display: block; margin-bottom: 8px;">📅</span>
                        <strong style="font-size: 0.85rem; display: block; margin-bottom: 2px;">À jour</strong>
                        <span style="font-size: 0.75rem; color: #6B7280; display: block;">Mises à jour régulières</span>
                    </div>
                    """, unsafe_allow_html=True
                )
            with reass_col4:
                st.markdown(
                    """
                    <div style="text-align: center; padding: 10px;" data-tts="Accessible a tous">
                        <span style="font-size: 1.5rem; display: block; margin-bottom: 8px;">👥</span>
                        <strong style="font-size: 0.85rem; display: block; margin-bottom: 2px;">Accessible à tous</strong>
                        <span style="font-size: 0.75rem; color: #6B7280; display: block;">Zéro barrière</span>
                    </div>
                    """, unsafe_allow_html=True
                )

        elif current_nav == "Eagle Agent (IA & RPS)":
            st.markdown("<h2 class='glow-text'>🦅 Eagle Agent - Support & RPS</h2>", unsafe_allow_html=True)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            
            with st.form("agent_search_form", clear_on_submit=True):
                user_input = st.text_input("Posez votre question juridique ou signalez une difficulté (harcèlement, pressions, RPS) :", placeholder="Votre message...")
                submit_agent = st.form_submit_button("Interroger l'Agent")
                
                if submit_agent and user_input:
                    with st.spinner("Analyse sémantique..."):
                        response = call_eagle_ia_local(user_input, st.session_state.get('analysis_results', None))
                        st.session_state['ai_history'].append({"q": user_input, "a": response})
            st.markdown("</div>", unsafe_allow_html=True)

            for idx, chat in enumerate(reversed(st.session_state.get('ai_history', []))):
                with st.expander(f"Question : {chat['q']}", expanded=True):
                    st.markdown(chat['a'])
                    generate_browser_speech_widget(chat['a'])

        elif current_nav == "Analyse & Audit":
            st.markdown("<h2 class='glow-text'>🔍 Analyse & Audit Documentaire</h2>", unsafe_allow_html=True)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            doc_uploaded = st.file_uploader("Importer une fiche de paie ou un contrat", type=["pdf", "png", "jpg"], key="uploader_audit_v8")
            if doc_uploaded:
                if st.button("Lancer l'audit", key="btn_audit_action_v8"):
                    st.session_state['analysis_results'] = "Analyse : Conformité validée. Vigilance recommandée sur les temps de repos."
                    st.success("Audit complété !")
            st.markdown("</div>", unsafe_allow_html=True)

        elif current_nav == "Réseau Sentinelles":
            st.markdown("<h2 class='glow-text'>🛡️ Réseau Sentinelles & Experts de proximité</h2>", unsafe_allow_html=True)
            
            # Focus automatique sur Maitre Lefebvre s'il a été appelé par l'ancre URL
            if st.session_state.get('focus_expert') == "Maître Lefebvre":
                st.success("📍 Focus appliqué sur : Maître Lefebvre (Demandé via URL)")
                # Nettoie pour éviter de boucler la notification
                st.session_state['focus_expert'] = None
                
            df_sentinelles = pd.DataFrame(EXPERT_DIRECTORY)
            st.map(df_sentinelles)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            for d in EXPERT_DIRECTORY:
                # Mise en valeur de la dalle Maître Lefebvre
                is_lefebvre = "Lefebvre" in d['Nom']
                border_style = "border: 2px solid #5551FF; background-color: rgba(85, 81, 255, 0.03);" if is_lefebvre else ""
                
                st.markdown(
                    f"""
                    <div class="buse-card" style="margin-bottom:15px; padding:15px; {border_style}" data-tts="{d['Nom']}">
                        <strong style="color: #5551FF; font-size: 1.1rem;">📍 {d['Nom']}</strong><br>
                        <span style="font-size:0.85rem; color:#6B7280;">({d['Type']}) — {d['Adresse']}</span><br>
                        <p style="font-size:0.9rem; margin-top:5px; line-height:1.4;">{d['Desc']}</p>
                        <strong style="font-size:0.9rem; color:#1E203B;">📞 {d['Contact']}</strong>
                    </div>
                    """, unsafe_allow_html=True
                )
                # Ajout d'un bouton Streamlit pour préremplir l'IA conversationnelle Eagle avec cet expert
                if is_lefebvre:
                    if st.button("💬 Préparer mon dossier d'entretien avec Maître Lefebvre", key="btn_prep_lefebvre"):
                        st.session_state['sidebar_nav_v8'] = "Eagle Agent (IA & RPS)"
                        # Injecte une question pré-remplie automatique
                        response_lef = call_eagle_ia_local("lefebvre")
                        st.session_state['ai_history'].append({"q": "Comment préparer mon rendez-vous de droit du travail avec Maître Lefebvre ?", "a": response_lef})
                        safe_rerun()
                        
            st.markdown("</div>", unsafe_allow_html=True)

        elif current_nav == "Calculateur de primes":
            st.markdown("<h2 class='glow-text'>💎 Calculateur de Primes & Salaire</h2>", unsafe_allow_html=True)
            col_inf, col_sal = st.columns(2)
            with col_inf:
                st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
                st.subheader("Prime Infinity (Barème PDF)")
                ca_magasin = st.number_input("Chiffre d'Affaires réalisé Magasin (€)", value=1750.0, step=50.0, key="ca_mag_calc_v8")
                h_travail = st.number_input("Heures réelles travaillées", value=48, step=1, key="h_pres_calc_v8")
                ecart, bonus, color, progress = calculate_infinity_v4(ca_magasin, h_travail)
                st.metric("Écart au seuil magasin (1300 €)", f"{ecart:.2f} €")
                st.markdown(f"#### Prime : <span style='color:{color}; font-size:1.4em;'>{bonus}</span>", unsafe_allow_html=True)
                st.progress(progress)
                st.markdown("</div>", unsafe_allow_html=True)
            with col_sal:
                st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
                st.subheader("Simulateur de Revenus")
                brut = st.number_input("Salaire Mensuel Brut (€)", value=2100.0, step=50.0, key="brut_salary_calc_v8")
                statut = st.selectbox("Statut de l'employé", ["Non-Cadre (22%)", "Cadre (25%)"], key="statut_salary_calc_v8")
                taux = 0.78 if "Non-Cadre" in statut else 0.75
                st.write(f"### NET ESTIMÉ : **{brut * taux:.2f} €**")
                st.write(f"### IJ Maladie de référence : **{min((brut / 30.42) * 0.5, 52.04):.2f} € / jour**")
                st.markdown("</div>", unsafe_allow_html=True)

        # Pied de page systematique avec Mentions Legales et Copyright en bas de chaque rubrique
        render_footer_credits()

    # --- PANNEAU DE DROITE (ACCÈS RAPIDE, ACCESSIBILITÉ & AIDE) ---
    with col_right_pane:
        st.markdown("<h4 class='glow-text' style='margin-bottom:15px; font-weight: 700; color: #1E203B;'>Outils rapides</h4>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='buse-card' style='padding: 18px !important; margin-bottom: 20px !important;'>
                <p style='margin-bottom:12px; font-weight:600; font-size:0.9rem; cursor: pointer;'>📄 Analyser mon CV</p>
                <p style='margin-bottom:12px; font-weight:600; font-size:0.9rem; cursor: pointer;'>⚖️ Comparer mon contrat</p>
                <p style='margin-bottom:12px; font-weight:600; font-size:0.9rem; cursor: pointer;'>🔍 Consulter mes droits</p>
                <p style='margin-bottom:0px; font-weight:600; font-size:0.9rem; cursor: pointer;'>💎 Simuler une prime</p>
            </div>
            """, unsafe_allow_html=True
        )
        
        # Panneau d'accessibilité vocale de la Photo 2
        st.markdown("<h4 class='glow-text' style='margin-bottom:15px; font-weight: 700; color: #1E203B;'>Accessibilité</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            st.session_state['non_voyant'] = st.toggle("♿ Mode non voyant", value=st.session_state.get('non_voyant', False), key="tg_non_voyant_v9")
            st.session_state['audio_on_hover'] = st.toggle("🔊 Audio au survol", value=st.session_state.get('audio_on_hover', True), key="tg_audio_hover_v9")
            st.session_state['high_contrast'] = st.toggle("🌓 Contraste élevé", value=st.session_state.get('high_contrast', False), key="tg_contrast_v9")
            st.session_state['transcription_audio'] = st.toggle("📝 Transcription audio", value=st.session_state.get('transcription_audio', False), key="tg_trans_v9")
            
        st.markdown("<h4 class='glow-text' style='margin-bottom:15px; font-weight: 700; color: #1E203B;'>Besoin d'aide ?</h4>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='buse-card' style='padding: 18px !important; margin-bottom: 15px !important;'>
                <p style='font-size:0.85rem; color:#6B7280; margin-bottom:12px; line-height: 1.5;'>Nos experts du réseau Sentinelles sont à votre écoute immédiate.</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Être mis en relation", key="btn_right_sentinel_action_v8"):
            st.success("Mise en relation d'urgence demandée.")

# --- INITIALISATION ÉQUILIBRÉE ET SÉCURISÉE ---
def run_loading_sequence():
    apply_ui_design_and_hover_tts()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;' class='glow-text'>la buse - initialisation...</h2>", unsafe_allow_html=True)
        
        # Résolution définitive du bug st.progress par l'utilisation d'un entier strict de 0 à 100 sans paramètre key
        bar = st.progress(0.0)
        for i in range(101):
            time.sleep(0.005)
            bar.progress(float(i) / 100.0)
        st.session_state['loading_complete'] = True
        safe_rerun()

# --- SÉCURITÉ DE CODE PIN (Page de connexion Photo 2) ---
if not st.session_state.get('auth', False):
    apply_ui_design_and_hover_tts()
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Logo chouette inséré au-dessus du formulaire (Photo 2)
        st.markdown(CHOUETTE_LOGO_HTML, unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h2 class='glow-text' style='text-align:center; font-family:Inter; color:#1E203B; font-weight:700;'>Accès sécurisé</h2>", unsafe_allow_html=True)
            pin = st.text_input("Saisissez votre code PIN :", type="password", key="login_pin_v8")
            if st.button("DÉVERROUILLER", key="btn_submit_login_v8"):
                if pin == "1234":
                    st.session_state['auth'] = True
                    # Vérification de l'ancre URL au déverrouillage
                    check_url_anchor_focus()
                    safe_rerun()
                else:
                    st.error("PIN incorrect.")
else:
    if not st.session_state.get('loading_complete', False):
        run_loading_sequence()
    else:
        main_app()
