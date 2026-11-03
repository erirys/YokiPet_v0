import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES AVANZADOS
# -----------------------------------------------------
st.set_page_config(page_title="YokiPet - Cuidado de Mascotas", page_icon="🐾", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Quicksand:wght@500;700&display=swap');

    .main {
        background-color: #fdfaf6;
        font-family: 'Quicksand', sans-serif;
        position: relative;
        overflow-x: hidden;
    }

    /* Título tradicional: Negro y Naranja con huellitas */
    .titulo-tradicional {
        font-family: 'Fredoka', sans-serif;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .titulo-yoki {
        color: #1a1a1a; /* Negro */
    }
    .titulo-pet {
        color: #ff7e5f; /* Naranja */
    }

    .creative-slogan {
        font-family: 'Fredoka', sans-serif;
        color: #4a4a4a;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 30px;
        background-color: #fff0eb;
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
        width: 100%;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Tarjetas con efecto 3D sutil y sombras */
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(255, 126, 95, 0.08);
        border-left: 6px solid #ff7e5f;
        margin-bottom: 22px;
        position: relative;
        z-index: 2; /* Por encima de las partículas flotantes */
    }

    .card-cuidador {
        border-left: 6px solid #2e7d32;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.08);
    }

    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        text-transform: uppercase;
    }
    .badge-pendiente {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
    }
    .badge-aprobado {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .badge-rechazado {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .aviso-prototipo {
        background: linear-gradient(90deg, #fff3cd 0%, #fef3d6 100%);
        color: #856404;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #ffeeba;
        text-align: center;
        font-weight: bold;
        margin-bottom: 25px;
        position: relative;
        z-index: 10;
    }

    /* Animaciones sutiles para elementos flotantes (Patitas, Plumas, Burbujas) */
    .area-flotante {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    }

    .elemento-flotante {
        position: absolute;
        bottom: -100px;
        font-size: 1.8rem;
        opacity: 0.25;
        animation: flotar 15s linear infinite;
    }

    @keyframes flotar { 
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0.25;
        }
        50% {
            opacity: 0.4;
        }
        100% {
            transform: translateY(-110vh) rotate(360deg);
            opacity: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Elementos flotantes sutiles decorando el fondo del formulario
st.markdown("""
<div class="area-flotante">
    <!-- Patitas flotantes -->
    <div class="elemento-flotante" style="left: 5%; animation-delay: 0s; animation-duration: 16s;">🐾</div>
    <div class="elemento-flotante" style="left: 85%; animation-delay: 2s; animation-duration: 18s;">🐾</div>
    <div class="elemento-flotante" style="left: 15%; animation-delay: 8s; animation-duration: 20s;">🐾</div>
    <!-- Plumas flotantes -->
    <div class="elemento-flotante" style="left: 25%; animation-delay: 1s; animation-duration: 22s;">🪶</div>
    <div class="elemento-flotante" style="left: 70%; animation-delay: 5s; animation-duration: 15s;">🪶</div>
    <div class="elemento-flotante" style="left: 50%; animation-delay: 9s; animation-duration: 19s;">🪶</div>
    <!-- Burbujas flotantes -->
    <div class="elemento-flotante" style="left: 40%; animation-delay: 3s; animation-duration: 14s; font-size: 1.2rem;">🧻</div>
    <div class="elemento-flotante" style="left: 90%; animation-delay: 6s; animation-duration: 17s; font-size: 1.5rem;">🧻</div>
    <div class="elemento-flotante" style="left: 60%; animation-delay: 11s; animation-duration: 21s; font-size: 1rem;">🧻</div>
</div>
""", unsafe_allow_html=True)

# Banner de advertencia obligatorio
st.markdown('<div class="aviso-prototipo">⚠️ Prototipo con datos ficticios. No se realizan reservas reales.</div>', unsafe_allow_html=True)

# Título e Identidad tradicional: Negro y Naranja con huellas acompañándolo
st.markdown('<h1 class="titulo-tradicional"><span class="titulo-yoki">🐾 Yoki</span><span class="titulo-pet">Pet 🐾</span></h1>', unsafe_allow_html=True)
st.markdown('<div class="creative-slogan">¿Quién cuidará de tus peluditos? ¡YOKI!</div>', unsafe_allow_html=True)

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

def obtener_explicacion_asistente(cuidadores_encontrados, mascota_info, moneda_simbolo):
    if not usar_ia or not client:
        return "*Modo sin IA activo. El catálogo determinista te asegura la mejor coincidencia según los filtros ingresados.*"

    prompt = f"""Actúa como un asistente experto de YokiPet.
    Analiza los siguientes cuidadores (YokiSitters) que cumplen con los filtros aplicados: {cuidadores_encontrados}.
    Explica brevemente y con un tono cálido al YokiParent de la mascota ({mascota_info}) por qué estas opciones son óptimas.
    Asegúrate de mostrar los precios usando el símbolo de moneda de visualización: {moneda_simbolo}.
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
# 3. LISTAS EXHAUSTIVAS DE PROVINCIAS Y ESTADOS (PAÍSES)
# -----------------------------------------------------
PAISES_CONFIG = {
    "Costa Rica": {
        "moneda": "CRC",
        "simbolo": "₡",
        "cambio_usd": 510.0,
        "zonas": ["San José", "Alajuela", "Cartago", "Heredia", "Guanacaste", "Puntarenas", "Limón"]
    },
    "México": {
        "moneda": "MXN",
        "simbolo": "Mex$",
        "cambio_usd": 17.0,
        "zonas": [
            "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua",
            "Coahuila", "Colima", "CDMX", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco",
            "Estado de México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
            "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas",
            "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
        ]
    },
    "Colombia": {
        "moneda": "COP",
        "simbolo": "Col$",
        "cambio_usd": 3900.0,
        "zonas": [
            "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá", "Caldas", "Caquetá",
            "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía", "Guaviare",
            "Huila", "La Guajira", "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo",
            "Quindío", "Risaralda", "San Andrés y Providencia", "Santander", "Sucre", "Tolima",
            "Valle del Cauca", "Vaupés", "Vichada"
        ]
    },
    "España": {
        "moneda": "EUR",
        "simbolo": "€",
        "cambio_usd": 0.92,
        "zonas": [
            "Andalucía", "Aragón", "Asturias", "Baleares", "Canarias", "Cantabria", "Castilla-La Mancha",
            "Castilla y León", "Cataluña", "Comunidad Valenciana", "Extremadura", "Galicia", "Madrid",
            "Murcia", "Navarra", "País Vasco", "La Rioja", "Ceuta", "Melilla"
        ]
    },
    "Estados Unidos": {
        "moneda": "USD",
        "simbolo": "$",
        "cambio_usd": 1.0,
        "zonas": [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
            "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
            "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
            "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
            "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
            "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
            "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
            "Wisconsin", "Wyoming"
        ]
    }
}

# -----------------------------------------------------
# 4. BASE DE DATOS FICTICIA INICIAL EN SESIÓN
# -----------------------------------------------------
if "sesion_iniciada" not in st.session_state:
    st.session_state.sesion_iniciada = False
if "usuario_nombre" not in st.session_state:
    st.session_state.usuario_nombre = ""
if "tipo_perfil" not in st.session_state:
    st.session_state.tipo_perfil = None
if "pais_seleccionado" not in st.session_state:
    st.session_state.pais_seleccionado = "Costa Rica"
if "tipo_moneda_vista" not in st.session_state:
    st.session_state.tipo_moneda_vista = "Local"

# Estructuras para Perfil del YokiParent
if "dueno_perfil" not in st.session_state:
    st.session_state.dueno_perfil = {
        "mascotas": [
            {"nombre": "Toby", "especie": "Perro", "raza": "Golden Retriever", "detalles": "Muy amigable, le gustan los paseos cortos."},
            {"nombre": "Félix", "especie": "Gato", "raza": "Mestizo", "detalles": "Independiente, asustadizo."},
            {"nombre": "Burbujas", "especie": "Pez", "raza": "Beta", "detalles": "Alimentar con hojuelas dos veces al día en cantidades pequeñas."}
        ],
        "metodo_pago": "Visa terminado en *4321 (Ficticio)",
        "direccion": "",
        "telefono_contacto": ""
    }

# Estructuras para Perfil del YokiSitter
if "info_cuidador" not in st.session_state:
    st.session_state.info_cuidador = {
        "experiencia": "Hola, amo mucho a todos los animales y tengo amplia experiencia cuidando peces, gatos y perros medianos.",
        "zona": "San José",
        "tarifa": 15.0,
        "servicio": "Hospedaje",
        "especies_aceptadas": ["Perro", "Gato", "Pez"],
        "completado": True
    }

if "solicitudes" not in st.session_state:
    st.session_state.solicitudes = [
        {
            "id": 0,
            "propietario": "María López",
            "mascotas": ["Toby"],
            "raza": "Perro, Golden Retriever",
            "fechas": "15/06/2025 al 20/06/2025",
            "detalles": "Necesita paseos dos veces al día. Muy amigable.",
            "estatus": "Pendiente",
            "postulantes": ["Andrés Fonseca"]
        },
        {
            "id": 1,
            "propietario": "Carlos Gómez",
            "mascotas": ["Félix"],
            "raza": "Gato, Mestizo",
            "fechas": "01/07/2025 al 05/07/2025",
            "detalles": "Solo requiere alimentación y limpieza de arenero una vez al día.",
            "estatus": "Pendiente",
            "postulantes": []
        }
    ]

cuidadores_base_db = [
    {"nombre": "Lucía Madrigal", "servicio": "Hospedaje", "zona_index": 0, "tarifa_usd": 20.0, "especies": ["Perro", "Gato"], "tamaño": "Todos"},
    {"nombre": "Andrés Fonseca", "servicio": "Paseos", "zona_index": 1, "tarifa_usd": 10.0, "especies": ["Perro"], "tamaño": "Mediano"},
    {"nombre": "Valeria Chaves", "servicio": "Guardería", "zona_index": 2, "tarifa_usd": 15.0, "especies": ["Gato", "Pez"], "tamaño": "Todos"}
]

PASSWORD_CORRECTA = "yoki123"

# -----------------------------------------------------
# 5. INGRESO SEGURO Y CONTROL DE ACCESO
# -----------------------------------------------------
if not st.session_state.sesion_iniciada:
    st.markdown("### 🔑 Ingreso Seguro a tu Cuenta YokiPet")
    st.write("Por favor introduce tu información, país y la contraseña demo `yoki123`.")

    with st.form("login_seguro"):
        nombre_input = st.text_input("Tu Nombre Completo")
        pais_input = st.selectbox("País del servicio", list(PAISES_CONFIG.keys()))
        perfil_seleccionado = st.selectbox("Selecciona tu perfil de acceso", ["YokiParent (Dueño)", "YokiSitter (Cuidador)"])
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
                st.session_state.pais_seleccionado = pais_input
                st.session_state.info_cuidador["zona"] = PAISES_CONFIG[pais_input]["zonas"][0]
                st.session_state.sesion_iniciada = True
                st.success("¡Acceso concedido exitosamente!")
                st.rerun()
else:
    config_actual = PAISES_CONFIG[st.session_state.pais_seleccionado]

    col_usr, col_mon, col_logout = st.columns([2, 1.5, 1])
    with col_usr:
        st.info(f"👤 **{st.session_state.usuario_nombre}** | {st.session_state.pais_seleccionado} ({st.session_state.tipo_perfil})")
    with col_mon:
        st.session_state.tipo_moneda_vista = st.radio("Visualización de Moneda:", ["Local", "USD"], horizontal=True, index=0 if st.session_state.tipo_moneda_vista == "Local" else 1)
    with col_logout:
        if st.button("Cerrar sesión"):
            st.session_state.sesion_iniciada = False
            st.session_state.usuario_nombre = ""
            st.session_state.tipo_perfil = None
            st.session_state.info_cuidador["completado"] = False
            st.rerun()

    def formatear_precio(tarifa_usd):
        if st.session_state.tipo_moneda_vista == "USD":
            return f"${tarifa_usd:.2f} USD"
        else:
            valor_local = tarifa_usd * config_actual["cambio_usd"]
            return f" {config_actual['simbolo']}{valor_local:,.0f} {config_actual['moneda']}"

    # -----------------------------------------------------
    # 6. PANEL DE YOKIPARENTS (DUEÑOS)
    # -----------------------------------------------------
    if st.session_state.tipo_perfil == "YokiParent (Dueño)":
        tab1, tab2, tab3 = st.tabs(["🙋‍♂️ Publicar Solicitud", "🔎 Buscar YokiSitter con IA", "⚙️ Mi Perfil YokiParent"])

        with tab1:
            st.markdown("### 📝 Publicar Solicitud de Cuidado Multimascota 🐾🪶🫧")
            st.write(f"Completa el formulario para publicar tu solicitud en **{st.session_state.pais_seleccionado}**.")

            lista_mascotas = st.session_state.dueno_perfil["mascotas"]

            if len(lista_mascotas) == 0:
                st.warning("⚠️ No tienes mascotas registradas. Ve a 'Mi Perfil YokiParent' para agregarlas.")
                lista_opciones_m = []
            else:
                lista_opciones_m = [pet["nombre"] for pet in lista_mascotas]

            mascotas_seleccionadas = st.multiselect("Selecciona una o más mascotas para cuidar", lista_opciones_m)

            with st.form("solicitud_form", clear_on_submit=True):
                nombre_dueño = st.text_input("Nombre del YokiParent", value=st.session_state.usuario_nombre, disabled=True)

                detalles_sugeridos = ""
                razas_sugeridas = ""
                if mascotas_seleccionadas:
                    detalles_partes = []
                    razas_partes = []
                    for nombre_sel in mascotas_seleccionadas:
                        pet_obj = next((item for item in lista_mascotas if item["nombre"] == nombre_sel), None)
                        if pet_obj:
                            detalles_partes.append(f"- {pet_obj['nombre']}: {pet_obj['detalles']}")
                            razas_partes.append(f"{pet_obj['nombre']} ({pet_obj['especie']} {pet_obj['raza']})")
                    detalles_sugeridos = "\n".join(detalles_partes)
                    razas_sugeridas = ", ".join(razas_partes)

                raza_mascota_disp = st.text_input("Mascotas e Identificación", value=razas_sugeridas if razas_sugeridas else "Escribe detalles adicionales si es necesario")

                col1, col2 = st.columns(2)
                with col1:
                    fecha_inicio = st.date_input("Desde", min_value=datetime.today())
                with col2:
                    fecha_fin = st.date_input("Hasta", min_value=datetime.today())

                detalles = st.text_area("Indicaciones o cuidados especiales agrupados", value=detalles_sugeridos)
                submit_button = st.form_submit_button("🚀 Publicar Anuncio de Cuidado")

                if submit_button:
                    if mascotas_seleccionadas:
                        nueva_solicitud = {
                            "id": len(st.session_state.solicitudes),
                            "propietario": nombre_dueño,
                            "mascotas": mascotas_seleccionadas,
                            "raza": raza_mascota_disp,
                            "fechas": f" {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}",
                            "detalles": detalles,
                            "estatus": "Pendiente",
                            "postulantes": []
                        }
                        st.session_state.solicitudes.append(nueva_solicitud)
                        st.balloons()
                        st.success(f"¡Genial! Tu solicitud para cuidar a {', '.join(mascotas_seleccionadas)} ha sido publicada con éxito.")
                    else:
                        st.error("❌ Por favor, selecciona al menos una mascota para publicar el anuncio.")

        with tab2:
            st.markdown("### 🔎 Buscador Inteligente de YokiSitters 🐾")
            st.write(f"Filtra nuestro catálogo en **{st.session_state.pais_seleccionado}** y encuentra tu cuidador ideal.")

            b_servicio = st.selectbox("Servicio requerido", ["Hospedaje", "Guardería", "Paseos"])
            b_zona = st.selectbox("Ubicación / Zona de servicio", config_actual["zonas"])
            b_especie = st.selectbox("Especie de mascota principal", ["Perro", "Gato", "Pez", "Ave", "Hámster", "Otro"])

            moneda_display = "USD" if st.session_state.tipo_moneda_vista == "USD" else config_actual["moneda"]
            b_presupuesto = st.number_input(f"Presupuesto máximo ({moneda_display})", min_value=1, value=50, step=5)
            presupuesto_usd = b_presupuesto if st.session_state.tipo_moneda_vista == "USD" else (b_presupuesto / config_actual["cambio_usd"])

            if st.button("Buscar YokiSitter ideal"):
                cat_local = []
                for i, c in enumerate(cuidadores_base_db):
                    c_copia = c.copy()
                    idx_zona = c["zona_index"] % len(config_actual["zonas"])
                    c_copia["zona"] = config_actual["zonas"][idx_zona]
                    cat_local.append(c_copia)

                encontrados = [
                    c for c in cat_local
                    if c['servicio'] == b_servicio
                    and c['zona'] == b_zona
                    and (b_especie in c['especies'] or 'Todos' in c.get('especies', []) or b_especie == 'Otro')
                    and c['tarifa_usd'] <= presupuesto_usd
                ]

                if encontrados:
                    st.success(f"Se encontraron {len(encontrados)} opciones que coinciden exactamente con tus criterios.")
                    info_mascota_busqueda = f"{b_especie} en la zona de {b_zona} para el servicio de {b_servicio}"
                    explicacion = obtener_explicacion_asistente(encontrados, info_mascota_busqueda, config_actual['simbolo'] if st.session_state.tipo_moneda_vista == 'Local' else '$')

                    st.markdown("### 🤖 Recomendación del Asistente YokiPet")
                    st.info(explicacion)

                    for cuid in encontrados:
                        precio_formateado = formatear_precio(cuid['tarifa_usd'])
                        especies_permitidas = ", ".join(cuid.get('especies', []))
                        st.markdown(f"""
                        <div class='card'>
                            <h3 style='margin-top:0; color:#2e7d32; font-family: Fredoka;'>⭐ {cuid['nombre']}</h3>
                            <p style='margin: 5px 0;'><b>📍 Zona:</b> {cuid['zona']} | <b>🛠️ Servicio:</b> {cuid['servicio']}</p>
                            <p style='margin: 5px 0;'><b>🐾 Especies que cuida:</b> {especies_permitidas}</p>
                            <p style='margin: 5px 0;'><b>💰 Tarifa por día:</b> {precio_formateado}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("😔 No se encontraron YokiSitters en el catálogo que coincidan exactamente con tus criterios.")

        with tab3:
            st.markdown("### ⚙️ Mi Perfil de YokiParent")

            st.markdown("#### 💳 Información de Perfil General")
            with st.form("dueño_info_form"):
                dir_input = st.text_input("Mi Dirección de Residencia", value=st.session_state.dueno_perfil["direccion"], placeholder="Ej: San José centro")
                tel_input = st.text_input("Número de Teléfono", value=st.session_state.dueno_perfil["telefono_contacto"], placeholder="Ej: +506 8888-8888")
                pago_input = st.selectbox("Método de Pago Preferido", ["Visa terminado en *4321 (Ficticio)", "Mastercard terminado en *9876 (Ficticio)", "YokiPay Wallet"])

                guardar_perfil_dueño = st.form_submit_button("Guardar Información de Perfil")
                if guardar_perfil_dueño:
                    st.session_state.dueno_perfil["direccion"] = dir_input
                    st.session_state.dueno_perfil["telefono_contacto"] = tel_input
                    st.session_state.dueno_perfil["metodo_pago"] = pago_input
                    st.success("✅ ¡Información de perfil actualizada exitosamente!")

            st.markdown("#### 🐠 Mis Mascotas Registradas 🐾🪶🫧")
            if len(st.session_state.dueno_perfil["mascotas"]) == 0:
                st.info("Aún no tienes mascotas registradas. Agrega una abajo.")
            else:
                for idx, pet in enumerate(st.session_state.dueno_perfil["mascotas"]):
                    col_pet_info, col_pet_del = st.columns([4, 1])
                    with col_pet_info:
                        emoji = "🐠" if pet['especie'] == 'Pez' else ("🐶" if pet['especie'] == 'Perro' else "🐱")
                        st.write(f"{emoji} **{pet['nombre']}** ({pet['especie']}) - *{pet['raza']}* | {pet['detalles']}")
                    with col_pet_del:
                        if st.button("🗑️", key=f"del_pet_{idx}"):
                            st.session_state.dueno_perfil["mascotas"].pop(idx)
                            st.rerun()

            st.markdown("##### ➕ Agregar nueva mascota")
            with st.form("add_mascota_form", clear_on_submit=True):
                n_nombre = st.text_input("Nombre de la mascota")
                n_especie = st.selectbox("Especie", ["Perro", "Gato", "Pez", "Ave", "Hámster", "Otro"])
                n_raza = st.text_input("Raza / Descripción física")
                n_detalles = st.text_area("Comportamiento o cuidados particulares")

                add_btn = st.form_submit_button("➕ Registrar Mascota")
                if add_btn:
                    if n_nombre.strip() == "":
                        st.error("Por favor introduce un nombre para tu mascota.")
                    else:
                        nueva_pet = {
                            "nombre": n_nombre,
                            "especie": n_especie,
                            "raza": n_raza,
                            "detalles": n_detalles
                        }
                        st.session_state.dueno_perfil["mascotas"].append(nueva_pet)
                        st.success(f"🎉 ¡{n_nombre} ha sido agregada a tu perfil!")
                        st.rerun()

            st.markdown("#### 📋 Mis Anuncios Publicados y Estado de Postulaciones")
            mis_solicitudes = [
                sol for sol in st.session_state.solicitudes
                if sol["propietario"] == st.session_state.usuario_nombre
            ]

            if len(mis_solicitudes) == 0:
                st.info("No has publicado ningún anuncio de cuidado activo en esta sesión.")
            else:
                for idx_sol, sol in enumerate(st.session_state.solicitudes):
                    if sol["propietario"] == st.session_state.usuario_nombre:
                        est_clase = "badge-pendiente" if sol['estatus'] == 'Pendiente' else ("badge-aprobado" if sol['estatus'] == 'Aprobado' else "badge-rechazado")
                        nombres_m = ", ".join(sol.get("mascotas", []))
                        st.markdown(f"""
                        <div style='background-color: #ffffff; padding: 20px; border-radius: 15px; margin-bottom: 15px; border: 1px solid #ff7e5f; box-shadow: 0 4px 10px rgba(0,0,0,0.02);'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <strong style='font-size: 1.15rem; color: #ff7e5f;'>🐾 Mascotas: {nombres_m}</strong>
                                <span class='badge {est_clase}'>{sol['estatus']}</span>
                            </div>
                            <div style='margin-top: 8px;'>
                                🏷️ <b>Detalles:</b> {sol['raza']}<br>
                                📅 <b>Fechas:</b> {sol['fechas']}<br>
                                📝 <b>Notas:</b> {sol['detalles']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if sol["estatus"] == "Pendiente":
                            if len(sol["postulantes"]) > 0:
                                st.write("👥 **YokiSitters postulados para este anuncio:**")
                                for postulante in sol["postulantes"]:
                                    c1, c2, c3 = st.columns([2, 1, 1])
                                    with c1:
                                        st.write(f"🔹 **{postulante}**")
                                    with c2:
                                        if st.button("✅ Aprobar", key=f"aprob_{sol['id']}_{postulante}"):
                                            sol["estatus"] = "Aprobado"
                                            st.success(f"¡Has aprobado a {postulante}!")
                                            st.rerun()
                                    with c3:
                                        if st.button("❌ Rechazar", key=f"rech_{sol['id']}_{postulante}"):
                                            sol["estatus"] = "Rechazado"
                                            st.warning(f"Has rechazado a {postulante}.")
                                            st.rerun()
                            else:
                                st.write("⏳ Aún no se han recibido postulaciones para esta solicitud.")

    # -----------------------------------------------------
    # 7. PANEL DE YOKISITTERS (CUIDADORES)
    # -----------------------------------------------------
    elif st.session_state.tipo_perfil == "YokiSitter (Cuidador)":
        tab1, tab2 = st.tabs(["🏡 Acceso a mi Perfil", "🔎 Solicitudes de Dueños Activas"])

        with tab1:
            st.markdown("### 🏡 Acceso a mi Perfil de YokiSitter")
            st.write(f"Gestiona tu experiencia, tarifas de servicio y revisa tus postulaciones en **{st.session_state.pais_seleccionado}**.")

            with st.form("perfil_cuidador_completo"):
                ex_input = st.text_area("Presentación, experiencia y cariño que ofreces",
                                        value=st.session_state.info_cuidador["experiencia"],
                                        placeholder="Ej: Cuento con certificación en primeros auxilios para mascotas y amo jugar...")

                col_perf1, col_perf2 = st.columns(2)
                with col_perf1:
                    zona_input = st.selectbox("Zona de servicio", config_actual["zonas"])
                with col_perf2:
                    servicio_input = st.selectbox("Servicio principal que ofrezco", ["Hospedaje", "Guardería", "Paseos"])

                # Selección múltiple de especies aceptadas por el YokiSitter
                especies_disponibles = ["Perro", "Gato", "Pez", "Ave", "Hámster", "Otro"]
                especies_seleccionadas = st.multiselect(
                    "🐾 Especies de animales que estoy dispuesto a cuidar (Selección múltiple)",
                    especies_disponibles,
                    default=st.session_state.info_cuidador.get("especies_aceptadas", ["Perro", "Gato"])
                )

                unidad_tarifa = "USD" if st.session_state.tipo_moneda_vista == "USD" else config_actual["moneda"]
                tarifa_input = st.number_input(f"Mi Tarifa sugerida por día ({unidad_tarifa})", min_value=1, value=20, step=5)

                guardar_perfil = st.form_submit_button("💾 Guardar y Actualizar Perfil")
                if guardar_perfil:
                    if ex_input.strip() == "":
                        st.error("⚠️ Por favor escribe una breve descripción sobre ti antes de guardar.")
                    elif not especies_seleccionadas:
                        st.error("⚠️ Selecciona al menos una especie de mascota que estás dispuesto a cuidar.")
                    else:
                        tarifa_en_usd = tarifa_input if st.session_state.tipo_moneda_vista == "USD" else (tarifa_input / config_actual["cambio_usd"])
                        st.session_state.info_cuidador = {
                            "experiencia": ex_input,
                            "zona": zona_input,
                            "tarifa": tarifa_en_usd,
                            "servicio": servicio_input,
                            "especies_aceptadas": especies_seleccionadas,
                            "completado": True
                        }
                        st.success("🎉 ¡Tu información de Perfil de YokiSitter ha sido actualizada!")

            # Vista previa estética de la tarjeta de presentación
            if st.session_state.info_cuidador["completado"]:
                st.markdown("#### 📇 Vista Previa de tu Tarjeta Pública")
                precio_formateado = formatear_precio(st.session_state.info_cuidador["tarifa"])
                especies_preview = ", ".join(st.session_state.info_cuidador.get("especies_aceptadas", []))
                st.markdown(f"""
                <div class='card card-cuidador'>
                    <h3 style='margin-top:0; color:#2e7d32; font-family: Fredoka;'>⭐ {st.session_state.usuario_nombre} (Tú)</h3>
                    <p style='margin: 5px 0;'><b>📍 Ubicación:</b> {st.session_state.info_cuidador['zona']} | <b>🛠️ Servicio:</b> {st.session_state.info_cuidador['servicio']}</p>
                    <p style='margin: 5px 0;'><b>🐾 Mascotas aceptadas:</b> {especies_preview}</p>
                    <p style='margin: 5px 0;'><b>💰 Tarifa por día:</b> {precio_formateado}</p>
                    <p style='margin: 10px 0; font-style: italic; color:#555;'>"{st.session_state.info_cuidador['experiencia']}"</p>
                </div>
                """, unsafe_allow_html=True)

            # Historial de postulaciones realizadas por este cuidador
            st.markdown("#### 📋 Mis Postulaciones Realizadas")
            postulaciones_hechas = [
                sol for sol in st.session_state.solicitudes
                if st.session_state.usuario_nombre in sol["postulantes"]
            ]

            if len(postulaciones_hechas) == 0:
                st.info("No has realizado ninguna postulación de cuidado todavía.")
            else:
                for sol in postulaciones_hechas:
                    est_clase = "badge-pendiente" if sol['estatus'] == 'Pendiente' else ("badge-aprobado" if sol['estatus'] == 'Aprobado' else "badge-rechazado")
                    nombres_m_sol = ", ".join(sol.get("mascotas", []))
                    st.markdown(f"""
                    <div style='background-color: #ffffff; padding: 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #d4edda; box-shadow: 0 4px 10px rgba(0,0,0,0.02);'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <strong>🐾 Solicitud de {sol['propietario']} ({nombres_m_sol})</strong>
                            <span class='badge {est_clase}'>{sol['estatus']}</span>
                        </div>
                        <p style='margin: 5px 0 0 0; font-size: 0.9rem; color: #666;'><b>📅 Fechas:</b> {sol['fechas']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        with tab2:
            st.markdown("### 🔎 Solicitudes de Cuidado Activas")
            st.write(f"YokiParents en **{st.session_state.pais_seleccionado}** que buscan tu ayuda:")

            if len(st.session_state.solicitudes) == 0:
                st.info("🌈 No hay anuncios pendientes en este momento.")
            else:
                for idx, sol in enumerate(st.session_state.solicitudes):
                    est_clase = "badge-pendiente" if sol['estatus'] == 'Pendiente' else ("badge-aprobado" if sol['estatus'] == 'Aprobado' else "badge-rechazado")
                    nombres_m_sol = ", ".join(sol.get("mascotas", []))
                    st.markdown(f"""
                    <div class='card'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <h3 style='margin-top:0; color:#ff7e5f; font-family: Fredoka;'>🐾 {nombres_m_sol}</h3>
                            <span class='badge {est_clase}'>{sol['estatus']}</span>
                        </div>
                        <p style='margin: 5px 0;'><b>👤 YokiParent:</b> {sol['propietario']}</p>
                        <p style='margin: 5px 0;'><b>🏷️ Mascotas:</b> {sol['raza']}</p>
                        <p style='margin: 5px 0;'><b>📅 Fechas solicitadas:</b> {sol['fechas']}</p>
                        <p style='margin: 10px 0; font-style: italic; color:#555;'>" {sol['detalles']} "</p>
                    </div>
                    """, unsafe_allow_html=True)

                    ya_postulado = st.session_state.usuario_nombre in sol["postulantes"]

                    if sol["estatus"] != "Pendiente":
                        st.write(f"🔒 *Esta solicitud ya está cerrada (Estado: {sol['estatus']})*.")
                    elif ya_postulado:
                        st.info("⏳ Ya te has postulado a este anuncio. Esperando la respuesta del YokiParent.")
                    else:
                        if st.button(f"🤝 Postularme para cuidar a {nombres_m_sol}", key=f"btn_cuidador_{idx}"):
                            sol["postulantes"].append(st.session_state.usuario_nombre)
                            st.success(f"🎉 ¡Te has postulado con éxito! Se notificará al YokiParent.")
                            st.rerun()
