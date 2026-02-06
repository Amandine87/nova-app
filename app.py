import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova AI", page_icon="✨")

# --- CONFIGURATION GOOGLE ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé manquante.")
    st.stop()

# --- MÉMOIRE DE LA CONVERSATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DÉTECTION DU MODÈLE ---
@st.cache_resource
def load_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    return genai.GenerativeModel(available_models[0] if available_models else 'gemini-1.5-flash')

model = load_model()

# --- INTERFACE ---
st.title("✨ Nova : Ton Assistante")
st.markdown("---")

# Affichage des messages passés
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Dis-moi quelque chose..."):
    # On affiche le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de Nova
    with st.chat_message("assistant"):
        try:
            # On envoie toute l'histoire à Nova pour qu'elle ait de la mémoire
            full_prompt = "Tu es Nova, une IA amicale et intelligente. Réponds de façon concise. \n\n"
            for m in st.session_state.messages:
                full_prompt += f"{m['role']}: {m['content']}\n"
            
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Oups : {e}")

# Bouton pour effacer la mémoire
if st.sidebar.button("Effacer la discussion"):
    st.session_state.messages = []
    st.rerun()
