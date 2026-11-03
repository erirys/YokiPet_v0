import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES
# -----------------------------------------------------
st.set_page_config(page_title="YokiPet - Cuidado de Mascotas", page_icon="🐾", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Quicksand:wght@500;700&display=swap');

    .main {
        background-color: #fcf9f5;
        font-family: 'Quicksand', sans-serif;
    }

    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(222, 142, 60, 0.1);
        border-left: 5px solid #ff7e5f;
        margin-bottom: 20px;
    }

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
    }

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

# Banner de advertencia obligatorio según especificacion.md
st.markdown('<div class="aviso-prototipo">⚠️ Prototipo con datos ficticios. No se realizan reservas reales.</div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🐾 YokiPet</h1>', unsafe_allow_html=True)
st.markdown('<div class="creative-slogan">La red de confianza para el cuidado de tus <span class="slogan-highlight">mascotas</span> en Costa Rica</div>', unsafe_allow_html=True)

# -----------------------------------------------------
# 2. CONFIGURACIÓN DE SECRETOS Y PIEZA DE IA (GEMINI)
# -----------------------------------------------------
gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", None))
usar_ia = False
client = None

if gemini_key:
    try:
        from google import genai
        client = genai.Client(api_key=gemini_key)
        usar_ia = True
    except Exception as e:
        pass

def obtener_explicacion_asistente(cuidadores_encontrados, mascota_info):
    if not usar_ia or not client:
        return "*Modo sin IA activo. El catálogo determinista te asegura la mejor coincidencia según los filtros ingresados.*"

    prompt = f"""Actúa como un asistente experto de YokiPet en Costa Rica.
    Analiza los siguientes cuidadores que cumplen con los filtros aplicados: {cuidadores_encontrados}.
    Explica brevemente y con un tono cálido al propietario de la mascota ({mascota_info}) por qué estas opciones son óptimas.
    No inventes tarifas, zonas, nombres ni valoraciones que no estén explícitas en los datos proporcionados."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as api_err:
        return "⚠️ La IA explicativa no está disponible temporalmente por límites de cuota o de red."

# -----------------------------------------------------
# 3. BASE DE DATOS FICTICIA INICIAL EN SESIÓN
# -----------------------------------------------------
if "sesion_iniciada" not in st.session_state:
    st.session_state.sesion_iniciada = False
if "usuario_nombre" not in st.session_state:
    st.session_state.usuario_nombre = ""
if "tipo_perfil" not in st.session_state:
    st.session_state.tipo_perfil = None
if "info_cuidador" not in st.session_state:
    st.session_state.info_cuidador = {
        "experiencia": "Excelente trato y cariño para tus mascotas.",
        "zona": "San José",
        "tarifa": 10000,
        "servicio": "Hospedaje"
    }

if "solicitudes" not in st.session_state:
    st.session_state.solicitudes = [
        {
            "propietario": "María López",
            "mascota": "Toby",
            "raza": "Perro, Golden Retriever",
            "fechas": "15/06/2025 al 20/06/2025",
            "detalles": "Necesita paseos dos veces al día. Muy amigable."
        },
        {
            "propietario": "Carlos Gómez",
            "mascota": "Michi",
            "raza": "Gato, Siamés",
            "fechas": "01/07/2025 al 05/07/2025",
            "detalles": "Solo requiere alimentación y limpieza de arenero una vez al día."
        }
    ]

cuidadores_db = [
    {"nombre": "Lucía Madrigal", "servicio": "Hospedaje", "zona": "San José", "tarifa": 12000, "especie": "Perro", "tamaño": "Todos"},
    {"nombre": "Andrés Fonseca", "servicio": "Paseos", "zona": "Heredia", "tarifa": 5000, "especie": "Perro", "tamaño": "Mediano"},
    {"nombre": "Valeria Chaves", "servicio": "Guardería", "zona": "Alajuela", "tarifa": 8000, "especie": "Gato", "tamaño": "Todos"}
]

# Contraseña de simulación fija para el acceso del prototipo
PASSWORD_CORRECTA = "yoki123"

# -----------------------------------------------------
# 4. FLUJO DE CONTROL DE ACCESO CON CONTRASEÑA
# -----------------------------------------------------
if not st.session_state.sesion_iniciada:
    st.markdown("### 🔑 Ingreso Seguro a tu Cuenta YokiPet")
    st.write("Por favor introduce tu información y contraseña demo `yoki123`.")
    
    with st.form("login_seguro"):
        nombre_input = st.text_input("Tu Nombre Completo")
        perfil_seleccionado = st.selectbox("Selecciona tu perfil de acceso", ["Dueño de Mascota", "Cuidador de Mascota"])
        password_input = st.text_input("Contraseña de seguridad", type="password")
        login_btn = st.form_submit_button("Iniciar sesión")
        
        if login_btn:
            if nombre_input.strip() == "":
                st.error("❌ Por favor, ingresa tu nombre.")
            elif password_input != PASSWORD_CORRECTA:
                st.error("❌ Contraseña incorrecta. Utiliza la contraseña demo `yoki123`.")
            else:
                st.session_state.usuario_nombre = nombre_input
                st.session_state.tipo_perfil = perfil_seleccionado
                st.session_state.sesion_iniciada = True
                st.success("¡Acceso concedido exitosamente!")
                st.rerun()
else:
    # Cabecera de usuario con logout
    col_usr, col_logout = st.columns([3, 1])
    with col_usr:
        st.info(f"👤 Conectado como: **{st.session_state.usuario_nombre}** | Rol: **{st.session_state.tipo_perfil}**")
    with col_logout:
        if st.button("Cerrar sesión"):
            st.session_state.sesion_iniciada = False
            st.session_state.usuario_nombre = ""
            st.session_state.tipo_perfil = None
            st.rerun()

    # -----------------------------------------------------
    # 5. DIRECCIONAMIENTO INTELIGENTE SEGÚN PERFIL
    # -----------------------------------------------------
    if st.session_state.tipo_perfil == "Dueño de Mascota":
        tab1, tab2 = st.tabs(["🙋‍♂️ Publicar Solicitud de Cuidado", "🔎 Buscar Cuidador con IA"])
        
        with tab1:
            st.header("Publicar Solicitud de Cuidado")
            st.write("Completa el formulario para que un cuidador se postule de manera simulada.")

            with st.form("solicitud_form", clear_on_submit=True):
                nombre_dueño = st.text_input("Nombre del dueño", value=st.session_state.usuario_nombre, disabled=True)
                nombre_mascota = st.text_input("Nombre de tu mascota")
                raza_mascota = st.text_input("Especie / Raza (ej: Gato Siamés, Perro Poodle)")

                col1, col2 = st.columns(2)
                with col1:
                    fecha_inicio = st.date_input("Desde", min_value=datetime.today())
                with col2:
                    fecha_fin = st.date_input("Hasta", min_value=datetime.today())

                detalles = st.text_area("Indicaciones o cuidados especiales")
                submit_button = st.form_submit_button("🚀 Publicar Anuncio de Cuidado")

                if submit_button:
                    if nombre_mascota:
                        nueva_solicitud = {
                            "propietario": nombre_dueño,
                            "mascota": nombre_mascota,
                            "raza": raza_mascota if raza_mascota else "Especie indeterminada",
                            "fechas": f"{fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}",
                            "detalles": detalles
                        }
                        st.session_state.solicitudes.append(nueva_solicitud)
                        st.balloons()
                        st.success(f"¡Genial! Tu solicitud para cuidar a {nombre_mascota} ha sido publicada con éxito.")
                    else:
                        st.error("❌ Por favor, ingresa el nombre de tu mascota.")

        with tab2:
            st.header("Buscador Inteligente de Cuidadores")
            st.write("Filtra nuestro catálogo y deja que el asistente te recomiende las mejores opciones.")

            b_servicio = st.selectbox("Servicio requerido", ["Hospedaje", "Guardería", "Paseos"])
            b_zona = st.selectbox("Ubicación en Costa Rica", ["San José", "Heredia", "Alajuela"])
            b_especie = st.selectbox("Especie de mascota", ["Perro", "Gato"])
            b_presupuesto = st.number_input("Presupuesto máximo (₡)", min_value=1000, value=15000, step=1000)

            if st.button("Buscar Cuidador ideal"):
                encontrados = [
                    c for c in cuidadores_db
                    if c['servicio'] == b_servicio
                    and c['zona'] == b_zona
                    and c['especie'] == b_especie
                    and c['tarifa'] <= b_presupuesto
                ]

                if encontrados:
                    st.success(f"Se encontraron {len(encontrados)} opciones que coinciden exactamente con tus criterios.")
                    info_mascota_busqueda = f"{b_especie} en la zona de {b_zona} para el servicio de {b_servicio}"
                    explicacion = obtener_explicacion_asistente(encontrados, info_mascota_busqueda)

                    st.markdown("### 🤖 Recomendación del Asistente YokiPet")
                    st.info(explicacion)

                    for cuid in encontrados:
                        st.markdown(f"""
                        <div class='card'>
                            <h3 style='margin-top:0; color:#2e7d32; font-family: Fredoka;'>⭐ {cuid['nombre']}</h3>
                            <p style='margin: 5px 0;'><b>📍 Zona:</b> {cuid['zona']} | <b>🛠️ Servicio:</b> {cuid['servicio']}</p>
                            <p style='margin: 5px 0;'><b>💰 Tarifa por día:</b> ₡{cuid['tarifa']:,}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("😔 No se encontraron cuidadores en el catálogo que coincidan exactamente con tus criterios.")

    elif st.session_state.tipo_perfil == "Cuidador de Mascota":
        tab1, tab2 = st.tabs(["🏡 Mi Información de Cuidador", "🔎 Solicitudes de Cuidado Activas"])
        
        with tab1:
            st.header("⚙️ Mi Perfil de Cuidador de Confianza")
            st.write("Aquí puedes definir tu tarifa diaria y tu cobertura para aparecer en las búsquedas.")
            
            with st.form("perfil_cuidador"):
                ex_input = st.text_area("Presentación / Experiencia profesional", value=st.session_state.info_cuidador["experiencia"])
                zona_input = st.selectbox("Zona de servicio", ["San José", "Heredia", "Alajuela"], index=["San José", "Heredia", "Alajuela"].index(st.session_state.info_cuidador["zona"]))
                tarifa_input = st.number_input("Tarifa por día (₡)", min_value=1000, value=st.session_state.info_cuidador["tarifa"], step=500)
                servicio_input = st.selectbox("Servicio principal", ["Hospedaje", "Guardería", "Paseos"], index=["Hospedaje", "Guardería", "Paseos"].index(st.session_state.info_cuidador["servicio"]))
                
                guardar_perfil = st.form_submit_button("Guardar Perfil")
                if guardar_perfil:
                    st.session_state.info_cuidador = {
                        "experiencia": ex_input,
                        "zona": zona_input,
                        "tarifa": tarifa_input,
                        "servicio": servicio_input
                    }
                    st.success("🎉 ¡Tu información de Cuidador se actualizó con éxito!")

        with tab2:
            st.markdown("### 🔎 Solicitudes de Cuidado Activas")
            st.write("Siguiente lista de dueños que necesitan tu atención urgente:")
            if len(st.session_state.solicitudes) == 0:
                st.info("🌈 No hay anuncios pendientes en este momento.")
            else:
                for idx, sol in enumerate(st.session_state.solicitudes):
                    st.markdown(f"""
                    <div class='card'>
                        <h3 style='margin-top:0; color:#ff7e5f; font-family: Fredoka;'>🐶 {sol['mascota']} ({sol['raza']})</h3>
                        <p style='margin: 5px 0;'><b>👤 Propietario:</b> {sol['propietario']}</p>
                        <p style='margin: 5px 0;'><b>📅 Fechas solicitadas:</b> {sol['fechas']}</p>
                        <p style='margin: 10px 0; font-style: italic; color:#555;'>" {sol['detalles']} "</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"🤝 Postularme para cuidar a {sol['mascota']}", key=f"btn_cuidador_{idx}"):
                        st.success(f"🎉 ¡Excelente! Te has postulado para cuidar a {sol['mascota']}. Se envió tu contacto a {sol['propietario']}.")
