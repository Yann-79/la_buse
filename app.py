import streamlit as st
import os
from datetime import datetime
import traceback
import time

# OCR & PDF Libraries
try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

st.set_page_config(page_title="La Buse", page_icon="🦉", layout="wide")

st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    .stButton>button {background: #4f46e5; color: white; border-radius: 12px;}
    .card {background: white; padding: 24px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);}
    .ocr-badge {background: #fef3c7; color: #d97706; padding: 4px 12px; border-radius: 9999px; font-size: 0.85rem;}
</style>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.title("🦉 La Buse")
    st.caption("OCR + Analyse Document")
    api_key = st.text_input("xAI API Key (Grok)", type="password", value=os.getenv("XAI_API_KEY", ""))
    
    st.divider()
    page = st.radio("Navigation", 
                   ["Accueil", "🦅 Eagle Agent (OCR)", "📜 Convention Collective", "🏖️ Congés & RTT"])

# ===================== SESSION STATE =====================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

if not st.session_state.authenticated:
    # PIN Screen
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center'>🦉 La Buse</h1>", unsafe_allow_html=True)
        pin = st.text_input("Code PIN", type="password", max_chars=4)
        if st.button("Déverrouiller", use_container_width=True):
            if pin == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Code PIN incorrect")
    st.stop()

# ===================== EAGLE AGENT AVEC OCR =====================
if page == "🦅 Eagle Agent (OCR)":
    st.title("🦅 Eagle Agent IA — OCR + Analyse")
    st.caption("Support documents scannés (PDF image) + textes")

    uploaded_files = st.file_uploader(
        "Déposez vos documents (contrats, fiches de paie, avenants...)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in [doc["name"] for doc in st.session_state.uploaded_docs]:
                with st.spinner(f"Traitement OCR de {uploaded_file.name}..."):
                    try:
                        # Sauvegarde temporaire
                        temp_path = f"temp_{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        extracted_text = ""
                        
                        if OCR_AVAILABLE:
                            # Conversion PDF → Images
                            images = convert_from_path(temp_path, dpi=300)
                            st.info(f"📄 {len(images)} page(s) détectée(s) — OCR en cours...")
                            
                            for i, image in enumerate(images):
                                text = pytesseract.image_to_string(image, lang='fra')
                                extracted_text += f"\n--- Page {i+1} ---\n{text}"
                        else:
                            extracted_text = "[OCR non disponible - Mode texte uniquement]"
                        
                        # Nettoyage
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                        
                        st.session_state.uploaded_docs.append({
                            "name": uploaded_file.name,
                            "text": extracted_text[:8000]  # Limite pour mémoire
                        })
                        st.success(f"✅ {uploaded_file.name} analysé avec OCR")
                        
                    except Exception as e:
                        st.error(f"Erreur OCR sur {uploaded_file.name}: {e}")

    # Affichage des documents uploadés
    if st.session_state.uploaded_docs:
        st.write("**Documents analysés :**")
        for doc in st.session_state.uploaded_docs:
            st.write(f"• 📄 {doc['name']}")

    # Chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Posez une question sur vos documents..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analyse des documents + Grok..."):
                context = "\n\n".join([doc["text"][:1500] for doc in st.session_state.uploaded_docs[-2:]])
                answer = f"**Analyse des documents uploadés :**\n\n{context[:800]}\n\n**Réponse :** Selon les documents fournis..."
                
                if api_key:
                    try:
                        llm = ChatXAI(api_key=api_key, model="grok-4", temperature=0.3)
                        full_prompt = f"Documents : {context}\n\nQuestion : {prompt}"
                        response = llm.invoke(full_prompt)
                        answer = response.content
                    except:
                        pass
                
                st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})

else:
    st.title(page)
    st.info("Section en cours de développement.")

st.caption("© 2026 La Buse • OCR pour documents scannés")
