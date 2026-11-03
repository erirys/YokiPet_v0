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
    }

    /* Tarjetas con efecto 3D sutil, gradientes de borde y sombras profundas */
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(255, 126, 95, 0.08);
        border-left: 6px solid #ff7e5f;
        margin-bottom: 22px;
        transition: transform 0.3s, box-shadow 0.3s;
        border-top: 1px solid rgba(255, 126, 95, 0.1);
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(255, 126, 95, 0.15);
    }

    /* Tarjeta específica para el perfil del YokiSitter */
    .card-cuidador {
        border-left: 6px solid #2e7d32;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.08);
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

    /* Insignias de estatus visuales y dinámicas */
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

    /* Banner Visualmente Atractivo */
    .hero-banner {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
        border-radius: 20px;
        padding: 30px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(255, 126, 95, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Banner de advertencia obligatorio
st.markdown('<div class="aviso-prototipo">⚠️ Prototipo con datos ficticios. No se realizan reservas reales.</div>', unsafe_allow_html=True)

# Hero Banner Visual con temática de Patitas, Plumas y Burbujas
st.markdown("""
<div class="hero-banner">
    <h1 style='color: white; margin: 0; font-family: "Fredoka"; font-size: 2.8rem;'>🐾 YokiPet 🪶</h1>
    <p style='margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;'>🫧 Encuentra amor, seguridad y compañía confiable para tus mascotas preferidas 🫧</p>
</div>
""", unsafe_allow_html=True)

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
            
