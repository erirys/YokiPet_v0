import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página con tema de color alegre
st.set_page_config(page_title="YokiPet", page_icon="🐾", layout="centered")

# Aplicar CSS personalizado para mejorar el diseño plano y añadir fuentes del slogan
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Quicksand:wght@500;700&display=swap');

    /* Color de fondo global sutil y fuentes */
    .main {
        background-color: #fcf9f5;
        font-family: 'Quicksand', sans-serif;
    }
    
    /* Estilo de tarjetas de solicitudes */
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(222, 142, 60, 0.1);
        border-left: 5px solid #ff7e5f;
        margin-bottom: 20px;
    }
    
    /* Título llamativo con degradado */
    .main-title {
        font-family: 'Fredoka', sans-serif;
        background: linear-gradient(45deg, #ff7e5f, #feb47b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* Slogan creativo con fuente divertida pero profesional */
    .creative-slogan {
        font-family: 'Fredoka', sans-serif;
        color: #4a4a4a;
        font-size: 1.4rem;
        text-align: center;
        margin-bottom: 25px;
        background: #fff0eb;
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
        width: 100%;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
    }
    .slogan-highlight {
        color: #ff7e5f;
        font-weight: 700;
        font-size: 1.6rem;
    }
    
    /* Aviso del Prototipo destacado */
    .aviso-prototipo {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ffeeba;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar el estado de la sesión para simular una base de datos temporal
if "solicitudes" not in st.session_state:
    st.session_state.solicitudes = [
        {
            "propietario": "María López",
            "mascota": "Toby",
            "raza": "Perro, Golden Retriever",
            "fechas": "15/06/2025 al 20/06/2025",
            "detalles": "Necesita paseos dos veces al día. Muy amigable y juguetón."
        },
        {
            "propietario": "Carlos Gómez",
            "mascota": "Michi",
            "raza": "Gato, Siamés",
            "fechas": "01/07/2025 al 05/07/2025",
            "detalles": "Solo requiere alimentación y limpieza de arenero una vez al día por la mañana."
        }
    ]

# Barra lateral interactiva y atractiva
with st.sidebar:
    st.markdown("<h2 style='text-align: center; font-family: Fredoka;'>🧡 YokiPet Club</h2>", unsafe_allow_html=True)
    st.write("¡Bienvenido a la comunidad más alegre de amantes de las mascotas!")
    st.image("https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400", use_container_width=True)
    
    st.markdown("---")
    st.markdown("**📌 Estado del Sistema:**")
    st.info("Servidores en línea • Versión 0.1 Demo")
    
    st.markdown("<div class='aviso-prototipo'>⚠ Prototipo con datos ficticios. No se realizan reservas reales.</div>", unsafe_allow_html=True)

# Banner de Bienvenida Principal
st.markdown("<h1 class='main-title'>YokiPet 🐾</h1>", unsafe_allow_html=True)
# Ubicación creativa del nuevo slogan solicitado
st.markdown("<div class='creative-slogan'>¿Quién cuidará de tus peluditos? ——— <span class='slogan-highlight'>¡Yoki!</span></div>", unsafe_allow_html=True)

# Métricas alegres e informativas en la parte superior
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="Mascotas felices", value=len(st.session_state.solicitudes), delta="+1 esta semana")
with col_m2:
    st.metric(label="Cuidadores verificados", value="24 Active", delta="100% confiable")
with col_m3:
    st.metric(label="Puntuación media", value="4.9 ★", delta="Impecable")

st.markdown("<br>", unsafe_allow_html=True)

# Pestañas de navegación estilizadas con iconos claros
tab1, tab2 = st.tabs(["🙋‍♂️ Dueños de Mascotas", "🏡 Cuidadores Disponibles"])

with tab1:
    st.markdown("### ✨ Publica la solicitud para tu consentido")
    st.write("¡Cuéntanos qué necesita tu mascota y los mejores cuidadores se postularán!")
    
    # Formulario dentro de un contenedor visual
    with st.form("solicitud_form", clear_on_submit=True):
        st.markdown("#### 📝 Formulario de Solicitud")
        nombre_dueño = st.text_input("Tu Nombre completo")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_mascota = st.text_input("Nombre de tu mascota")
        with col_f2:
            raza_mascota = st.text_input("Raza y tipo (Ej: Husky, Gato persa)")
            
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            fecha_inicio = st.date_input("¿Desde cuándo?", min_value=datetime.today())
        with col_d2:
            fecha_fin = st.date_input("¿Hasta cuándo?", min_value=datetime.today())
            
        detalles = st.text_area("📝 Indicaciones, personalidad o cuidados especiales de tu mascota")
        
        submit_button = st.form_submit_button("🚀 Publicar Anuncio de Cuidado")
        
        if submit_button:
            if nombre_dueño and nombre_mascota:
                nueva_solicitud = {
                    "propietario": nombre_dueño,
                    "mascota": nombre_mascota,
                    "raza": raza_mascota if raza_mascota else "Especie indeterminada",
                    "fechas": f"{fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}",
                    "detalles": detalles
                }
                st.session_state.solicitudes.append(nueva_solicitud)
                st.balloons() # Animación festiva de globos al publicar con éxito
                st.success(f"¡Genial! El anuncio de {nombre_mascota} ya está disponible en la pestaña de cuidadores.")
            else:
                st.error("❌ Por favor, ingresa al menos tu nombre y el de tu mascota para poder ayudarte.")

with tab2:
    st.markdown("### 🔎 Solicitudes de Cuidado Activas")
    st.write("Aquí verás los anuncios publicados por dueños de mascotas que buscan tu cariño y atención:")
    
    if len(st.session_state.solicitudes) == 0:
        st.info("🌈 No hay anuncios pendientes en este momento. ¡Vuelve más tarde!")
    else:
        for idx, sol in enumerate(st.session_state.solicitudes):
            # Crear contenedor con tarjeta visual
            st.markdown(f"""
            <div class='card'>
                <h3 style='margin-top:0; color:#ff7e5f; font-family: Fredoka;'>🐶 {sol['mascota']} ({sol['raza']})</h3>
                <p style='margin: 5px 0;'><b>👤 Propietario:</b> {sol['propietario']}</p>
                <p style='margin: 5px 0;'><b>📅 Fechas solicitadas:</b> {sol['fechas']}</p>
                <p style='margin: 10px 0; font-style: italic; color:#555;'>" {sol['detalles']} "</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón interactivo debajo de la tarjeta
            if st.button(f"🤝 Postularme para cuidar a {sol['mascota']}", key=f"btn_{idx}"):
                st.success(f"🎉 ¡Increíble! Te has postulado para cuidar a {sol['mascota']}. Hemos enviado un aviso ficticio a {sol['propietario']}.")
            st.markdown("<br>", unsafe_allow_html=True)
