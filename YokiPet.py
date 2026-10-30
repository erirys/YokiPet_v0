%%writefile YokiPet.py
import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="YokiPet - Cuidado de Mascotas", page_icon="🐾", layout="centered")

# Inicializar el estado de la sesión para simular una base de datos temporal
if "solicitudes" not in st.session_state:
    st.session_state.solicitudes = [
        {
            "propietario": "María López",
            "mascota": "Toby (Perro, Golden Retriever)",
            "fechas": "15/06/2025 al 20/06/2025",
            "detalles": "Necesita paseos dos veces al día. Muy amigable."
        },
        {
            "propietario": "Carlos Gómez",
            "mascota": "Michi (Gato, Siamés)",
            "fechas": "01/07/2025 al 05/07/2025",
            "detalles": "Solo requiere alimentación y limpieza de arenero una vez al día."
        }
    ]

# Título principal
st.title("🐾 YokiPet")
st.subheader("La red de confianza para el cuidado de tus mascotas")

# Pestañas de navegación
tab1, tab2 = st.tabs(["🙋‍♂️ Dueños de Mascotas", "🏡 Cuidadores Disponibles"])

with tab1:
    st.header("Publicar Solicitud de Cuidado")
    st.write("Completa el formulario para que un cuidador de confianza se ponga en contacto contigo.")
    
    with st.form("solicitud_form", clear_on_submit=True):
        nombre_dueño = st.text_input("Tu Nombre completo")
        nombre_mascota = st.text_input("Nombre y tipo de mascota (Ej: Bruno - Pastor Alemán)")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Desde", min_value=datetime.today())
        with col2:
            fecha_fin = st.date_input("Hasta", min_value=datetime.today())
            
        detalles = st.text_area("Indicaciones o cuidados especiales")
        
        submit_button = st.form_submit_button("Publicar Solicitud")
        
        if submit_button:
            if nombre_dueño and nombre_mascota:
                nueva_solicitud = {
                    "propietario": nombre_dueño,
                    "mascota": nombre_mascota,
                    "fechas": f"{fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}",
                    "detalles": detalles
                }
                st.session_state.solicitudes.append(nueva_solicitud)
                st.success("¡Tu solicitud ha sido publicada con éxito! Un cuidador la revisará pronto.")
            else:
                st.error("Por favor, completa los campos requeridos (Nombre y Mascota).")

with tab2:
    st.header("Solicitudes de Cuidado Activas")
    st.write("Explora las mascotas que necesitan atención en tu área:")
    
    if len(st.session_state.solicitudes) == 0:
        st.info("No hay solicitudes activas en este momento.")
    else:
        for idx, sol in enumerate(st.session_state.solicitudes):
            with st.container():
                st.markdown(f"### 🐶 {sol['mascota']}")
                st.write(f"**Dueño:** {sol['propietario']}")
                st.write(f"**Fechas:** {sol['fechas']}")
                st.write(f"**Notas:** {sol['detalles']}")
                
                if st.button(f"Postularme para cuidar a {sol['mascota'].split(' ')[0]}", key=f"btn_{idx}"):
                    st.success(f"🎉 ¡Te has postulado! Hemos notificado a {sol['propietario']}.")
                st.markdown("---")
