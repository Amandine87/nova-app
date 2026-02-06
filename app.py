import streamlit as st
import google.generativeai as genai

# 1. Configuration et Style dynamique
st.set_page_config(page_title="Nova Ultra", page_icon="🚀")

# Barre latérale pour les options
with st.sidebar:
    st.title("⚙️ Réglages Nova")
    humeur = st.selectbox("Humeur de Nova", ["Amicale ✨", "Professionnelle 💼", "Créative 🎨", "Humoristique 🤡"])
    mode_expert = st.toggle("Mode Expert (Réponses détaillées)")
    if st.button("🗑️ Effacer la mémoire"):
        st.session_state.messages = []
        st.rerun()

# 2. Connexion Google
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé manquante.")
    st.stop()

# 3. Mémoire et Modèle
if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    return genai.GenerativeModel(available_models[0] if available_models else 'gemini-1.5-flash')

model = load_model()

# 4. Interface
st.title(f"Assistant Nova : {humeur}")
st.info(f"Nova agit actuellement en mode : **{humeur}**")

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Logique de réponse
if prompt := st.chat_input("Pose ta question à Nova..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Construction du caractère de Nova selon les réglages
            precision = "détaillée et technique" if mode_expert else "simple et concise"
            system_instruction = f"Tu es Nova. Ton humeur est {humeur}. Ta réponse doit être {precision}."
            
            # On prépare l'historique
            history = ""
            for m in st.session_state.messages:
                history += f"{m['role']}: {m['content']}\n"
            
            response = model.generate_content(f"{system_instruction}\n\nHistorique :\n{history}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
