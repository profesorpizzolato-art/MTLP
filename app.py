import streamlit as st
import numpy as np
import pandas as pd

# Importación de módulos locales
from modules.modulo_crudo import calcular_api_corregido, calcular_bsw, evaluar_conformidad_crudo
from modules.modulo_agua import calcular_sst, calcular_indice_langelier
from modules.modulo_gas import calcular_propiedades_gas
from modules.modulo_calidad import generar_grafico_shewhart

# Configuración de página
st.set_page_config(
    page_title="Simulador de Laboratorio Petrolero | IPCL MENFA",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado CSS
st.markdown("""
    <style>
    .main-header {
        font-size:26px;
        font-weight:bold;
        color: #1E3A8A;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .stMetric {
        background-color: #F8FAFC;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BARRA LATERAL - NAVEGACIÓN Y AUTORÍA
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/petroleum-press.png", width=70)
st.sidebar.title("LAB-PETRO MENFA")
st.sidebar.caption("Sistema de Simulación y Control de Calidad Analítica")

opcion_modulo = st.sidebar.radio(
    "Seleccione Módulo de Trabajo:",
    [
        "1. Crudo: °API y BS&W",
        "2. Agua: SST e Incrustaciones",
        "3. Gas Natural: Cromatografía",
        "4. Control de Calidad (ISO 17025)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Autoría y Desarrollo:**  
Fabricio Pizzolato  
*IPCL MENFA / Formación Técnica Oil & Gas*
""")

# -----------------------------------------------------------------------------
# MÓDULO 1: PETRÓLEO CRUDO (ASTM D1298 / ASTM D4007)
# -----------------------------------------------------------------------------
if opcion_modulo == "1. Crudo: °API y BS&W":
    st.markdown('<div class="main-header">🧪 Módulo de Análisis de Petróleo Crudo</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Densidad y Gravedad °API (ASTM D1298)")
        api_obs = st.number_input("°API Observado (Lectura de Hidrómetro):", min_value=5.0, max_value=70.0, value=28.5, step=0.1)
        temp_f = st.number_input("Temperatura de la Muestra (°F):", min_value=40.0, max_value=120.0, value=85.0, step=0.5)
        
        api_60, sg_60 = calcular_api_corregido(api_obs, temp_f)
        
        st.markdown("#### Resultados Corregidos (a 60°F):")
        m1, m2 = st.columns(2)
        m1.metric("°API Corregido (60°F)", f"{api_60} °API")
        m2.metric("Gravedad Específica (SG)", f"{sg_60}")

    with col2:
        st.subheader("2. Agua y Sedimentos - BS&W (ASTM D4007)")
        st.caption("Método por Centrifugación en Tubos Cónicos de 100 mL")
        
        t1 = st.number_input("Lectura Agua/Sedimento Tubo 1 (mL):", min_value=0.0, max_value=15.0, value=0.3, step=0.05)
        t2 = st.number_input("Lectura Agua/Sedimento Tubo 2 (mL):", min_value=0.0, max_value=15.0, value=0.3, step=0.05)
        limite_contrato = st.number_input("Límite Contractual Máximo BS&W (%):", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        
        bsw_total = calcular_bsw(t1, t2)
        conforme, clasificacion = evaluar_conformidad_crudo(api_60, bsw_total, limite_contrato)
        
        st.markdown("#### Evaluación de Calidad de Despacho:")
        st.metric("BS&W Total Calculado", f"{bsw_total} % v/v")
        
        if conforme:
            st.success(f"✅ **CONFORME PARA TRANSFERENCIA DE CUSTODIA** ({clasificacion})")
        else:
            st.error(f"❌ **FORA DE ESPECIFICACIÓN** (Excede el límite del {limite_contrato}%)")

# -----------------------------------------------------------------------------
# MÓDULO 2: AGUA DE FORMACIÓN E INYECCIÓN
# -----------------------------------------------------------------------------
elif opcion_modulo == "2. Agua: SST e Incrustaciones":
    st.markdown('<div class="main-header">💧 Módulo de Fisicoquímica de Aguas Petroleras</div>', unsafe_allow_html=True)
    
  # ✅ Correcto (plural)
tab1, tab2 = st.tabs(["Sólidos Suspendidos Totales (SST)", "Índice de Incrustación (LSI)"])
    
    with tab1:
        st.subheader("Determinación Gravimétrica de SST (SM 2540 D)")
        c1, c2, c3 = st.columns(3)
        p_seco = c1.number_input("Peso Filtro Seco (g):", min_value=0.0000, value=0.4120, format="%.4f")
        p_final = c2.number_input("Peso Filtro + Residuo (g):", min_value=0.0000, value=0.4355, format="%.4f")
        vol_ml = c3.number_input("Volumen Muestra Filtrada (mL):", min_value=1.0, value=250.0, step=10.0)
        
        sst_resultado = calcular_sst(p_seco, p_final, vol_ml)
        st.metric("Concentración de SST", f"{sst_resultado} mg/L")
        
        if sst_resultado > 50.0:
            st.warning("⚠️ Alta carga de sólidos: Alto riesgo de taponamiento en formación receptora.")
        else:
            st.success("✅ Nivel de SST apto para sistemas de inyección estándar.")

    with tab2:
        st.subheader("Índice de Saturación de Langelier (LSI)")
        col_a, col_b = st.columns(2)
        
        ph = col_a.number_input("pH de la Muestra:", min_value=2.0, max_value=12.0, value=7.4, step=0.1)
        temp_c = col_a.number_input("Temperatura del Sistema (°C):", min_value=10.0, max_value=90.0, value=45.0, step=1.0)
        tds = col_a.number_input("TDS (Sólidos Totales Disueltos mg/L):", min_value=100.0, value=15000.0, step=500.0)
        
        ca = col_b.number_input("Calcio Ca2+ (mg/L):", min_value=1.0, value=400.0, step=10.0)
        alcalinidad = col_b.number_input("Alcalinidad Total (mg/L CaCO3):", min_value=1.0, value=600.0, step=10.0)
        
        lsi_val, tendencia = calcular_indice_langelier(ph, temp_c, tds, ca, alcalinidad)
        
        st.markdown("#### Diagnóstico de Tendencia:")
        st.metric("Índice LSI", f"{lsi_val}")
        
        if "Incrustante" in tendencia:
            st.warning(f"⚠️ **TENDENCIA INCRUSTANTE** ({tendencia}): Riesgo de precipitación de CaCO3.")
        elif "Corrosiva" in tendencia:
            st.error(f"🔴 **TENDENCIA CORROSIVA** ({tendencia}): Agua agresiva para tubulares metálicos.")
        else:
            st.info(f"🟢 **SISTEMA EN EQUILIBRIO** ({tendencia})")

# -----------------------------------------------------------------------------
# MÓDULO 3: GAS NATURAL (CROMATOGRAFÍA GPA 2261)
# -----------------------------------------------------------------------------
elif opcion_modulo == "3. Gas Natural: Cromatografía":
    st.markdown('<div class="main-header">🔥 Módulo de Composición y Poder Calorífico de Gas</div>', unsafe_allow_html=True)
    
    st.subheader("Composición Molar de la Muestra (% Molar)")
    st.caption("Ingrese la composición porcentual reportada por el cromatógrafo de gases.")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    
    c1 = col_g1.number_input("Metano (C1):", value=85.0, min_value=0.0, max_value=100.0)
    c2 = col_g1.number_input("Etano (C2):", value=6.0, min_value=0.0, max_value=100.0)
    c3 = col_g1.number_input("Propano (C3):", value=3.0, min_value=0.0, max_value=100.0)
    
    ic4 = col_g2.number_input("i-Butano (iC4):", value=0.8, min_value=0.0, max_value=100.0)
    nc4 = col_g2.number_input("n-Butano (nC4):", value=1.2, min_value=0.0, max_value=100.0)
    c5_plus = col_g2.number_input("Pentanos y Superiores (C5+):", value=1.0, min_value=0.0, max_value=100.0)
    
    co2 = col_g3.number_input("Dióxido de Carbono (CO2):", value=1.5, min_value=0.0, max_value=100.0)
    n2 = col_g3.number_input("Nitrógeno (N2):", value=1.4, min_value=0.0, max_value=100.0)
    h2s = col_g3.number_input("Sulfuro de Hidrógeno (H2S):", value=0.1, min_value=0.0, max_value=100.0)
    
    comp_dict = {'C1': c1, 'C2': c2, 'C3': c3, 'iC4': ic4, 'nC4': nc4, 'C5+': c5_plus, 'CO2': co2, 'N2': n2, 'H2S': h2s}
    total_molar = sum(comp_dict.values())
    
    st.markdown("---")
    if abs(total_molar - 100.0) > 0.01:
        st.error(f"❌ La suma de componentes molares debe ser 100.0%. Suma actual: **{round(total_molar, 2)}%**")
    else:
        mw, sg_gas, pcs = calcular_propiedades_gas(comp_dict)
        
        st.success("✅ Composición Normalizada al 100%")
        m_g1, m_g2, m_g3 = st.columns(3)
        m_g1.metric("Peso Molecular Medio", f"{mw} g/mol")
        m_g2.metric("Gravedad Específica (Aire=1)", f"{sg_gas}")
        m_g3.metric("Poder Calorífico Superior (PCS)", f"{pcs} BTU/SCF")

# -----------------------------------------------------------------------------
# MÓDULO 4: CONTROL DE CALIDAD ISO/IEC 17025
# -----------------------------------------------------------------------------
elif opcion_modulo == "4. Control de Calidad (ISO 17025)":
    st.markdown('<div class="main-header">📈 Control Interno de Calidad y Gráficos de Shewhart</div>', unsafe_allow_html=True)
    
    st.subheader("Seguimiento de Material de Referencia Certificado (MRC)")
    st.caption("Gráfico de control para la verificación diaria de instrumentos de medición.")
    
    col_q1, col_q2 = st.columns(2)
    mrc_nom = col_q1.number_input("Valor Certificado del MRC:", value=0.8500, format="%.4f")
    desv_est = col_q2.number_input("Desviación Estándar Aceptada (s):", value=0.0012, format="%.4f")
    
    st.markdown("#### Simulación de Ensayos Diarios:")
    # Generación de 15 puntos simulados
    np.random.seed(42)
    datos_base = list(np.random.normal(mrc_nom, desv_est, 14))
    
    # Permitir al usuario ingresar la medición de hoy
    dato_hoy = st.number_input("Ingrese la Medición de Hoy (Día 15):", value=float(round(datos_base[-1], 4)), format="%.4f")
    datos_completos = datos_base + [dato_hoy]
    
    fig_shewhart = generar_grafico_shewhart(datos_completos, mrc_nom, desv_est)
    st.plotly_chart(fig_shewhart, use_container_width=True)
    
    lcs = mrc_nom + 3 * desv_est
    lci = mrc_nom - 3 * desv_est
    
    if dato_hoy > lcs or dato_hoy < lci:
        st.error("🚨 **CONDICIÓN FUERA DE CONTROL DETECTADA (Regla de Westgard / Shewhart):** El valor de hoy supera los límites de control (±3s). Suspender ensayos e iniciar investigación de No Conformidad.")
    else:
        st.success("✅ **SISTEMA BAJO CONTROL ANALÍTICO:** El proceso cumple las especificaciones de exactitud.")
