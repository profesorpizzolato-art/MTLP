import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="MENFA - Manual del Laboratorista Petrolero",
    page_icon="🧪",
    layout="wide"
)

# Estilos personalizados (CSS simple para acentos industriales)
st.markdown("""
    <style>
        .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; }
        .sub-header { font-size: 20px; font-weight: bold; color: #374151; }
        .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Menú lateral
st.sidebar.image("https://via.placeholder.com/150x50.png?text=MENFA+Logo", use_container_width=True)
st.sidebar.title("Navegación MENFA")
menu = st.sidebar.selectbox(
    "Seleccione una sección:",
    [
        "🏠 Presentación del Manual",
        "📚 Índice General (Partes I a XII)",
        "📋 Consultas de Fichas Técnicas",
        "🧮 Simulador Rápido (Crudo y Agua)",
        "⚙️ Gestión de SOPs"
    ]
)

# 1. PRESENTACIÓN
if menu == "🏠 Presentación del Manual":
    st.markdown('<p class="main-header">🧪 Manual Técnico del Laboratorista Petrolero</p>', unsafe_allow_html=True)
    st.markdown("**Formación Profesional para Operaciones de Laboratorio en la Industria del Petróleo y Gas**")
    st.markdown("*MENFA Capacitaciones* — Mendoza, Argentina.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Objetivo del Sistema")
        st.write("""
        Este software complementa el soporte documental alojado en el repositorio de GitHub. 
        Permite consultar la estructura técnica, validar procedimientos estandarizados (SOP) 
        y realizar simulaciones analíticas rápidas para aplicaciones en terreno y plantas de proceso.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔒 Principio Rector")
        st.info("“La calidad del resultado comienza con la calidad de la muestra.”")
        st.write("Integridad de datos, trazabilidad metrológica y estricto cumplimiento de normativas HSE.")
        st.markdown('</div>', unsafe_allow_html=True)

# 2. ÍNDICE GENERAL
elif menu == "📚 Índice General (Partes I a XII)":
    st.markdown('<p class="main-header">📚 Estructura General del Manual</p>', unsafe_allow_html=True)
    
    partes = {
        "PARTE I — Fundamentos Profesionales": ["El Laboratorista en el Oil & Gas", "Organización del Laboratorio"],
        "PARTE II — Fundamentos Técnicos": ["Fundamentos de Laboratorio", "Metrología y Calidad de las Mediciones"],
        "PARTE III — Seguridad y Ambiente": ["Seguridad, Higiene y Ambiente (HSE)"],
        "PARTE IV — Muestreo": ["Muestreo de Fluidos Petroleros"],
        "PARTE V — Laboratorio de Crudo": ["Caracterización del Petróleo y Ensayos Físico-Químicos"],
        "PARTE VI — Laboratorio de Agua": ["Análisis de Aguas Petroleras (Formación, Inyección, Proceso)"],
        "PARTE VII — Laboratorio de Gas": ["Análisis de Gas Natural y Cromatografía"],
        "PARTE VIII — Calidad": ["Gestión de Calidad Analítica (ISO/IEC 17025)"],
        "PARTE IX — Normativa": ["Marco Normativo (Legislación, API, ASTM, ISO, IRAM)"],
        "PARTE X — Procedimientos": ["Procedimientos Operativos Estándar (MENFA-SOP-LAB)"],
        "PARTE XI — Práctica Profesional": ["Casos y Simulaciones de Desviaciones Operativas"],
        "PARTE XII — Evaluación": ["Evaluación Profesional y Perfil de Egreso"]
    }
    
    for parte, temas in partes.items():
        with st.expander(parte):
            for tema in temas:
                st.write(f"- {tema}")

# 3. FICHAS TÉCNICAS
elif menu == "📋 Consultas de Fichas Técnicas":
    st.markdown('<p class="main-header">📋 Fichas Técnicas Normalizadas</p>', unsafe_allow_html=True)
    st.write("Seleccione el ensayo para visualizar su estructura estandarizada:")
    
    ensayo = st.selectbox(
        "Ensayo disponible:",
        ["Determinación de Agua y Sedimentos (BS&W - Centrifuga)", "Determinación de Densidad y Gravedad API", "Determinación de Salinidad en Crudo"]
    )
    
    if ensayo == "Determinación de Agua y Sedimentos (BS&W - Centrifuga)":
        st.markdown("### Ficha Técnica: MENFA-FT-LAB-01 (BS&W)")
        st.markdown("""
        * **Objetivo:** Determinar el porcentaje volumétrico de agua y sedimentos en petróleo crudo mediante centrifugación.
        * **Normativa:** ASTM D4007 / API MPMS Capítulo 10.3.
        * **Equipos:** Centrífuga con calentamiento, tubos cónicos normalizados de 100 mL.
        * **Solventes / Reactivos:** Solvente aromático (xileno) y deemulsificante comercial.
        * **Criterio de Aceptación:** Repetibilidad conforme a especificación de norma para transferencia de custodia.
        """)

# 4. SIMULADOR RÁPIDO
elif menu == "🧮 Simulador Rápido (Crudo y Agua)":
    st.markdown('<p class="main-header">🧮 Simulador Operativo de Laboratorio</p>', unsafe_allow_html=True)
    st.write("Herramienta de cálculo rápido para control de parámetros en batería o planta.")
    
    tab1, tab2 = st.tabs(["Calculadora de Gravedad API", "Control de BS&W"])
    
    with tab1:
        st.subheader("Conversión de Densidad a Gravedad API")
        densidad_15 = st.number_input("Densidad relativa a 15.56 °C (60 °F):", min_value=0.500, max_value=1.100, value=0.8550, format="%.4f")
        if st.button("Calcular Gravedad API"):
            api = (141.5 / densidad_15) - 131.5
            st.success(f"Gravedad API resultante: **{api:.2f} °API**")
            
    with tab2:
        st.subheader("Cálculo de Porcentaje de Agua y Sedimentos")
        vol_agua = st.number_input("Volumen de fase separada en tubo (mL):", min_value=0.0, max_value=100.0, value=1.5, format="%.2f")
        vol_muestra = st.number_input("Volumen total de muestra en tubo (mL):", min_value=1.0, max_value=100.0, value=100.0, format="%.2f")
        if st.button("Calcular BS&W %"):
            bsw = (vol_agua / vol_muestra) * 100.0
            st.metric(label="Porcentaje de BS&W", value=f"{bsw:.2f} %")
            if bsw > 2.0:
                st.warning("⚠️ Alerta: El contenido de BS&W supera el límite operativo estándar de 2%. Verificar proceso de deshidratación.")
            else:
                st.info("✅ Parámetro dentro de rangos operativos normales.")

# 5. GESTIÓN DE SOPS
elif menu == "⚙️ Gestión de SOPs":
    st.markdown('<p class="main-header">⚙️ Procedimientos Operativos Estándar (SOP)</p>', unsafe_allow_html=True)
    st.write("Estructura base de codificación interna para el sistema de calidad del laboratorio:")
    
    sop_code = st.selectbox("Seleccione SOP:", ["MENFA-SOP-LAB-001 (Recepción y Criterio de Muestras)", "MENFA-SOP-LAB-002 (Control de Calidad Analítica)"])
    
    if "001" in sop_code:
        st.markdown("### MENFA-SOP-LAB-001: Recepción y Verificación de Muestras")
        st.code("""
1. OBJETIVO: Establecer los criterios de aceptación y rechazo de muestras de fluidos petroleros.
2. ALCANCE: Aplicable a todos los laboratorios de campo y plantas de MENFA Capacitaciones.
3. RESPONSABILIDADES: El Laboratorista Petrolero en turno es responsable de verificar la integridad.
4. PASOS DE CONTROL:
   - Verificar correspondencia entre etiqueta física y hoja de cadena de custodia.
   - Comprobar ausencia de pérdidas en el envase contenedor.
   - Registrar temperatura y estado de conservación al ingreso.
        """, language="text")
# 5. GESTIÓN DE SOPS (Actualización con SOP-CR-004)
elif menu == "⚙️ Gestión de SOPs":
    st.markdown('<p class="main-header">⚙️ Procedimientos Operativos Estándar (SOP)</p>', unsafe_allow_html=True)
    st.write("Seleccione el procedimiento normalizado del sistema de calidad:")
    
    sop_code = st.selectbox(
        "Seleccione SOP:", 
        [
            "MENFA-SOP-LAB-001 (Recepción y Criterio de Muestras)", 
            "MENFA-SOP-LAB-002 (Control de Calidad Analítica)",
            "SOP-CR-004 (Determinación de Agua en Petróleo Crudo por Destilación - ASTM D4006)"
        ]
    )
    
    if "001" in sop_code:
        st.markdown("### MENFA-SOP-LAB-001: Recepción y Verificación de Muestras")
        st.code("""
1. OBJETIVO: Establecer los criterios de aceptación y rechazo de muestras de fluidos petroleros.
2. ALCANCE: Aplicable a todos los laboratorios de campo y plantas de MENFA Capacitaciones.
3. RESPONSABILIDADES: El Laboratorista Petrolero en turno es responsable de verificar la integridad.
        """, language="text")
        
    elif "SOP-CR-004" in sop_code:
        st.markdown("### SOP-CR-004: Determinación de Agua en Petróleo Crudo por Destilación")
        st.markdown("""
        * **Normativa de Referencia:** ASTM D4006
        * **Área:** Laboratorio de Crudo
        * **Objetivo:** Determinar el contenido de agua mediante destilación con solvente y condensación en trampa graduada.
        
        #### ⚠️ Puntos Críticos de Seguridad y Operación:
        1. **Calentamiento controlado:** Evitar incrementos bruscos de temperatura para prevenir ebullición violenta, formación excesiva de espuma o rotura del material de vidrio.
        2. **Verificación del sistema:** Comprobar ausencia de fugas, correcta circulación del refrigerante en el condensador y limpieza absoluta de la trampa graduada.
        3. **Lectura de resultados:** Esperar la estabilización completa del sistema y realizar la lectura evitando errores de paralaje sobre el menisco.
        """)
