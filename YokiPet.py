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
    <div class="elemento-flotante" style="left: 40%; animation-delay: 3s; animation-duration: 14s; font-size: 1.2rem;">🫧</div>
    <div class="elemento-flotante" style="left: 90%; animation-delay: 6s; animation-duration: 17s; font-size: 1.5rem;">🫧</div>
    <div class="elemento-flotante" style="left: 60%; animation-delay: 11s; animation-duration: 21s; font-size: 1rem;">🫧</div>
</div>
""", unsafe_allow_html=True)

# Banner de advertencia obligatorio
st.markdown('<div class="aviso-prototipo">⚠️ Prototipo con datos ficticios. No se realizan reservas reales.</div>', unsafe_allow_html=True)

# Título e Identidad tradicional: Negro y Naranja con huellas acompañándolo
st.markdown('<h1 class="titulo-tradicional"><span class="titulo-yoki">🐾 Yoki</span><span class="titulo-pet">Pet 🐾</span></h1>', unsafe_allow_html=True)
st.markdown('<div class="creative-slogan">Encuentra amor, seguridad y compañía confiable para tus mascotas preferidas</div>', unsafe_allow_html=True)

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
            
