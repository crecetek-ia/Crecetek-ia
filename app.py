import pandas as pd
import streamlit as st
from google import genai

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Lion Tech | Centro de Comando Comercial & IA",
    page_icon="🦁",
    layout="wide",
)

# ==========================================
# 2. ESTILO VISUAL PREMIUM INDUSTRIAL
# ==========================================
st.markdown(
    """
    <style>
    /* Fondo principal y texto general */
    .stApp { background-color: #fefefb; color: #000000 !important; }
    html, body, p, label, h1, h2, h3, h4, h5, h6, .stMarkdown, span, div {
        color: #000000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #f4f4ee !important;
        border-right: 1px solid #e2e2d8;
    }
    
    /* Botones de expandir/contraer */
    [data-testid="stSidebarCollapseButton"] button, 
    button[aria-label="Close sidebar"], 
    button[aria-label="Open sidebar"],
    [data-testid="stHeader"] button {
        background-color: #1b7a3e !important;
        border: 1px solid #145c2e !important;
        border-radius: 50% !important;
    }
    
    /* Botones principales */
    .stButton>button, button[data-testid="baseButton-secondaryFormSubmit"] {
        background-color: #1b7a3e !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 0.6rem 1.4rem !important;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #145c2e !important;
        color: #ffffff !important;
    }
    
    /* Inputs y Textareas */
    .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
    }
    
    /* Tarjetas Semáforo (Módulo 3) */
    .semaforo-card {
        padding: 15px; border-radius: 8px; margin-bottom: 15px; font-weight: bold;
    }
    .semaforo-verde { background-color: #e8f5e9; border-left: 6px solid #2e7d32; color: #1b5e20 !important; }
    .semaforo-amarillo { background-color: #fffde7; border-left: 6px solid #fbc02d; color: #f57f17 !important; }
    .semaforo-rojo { background-color: #ffebee; border-left: 6px solid #c62828; color: #b71c1c !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# REGLAS CORPORATIVAS (PROMPT BASE)
# ==========================================
NORMATIVA_CORPORATIVA = """
NORMATIVA CORPORATIVA DE PUBLICACIÓN (LT-MAN-MKT-001 - LION TECH):
- Títulos en Mercado Libre: Seguir fórmula obligatoria: [Tipo de producto] + [Conector] + [Modelo del equipo].
- Conectores válidos: "compatible con", "de repuesto para", "para", "adaptador para".
- Abreviaciones obligatorias: Samsung -> SAM, iPhone/Apple -> IPH, AirPods -> TWS o BT, Xiaomi -> XMI, Huawei -> HW.
- Términos prohibidos: "original", "AAA", "1:1", "G5", "réplica", "clon", "calidad premium", "tipo AirPods", "importado de fábrica".
- Exigencia SENIAT (Venezuela): Incluir RIF de la empresa en publicaciones comerciales y posts.
- Nota obligatoria: "Este producto es un artículo de reemplazo de terceros, diseñado para ser compatible con los modelos indicados. No es un componente fabricado por la marca original."
"""

# ==========================================
# 3. BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("🦁 Lion Tech IA")
    st.caption("Centro de Comando Comercial & E-Commerce")
    st.markdown("---")
    
    api_key = st.text_input("🔑 API Key de Gemini:", type="password", help="Pega aquí tu API Key de Google AI Studio")
    
    # Modelos de nueva generación (Actualizados)
    modelo_gemini = st.selectbox(
        "🤖 Modelo Gemini:",
        ["gemini-3.8-flash", "gemini-3.8-pro"],
        index=0
    )
    
    st.markdown("---")
    modulo = st.radio(
        "📌 Selecciona un Módulo:",
        [
            "1. Cotizador de Mostrador",
            "2. Analista de Inventario",
            "3. Auditor de Precios & Objeciones",
            "4. Transformador de Catálogo",
        ],
    )

# Inicializar Cliente API de forma segura
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"Error inicializando API: {e}")

# ==========================================
# MÓDULO 1: COTIZADOR DE MOSTRADOR
# ==========================================
if modulo == "1. Cotizador de Mostrador":
    st.title("🛒 Módulo 1: Asistente de Mostrador")
    st.caption("Respuesta rápida multicanal alineada con inventario y normativas.")

    col1, col2 = st.columns(2)
    with col1:
        consulta = st.text_area(
            "Consulta del cliente o vendedor:",
            height=120,
            placeholder="Ej: Cliente pregunta por kit de herramientas RF4 y pantalla para IPH 11, quiere saber precio total, descuento y garantía.",
        )
    with col2:
        productos_file = st.file_uploader("Carga inventario (.csv o .txt):", type=["csv", "txt"])
        
    btn1 = st.button("🚀 Generar Cotización")

    if btn1:
        if not api_key:
            st.error("⚠️ Ingresa tu API Key en la barra lateral.")
        elif not consulta:
            st.warning("⚠️ Escribe la consulta del cliente.")
        else:
            with st.spinner("Procesando respuesta con IA..."):
                contexto = "Base de datos no cargada (Usar conocimiento general)."
                if productos_file:
                    try:
                        if productos_file.name.endswith(".csv"):
                            df = pd.read_csv(productos_file)
                            contexto = f"BASE DE DATOS:\n{df.head(50).to_string()}\n"
                        else:
                            contexto = f"BASE DE DATOS:\n{productos_file.read().decode('utf-8')}\n"
                    except Exception as ex:
                        st.warning(f"Error al leer archivo: {ex}")

                prompt = f"""
                {NORMATIVA_CORPORATIVA}
                CONTEXTO DE INVENTARIO: {contexto}
                SOLICITUD: "{consulta}"
                
                Genera DOS respuestas separadas.
                ---RESPUESTA_WHATSAPP---
                Mensaje persuasivo, emojis, saludo, viñetas, total calculado y llamada a la acción.
                ---RESPUESTA_MOSTRADOR---
                Ficha técnica sobria sin emojis, especificaciones y términos de garantía.
                """
                try:
                    res = client.models.generate_content(model=modelo_gemini, contents=prompt)
                    raw = res.text
                    
                    if "---RESPUESTA_MOSTRADOR---" in raw:
                        partes = raw.split("---RESPUESTA_MOSTRADOR---")
                        wa = partes[0].replace("---RESPUESTA_WHATSAPP---", "").strip()
                        ml = partes[1].strip()
                    else:
                        wa, ml = raw, raw

                    t1, t2 = st.tabs(["💬 Versión WhatsApp", "📋 Ficha Técnica"])
                    with t1: st.markdown(wa)
                    with t2: st.markdown(ml)
                except Exception as err:
                    st.error(f"Error de la API: {err}. Verifica tu API Key y tu conexión.")

# ==========================================
# MÓDULO 2: ANALISTA DE INVENTARIO
# ==========================================
elif modulo == "2. Analista de Inventario":
    st.title("📊 Módulo 2: Analista de Inventario & Promociones")
    
    col1, col2 = st.columns(2)
    with col1:
        meta = st.selectbox("Objetivo estratégico:", ["Liquidar inventario", "Aumentar ticket promedio", "Promo relámpago"])
        inv_file = st.file_uploader("Sincronizar inventario (.csv):", type=["csv", "txt"])
    
    with col2:
        if inv_file:
            df_inv = pd.read_csv(inv_file) if inv_file.name.endswith(".csv") else inv_file.read().decode("utf-8")
            st.dataframe(df_inv) if isinstance(df_inv, pd.DataFrame) else st.text_area("Datos:", df_inv)
            inv_data = df_inv.to_string() if isinstance(df_inv, pd.DataFrame) else df_inv
        else:
            inv_data = """SKU | Producto | Días Stock | Precio Normal
            BAT-SAM-A70 | Batería SAM A70 | 85 | $18
            CAR-USB-45W | Cargador USB-C 45W | 10 | $22
            AUD-TWS-PRO | Audífonos TWS IPH | 75 | $25"""
            st.info("Usando catálogo Demo.")

    btn2 = st.button("🔥 Generar Estrategias")
    if btn2:
        if not api_key:
            st.error("⚠️ Ingresa tu API Key.")
        else:
            with st.spinner("Analizando y creando combos..."):
                prompt = f"""
                {NORMATIVA_CORPORATIVA}
                INVENTARIO: {inv_data}
                OBJETIVO: {meta}
                Crea 3 combos atractivos emparejando artículos estancados con estrellas. Incluye:
                Nombre del combo, Descuento, Copy para WhatsApp/IG y Brief visual para diseñador.
                """
                try:
                    res = client.models.generate_content(model=modelo_gemini, contents=prompt)
                    st.markdown(res.text)
                except Exception as err:
                    st.error(f"Error de la API: {err}")

# ==========================================
# MÓDULO 3: AUDITOR DE PRECIOS
# ==========================================
elif modulo == "3. Auditor de Precios & Objeciones":
    st.title("🥊 Módulo 3: Auditor de Precios")
    
    col1, col2 = st.columns(2)
    with col1:
        producto_nuestro = st.text_input("Producto Lion Tech:", "Pantalla de repuesto para IPH 11 - LCD")
        precio_nuestro = st.number_input("Nuestro precio ($):", value=35.0)
        costo_producto = st.number_input("Nuestro costo ($):", value=20.0)
    with col2:
        competidor = st.text_input("Competidor:", "Vendedor ML Genérico")
        precio_competidor = st.number_input("Precio competidor ($):", value=32.0)
        detalles_competidor = st.text_input("Detalles rival:", "Sin garantía, sin factura")

    # Cálculos seguros
    diferencia = precio_nuestro - precio_competidor
    margen_actual = precio_nuestro - costo_producto
    descuento_maximo = max(0.0, margen_actual * 0.5) 
    precio_limite_piso = precio_nuestro - descuento_maximo

    st.markdown("---")
    c_sem, c_calc = st.columns(2)
    
    with c_sem:
        if diferencia <= 0:
            st.markdown("""<div class="semaforo-card semaforo-verde">🟢 VERDE: PRECIO LÍDER</div>""", unsafe_allow_html=True)
        elif diferencia <= (precio_nuestro * 0.10):
            st.markdown(f"""<div class="semaforo-card semaforo-amarillo">🟡 AMARILLO: BRECHA ESTRECHA (${diferencia:.2f} extra)</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="semaforo-card semaforo-rojo">🔴 ROJO: ALTA COMPETENCIA (${diferencia:.2f} extra)</div>""", unsafe_allow_html=True)

    with c_calc:
        st.metric("Piso Máximo Negociable", f"${precio_limite_piso:.2f}", f"-${descuento_maximo:.2f} máx desc.")

    if st.button("🥊 Generar Matador de Objeciones"):
        if not api_key:
            st.error("⚠️ Ingresa tu API Key.")
        else:
            with st.spinner("Generando guion de ventas..."):
                prompt = f"""
                {NORMATIVA_CORPORATIVA}
                Producto: {producto_nuestro} | Precio Nuestro: ${precio_nuestro} | Piso Autorizado: ${precio_limite_piso}
                Rival: {competidor} | Precio Rival: ${precio_competidor} | Fallas rival: {detalles_competidor}
                
                Actúa como Director de Ventas. Genera:
                1. Diagnóstico rápido.
                2. Guion para el cliente que desmonta al rival amablemente.
                3. Contraoferta final usando el Precio Piso Autorizado si el cliente duda.
                """
                try:
                    res = client.models.generate_content(model=modelo_gemini, contents=prompt)
                    st.markdown(res.text)
                except Exception as err:
                    st.error(f"Error de la API: {err}")

# ==========================================
# MÓDULO 4: TRANSFORMADOR OMNICANAL
# ==========================================
elif modulo == "4. Transformador de Catálogo":
    st.title("🚀 Módulo 4: Transformador de Catálogo")
    
    col1, col2 = st.columns(2)
    with col1:
        prod_nombre = st.text_input("Producto:", "Batería para Samsung A70")
        prod_sku = st.text_input("SKU:", "BAT-SAM-A70")
        prod_precio = st.text_input("Precio ($):", "18.00")
    with col2:
        prod_caracteristicas = st.text_area("Especificaciones:", "4500mAh, incluye adhesivo, 100% testeada.")

    if st.button("⚡ Generar Kit Omnicanal"):
        if not api_key:
            st.error("⚠ Ingresa tu API Key.")
        else:
            with st.spinner("Creando contenido para ML, Reels e Instagram..."):
                prompt = f"""
                {NORMATIVA_CORPORATIVA}
                Producto: {prod_nombre} | SKU: {prod_sku} | Precio: ${prod_precio}
                Specs: {prod_caracteristicas}
                
                Genera:
                1. Publicación Mercado Libre (Título SEO normativo y Descripción).
                2. Guion 30s CapCut/Reels (Gancho, Nudo, Desenlace).
                3. Carrusel Instagram (4 Diapositivas).
                4. Prompt Midjourney/Canva para crear la imagen publicitaria.
                """
                try:
                    res = client.models.generate_content(model=modelo_gemini, contents=prompt)
                    st.markdown(res.text)
                except Exception as err:
                    st.error(f"Error de la API: {err}")