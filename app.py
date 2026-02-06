import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURATION VISUELLE
st.set_page_config(page_title="Nova Vision", page_icon="🎓")

# 2. CONNEXION API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# 3. MODÈLE (Version 'latest' pour corriger l'erreur 404)
@st.cache_resource
def get_model():
    # On utilise la version 'latest' qui est la plus stable pour la vision
    return genai.GenerativeModel('gemini-1.5-flash-latest')

model = get_model()

# 4. BARRE LATÉRALE
with st.sidebar:
    st.title("⚙️ Réglages")
    niveau = st.selectbox("Niveau", ["Primaire", "Collège", "Lycée"])
    uploaded_file = st.file_uploader("Scanner l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

# 5. MÉMOIRE DU CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✨ Nova Vision")
st.write(f"Mode : Tutrice spécialisée ({niveau})")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# 6. ENVOI ET ANALYSE (Corrigé pour éviter l'IndentationError)
if prompt := st.chat_input("Ta question sur l'exercice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # On prépare le contenu
            instructions = f"Tu es Nova, une prof pour le niveau {niveau}. Aide l'élève de façon pédagogue."
            full_content = [instructions, prompt]
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                full_content.append(img)
                st.image(img, width=250, caption="Document en cours d'analyse")

            with st.spinner("Nova examine ton document..."):
                response = model.generate_content(full_content)
                res_text = response.text
                
            st.write(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error(f"Erreur technique : {e}")
            st.info("Conseil : Vérifie que ton image n'est pas trop lourde.")
