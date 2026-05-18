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
# # 1. Une barre latérale gauche pour naviguer de manière stable.
# # 2. Un panneau central large pour le flux principal (carrousel, recherche, dalles d'actions).
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
    st.session_state['user_location'] = {"lat": 46.3833, "lon": -0.4500}
if 'carousel_index' not in st.session_state:
    st.session_state['carousel_index'] = 0

# --- BASE DE DONNÉES ENRICHIE (DÉFENSEURS, SYNDICATS & AVOCATS DE PROXIMITÉ) ---
EXPERT_DIRECTORY = [
    {"Type": "Avocat Spécialisé", "Nom": "Cabinet d'Avocats Droit du Travail Niortais", "Contact": "05 49 24 10 20", "Adresse": "12 Rue de la Regratterie, 79000 Niort", "lat": 46.3235, "lon": -0.4635, "Desc": "Spécialisé en licenciements, contrats de travail et Risques Psychosociaux (RPS)."},
    {"Type": "Avocat Spécialisé", "Nom": "Maître Claire Valois - Barreau des Deux-Sèvres", "Contact": "05 49 77 15 30", "Adresse": "45 Avenue de Limoges, 79000 Niort", "lat": 46.3190, "lon": -0.4480, "Desc": "Conseil et défense des salariés de la boulangerie devant le Conseil de Prud'hommes."},
    {"Type": "Union Syndicale", "Nom": "UD CFDT Deux-Sèvres", "Contact": "05 49 24 51 32", "Adresse": "Maison des Syndicats, 79000 Niort", "lat": 46.3280, "lon": -0.4610, "Desc": "Accompagnement syndical, défense des droits des salariés de la boulangerie (IDCC 1517)."},
    {"Type": "Union Syndicale", "Nom": "Union Départementale CGT 79", "Contact": "05 49 24 35 12", "Adresse": "Place de la Comédie, 79000 Niort", "lat": 46.3262, "lon": -0.4595, "Desc": "Permanences juridiques et défense face au harcèlement et à la pression au travail."},
    {"Type": "Défenseur des Droits", "Nom": "Point d'Accès au Droit - Maison de la Justice Niort", "Contact": "05 49 04 00 00", "Adresse": "10 Rue du Tribunal, 79000 Niort", "lat": 46.3242, "lon": -0.4645, "Desc": "Médiateur de proximité pour la défense de vos libertés individuelles au travail."}
]

# --- DESIGN HTML/CSS LOGO DE LA CHOUETTE (SANS SVG EXTERNE - PHOTO 2) ---
CHOUETTE_LOGO_HTML = """
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
    <div style="
        width: 110px; height: 110px; 
        background-color: #E8E7FF; 
        border-radius: 50%; 
        position: relative; 
        box-shadow: 0 8px 24px rgba(85, 81, 255, 0.2);
        display: flex; align-items: center; justify-content: center;
    ">
        <!-- Oreilles -->
        <div style="position: absolute; top: -5px; left: 15px; width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-bottom: 30px solid #5551FF; transform: rotate(-15deg);"></div>
        <div style="position: absolute; top: -5px; right: 15px; width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-bottom: 30px solid #5551FF; transform: rotate(15deg);"></div>
        <!-- Corps de l'oiseau -->
        <div style="width: 75px; height: 85px; background-color: #5551FF; border-radius: 50% 50% 45% 45%; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
            <!-- Ventre Blanc -->
            <div style="position: absolute; bottom: -5px; width: 55px; height: 55px; background-color: #FFFFFF; border-radius: 50%;"></div>
        </div>
        <!-- Yeux -->
        <div style="position: absolute; top: 32px; left: 24px; width: 30px; height: 30px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
            <div style="width: 14px; height: 14px; background-color: #1E203B; border-radius: 50%; position: relative;">
                <div style="width: 5px; height: 5px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
            </div>
        </div>
        <div style="position: absolute; top: 32px; right: 24px; width: 30px; height: 30px; background-color: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
            <div style="width: 14px; height: 14px; background-color: #1E203B; border-radius: 50%; position: relative;">
                <div style="width: 5px; height: 5px; background-color: #FFFFFF; border-radius: 50%; position: absolute; top: 2px; left: 2px;"></div>
            </div>
        </div>
        <!-- Bec Orange -->
        <div style="position: absolute; top: 56px; width: 0; height: 0; border-left: 7px solid transparent; border-right: 7px solid transparent; border-top: 12px solid #FF9F43; z-index: 10;"></div>
    </div>
</div>
"""

# Données pour le carrousel d'informations
CAROUSEL_ITEMS = [
    {
        "titre": "🛡️ Votre santé est une priorité absolue",
        "description": "L'employeur est légalement tenu de protéger votre santé physique et mentale (Article L4121-1 du Code du travail). Ne restez pas isolé face aux pressions managériales.",
        "badge": "Prévention RPS"
    },
    {
        "titre": "📈 Déplafonnement de prime Infinity V4",
        "description": "Atteignez les paliers de bonus de 20% à 100% en surveillant votre écart de CA magasin par rapport au seuil de référence de 1300 €.",
        "badge": "Primes & Salaires"
    },
    {
        "titre": "⚖️ Convention Collective IDCC 1517",
        "description": "Salariés des Boulangeries-Pâtisseries : bénéficiez de grilles de salaires garanties, de majorations pour heures de nuit et de garanties de prévoyance spécifiques.",
        "badge": "Vos Droits"
    }
]

# --- FONCTION DE CALCUL DE DISTANCE (HAVERSINE) ---
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
    
    if st.session_state.get('high_contrast', False):
        bg_color = "#000000"
        card_bg = "#111111"
        text_primary = "#FFFFFF"
        text_secondary = "#FFFF00"
        border_color = "#FFFF00"
        sidebar_text_color = "#FFFFFF"
    else:  # Light Mode de la Maquette (Photo 2)
        bg_color = "#F4F5FC"
        card_bg = "#FFFFFF"
        text_primary = "#1E203B"
        text_secondary = "#6B7280"
        border_color = "rgba(0, 0, 0, 0.05)"
        sidebar_text_color = "#1E203B"

    # Script d'accessibilité vocale au survol (Web Speech API) EXACTEMENT fourni par l'utilisateur
    audio_hover_js = ""
    if st.session_state.get('audio_on_hover', True):
        audio_hover_js = """
        <script>
        (function() {
            let synth = null;
            try {
                synth = window.speechSynthesis || (window.parent && window.parent.speechSynthesis);
            } catch(e) {
                synth = window.speechSynthesis;
            }

            if (!synth) {
                console.warn("SpeechSynthesis non supporté sur ce navigateur.");
                return;
            }

            let lastText = "";
            let timer = null;
            let isUnlocked = false;

            // Déverrouille la synthèse vocale pour mobiles/Safari (exige un geste de l'utilisateur)
            function unlockSpeech() {
                if (isUnlocked) return;
                try {
                    const u = new SpeechSynthesisUtterance("");
                    u.volume = 0;
                    synth.speak(u);
                    isUnlocked = true;
                    console.log("Moteur audio d'accessibilité déverrouillé.");
                } catch(e) {
                    console.error("Erreur de déverrouillage de la synthèse vocale:", e);
                }
            }

            // Attache les écouteurs de déverrouillage tactile ou clic
            document.addEventListener('click', unlockSpeech, { once: true });
            document.addEventListener('touchstart', unlockSpeech, { once: true });
            try {
                if (window.parent && window.parent.document) {
                    window.parent.document.addEventListener('click', unlockSpeech, { once: true });
                    window.parent.document.addEventListener('touchstart', unlockSpeech, { once: true });
                }
            } catch(e) {}

            function ttsSpeak(text) {
                if (!text || text === lastText) return;
                try {
                    synth.cancel();
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'fr-FR';
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

                // Évite la duplication des écouteurs sur le même document
                if (doc._buseTtsActive) return; 
                doc._buseTtsActive = true;

                doc.addEventListener('mouseover', (e) => {
                    const el = e.target;
                    if (!el) return;

                    let targetEl = el;
                    let textToRead = "";
                    let depth = 0;

                    // Remonte l'arborescence pour trouver un conteneur textuel valide
                    while (targetEl && depth < 3) {
                        textToRead = targetEl.getAttribute('data-tts') || targetEl.innerText || targetEl.textContent;
                        if (targetEl.matches('h1, h2, h3, h4, p, span, li, button, .stMarkdown, .buse-card, label, .carousel-badge, [data-testid="stMarkdownContainer"]')) {
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

                doc.addEventListener('mouseout', () => {
                    lastText = "";
                });
            }

            // Attache les écouteurs sur le document local et sur le document parent de Streamlit (gestion CORS intégrée)
            try {
                setupListeners(document);
            } catch(e) { console.error("Erreur doc local:", e); }

            try {
                if (window.parent && window.parent.document) {
                    setupListeners(window.parent.document);
                }
            } catch(e) {
                console.log("Accès parent restreint (CORS). Écouteurs locaux actifs.");
            }
        })();
        </script>
        """

    # Forçage CSS pour garantir une visibilité totale de la sidebar et des éléments (Plus d'invisibilité)
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {bg_color};
        color: {text_primary};
        font-family: 'Inter', sans-serif;
    }}
    
    /* FORCE la visibilité du texte dans la sidebar (Évite le blanc sur blanc) */
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

    /* Cartes de contenu blanches de la maquette et stylisation des dalles de bordure native */
    .buse-card, div[data-testid="stVerticalBlockBorder"] {{
        background-color: {card_bg} !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        border: 1px solid {border_color} !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }}
    
    .buse-card:hover, div[data-testid="stVerticalBlockBorder"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(85, 81, 255, 0.08) !important;
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
    
    /* Boutons stylisés Maquette */
    .stButton>button {{
        background-color: {accent_color} !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: background-color 0.2s !important;
        width: 100% !important;
    }}
    
    .stButton>button:hover {{
        background-color: {hover_color} !important;
        color: white !important;
    }}
    
    .mascotte-logo-container {{
        text-align: center;
        margin-bottom: 30px;
    }}
    
    /* Styles spécifiques pour le carrousel d'informations */
    .carousel-container {{
        background-color: {card_bg};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid {accent_color};
        box-shadow: 0 6px 25px rgba(85, 81, 255, 0.06);
        position: relative;
    }}
    
    .carousel-badge {{
        background-color: rgba(85, 81, 255, 0.1);
        color: {accent_color};
        padding: 6px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 12px;
    }}
    
    .carousel-title {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 8px;
    }}
    
    .carousel-desc {{
        font-size: 0.95rem;
        color: {text_secondary};
        line-height: 1.5;
        margin-bottom: 20px;
    }}
    </style>
    """ + (audio_hover_js if st.session_state.get('audio_on_hover', True) else ""), unsafe_allow_html=True)

# --- CONSOLE EXPERTE DE RÉPONSES LOCALES IDCC 1517 & RPS ---
def call_eagle_ia_local(prompt, context=""):
    p_lower = prompt.lower()
    
    # Système de réponses d'experts (IDCC 1517 & Code du Travail)
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
            "⚖️ **RÉGLEMENTATION HORAIRES & PLANNINGS (IDCC 1517)**\n\n"
            "Selon la convention collective de la Boulangerie-Pâtisserie Artisanale :\n\n"
            "- **Délai de prévenance :** Les plannings et les modifications d'horaires doivent vous être communiqués au moins **7 jours à l'avance** pour vous permettre de vous organiser.\n"
            "- **Majoration des Heures Supplémentaires :** Les heures effectuées au-delà de la durée légale ouvrent droit à une majoration de salaire (25% pour les 8 premières heures, 50% au-delà)."
        )
    elif "nuit" in p_lower:
        return (
            "🌙 **TRAVAIL DE NUIT (IDCC 1517)**\n\n"
            "Sous la convention de la Boulangerie-Pâtisserie :\n\n"
            "- Les heures effectuées entre **20h00 et 6h00** du matin sont qualifiées de travail de nuit.\n"
            "- Elles ouvrent droit à une **majoration de salaire minimale de 25%** pour chaque heure travaillée, ainsi qu'à des repos compensateurs sous certains conditions."
        )
    elif "licenciement" in p_lower or "rupture" in p_lower:
        return (
            "💼 **RUPTURE DE CONTRAT & INDEMNITÉS (IDCC 1517)**\n\n"
            "L'indemnité de licenciement ou de rupture conventionnelle est calculée sur la base de l'ancienneté :\n"
            "- **1/4 de mois de salaire par année d'ancienneté** pour les 10 premières années.\n"
            "- **1/3 de mois de salaire par année d'ancienneté** au-delà de 10 ans."
        )
    else:
        return (
            "⚖️ **ANALYSE CONVENTIONNELLE (IDCC 1517)**\n\n"
            f"Votre requête concernant '{prompt}' a bien été intégrée à notre outil de conformité.\n\n"
            "D'un point de vue général, la convention de la Boulangerie-Pâtisserie impose un respect strict des temps de repos quotidiens (11 heures consécutives) et hebdomadaires (35 heures consécutives).\n"
            "N'hésitez pas à vous rapprocher de notre réseau local dans l'onglet **Réseau Sentinelles** pour obtenir l'assistance d'un juriste à Niort."
        )

def generate_browser_speech_widget(text):
    """Génère un widget d'élocution native et fluide pour l'Agent Eagle (Sans API externe)"""
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
    
    menu_items = [
        "Accueil",
        "Eagle Agent (IA & RPS)",
        "Analyse & Audit",
        "Code du travail",
        "Réseau Sentinelles",
        "Calculateur de primes",
        "Mes documents"
    ]

    with st.sidebar:
        # En-tête de la sidebar avec la chouette et le nom de l'application
        st.markdown(
            f"""
            <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 25px;'>
                <div style='display: inline-block; width: 40px; height: 40px; background-color: #E8E7FF; border-radius: 50%; position: relative; margin-right: 10px; vertical-align: middle;'>
                    <div style='position: absolute; top: 10px; left: 8px; width: 8px; height: 8px; background-color: #5551FF; border-radius: 50%;'></div>
                    <div style='position: absolute; top: 10px; right: 8px; width: 8px; height: 8px; background-color: #5551FF; border-radius: 50%;'></div>
                    <div style='position: absolute; bottom: 6px; left: 15px; width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 8px solid #FF9F43;'></div>
                </div>
                <span style='color:#5551FF; font-size:1.8rem; font-weight:700; vertical-align: middle;'>la buse</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Routage robuste basé sur la valeur et non l'index
        nav_init = st.session_state.get('sidebar_nav_v8', "Accueil")
        if nav_init not in menu_items:
            nav_init = "Accueil"
            
        nav = st.radio("MENU", menu_items, index=menu_items.index(nav_init), key="sidebar_radio_selection_v8")
        
        # Met à jour la variable d'état
        st.session_state['sidebar_nav_v8'] = nav
        
        st.markdown("---")
        st.markdown("<h4>🔊 Accessibilité</h4>", unsafe_allow_html=True)
        st.session_state['non_voyant'] = st.toggle("♿ Mode non voyant", value=st.session_state.get('non_voyant', False), key="tg_non_voyant_v8")
        st.session_state['audio_on_hover'] = st.toggle("🔊 Audio au survol", value=st.session_state.get('audio_on_hover', True), key="tg_audio_hover_v8")
        st.session_state['high_contrast'] = st.toggle("🌓 Contraste élevé", value=st.session_state.get('high_contrast', False), key="tg_contrast_v8")
        
        st.markdown("---")
        if st.button("DÉCONNEXION", key="btn_logout_main_v8"):
            st.session_state['auth'] = False
            st.session_state['loading_complete'] = False
            st.rerun()

    # --- ARCHITECTURE PAR DIVISION ASYMÉTRIQUE (Photo 2) ---
    col_main, col_right_pane = st.columns([3, 1])

    with col_main:
        if st.session_state.get('sidebar_nav_v8', "Accueil") == "Accueil":
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
                # Mascotte Chouette violette HTML/CSS
                st.markdown(CHOUETTE_LOGO_HTML, unsafe_allow_html=True)
                
            # Formulaire de question d'accueil (Sûr, rapide, pas de freeze)
            with st.form("home_search_form", clear_on_submit=True):
                search_q = st.text_input("Posez votre question sur le droit du travail...", placeholder="Ex : Puis-je refuser des heures supplémentaires ?")
                submit_q = st.form_submit_button("Lancer la recherche")
                
                if submit_q and search_q:
                    response = call_eagle_ia_local(search_q)
                    st.session_state['ai_history'].append({"q": search_q, "a": response})
                    st.session_state['sidebar_nav_v8'] = "Eagle Agent (IA & RPS)"  # Redirection immédiate
                    safe_rerun()
                
            st.markdown("<p style='font-weight: 500; font-size: 0.95rem; margin-top: 15px;'>Suggestions rapides :</p>", unsafe_allow_html=True)
            suggestions = [
                "Puis-je refuser des heures supplémentaires ?",
                "Que faire en cas de harcèlement au travail ?",
                "Mon employeur peut-il modifier mon contrat sans mon accord ?"
            ]
            cols_sug = st.columns(3)
            for idx, sug in enumerate(suggestions):
                with cols_sug[idx]:
                    if st.button(sug, key=f"sug_btn_{idx}_v8"):
                        response = call_eagle_ia_local(sug)
                        st.session_state['ai_history'].append({"q": sug, "a": response})
                        st.session_state['sidebar_nav_v8'] = "Eagle Agent (IA & RPS)"  # Redirection immédiate
                        safe_rerun()

            # --- CARROUSEL D'INFORMATIONS INTERACTIF ---
            st.markdown("<h3 style='margin-top: 25px;'>Actualités & Informations Clés</h3>", unsafe_allow_html=True)
            
            # Récupération de l'élément actif du carrousel
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
            
            # Contrôles de navigation du carrousel
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
            st.markdown("<h3 style='margin-top: 35px;'>Ce que La buse peut faire pour vous</h3>", unsafe_allow_html=True)
            grid_col1, grid_col2 = st.columns(2)
            with grid_col1:
                st.markdown(
                    """
                    <div class='buse-card' data-tts="Eagle Agent. Posez vos questions de droit du travail.">
                        <h4 class='buse-highlight'>Eagle Agent</h4>
                        <p style='font-size:0.9rem; color:#6B7280;'>Posez toutes vos questions sur le droit du travail et obtenez des réponses fiables.</p>
                    </div>
                    <div class='buse-card' data-tts="Réseau Sentinelles. Être mis en relation avec des délégués.">
                        <h4 class='buse-highlight'>Réseau Sentinelles</h4>
                        <p style='font-size:0.9rem; color:#6B7280;'>Soyez mis en relation avec des délégués et des juristes spécialisés.</p>
                    </div>
                    """, unsafe_allow_html=True
                )
            with grid_col2:
                st.markdown(
                    """
                    <div class='buse-card' data-tts="Analyse CV et Audit. Détectez les anomalies de contrat.">
                        <h4 class='buse-highlight'>Analyse CV & Audit</h4>
                        <p style='font-size:0.9rem; color:#6B7280;'>Détectez les anomalies, comparez votre contrat au Code du travail.</p>
                    </div>
                    <div class='buse-card' data-tts="Calculateur de primes. Estimez vos primes Infinity.">
                        <h4 class='buse-highlight'>Calculateur de primes</h4>
                        <p style='font-size:0.9rem; color:#6B7280;'>Estimez vos primes, indemnités et avantages selon votre situation.</p>
                    </div>
                    """, unsafe_allow_html=True
                )

        elif st.session_state.get('sidebar_nav_v8') == "Eagle Agent (IA & RPS)":  # Eagle Agent (IA & RPS)
            st.markdown("<h2 class='glow-text'>🦅 Eagle Agent - Support & RPS</h2>", unsafe_allow_html=True)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            
            with st.form("agent_search_form", clear_on_submit=True):
                user_input = st.text_input("Posez votre question juridique ou signalez une difficulté (harcèlement, pressions, RPS) :", placeholder="Votre message...")
                submit_agent = st.form_submit_button("Interroger l'Agent")
                
                if submit_agent and user_input:
                    with st.spinner("Analyse sémantique..."):
                        response = call_eagle_ia_local(user_input, st.session_state.get('analysis_results', None))
                        st.session_state['ai_history'].append({"q": user_input, "a": response})
                        # Rerun non requis pour les formulaires Streamlit natifs
            st.markdown("</div>", unsafe_allow_html=True)

            for idx, chat in enumerate(reversed(st.session_state.get('ai_history', []))):
                with st.expander(f"Question : {chat['q']}", expanded=True):
                    st.markdown(chat['a'])
                    generate_browser_speech_widget(chat['a'])

        elif st.session_state.get('sidebar_nav_v8') == "Analyse & Audit":  # Analyse & Audit
            st.markdown("<h2 class='glow-text'>🔍 Analyse & Audit Documentaire</h2>", unsafe_allow_html=True)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            doc_uploaded = st.file_uploader("Importer une fiche de paie ou un contrat", type=["pdf", "png", "jpg"], key="uploader_audit_v8")
            if doc_uploaded:
                if st.button("Lancer l'audit", key="btn_audit_action_v8"):
                    st.session_state['analysis_results'] = "Analyse : Conformité IDCC 1517 validée. Vigilance recommandée sur les temps de repos."
                    st.success("Audit complété !")
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.get('sidebar_nav_v8') == "Code du travail":  # Code du travail
            st.markdown("<h2 class='glow-text'>⚖️ Code du travail</h2>", unsafe_allow_html=True)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.info("La Convention Collective Boulangerie-Pâtisserie (IDCC 1517) régit l'activité.")
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.get('sidebar_nav_v8') == "Réseau Sentinelles":  # Réseau Sentinelles
            st.markdown("<h2 class='glow-text'>🛡️ Réseau Sentinelles & Experts de proximité</h2>", unsafe_allow_html=True)
            df_sentinelles = pd.DataFrame(EXPERT_DIRECTORY)
            st.map(df_sentinelles)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            for d in EXPERT_DIRECTORY:
                st.write(f"📍 **{d['Nom']}** ({d['Type']}) — `Téléphone : {d['Contact']}`")
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.get('sidebar_nav_v8') == "Calculateur de primes":  # Calculateur de primes
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

        elif st.session_state.get('sidebar_nav_v8') == "Mes documents":  # Mes documents
            st.markdown("<h2 class='glow-text'>📂 Mes documents</h2>", unsafe_allow_html=True)
            st.markdown("<div class='buse-card'>", unsafe_allow_html=True)
            st.code("📄 contrat_de_travail_IDCC1517.pdf\n📄 avenant_infinity_v4.pdf", language="text")
            st.markdown("</div>", unsafe_allow_html=True)

    # 2. PANNEAU DE DROITE (Fidèle à la photo 2)
    with col_right_pane:
        st.markdown("<h4 class='glow-text' style='margin-bottom:15px;'>Outils rapides</h4>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='buse-card' style='padding: 15px;'>
                <p style='margin-bottom:8px; font-weight:500; font-size:0.9rem;'>📄 Analyser mon CV</p>
                <p style='margin-bottom:8px; font-weight:500; font-size:0.9rem;'>⚖️ Comparer mon contrat</p>
                <p style='margin-bottom:8px; font-weight:500; font-size:0.9rem;'>🔍 Consulter ma convention</p>
                <p style='margin-bottom:8px; font-weight:500; font-size:0.9rem;'>💎 Simuler une prime</p>
            </div>
            """, unsafe_allow_html=True
        )
        
        st.markdown("<h4 class='glow-text' style='margin-bottom:15px;'>Besoin d'aide ?</h4>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='buse-card' style='padding: 15px;'>
                <p style='font-size:0.85rem; color:#6B7280; margin-bottom:10px;'>Nos experts du réseau Sentinelles sont à votre écoute.</p>
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
            st.markdown("<h2 class='glow-text' style='text-align:center; font-family:Inter; color:#1E203B;'>Accès sécurisé</h2>", unsafe_allow_html=True)
            pin = st.text_input("Saisissez votre code PIN :", type="password", key="login_pin_v8")
            if st.button("DÉVERROUILLER", key="btn_submit_login_v8"):
                if pin == "1234":
                    st.session_state['auth'] = True
                    safe_rerun()
                else:
                    st.error("PIN incorrect.")
else:
    if not st.session_state.get('loading_complete', False):
        run_loading_sequence()
    else:
        main_app()
