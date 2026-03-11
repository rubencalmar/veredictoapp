import streamlit as st
import google.generativeai as genai

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    PROMPT_CONFIG = st.secrets["SISTEMA_EXPERTO_SEGUROS"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("Error: Configura los Secrets en Streamlit (GOOGLE_API_KEY y SISTEMA_EXPERTO_SEGUROS).")
    st.stop()

def main():
    st.set_page_config(page_title="Justiciero Seguros", page_icon="🛡️")
    st.title("🛡️ El Justiciero de tus Seguros")

    model = genai.GenerativeModel(
        model_name=st.secrets["MODELO"],
        system_instruction=PROMPT_CONFIG
    )

    uploaded_file = st.file_uploader("Sube tu póliza en PDF", type="pdf")

    if uploaded_file:
        pregunta = st.text_input("¿Cuál es el problema con tu seguro?")
        
        if pregunta:
            with st.spinner('Analizando con rigor legal...'):
                uploaded_file.seek(0)
                pdf_content = {"mime_type": "application/pdf", "data": uploaded_file.read()}
                
                response = model.generate_content([pdf_content, pregunta])
                
                st.markdown("### 📢 Resultado del Análisis")
                st.write(response.text)

if __name__ == "__main__":
    main()