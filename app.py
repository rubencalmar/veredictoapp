import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Diagnóstico de Modelos")

try:
    # Esto nos dirá qué modelos ve tu API Key realmente
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    st.write("Modelos disponibles para tu cuenta:")
    st.json(models)
    
    # Intentar instanciar el modelo de tus secrets
    target_model = st.secrets["MODELO"]
    st.write(f"Intentando conectar con: {target_model}")
    
    model = genai.GenerativeModel(target_model)
    response = model.generate_content("Hola, ¿estás ahí?")
    st.success(f"Conexión exitosa: {response.text}")

except Exception as e:
    st.error(f"Error detectado: {e}")