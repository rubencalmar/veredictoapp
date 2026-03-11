import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    model = genai.GenerativeModel(
        model_name=st.secrets["MODELO"], 
        system_instruction=st.secrets["SISTEMA_EXPERTO_SEGUROS"]
    )
except KeyError as e:
    st.error(f"Falta una configuración crítica en los Secrets: {e}")
    st.stop()

st.title("🛡️ El Justiciero de tus Seguros")

file = st.file_uploader("Sube tu póliza (PDF)", type="pdf")
query = st.text_input("¿Qué quieres saber?")

if file and query:
    if st.button("Analizar"):
        try:
            with st.spinner("Analizando..."):
                # Mandamos los bytes directamente
                response = model.generate_content([
                    {"mime_type": "application/pdf", "data": file.getvalue()},
                    query
                ])
                
                st.session_state.result = response.text
                st.markdown("---")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error en la API: {e}")

# Lógica de la carta formal
if "result" in st.session_state:
    if st.button("📄 Generar Carta Formal"):
        with st.spinner("Redactando..."):
            carta = model.generate_content(f"Redacta una reclamación formal basada en: {st.session_state.result}")
            st.text_area("Borrador:", value=carta.text, height=300)