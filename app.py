import streamlit as st

st.set_page_config(page_title="Nova - Ton Coach Révision", page_icon="🎓")

st.title("🎓 Nova : Ton compagnon de révision")
st.markdown("---")

niveau = st.sidebar.radio("Ton niveau :", ["Collège (Cool)", "Lycée (Sérieux)"])

if niveau == "Collège (Cool)":
    st.write("### Salut ! 👋 Prêt à décrocher tes badges ce soir ?")
    placeholder = "Explique-moi ton cours ou ton exercice..."
else:
    st.write("### Bonjour. Quelle notion souhaites-tu approfondir ?")
    placeholder = "Décris la difficulté méthodologique que tu rencontres..."

user_input = st.text_area("Ta demande :", placeholder=placeholder)

if st.button("Demander de l'aide"):
    if user_input:
        st.info("Connexion à l'IA en cours... (C'est ici que la magie opérera !)")
        if niveau == "Collège (Cool)":
            st.success("🏆 Badge débloqué : 'Première Étincelle' !")
    else:
        st.warning("Écris quelque chose pour que je puisse t'aider !")
