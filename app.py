import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURATION
st.set_page_config(page_title="Nova Vision", page_icon="🎓")

# 2. CONNEXION
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# 3. MODÈLE (Correction de l'erreur 404)
@st.cache_resource
def get_model():
    # Utilisation du nom complet pour éviter les erreurs de version
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# 4. BARRE LATÉRALE
with st.sidebar:
    st.title("⚙️ Options")
    niveau = st.selectbox("Niveau", ["Primaire", "Collège", "Lycée"])
    uploaded_file = st.file_uploader("Importer l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

# 5. HISTORIQUE
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✨ Nova Vision")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# 6. ENVOI ET RÉPONSE (Attention aux décalages ici !)
if prompt := st.chat_input("Ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            full_content = [f"Tu es Nova, tutrice niveau {niveau}.", prompt]
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                full_content.append(img)
                st.image(img, width=250)

            with st.spinner("Nova réfléchit..."):
                response = model.generate_content(full_content)
                res_text = response.text
                
            st.write(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error(f"Erreur : {e}")
