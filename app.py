import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURATION
st.set_page_config(page_title="Nova Vision", page_icon="🎓")

# 2. CONNEXION API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# 3. DÉTECTION AUTOMATIQUE DU MODÈLE (Anti-404)
@st.cache_resource
def get_best_model():
    try:
        # On récupère la liste des modèles supportés par ton compte
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # On cherche en priorité Flash (rapide et voit les images)
        flash_models = [m for m in models if "flash" in m]
        if flash_models:
            return genai.GenerativeModel(flash_models[0])
        # Sinon on prend le premier disponible
        return genai.GenerativeModel(models[0])
    except Exception as e:
        # Solution de secours si la liste échoue
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_best_model()

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
st.write(f"Modèle détecté : `{model.model_name}`") # Pour vérifier ce qu'il a trouvé

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# 6. ENVOI ET ANALYSE
if prompt := st.chat_input("Ta question sur l'exercice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            instructions = f"Tu es Nova, une prof pour le niveau {niveau}. Aide l'élève de façon pédagogue sans donner la réponse brute tout de suite."
            full_content = [instructions, prompt]
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                full_content.append(img)
                st.image(img, width=250)

            with st.spinner("Nova analyse ton document..."):
                response = model.generate_content(full_content)
                res_text = response.text
                
            st.write(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error(f"Erreur technique : {e}")
            st.info("Essaye de rafraîchir la page ou de vérifier ta connexion.")
