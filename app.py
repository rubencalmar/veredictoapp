import streamlit as st
import google.generativeai as genai

# Configuración inicial desde Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Ajustamos la temperatura a 0.1 para máxima consistencia y homogeneidad
    model = genai.GenerativeModel(
        model_name=st.secrets["MODELO"], 
        system_instruction=st.secrets["SISTEMA_EXPERTO_SEGUROS"],
        generation_config={"temperature": 0.1, "top_p": 0.1} 
    )
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

st.title("🛡️ El Justiciero de tus Seguros")

# Inicializamos variables en el estado de la sesión si no existen
if "analisis" not in st.session_state:
    st.session_state.analisis = None
if "carta" not in st.session_state:
    st.session_state.carta = None

# 1. Inputs del usuario
file = st.file_uploader("Sube tu póliza (PDF)", type="pdf")
query = st.text_input("¿Qué quieres saber?")

# 2. Lógica del Botón "Analizar" (Solo aparece si hay archivo y pregunta)
if file and query:
    if st.button("🔍 Analizar contrato"):
        with st.spinner("Analizando con rigor legal..."):
            try:
                # Procesamos el PDF
                pdf_part = {"mime_type": "application/pdf", "data": file.getvalue()}
                response = model.generate_content([pdf_part, query])
                
                # Guardamos en el estado para que no se borre al pulsar otros botones
                st.session_state.analisis = response.text
                st.session_state.carta = None # Reset de la carta si hay nuevo análisis
            except Exception as e:
                st.error(f"Error en el análisis: {e}")

# 3. Mostrar el Análisis (Si existe en el estado)
if st.session_state.analisis:
    st.markdown("---")
    st.subheader("📢 Resultado del Análisis")
    st.write(st.session_state.analisis)

    # 4. Lógica de la Carta de Reclamación
    st.markdown("---")
    if st.button("📄 Generar Carta Formal"):
        with st.spinner("Redactando reclamación..."):
            prompt_carta = f"Redacta una reclamación formal basada estrictamente en este análisis: {st.session_state.analisis}"
            carta_response = model.generate_content(prompt_carta)
            st.session_state.carta = carta_response.text

    # 5. Mostrar la Carta y el Botón de Descarga
    if st.session_state.carta:
        st.text_area("Borrador de la reclamación:", value=st.session_state.carta, height=300)
        
        st.download_button(
            label="⬇️ Descargar carta en .txt",
            data=st.session_state.carta,
            file_name="reclamacion_seguro.txt",
            mime="text/plain"
        )