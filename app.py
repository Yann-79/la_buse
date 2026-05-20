import streamlit as st
import os
from datetime import datetime
import traceback
import time

st.set_page_config(page_title="La Buse", page_icon="🦉", layout="wide")

# ===================== TENTATIVE D'IMPORT LANGCHAIN =====================
try:
    from langchain_xai import ChatXAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    st.warning("⚠️ Package `langchain-xai` non installé. Certaines fonctionnalités IA seront limitées.")

st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    .stButton>button {background: #4f46e5; color: white; border-radius: 12px;}
    .error-box {background: #fee2e2; padding: 15px; border-radius: 10px; border-left: 5px solid #ef4444;}
    .success-box {background: #ecfdf5; padding: 15px; border-radius: 10px; border-left: 5px solid #10b981;}
</style>
""", unsafe_allow_html=True)

# ===================== UTILITAIRE SÉCURISÉ =====================
def safe_execute_with_progress(func, *args, progress_text="Traitement en cours...", error_msg="Une erreur est survenue", **kwargs):
    progress_bar = st.progress(0, text=progress_text)
    try:
        for i in range(1, 101, 20):
            time.sleep(0.1)
            progress_bar.progress(i, text=progress_text)
        
        result = func(*args, **kwargs)
        progress_bar.progress(100, text="✅ Terminé")
        time.sleep(0.3)
        progress_bar.empty()
        return result
    except Exception as e:
        progress_bar.empty()
        st.markdown(f"""
        <div class="error-box">
            ❌ <strong>{error_msg}</strong><br>
            {str(e)}
        </div>
        """, unsafe_allow_html=True)
        return None

# ===================== SIDEBAR =====================
with st.sidebar:
    st.title("🦉 La Buse")
    st.caption("Assistant Droit du Travail")
    api_key = st.text_input("xAI API Key (Grok)", type="password", value=os.getenv("XAI_API_KEY", ""))
    
    st.divider()
    page = st.radio("Navigation", 
                   ["Accueil", 
                    "📜 Convention Collective",
                    "🏖️ Congés Payés", 
                    "⏰ Jours de RTT"])

# ===================== AUTH =====================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_cc" not in st.session_state:
    st.session_state.current_cc = None

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center'>🦉 La Buse</h1>", unsafe_allow_html=True)
        pin = st.text_input("Code PIN", type="password", max_chars=4)
        if st.button("Déverrouiller", use_container_width=True):
            if pin == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Code PIN incorrect")
    st.stop()

# ===================== PAGE CONVENTION COLLECTIVE =====================
if page == "📜 Convention Collective":
    st.title("📜 Convention Collective")
    
    idcc = st.text_input("IDCC ou Nom de la Convention", placeholder="650, Syntec...")
    
    if st.button("Charger Convention", type="primary"):
        if not LANGCHAIN_AVAILABLE:
            st.error("❌ `langchain-xai` n'est pas installé. Exécutez : `pip install langchain-xai`")
        elif not api_key:
            st.warning("⚠️ Veuillez entrer votre clé API Grok")
        else:
            def load_convention():
                llm = ChatXAI(api_key=api_key, model="grok-4", temperature=0.2)
                resp = llm.invoke(f"Résume les points clés de la convention collective {idcc}")
                return {"idcc": idcc, "details": resp.content}
            
            result = safe_execute_with_progress(load_convention, progress_text="Chargement via Grok...")
            if result:
                st.session_state.current_cc = result
                st.success(f"✅ Convention {idcc} chargée")

else:
    st.title(page)
    st.info("Section en cours de développement")

st.caption("© 2026 La Buse • Gestion des erreurs + Progress Bar")
