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
st.sidebar.image("https://dummyimage.com/150x50/000/fff&text=MENFA+Logo", use_container_width=True)
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

# 2. ÍNDICE GENERAL (DESARROLLADO)
elif menu == "📚 Índice General (Partes I a XII)":
    st.markdown('<p class="main-header">📚 Estructura General del Manual Técnico</p>', unsafe_allow_html=True)
    st.write("Seleccione un módulo temático para explorar su contenido conceptual y técnico detallado:")

    # Selector de módulos
    modulo = st.selectbox(
        "Seleccione la Parte del Manual a consultar:",
        [
            "PARTE I — Fundamentos Profesionales",
            "PARTE II — Fundamentos Técnicos",
            "PARTE III — Seguridad y Ambiente",
            "PARTE IV — Muestreo",
            "PARTE V — Laboratorio de Crudo",
            "PARTE VI — Laboratorio de Agua",
            "PARTE VII — Laboratorio de Gas",
            "PARTE VIII — Calidad",
            "PARTE IX — Normativa",
            "PARTE X — Procedimientos",
            "PARTE XI — Práctica Profesional",
            "PARTE XII — Evaluación"
        ]
    )

    st.markdown("---")

    # DESARROLLO DE CADA PARTE
    if modulo == "PARTE I — Fundamentos Profesionales":
        st.subheader("PARTE I — Fundamentos Profesionales")
        
        with st.expander("1.1 El Laboratorista en el Oil & Gas", expanded=True):
            st.markdown("""
            * **Rol estratégico:** El laboratorista no solo ejecuta ensayos, sino que valida datos críticos para la **transferencia de custodia**, el control de procesos en planta y la prevención de daños a instalaciones.
            * **Responsabilidades clave:**
                * Garantizar la integridad física y la trazabilidad de las muestras recibidas.
                * Aplicar normativas vigentes (ASTM, API, ISO) con rigor metrológico.
                * Reportar desvíos fuera de especificación (Off-Spec) de forma oportuna.
            * **Perfil profesional:** Dominio de química de fluidos petroleros, ética profesional en la generación de resultados y cultura preventiva de seguridad.
            """)

        with st.expander("1.2 Organización del Laboratorio"):
            st.markdown("""
            * **Distribución de áreas operativas:**
                * *Área de recepción y log-in:* Registro y almacenamiento temporal de muestras.
                * *Laboratorio de crudo:* Ensayos de BSW, densidad, salinidad, viscosidad y destilación.
                * *Laboratorio de agua y gas:* Análisis físico-químico de aguas e interpretación cromatográfica.
                * *Depósito de reactivos:* Almacenamiento clasificado según matrices de compatibilidad química.
            * **Flujo de trabajo estandarizado:** Entrada de Muestra $\\rightarrow$ Preparación/Homogeneización $\\rightarrow$ Ensayo $\\rightarrow$ Control QA/QC $\\rightarrow$ Emisión de Certificado Analítico.
            """)

    elif modulo == "PARTE II — Fundamentos Técnicos":
        st.subheader("PARTE II — Fundamentos Técnicos")
        
        with st.expander("2.1 Fundamentos de Laboratorio", expanded=True):
            st.markdown("""
            * **Química de Hidrocarburos:** Clasificación de compuestos (Parafinas, Naftenos, Aromáticos, Asfaltenos - PNAA).
            * **Operaciones Unitarias:** Extracción, destilación, centrifugación y evaporación aplicadas a matrices de petróleo.
            * **Manejo de Reactivos:** Preparación de soluciones valoradas, estándares de referencia y manejo seguro de solventes aromáticos (Xileno, Tolueno).
            """)

        with st.expander("2.2 Metrología y Calidad de las Mediciones"):
            st.markdown("""
            * **Conceptos clave:** Precisión vs. Exactitud, Repetibilidad ($r$) y Reproducibilidad ($R$).
            * **Incertidumbre de la medición:** Identificación de fuentes de error sistemáticas y aleatorias.
            * **Calibración y Verificación:** Mantenimiento preventivo, ajuste de termómetros, balanzas analíticas y densímetros digitales.
            """)

    elif modulo == "PARTE III — Seguridad y Ambiente":
        st.subheader("PARTE III — Seguridad, Higiene y Ambiente (HSE)")
        
        with st.expander("3.1 Gestión de Seguridad en el Laboratorio Petrolero", expanded=True):
            st.markdown("""
            * **EPP Específico:** Uso obligatorio de antiparras con protección lateral, guantes de nitrilo/neopreno, guardapolvo ignífugo y calzado de seguridad.
            * **Sistemas de Protección Colectiva:** Cabinas de extracción de gases (fume hoods), duchas y lavaojos de emergencia.
            * **SGA (Sistema Globalmente Armonizado):** Pictogramas de peligro y lectura correcta de Hojas de Datos de Seguridad (FDS / MSDS).
            * **Gestión de Residuos:** Clasificación de efluentes líquidos (solventes orgánicos, ácidos, aguas hidrocarburadas) y sólidos contaminados.
            """)

    elif modulo == "PARTE IV — Muestreo":
        st.subheader("PARTE IV — Muestreo de Fluidos Petroleros")
        
        with st.expander("4.1 Técnicas y Protocolos de Muestreo (ASTM D4057 / D4177)", expanded=True):
            st.markdown("""
            * **Tipos de Muestra:** Muestra puntual (top, middle, bottom), muestra corrida, muestra compuesta y muestra continua en línea.
            * **Equipamiento de Muestreo:** Ladrones de muestra (Bacon Bomb), botellas lastradas, recipientes de presión constante para Gas/GLP.
            * **Cadena de Custodia:** Documentación obligatoria que garantiza el historial, origen, preservación y sellado inviolable de la muestra.
            """)

    elif modulo == "PARTE V — Laboratorio de Crudo":
        st.subheader("PARTE V — Caracterización del Petróleo y Ensayos Físico-Químicos")
        
        with st.expander("5.1 Ensayos Estándar para Calidad de Crudo", expanded=True):
            st.markdown("""
            * **BS&W (Water & Sediment):** Determinación por centrifugación (ASTM D4007) y por destilación (ASTM D4006).
            * **Gravedad API y Densidad:** Medición con hidrómetro (ASTM D1298) y densímetro digital de tubo en U oscilante (ASTM D5002).
            * **Salinidad:** Determinación electrométrica de cloruros (ASTM D3230) expresado en PTB (lbs/1000 bbl).
            * **Viscosidad Kinemática:** Uso de viscosímetros capilares de vidrio (ASTM D445).
            * **Punto de Escurrimiento (Pour Point):** Evaluación de temperatura de fluidez (ASTM D97).
            """)

    elif modulo == "PARTE VI — Laboratorio de Agua":
        st.subheader("PARTE VI — Análisis de Aguas Petroleras")
        
        with st.expander("6.1 Caracterización de Agua de Formación e Inyección", expanded=True):
            st.markdown("""
            * **Físico-Química:** pH, conductividad eléctrica, sólidos suspendidos totales (SST) y turbidez.
            * **Fisiología Iónica (Fórmula de Stiff/Schoeller):** Determinación de Cationes ($Ca^{2+}$, $Mg^{2+}$, $Na^+$, $Fe^{total}$) y Aniones ($Cl^-$, $SO_4^{2-}$, $HCO_3^-$).
            * **Compatibilidad de Aguas:** Predicción de incrustaciones de carbonatos ($CaCO_3$) y sulfatos ($BaSO_4$) mediante índices de estabilidad (Langelier / Stiff-Davis).
            * **Aceite en Agua (TOG/FOG):** Extracción por solvente y medición por espectrofotometría IR o UV.
            """)

    elif modulo == "PARTE VII — Laboratorio de Gas":
        st.subheader("PARTE VII — Análisis de Gas Natural y Cromatografía")
        
        with st.expander("7.1 Ensayos y Caracterización de Gas Natural", expanded=True):
            st.markdown("""
            * **Cromatografía en Fase Gaseosa (GC):** Determinación de composición ($C_1$ a $C_6+$), inertes ($N_2$, $CO_2$).
            * **Propiedades Calculadas (GPA 2172):**Poder Calorífico Superior e Inferior (BTU/cu.ft), Densidad Relativa y Factor de Compresibilidad ($Z$).
            * **Humedad y Contaminantes:** Punto de rocío de agua y de hidrocarburos, detección de sulfuro de hidrógeno ($H_2S$) y mercaptanos.
            """)

    elif modulo == "PARTE VIII — Calidad":
        st.subheader("PARTE VIII — Gestión de Calidad Analítica (ISO/IEC 17025)")
        
        with st.expander("8.1 Aseguramiento de la Calidad (QA/QC)", expanded=True):
            st.markdown("""
            * **Herramientas de Control Interno:**
                * Análisis de muestras ciegas, duplicados analíticos y espigas (Spikes).
                * Cartas de control de Shewhart para monitoreo de tendencia de equipos.
            * **Trazabilidad:** Uso de Materiales de Referencia Certificados (MRC).
            * **Auditorías y Ensayos de Aptitud:** Participación en rondas interlaboratorios (Proficiency Testing).
            """)

    elif modulo == "PARTE IX — Normativa":
        st.subheader("PARTE IX — Marco Normativo y Estandarización")
        
        with st.expander("9.1 Organismos de Normalización en la Industria", expanded=True):
            st.markdown("""
            * **ASTM International:** Métodos de ensayo estándar para productos petroleros y lubricantes (Comité D02).
            * **API MPMS:** *Manual of Petroleum Measurement Standards* (Enfoque en transferencia de custodia y medición).
            * **ISO e IRAM:** Normas de sistemas de gestión y métodos regionales estandarizados.
            * **Resoluciones Secretaría de Energía:** Regulaciones locales para especificaciones de venta y transporte de fluidos.
            """)

    elif modulo == "PARTE X — Procedimientos":
        st.subheader("PARTE X — Procedimientos Operativos Estándar (SOP)")
        
        with st.expander("10.1 Estructura Documental de un SOP (Standard Operating Procedure)", expanded=True):
            st.markdown("""
            * **Estructura jerárquica recomendada:**
                1. *Objetivo y Alcance:* Definición clara de la matriz y el rango de aplicación.
                2. *Documentos de Referencia:* Normas ASTM/API base.
                3. *Reactivos y Materiales:* Especificación de pureza de solventes y calibración de instrumental.
                4. *Procedimiento Paso a Paso:* Instrucciones secuenciales de ensayo.
                5. *Cálculos y Reporte:* Fórmulas de cálculo de concentración y criterios de redondeo.
                6. *Criterios de Aceptación/Rechazo:* Tolerancias de repetibilidad según norma.
            """)

    elif modulo == "PARTE XI — Práctica Profesional":
        st.subheader("PARTE XI — Casos y Simulaciones de Desviaciones Operativas")
        
        with st.expander("11.1 Resolución de Problemas en Planta y Campo", expanded=True):
            st.markdown("""
            * **Estudio de Caso 1:** Emulsiones severas (Tight Emulsions) no rotas en la centrifugación de BS&W. Estrategias de ajuste de deemulsificante y temperatura.
            * **Estudio de Caso 2:** Discrepancias en volumen de transferencia de custodia por error de medición de densidad/temperatura.
            * **Estudio de Caso 3:** Contaminación de agua de reinyección con sólidos en suspensión (daño de formación por colmatación).
            """)

    elif modulo == "PARTE XII — Evaluación":
        st.subheader("PARTE XII — Evaluación Profesional y Perfil de Egreso")
        
        with st.expander("12.1 Validación de Competencias del Laboratorista Petrolero", expanded=True):
            st.markdown("""
            * **Perfil del Egresado MENFA:** Profesional capacitado para operar de forma autónoma en laboratorios de yacimiento, refinerías y plantas de tratamiento de fluidos.
            * **Matriz de Competencias:**
                * Execución analítica bajo normas ASTM/API.
                * Gestión de la seguridad HSE y manejo de residuos.
                * Interpretación de resultados para la toma de decisiones operativas en producción.
            """)

# 3. FICHAS TÉCNICAS
elif menu == "📋 Consultas de Fichas Técnicas":
    st.markdown('<p class="main-header">📋 Fichas Técnicas Normalizadas</p>', unsafe_allow_html=True)
    st.write("Seleccione el ensayo para visualizar su estructura estandarizada:")
    
    ensayo = st.selectbox(
        "Ensayo disponible:",
        [
            "Determinación de Agua y Sedimentos (BS&W - Centrífuga)",
            "Determinación de Densidad y Gravedad API",
            "Determinación de Salinidad en Crudo"
        ]
    )
    
    if ensayo == "Determinación de Agua y Sedimentos (BS&W - Centrífuga)":
        st.markdown("### Ficha Técnica: MENFA-FT-LAB-01 (BS&W)")
        st.markdown("""
        * **Objetivo:** Determinar el porcentaje volumétrico de agua y sedimentos en petróleo crudo mediante centrifugación.
        * **Normativa:** ASTM D4007 / API MPMS Capítulo 10.3.
        * **Equipos:** Centrífuga con calentamiento, tubos cónicos normalizados de 100 mL.
        * **Solventes / Reactivos:** Solvente aromático (xileno) y deemulsificante comercial.
        * **Criterio de Aceptación:** Repetibilidad conforme a especificación de norma para transferencia de custodia.
        """)
        
    elif ensayo == "Determinación de Densidad y Gravedad API":
        st.markdown("### Ficha Técnica: MENFA-FT-LAB-02 (Densidad y API)")
        st.markdown("""
        * **Objetivo:** Determinar la densidad relativa y gravedad API en petróleo crudo y productos líquidos.
        * **Normativa:** ASTM D1298 (Densímetro de vidrio) / ASTM D5002 (Densímetro digital).
        * **Equipos:** Hidrómetros/densímetros calibrados, probetas graduadas, baño termostático.
        * **Criterio de Aceptación:** Corrección de lecturas a temperatura estándar de 60 °F (15,56 °C) según tablas ASTM/API.
        """)
        
    elif ensayo == "Determinación de Salinidad en Crudo":
        st.markdown("### Ficha Técnica: MENFA-FT-LAB-03 (Salinidad)")
        st.markdown("""
        * **Objetivo:** Determinar la concentración aproximada de cloruros (sales) disueltos en petróleo crudo.
        * **Normativa:** ASTM D3230 (Electrométrico).
        * **Equipos:** Analizador de salinidad electrométrico, vaso de precipitado, electrodos.
        * **Solventes / Reactivos:** Mezcla de alcoholes solventes (Metanol/Tolueno) y estándar de calibración.
        * **Criterio de Aceptación:** Expresión de resultados en libras de sal por mil barriles (PTB) o mg/L de NaCl.
        """)

# 4. SIMULADOR RÁPIDO
elif menu == "🧮 Simulador Rápido (Crudo y Agua)":
    st.markdown('<p class="main-header">🧮 Simulador Operativo de Laboratorio</p>', unsafe_allow_html=True)
    st.write("Herramienta de cálculo rápido para control de parámetros en batería o planta.")
    
    tab1, tab2 = st.tabs(["Calculadora de Gravedad API", "Control de BS&W"])
    
    with tab1:
        st.subheader("Conversión de Densidad a Gravedad API")
        densidad_15 = st.number_input("Densidad relativa a 15,56 °C (60 °F):", min_value=0.500, max_value=1.100, value=0.8550, format="%.4f")
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
4. PASOS DE CONTROL:
   - Verificar correspondencia entre etiqueta física y hoja de cadena de custodia.
   - Comprobar ausencia de pérdidas en el contenedor del envase.
   - Registrar temperatura y estado de conservación al ingreso.
        """, language="text")
        
    elif "002" in sop_code:
        st.markdown("### MENFA-SOP-LAB-002: Control de Calidad Analítica")
        st.code("""
1. OBJETIVO: Establecer los alineamientos de aseguramiento de calidad (QA/QC).
2. ALCANCE: Mediciones cuantitativas en laboratorios de ensayo.
3. CONTROL: Uso de duplicados, patrones de referencia y cartas de control.
        """, language="text")

    elif "SOP-CR-004" in sop_code:
        st.markdown("### SOP-CR-004: Determinación de Agua en Petróleo Crudo por Destilación")
        st.markdown("""
        * **Normativa de Referencia:** ASTM D4006
        * **Área:** Laboratorio de Crudo
        * **Objetivo:** Determinar el contenido de agua mediante destilación con solvente y condensación en trampa graduada.
        
        #### ⚠️ Puntos Críticos de Seguridad y Operación:
        1. **Calentamiento controlado:** Evite incrementos bruscos de temperatura para prevenir ebullición violenta, formación excesiva de espuma o rotura del material de vidrio.
        2. **Verificación del sistema:** Comprobar ausencia de fugas, correcta circulación del refrigerante en el condensador y limpieza absoluta de la trampa graduada.
        3. **Lectura de resultados:** Esperar la estabilización completa del sistema y realizar la lectura evitando errores de paralaje sobre el menisco.
        """)
