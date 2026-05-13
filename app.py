import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="La Buse - Boulanger",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Design global */
    .main { background-color: #f0f2f6; }
    .stApp { max-width: 100%; }
    
    /* Boutons et éléments interactifs */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        background-color: #004a99; 
        color: white; 
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #f26b21; transform: scale(1.02); }
    
    /* Cartes et sections */
    .card { 
        padding: 20px; 
        border-radius: 15px; 
        background-color: white; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); 
        margin-bottom: 15px;
        border-left: 5px solid #f26b21;
    }
    
    /* Adaptation Mobile spécifique */
    @media (max-width: 640px) {
        h1 { font-size: 1.8rem !important; }
        .stMarkdown { font-size: 0.9rem !important; }
    }
    
    /* Style de la barre latérale */
    .css-1d391kg { background-color: #004a99; }
    .sidebar-text { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

BOULANGER_DATA = {
    "name": "Boulanger",
    "idcc": "1517",
    "convention": "Commerces de détail non alimentaires",
    "syndicats": {
        "UNSA": {
            "nom": "UNSA Boulanger",
            "contact": "Stéphane SOURDET",
            "tel": "07 60 36 79 47",
            "email": "contact@unsa-boulanger.com",
            "site": "https://www.unsa-boulanger.com",
            "infos": "Premier syndicat de Boulanger. Aide juridique, défense des droits et accompagnement au quotidien.",
            "app_link": "Appli UNSA disponible sur Google Play / App Store"
        },
        "CFTC": {
            "nom": "CFTC Boulanger",
            "contact": "Aziz CHIADMI",
            "tel": "06 51 92 56 99",
            "site": "https://cftc-boulanger.fr",
            "infos": "Expertise sur les NAO 2026, revalorisation du BSC, frais repas et reconnaissance du tutorat.",
            "app_link": None
        },
        "CFDT": {
            "nom": "CFDT Boulanger",
            "contact": "Claire AVRILLON",
            "tel": "07 84 71 12 09",
            "email": "c.avrillon.cfdt@gmail.com",
            "site": "https://www.cfdt.fr",
            "infos": "Accompagnement personnalisé. Application mobile dédiée 'CFDT Boulanger' avec livret d'accueil.",
            "app_link": "Application 'CFDT BOULANGER' disponible"
        },
        "CGT": {
            "nom": "CGT Boulanger",
            "contact": "W. Bachir AHAMED / S. GROUSSAUD",
            "tel": "06 11 42 07 82",
            "email": "uescgt.boulanger@gmail.com",
            "infos": "Protection des salariés de l'UES. Présence active sur Instagram (@lacgt_groupeboulanger) et TikTok.",
            "app_link": None
        },
        "FO": {
            "nom": "FO Boulanger",
            "contact": "Délégués Nationaux FO",
            "tel": None,
            "email": None,
            "site": "https://www.fo-boulanger.fr",
            "infos": "Campagne actuelle pour les étrennes (500€). Application mobile 'FO BOULANGER' très complète.",
            "app_link": "Application 'FO BOULANGER' disponible"
        }
    }
}

with st.sidebar:
    st.image("https://www.boulanger.com/favicon.ico", width=60)
    st.title("🦅 La Buse")
    st.subheader("Navigation")
    
    # Menu simplifié sans Chatbot
    menu = st.radio(
        "Accès rapide :",
        ["🏠 Accueil", "🤝 Vos Syndicats", "📜 Ma Convention (IDCC)", "📍 Proximité", "📱 Accès iPhone"]
    )
    
    st.divider()
    st.write(f"🏢 **Enseigne :** {BOULANGER_DATA['name']}")
    st.write(f"⚖️ **IDCC :** {BOULANGER_DATA['idcc']}")
    
if menu == "🏠 Accueil":
    st.title(f"Bienvenue, Salarié {BOULANGER_DATA['name']}")
    
    st.markdown(f"""
    <div class="card">
        <h3>📢 Actualités Sociales</h3>
        <p><b>Dossier NAO 2026 :</b> Les négociations annuelles obligatoires sont au cœur des revendications (Salaires, Primes BES, Conditions de travail).</p>
        <p>Consultez l'onglet <b>Vos Syndicats</b> pour contacter vos délégués ou télécharger leurs applications mobiles.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Le saviez-vous ?** Votre convention collective (IDCC 1517) prévoit des jours de congés supplémentaires pour ancienneté.")
    with col2:
        st.warning("⚠️ **Rappel :** Les élections CSE approchent. Restez informés via vos organisations syndicales.")

elif menu == "🤝 Vos Syndicats":
    st.title("Vos Représentants Syndicaux")
    st.write("Retrouvez les fiches de contact extraites des dernières publications officielles.")

    for key, s in BOULANGER_DATA["syndicats"].items():
        with st.expander(f"📌 {s['nom']} - {s['contact']}"):
            st.write(f"**Mission :** {s['infos']}")
            
            # Grille de contact
            c1, c2 = st.columns(2)
            with c1:
                if s['tel']: st.link_button(f"📞 Appeler {s['contact']}", f"tel:{s['tel']}")
                if s['email']: st.write(f"📧 **Email :** {s['email']}")
            with c2:
                if s['site']: st.link_button(f"🌐 Visiter le site {key}", s['site'])
                if s['app_link']: st.success(f"📱 {s['app_link']}")

elif menu == "📜 Ma Convention (IDCC)":
    st.title(f"Convention IDCC {BOULANGER_DATA['idcc']}")
    st.caption(f"Libellé : {BOULANGER_DATA['convention']}")
    
    tab1, tab2, tab3 = st.tabs(["💶 Salaires", "📅 Congés", "🚀 Avantages"])
    
    with tab1:
        st.subheader("Grille des Salaires Minima (Branche)")
        grid_data = {
            "Niveau": ["1 (Employé)", "2", "3", "4 (Maîtrise)", "5", "Cadre"],
            "Minimum Brut": ["1 766,92€", "1 785,00€", "1 830,00€", "1 960,00€", "2 150,00€", "2 850,00€"]
        }
        st.table(pd.DataFrame(grid_data))
        st.caption("Données indicatives - Se référer aux derniers accords NAO de l'entreprise.")
        
    with tab2:
        st.markdown("""
        - **Congés Payés :** 2,5 jours ouvrables par mois.
        - **Ancienneté :** 
            - +1 jour après 10 ans.
            - +2 jours après 15 ans.
            - +3 jours après 20 ans.
        """)
        
    with tab3:
        st.write("La convention prévoit des dispositions sur la prévoyance, la mutuelle et le maintien de salaire en cas de maladie (sous conditions d'ancienneté).")

elif menu == "📍 Proximité":
    st.title("Trouver mon élu local")
    region = st.selectbox("Ma Région :", ["Hauts-de-France (Siège)", "Île-de-France", "Auvergne-Rhône-Alpes", "PACA", "Autre"])
    
    if region == "Hauts-de-France (Siège)":
        st.success("🏢 **Contact Prioritaire :** Stéphane SOURDET (UNSA) ou Aziz CHIADMI (CFTC)")
    elif region == "Île-de-France":
        st.info("📍 **Contact Régional :** Claire AVRILLON (CFDT) - 07 84 71 12 09")
    else:
        st.write("Recherche de délégués locaux en cours... Utilisez les numéros nationaux en attendant.")

elif menu == "📱 Accès iPhone":
    st.title("Installer sur votre iPhone")
    
    st.markdown("""
    <div class="card">
        <h4>Étape 1 : Ouvrir dans Safari</h4>
        <p>Assurez-vous d'utiliser le navigateur <b>Safari</b> pour bénéficier de l'intégration iOS.</p>
        
        <h4>Étape 2 : Ajouter à l'écran d'accueil</h4>
        <p>1. Appuyez sur l'icône <b>Partager</b> (le carré avec une flèche vers le haut).</p>
        <p>2. Faites défiler les options et choisissez <b>"Sur l'écran d'accueil"</b>.</p>
        <p>3. Validez en haut à droite sur <b>"Ajouter"</b>.</p>
        
        <h4>Étape 3 : C'est prêt !</h4>
        <p>L'icône 🦅 apparaîtra sur votre iPhone comme une application classique.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📤 Générer un lien de partage"):
        st.code("L'URL apparaîtra ici après votre déploiement sur Streamlit Cloud.")

st.divider()
st.caption("Projet 'La Buse' - Plateforme indépendante d'information sociale pour les salariés Boulanger. Données issues de sources publiques.")