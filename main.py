import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import requests

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Memento - VIH & Chatbot",
    page_icon="🎗️",
    layout="wide"
)

# Configuración de la API de DeepSeek
# (Sustituye por tu clave válida)
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la API de DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

if not DEEPSEEK_API_KEY:
    st.error("Falta la variable DEEPSEEK_API_KEY. Configúrala en tu archivo .env")
    st.stop()

# ---------------------------------------------------------
# 2. INYECCIÓN DE TUS ESTILOS CSS PERSONALIZADOS
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Tipografía para Encabezados h1, h2, h3 */
    h1, h2, h3 {
        font-family: 'Times New Roman', Times, serif !important;
        color: rgb(105, 2, 2) !important;
    }

    /* Estilo de Botones nativos (.button de tu CSS) */
    div.stButton > button {
        background-color: rgb(245, 242, 242) !important;
        color: rgb(161, 23, 23) !important;
        border: none !important;
        padding: 12px 28px !important;
        text-align: center !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }

    /* Efecto :hover para los botones */
    div.stButton > button:hover {
        background-color: rgb(141, 5, 5) !important;
        color: rgb(243, 241, 241) !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
    }

    /* Animación e iluminación para imágenes */
    .stImage img {
        border-radius: 8px;
        transition: box-shadow 0.3s ease, transform 0.3s ease !important;
    }

    .stImage img:hover {
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3) !important;
        transform: translateY(-4px) !important;
    }

    /* Tarjetas estilo (.fotos-card) con sombra roja */
    .fotos-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #f0f0f0;
        box-shadow: 0px 12px 25px 0px rgba(133, 20, 20, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }

    .fotos-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 16px 30px 0px rgba(133, 20, 20, 0.3);
    }

    /* Estilo del Logo circular */
    .logo-img {
        width: 150px;
        height: 150px;
        object-fit: cover;
        border-radius: 50%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .logo-img:hover {
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3);
        transform: translateY(-4px);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. LÓGICA DE LA API DE DEEPSEEK
# ---------------------------------------------------------
def enviar_mensaje(mensajes, modelo='deepseek-chat'):
    """Envía el historial de la conversación a la API de DeepSeek"""
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Instrucción inicial para orientar el modelo al contexto del sitio web
    system_prompt = {
        "role": "system",
        "content": "Eres un asistente virtual empático, educativo y respetuoso especializado en brindar información clara sobre la prevención, mitos y realidades del VIH en Colombia."
    }

    payload = [system_prompt] + mensajes

    data = {
        'model': modelo,
        'messages': payload
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            error_detail = response.json() if response.text else "Sin detalles"
            return f"❌ Error {response.status_code}: {error_detail}"

        return response.json()['choices'][0]['message']['content']

    except requests.exceptions.Timeout:
        return "⏰ Tiempo de espera agotado. Por favor, intenta de nuevo."
    except requests.exceptions.RequestException as e:
        return f"🔌 Error de conexión: {e}"
    except Exception as e:
        return f"⚠️ Error Inesperado: {e}"

# ---------------------------------------------------------
# 4. BARRA LATERAL Y NAVEGACIÓN
# ---------------------------------------------------------
st.sidebar.title("🎗️ Memento")
menu = st.sidebar.radio(
    "Ir a la sección:",
    ["Inicio", "Información", "🤖 Chatbot Asistente", "Testimonios", "Videos", "Galería", "Entidades"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Plataforma informativa y de prevención sobre el VIH en Colombia.")

# ---------------------------------------------------------
# 5. SECCIONES DE LA APLICACIÓN
# ---------------------------------------------------------

# --- INICIO ---
if menu == "Inicio":
    st.title("Ejemplo de Botones y Banners")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("Click aquí"):
            st.success("¡Hiciste click en el botón principal!")
    with col_b2:
        if st.button("Otro botón"):
            st.info("¡Hiciste click en el segundo botón!")

    st.markdown("---")
    st.title("Rompe paradigmas: Estigma")
    st.write("Romper el esquema sobre el VIH es reemplazar los prejuicios por información, respeto e inclusión hacia quienes viven con esta condición.")
    
    tab1, tab2, tab3 = st.tabs(["Rompe Paradigmas", "Prevención es Vida", "Historias que Hablan"])
    with tab1:
        st.subheader("El VIH no distingue de edad")
        st.info("Reemplazar prejuicios por información, respeto e inclusión.")
    with tab2:
        st.subheader("Prevención es vida")
        st.success("Informarse, cuidarse y actuar responsablemente protege nuestra salud y la de quienes nos rodean.")
    with tab3:
        st.subheader("Historias que hablan")
        st.warning("Los testimonios nos muestran experiencias reales que inspiran y educan.")

# --- INFORMACIÓN Y ESTADÍSTICAS ---
elif menu == "Información":
    st.title("¿Qué debes saber sobre el VIH?")
    st.caption("Información sobre el VIH para los jóvenes colombianos")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="fotos-card">
            <h3>¿Qué es el VIH?</h3>
            <p>El VIH es un virus que debilita el sistema inmunitario. No tiene cura, pero con tratamiento se controla por completo y se lleva una vida normal.</p>
        </div>
        <div class="fotos-card">
            <h3>¿Cómo se contagia?</h3>
            <p>Se transmite principalmente por relaciones sexuales sin preservativo, compartir jeringas o de madre a hijo. No se contagia por saliva, besos ni abrazos.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="fotos-card">
            <h3>¿Cuáles son sus síntomas?</h3>
            <p>En las primeras semanas puede causar una gripe leve, pero luego pasa años sin síntomas. La única forma de detectarlo es con una prueba de sangre.</p>
        </div>
        <div class="fotos-card">
            <h3>¿Cómo prevenir el VIH?</h3>
            <p>Se previene usando preservativo, no compartiendo jeringas y mediante medicamentos como la PrEP o la PEP.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 Indicadores Globales (2024)")

    # Tabla en Pandas
    df_stats = pd.DataFrame({
        "Indicador": [
            "Personas que viven con VIH",
            "Personas con tratamiento antirretroviral",
            "Nuevas infecciones por VIH",
            "Muertes relacionadas con el sida"
        ],
        "Cifra (Millones)": [40.8, 31.6, 1.3, 0.63]
    })

    st.table(df_stats)

    # Gráfico Plotly Express
    st.subheader("Gráfico Interactivo")
    fig_plotly = px.bar(
        df_stats, 
        x="Indicador", 
        y="Cifra (Millones)", 
        color="Indicador",
        title="Estadísticas de VIH a Nivel Mundial",
        text_auto=True
    )
    st.plotly_chart(fig_plotly, use_container_width=True)

# --- CHATBOT INTEGRADO CON DEEPSEEK ---
elif menu == "🤖 Chatbot Asistente":
    st.title("🤖 Chatbot Asistente sobre el VIH")
    st.write("Haz tus preguntas sobre prevención, tratamiento, síntomas y apoyo.")

    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()

    # Inicialización del historial
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Muestra los mensajes previos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto del usuario
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pensando respuesta..."):
                respuesta = enviar_mensaje(st.session_state.messages)
                st.markdown(respuesta)

        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# --- TESTIMONIOS ---
elif menu == "Testimonios":
    st.title("Testimonios")
    st.write("Historias reales para crear conciencia, promover la empatía y eliminar prejuicios.")

    t1, t2, t3 = st.columns(3)
    with t1:
        st.error('"Cuando recibí el diagnóstico sentí mucho miedo, pero con el apoyo de mi familia y el tratamiento aprendí que puedo seguir viviendo y cumpliendo mis metas."')
        st.caption("— **Laura, 24 años** (Barranquilla, Atlántico)")

    with t2:
        st.info('"Mi diagnóstico me enseñó a valorar cada día. Con responsabilidad y apoyo he demostrado que el VIH no define quién soy."')
        st.caption("— **Andrés, 21 años** (Tunja, Boyacá)")

    with t3:
        st.success('"Al conocer mi diagnóstico pensé que todo había cambiado. Con el tiempo entendí que puedo llevar una vida plena y seguir luchando por mis sueños."')
        st.caption("— **Sofía, 27 años** (Bogotá, Cundinamarca)")

# --- VIDEOS ---
elif menu == "Videos":
    st.title("Videos Informativos")
    st.write("Aprende más sobre el VIH en Colombia.")
    st.video("https://www.youtube.com/watch?v=BGPe8bqhTQk")
    st.video("https://www.youtube.com/watch?v=PNadccDpbOc")

# --- GALERÍA ---
elif menu == "Galería":
    st.title("Galería de Imágenes")
    st.caption("Imágenes de campañas y acciones de prevención del VIH.")

    # Reemplaza las URLs de placeholder por las rutas de tus imágenes ('img/gal1.png') cuando estés listo
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.image("https://via.placeholder.com/400x300/851414/FFFFFF?text=Campa%C3%B1a+1", caption="Campaña de prevención 1")
        st.image("https://via.placeholder.com/400x300/851414/FFFFFF?text=Campa%C3%B1a+4", caption="Campaña de prevención 4")
    with col_g2:
        st.image("https://via.placeholder.com/400x300/851414/FFFFFF?text=Campa%C3%B1a+2", caption="Campaña de prevención 2")
        st.image("https://via.placeholder.com/400x300/851414/FFFFFF?text=Campa%C3%B1a+5", caption="Campaña de prevención 5")
    with col_g3:
        st.image("https://via.placeholder.com/400x300/851414/FFFFFF?text=Campa%C3%B1a+3", caption="Campaña de prevención 3")
        st.image("https://via.placeholder.com/400x300/851414/FFFFFF?text=Campa%C3%B1a+6", caption="Campaña de prevención 6")

# --- ENTIDADES ---
elif menu == "Entidades":
    st.title("Entidades de Prevención en Colombia")

    entidades = [
        {"nombre": "FUNDACIÓN EUDES", "link": "https://fundacioneudes.co/"},
        {"nombre": "FUNDACIÓN AHF COLOMBIA", "link": "https://ahfcolombia.org.co/"},
        {"nombre": "FUNDACIÓN SANTA FE DE BOGOTÁ", "link": "https://fundacionsantafedebogota.com/"},
        {"nombre": "AIDS HEALTHCARE FOUNDATION", "link": "https://www.aidshealth.org/"},
        {"nombre": "FUNDACIÓN NACIONAL ANCLA", "link": "https://fundacionancla.co/"}
    ]

    for ent in entidades:
        st.markdown(f"💎 **[{ent['nombre']}]({ent['link']})**")
        st.write("Fundación de prevención e información sobre el VIH en Colombia.")
        st.markdown("---")
