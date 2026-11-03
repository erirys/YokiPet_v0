import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES MEJORADOS
# -----------------------------------------------------
st.set_page_config(page_title="YokiPet - Cuidado de Mascotas", page_icon="🐾", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Quicksand:wght@500;700&display=swap');

    .main {
        background-color: #fdfaf6;
        font-family: 'Quicksand', sans-serif;
    }

    /* Tarjetas con efecto 3D sutil y degradados */
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(255, 126, 95, 0.08);
        border-left: 6px solid #ff7e5f;
        margin-bottom: 22px;
        transition: transform 0.2s, box-shadow 0.2s;
        border-top: 1px solid rgba(255, 126, 95, 0.1);
    }
    
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(255, 126, 95, 0.15);
    }

    /* Tarjeta específica para el perfil del cuidador */
    .card-cuidador {
        border-left: 6px solid #2e7d32;
        box-shadow: 0 8px 24px rgba(46, 125, 50, 0.08);
    }

    .main-title {
        font-family: 'Fredoka', sans-serif;
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 50%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2px;
        filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.05));
    }

    .creative-slogan {
        font-family: 'Fredoka', sans-serif;
        color: #4a4a4a;
        font-size: 1.4rem;
        text-align: center;
        margin-bottom: 30px;
        background: linear-gradient(120deg, #fff0eb 0%, #ffe5dc 100%);
        padding: 12px 24px;
        border-radius: 25px;
        display: inline-block;
        width: 100%;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.03);
        border: 1px solid rgba(255, 126, 95, 0.15);
    }

    .slogan-highlight {
        color: #ff7e5f;
        font-weight: 700;
    }

    /* Insignias de estatus visuales y atractivas */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-align: center;
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
        box-shadow: 0 4px 10px rgba(133, 100, 4, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Banner de advertencia obligatorio
st.markdown('<div class="aviso-prototipo">⚠️ Prototipo con datos ficticios. No se realizan reservas reales.</div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🐾 YokiPet</h1>', unsafe_allow_html=True)
st.markdown('<div class="creative-slogan">La red de confianza para el cuidado de tus <span class="slogan-highlight">mascotas</span></div>', unsafe_allow_html=True)

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
    Analiza los siguientes cuidadores que cumplen con los filtros aplicados: {cuidadores_encontrados}.
    Explica brevemente y con un tono cálido al propietario de la mascota ({mascota_info}) por qué estas opciones son óptimas.
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
# 3. CONFIGURACIÓN DE PAÍSES Y TIPOS DE CAMBIO
# -----------------------------------------------------
PAISES_CONFIG = {
    "Costa Rica": {"moneda": "CRC", "simbolo": "₡", "cambio_usd": 510.0, "zonas": ["San José", "Heredia", "Alajuela"]},
    "México": {"moneda": "MXN", "simbolo": "Mex$", "cambio_usd": 17.0, "zonas": ["CDMX", "Guadalajara", "Monterrey"]},
    "Colombia": {"moneda": "COP", "simbolo": "Col$", "cambio_usd": 3900.0, "zonas": ["Bogotá", "Medellín", "Cali"]},
    "España": {"moneda": "EUR", "simbolo": "€", "cambio_usd": 0.92, "zonas": ["Madrid", "Barcelona", "Valencia"]},
    "Estados Unidos": {"moneda": "USD", "simbolo": "$", "cambio_usd": 1.0, "zonas": ["Miami", "Nueva York", "Los Ángeles"]}
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

# Estructuras para Perfil del Dueño
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

if "info_cuidador" not in st.session_state:
    st.session_state.info_cuidador = {
        "experiencia": "",
        "zona": "San José",
        "tarifa": 8000,
        "servicio": "Hospedaje",
        "completado": False
    }

if "solicitudes" not in st.session_state:
    st.session_state.solicitudes = [
        {
            "id": 0,
            "propietario": "María López",
            "mascota": "Toby",
            "raza": "Perro, Golden Retriever",
            "fechas": "15/06/2025 al 20/06/2025",
            "detalles": "Necesita paseos dos veces al día. Muy amigable.",
            "estatus": "Pendiente",
            "postulantes": ["Andrés Fonseca"]
        },
        {
            "id": 1,
            "propietario": "Carlos Gómez",
            "mascota": "Michi",
            "raza": "Gato, Siamés",
            "fechas": "01/07/2025 al 05/07/2025",
            "detalles": "Solo requiere alimentación y limpieza de arenero una vez al día.",
            "estatus": "Pendiente",
            "postulantes": []
        }
    ]

cuidadores_base_db = [
    {"nombre": "Lucía Madrigal", "servicio": "Hospedaje", "zona_index": 0, "tarifa_usd": 20.0, "especie": "Perro", "tamaño": "Todos"},
    {"nombre": "Andrés Fonseca", "servicio": "Paseos", "zona_index": 1, "tarifa_usd": 10.0, "especie": "Perro", "tamaño": "Mediano"},
    {"nombre": "Valeria Chaves", "servicio": "Guardería", "zona_index": 2, "tarifa_usd": 15.0, "especie": "Gato", "tamaño": "Todos"}
]

PASSWORD_CORRECTA = "yoki123"

# -----------------------------------------------------
# 5. FLUJO DE CONTROL DE ACCESO CON PAÍS Y CONTRASEÑA
# -----------------------------------------------------
if not st.session_state.sesion_iniciada:
    st.markdown("### 🔑 Ingreso Seguro a tu Cuenta YokiPet")
    st.write("Por favor introduce tu información, país y la contraseña demo `yoki123`.")

    with st.form("login_seguro"):
        nombre_input = st.text_input("Tu Nombre Completo")
        pais_input = st.selectbox("País del servicio", list(PAISES_CONFIG.keys()))
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
            return f"{config_actual['simbolo']}{valor_local:,.0f} {config_actual['moneda']}"

    # -----------------------------------------------------
    # 6. DIRECCIONAMIENTO INTELIGENTE SEGÚN PERFIL
    # -----------------------------------------------------
    if st.session_state.tipo_perfil == "Dueño de Mascota":
        tab1, tab2, tab3 = st.tabs(["🙋‍♂️ Publicar Solicitud", "🔎 Buscar Cuidador con IA", "⚙️ Mi Perfil de Dueño"])

        with tab1:
            st.markdown("### 📝 Publicar Solicitud de Cuidado")
            st.write(f"Completa el formulario para publicar tu solicitud en **{st.session_state.pais_seleccionado}**.")

            lista_mascotas = st.session_state.dueno_perfil["mascotas"]
            
            if len(lista_mascotas) == 0:
                st.warning("⚠️ No tienes mascotas registradas. Ve a la pestaña 'Mi Perfil de Dueño' para agregar tus mascotas.")
                pet_names = ["Escribir manualmente"]
            else:
                pet_names = [pet["nombre"] for pet in lista_mascotas] + ["Otra mascota"]

            mascota_seleccionada = st.selectbox("Seleccionar mascota para la solicitud", pet_names)

            with st.form("solicitud_form", clear_on_submit=True):
                nombre_dueño = st.text_input("Nombre del dueño", value=st.session_state.usuario_nombre, disabled=True)
                
                if mascota_seleccionada != "Otra mascota" and mascota_seleccionada != "Escribir manualmente" and len(lista_mascotas) > 0:
                    datos_pet = next((item for item in lista_mascotas if item["nombre"] == mascota_seleccionada), None)
                    nombre_mascota = st.text_input("Nombre de tu mascota", value=datos_pet["nombre"], disabled=True)
                    raza_mascota = st.text_input("Especie / Raza", value=f"{datos_pet['especie']} ({datos_pet['raza']})", disabled=True)
                    detalles_def = datos_pet["detalles"]
                else:
                    nombre_mascota = st.text_input("Nombre de tu mascota")
                    raza_mascota = st.text_input("Especie / Raza (ej: Gato Siamés, Perro Poodle)")
                    detalles_def = ""

                col1, col2 = st.columns(2)
                with col1:
                    fecha_inicio = st.date_input("Desde", min_value=datetime.today())
                with col2:
                    fecha_fin = st.date_input("Hasta", min_value=datetime.today())

                detalles = st.text_area("Indicaciones o cuidados especiales", value=detalles_def)
                submit_button = st.form_submit_button("🚀 Publicar Anuncio de Cuidado")

                if submit_button:
                    if nombre_mascota:
                        nueva_solicitud = {
                            "id": len(st.session_state.solicitudes),
                            "propietario": nombre_dueño,
                            "mascota": nombre_mascota,
                            "raza": raza_mascota if raza_mascota else "Especie indeterminada",
                            "fechas": f"{fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}",
                            "detalles": detalles,
                            "estatus": "Pendiente",
                            "postulantes": []
                        }
                        st.session_state.solicitudes.append(nueva_solicitud)
                        st.balloons()
                        st.success(f"¡Genial! Tu solicitud para cuidar a {nombre_mascota} ha sido publicada con éxito.")
                    else:
                        st.error("❌ Por favor, ingresa el nombre de tu mascota.")

        with tab2:
            st.markdown("### 🔎 Buscador Inteligente de Cuidadores")
            st.write(f"Filtra nuestro catálogo en **{st.session_state.pais_seleccionado}** y deja que el asistente te recomiende las mejores opciones.")

            b_servicio = st.selectbox("Servicio requerido", ["Hospedaje", "Guardería", "Paseos"])
            b_zona = st.selectbox("Ubicación / Zona de servicio", config_actual["zonas"])
            b_especie = st.selectbox("Especie de mascota", ["Perro", "Gato", "Pez", "Ave", "Otro"])

            moneda_display = "USD" if st.session_state.tipo_moneda_vista == "USD" else config_actual["moneda"]
            b_presupuesto = st.number_input(f"Presupuesto máximo ({moneda_display})", min_value=1, value=50, step=5)
            presupuesto_usd = b_presupuesto if st.session_state.tipo_moneda_vista == "USD" else (b_presupuesto / config_actual["cambio_usd"])

            if st.button("Buscar Cuidador ideal"):
                cat_local = []
                for i, c in enumerate(cuidadores_base_db):
                    c_copia = c.copy()
                    c_copia["zona"] = config_actual["zonas"][c["zona_index"]]
                    cat_local.append(c_copia)

                encontrados = [
                    c for c in cat_local
                    if c['servicio'] == b_servicio
                    and c['zona'] == b_zona
                    and (c['especie'] == b_especie or c['especie'] == 'Todos' or b_especie == 'Otro')
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
                        st.markdown(f"""
                        <div class='card'>
                            <h3 style='margin-top:0; color:#2e7d32; font-family: Fredoka;'>⭐ {cuid['nombre']}</h3>
                            <p style='margin: 5px 0;'><b>📍 Zona:</b> {cuid['zona']} | <b>🛠️ Servicio:</b> {cuid['servicio']}</p>
                            <p style='margin: 5px 0;'><b>💰 Tarifa por día:</b> {precio_formateado}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("😔 No se encontraron cuidadores en el catálogo que coincidan exactamente con tus criterios.")

        with tab3:
            st.markdown("### ⚙️ Mi Perfil de Dueño de Mascotas")
            
            st.markdown("#### 💳 Información de Perfil General")
            with st.form("dueño_info_form"):
                dir_input = st.text_input("Mi Dirección de Residencia", value=st.session_state.dueno_perfil["direccion"], placeholder="Ej: Barrio Amón, San José")
                tel_input = st.text_input("Número de Teléfono", value=st.session_state.dueno_perfil["telefono_contacto"], placeholder="Ej: +506 8888-8888")
                pago_input = st.selectbox("Método de Pago Preferido", ["Visa terminado en *4321 (Ficticio)", "Mastercard terminado en *9876 (Ficticio)", "YokiPay Wallet"])
                
                guardar_perfil_dueño = st.form_submit_button("Guardar Información de Perfil")
                if guardar_perfil_dueño:
                    st.session_state.dueno_perfil["direccion"] = dir_input
                    st.session_state.dueno_perfil["telefono_contacto"] = tel_input
                    st.session_state.dueno_perfil["metodo_pago"] = pago_input
                    st.success("✅ ¡Información de perfil actualizada exitosamente!")

            # Sub-sección 2: Mis Mascotas Registradas (Agregar / Eliminar)
            st.markdown("#### 🐠 Mis Mascotas Registradas")
            
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

            # Sub-sección 3: Historial y Control de Publicaciones
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
                        st.markdown(f"""
                        <div style='background-color: #ffffff; padding: 20px; border-radius: 15px; margin-bottom: 15px; border: 1px solid #ff7e5f; box-shadow: 0 4px 10px rgba(0,0,0,0.02);'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <strong style='font-size: 1.15rem; color: #ff7e5f;'>🐾 {sol['mascota']} ({sol['raza']})</strong>
                                <span class='badge {est_clase}'>{sol['estatus']}</span>
                            </div>
                            <div style='margin-top: 8px;'>
                                📅 <b>Fechas:</b> {sol['fechas']}<br>
                                📝 <b>Notas:</b> {sol['detalles']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Visualizar postulaciones recibidas para este anuncio específico
                        if sol["estatus"] == "Pendiente":
                            if len(sol["postulantes"]) > 0:
                                st.write("👥 **Cuidadores postulados para este anuncio:**")
                                for postulante in sol["postulantes"]:
                                    c1, c2, c3 = st.columns([2, 1, 1])
                                    with c1:
                                        st.write(f"🔹 **{postulante}** se ofreció para cuidar a {sol['mascota']}.")
                                    with c2:
                                        if st.button("✅ Aprobar", key=f"aprob_{sol['id']}_{postulante}"):
                                            sol["estatus"] = "Aprobado"
                                            st.success(f"¡Has aprobado a {postulante} para el cuidado de {sol['mascota']}!")
                                            st.rerun()
                                    with c3:
                                        if st.button("❌ Rechazar", key=f"rech_{sol['id']}_{postulante}"):
                                            sol["estatus"] = "Rechazado"
                                            st.warning(f"Has rechazado la postulación de {postulante}.")
                                            st.rerun()
                            else:
                                st.write("⏳ Aún no se han recibido postulaciones para esta solicitud.")

    elif st.session_state.tipo_perfil == "Cuidador de Mascota":
        tab1, tab2 = st.tabs(["🏡 Mi Perfil de Cuidador", "🔎 Solicitudes de Dueños Activas"])

        with tab1:
            st.markdown("### 🏡 Mi Perfil de Cuidador Profesional")
            st.write(f"Completa tu información de servicio para el mercado de **{st.session_state.pais_seleccionado}**.")

            with st.form("perfil_cuidador"):
                ex_input = st.text_area("Presentación, experiencia y cariño que ofreces",
                                        value=st.session_state.info_cuidador["experiencia"],
                                        placeholder="Ej: Tengo 5 años de experiencia cuidando perritos medianos, me encanta sacarlos a pasear al parque...")
                zona_input = st.selectbox("Zona de servicio", config_actual["zonas"])

                unidad_tarifa = "USD" if st.session_state.tipo_moneda_vista == "USD" else config_actual["moneda"]
                tarifa_input = st.number_input(f"Mi Tarifa sugerida por día ({unidad_tarifa})", min_value=1, value=20, step=5)
                servicio_input = st.selectbox("Servicio principal que ofrezco", ["Hospedaje", "Guardería", "Paseos"])

                guardar_perfil = st.form_submit_button("💾 Guardar y Actualizar Perfil")
                if guardar_perfil:
                    if ex_input.strip() == "":
                        st.error("⚠️ Por favor escribe una breve descripción sobre ti antes de guardar.")
                    else:
                        tarifa_en_usd = tarifa_input if st.session_state.tipo_moneda_vista == "USD" else (tarifa_input / config_actual["cambio_usd"])
                        st.session_state.info_cuidador = {
                            "experiencia": ex_input,
                            "zona": zona_input,
                            "tarifa": tarifa_en_usd,
                            "servicio": servicio_input,
                            "completado": True
                        }
                        st.success("🎉 ¡Tu información de Cuidador se actualizó con éxito en el sistema!")

            if st.session_state.info_cuidador["completado"]:
                st.markdown("#### 📇 Vista Previa de tu Tarjeta de Presentación")
                precio_formateado = formatear_precio(st.session_state.info_cuidador["tarifa"])
                st.markdown(f"""
                <div class='card card-cuidador'>
                    <h3 style='margin-top:0; color:#2e7d32; font-family: Fredoka;'>⭐ {st.session_state.usuario_nombre} (Tú)</h3>
                    <p style='margin: 5px 0;'><b>📍 Zona:</b> {st.session_state.info_cuidador['zona']} | <b>🛠️ Servicio:</b> {st.session_state.info_cuidador['servicio']}</p>
                    <p style='margin: 5px 0;'><b>💰 Tarifa por día:</b> {precio_formateado}</p>
                    <p style='margin: 10px 0; font-style: italic; color:#555;'>"{st.session_state.info_cuidador['experiencia']}"</p>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.markdown("### 🔎 Solicitudes de Cuidado Activas")
            st.write(f"Estos dueños de mascotas en **{st.session_state.pais_seleccionado}** necesitan tu ayuda urgentemente:")
            
            if len(st.session_state.solicitudes) == 0:
                st.info("🌈 No hay anuncios pendientes en este momento.")
            else:
                for idx, sol in enumerate(st.session_state.solicitudes):
                    est_clase = "badge-pendiente" if sol['estatus'] == 'Pendiente' else ("badge-aprobado" if sol['estatus'] == 'Aprobado' else "badge-rechazado")
                    
                    st.markdown(f"""
                    <div class='card'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <h3 style='margin-top:0; color:#ff7e5f; font-family: Fredoka;'>🐶 {sol['mascota']} ({sol['raza']})</h3>
                            <span class='badge {est_clase}'>{sol['estatus']}</span>
                        </div>
                        <p style='margin: 5px 0;'><b>👤 Propietario:</b> {sol['propietario']}</p>
                        <p style='margin: 5px 0;'><b>📅 Fechas solicitadas:</b> {sol['fechas']}</p>
                        <p style='margin: 10px 0; font-style: italic; color:#555;'>" {sol['detalles']} "</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Control de postulaciones dinámicas del cuidador conectado
                    ya_postulado = st.session_state.usuario_nombre in sol["postulantes"]
                    
                    if sol["estatus"] != "Pendiente":
                        st.write(f"🔒 *Esta solicitud ya está cerrada (Estado: {sol['estatus']})*.")
                    elif ya_postulado:
                        st.info("⏳ Ya te has postulado a este anuncio. Esperando aprobación del dueño de la mascota.")
                    else:
                        if st.button(f"🤝 Postularme para cuidar a {sol['mascota']}", key=f"btn_cuidador_{idx}"):
                            sol["postulantes"].append(st.session_state.usuario_nombre)
                            st.success(f"🎉 ¡Excelente! Te has postulado para cuidar a {sol['mascota']}. Se notificó a {sol['propietario']}.")
                            st.rerun()
