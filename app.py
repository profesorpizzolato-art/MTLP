import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Importación de módulos locales
from modules.modulo_crudo import calcular_api_corregido, calcular_bsw, evaluar_conformidad_crudo
from modules.modulo_agua import calcular_sst, calcular_indice_langelier
from modules.modulo_gas import calcular_propiedades_gas
from modules.modulo_calidad import generar_grafico_shewhart

# Configuración de página
st.set_page_config(
    page_title="Simulador interactivo de Laboratorio | IPCL MENFA",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS avanzados para tableros e indicadores
st.markdown("""
    <style>
    .main-header {
        font-size:26px;
        font-weight:bold;
        color: #1E3A8A;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BARRA LATERAL - NAVEGACIÓN Y AUTORÍA
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/petroleum-press.png", width=70)
st.sidebar.title("LAB-PETRO MENFA 2.0")
st.sidebar.caption("Simulador Interactivo de Procesos y Laboratorio Oil & Gas")

opcion_modulo = st.sidebar.radio(
    "Seleccione Módulo de Trabajo:",
    [
        "1. Crudo: Deshidratación y Centrifugado",
        "2. Agua: Tratamiento e Incrustación",
        "3. Gas Natural: Cromatografía y Mezcla",
        "4. Control de Calidad Dinámico (ISO 17025)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Autoría y Desarrollo:**  
Fabricio Pizzolato  
*IPCL MENFA / Formación Técnica Oil & Gas*
""")

# -----------------------------------------------------------------------------
# MÓDULO 1: PETRÓLEO CRUDO (INTERACTIVO)
# -----------------------------------------------------------------------------
if opcion_modulo == "1. Crudo: Deshidratación y Centrifugado":
    st.markdown('<div class="main-header">🧪 Módulo Interactivo: Calidad de Crudo y Deshidratación</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Parámetros de Prueba (ASTM D1298 / D4007)")
        
        api_obs = st.slider("°API Observado (Lectura en probeta):", min_value=10.0, max_value=50.0, value=28.5, step=0.1)
        temp_f = st.slider("Temperatura de Ensayo (°F):", min_value=50.0, max_value=140.0, value=85.0, step=1.0)
        
        st.markdown("---")
        st.caption("Prueba de Centrifugación (Tubos Cónicos 100 mL)")
        t1 = st.slider("Agua + Sedimento Tubo 1 (mL):", min_value=0.0, max_value=5.0, value=0.3, step=0.05)
        t2 = st.slider("Agua + Sedimento Tubo 2 (mL):", min_value=0.0, max_value=5.0, value=0.3, step=0.05)
        limite_contrato = st.number_input("Límite Contractual BS&W (% v/v):", min_value=0.1, max_value=3.0, value=0.5, step=0.1)

    with col2:
        st.subheader("📊 Resultados en Tiempo Real")
        
        api_60, sg_60 = calcular_api_corregido(api_obs, temp_f)
        bsw_total = calcular_bsw(t1, t2)
        conforme, clasificacion = evaluar_conformidad_crudo(api_60, bsw_total, limite_contrato)
        
        # Métricas principales
        m1, m2, m3 = st.columns(3)
        m1.metric("°API Corregido (60°F)", f"{api_60} °API")
        m2.metric("Gravedad Específica", f"{sg_60}")
        m3.metric("BS&W Total", f"{bsw_total} %")

        # Alerta visual
        if conforme:
            st.success(f"✅ **CRUDO APTO PARA DESPACHO** | Clasificación: **{clasificacion}**")
        else:
            st.error(f"❌ **RECHAZADO EN TANQUE DE DESPACHO** | Supera el máximo contractual de {limite_contrato}% BS&W")

        # Gráfico interactivo de torta (Composición de la Muestra)
        porcentaje_petro = max(0.0, 100.0 - bsw_total)
        fig_pie = px.pie(
            names=['Petróleo Neto', 'Agua + Sedimento (BS&W)'],
            values=[porcentaje_petro, bsw_total],
            color_discrete_sequence=['#1E3A8A', '#EF4444'],
            title="Composición Volumétrica de la Muestra",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 2: AGUA (INTERACTIVO CON DOSIFICACIÓN DE QUÍMICOS)
# -----------------------------------------------------------------------------
elif opcion_modulo == "2. Agua: Tratamiento e Incrustación":
    st.markdown('<div class="main-header">💧 Módulo Interactivo: Fisicoquímica y Trata de Agua</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Sólidos Suspendidos (SST)", "Índice de Langelier (LSI)", "🧪 Calculadora de Química"])
    
    with tab1:
        st.subheader("Simulación Gravimétrica de Filtración")
        c1, c2 = st.columns(2)
        
        with c1:
            peso_seco = st.number_input("Masa Filtro Tarado (g):", value=0.4120, format="%.4f")
            peso_final = st.slider("Masa Filtro + Residuo (g):", min_value=float(peso_seco), max_value=float(peso_seco + 0.1), value=float(peso_seco + 0.0235), step=0.001, format="%.4f")
            vol_ml = st.select_slider("Volumen Filtrado (mL):", options=[100, 250, 500, 1000], value=250)
            
            sst = calcular_sst(peso_seco, peso_final, vol_ml)

        with c2:
            st.metric("Resultado SST", f"{sst} mg/L (ppm)")
            
            # Indicador de severidad
            if sst > 80:
                st.error("🔴 **Calidad Crítica:** Requiere retrolavado inmediato de filtros de cáscara de nuez.")
            elif sst > 30:
                st.warning("🟡 **Calidad Aceptable:** Vigilar presión diferencial en planta de inyección.")
            else:
                st.success("🟢 **Calidad Óptima:** Apagado de riesgo de taponamiento de la formación.")

    with tab2:
        st.subheader("Modelado Interactivo de Tendencia Incrustante / Corrosiva")
        
        col_lsi1, col_lsi2 = st.columns(2)
        with col_lsi1:
            ph = st.slider("pH Muestra:", 4.0, 10.0, 7.5, 0.1)
            temp_c = st.slider("Temperatura del Agua (°C):", 10.0, 90.0, 50.0, 1.0)
            tds = st.slider("TDS - Salinidad Total (mg/L):", 1000, 50000, 18000, 1000)
        
        with col_lsi2:
            ca = st.slider("Dureza Calcio Ca2+ (mg/L):", 50, 2000, 450, 25)
            alc = st.slider("Alcalinidad Total (mg/L CaCO3):", 50, 2000, 600, 25)
            
            lsi_val, tendencia = calcular_indice_langelier(ph, temp_c, tds, ca, alc)
            st.metric("Índice de Langelier (LSI)", f"{lsi_val}")
            
            if lsi_val > 0.2:
                st.warning(f"⚠️ **{tendencia}:** Riesgo de incrustación de CaCO3 en tubulares.")
            elif lsi_val < -0.2:
                st.error(f"🔴 **{tendencia}:** Severo ataque corrosivo al acero.")
            else:
                st.success(f"🟢 **{tendencia}:** Agua balanceada.")

    with tab3:
        st.subheader("🧪 Estimador de Dosificación de Antiincrustante en Planta")
        
        caudal_m3d = st.slider("Caudal de Agua a Tratar (m³/día):", 500, 10000, 3000, 250)
        ppm_dosis = st.slider("Dosis Recomendada por Laboratorio (ppm o g/m³):", 5, 100, 25, 5)
        precio_litro = st.number_input("Costo del Producto Químico (USD/Litro):", value=3.50, step=0.50)
        
        quimico_diario_l = (caudal_m3d * ppm_dosis) / 1000.0
        costo_diario = quimico_diario_l * precio_litro
        
        k1, k2 = st.columns(2)
        k1.metric("Consumo Diario de Químico", f"{round(quimico_diario_l, 1)} L/día")
        k2.metric("Costo Operativo Diario", f"{round(costo_diario, 2)} USD/día")

# -----------------------------------------------------------------------------
# MÓDULO 3: GAS NATURAL (INTERACTIVO CON GRÁFICO CROMATOGRÁFICO)
# -----------------------------------------------------------------------------
elif opcion_modulo == "3. Gas Natural: Cromatografía y Mezcla":
    st.markdown('<div class="main-header">🔥 Módulo Interactivo: Cromatografía de Gas Natural</div>', unsafe_allow_html=True)
    
    st.subheader("Composición Molar Ajustable (% Molar)")
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        c1 = st.slider("% Metano (C1):", 50.0, 98.0, 84.0, 0.5)
        c2 = st.slider("% Etano (C2):", 1.0, 15.0, 6.5, 0.5)
        c3 = st.slider("% Propano (C3):", 0.5, 10.0, 3.5, 0.1)
        ic4 = st.slider("% i-Butano (iC4):", 0.1, 5.0, 0.8, 0.1)
        nc4 = st.slider("% n-Butano (nC4):", 0.1, 5.0, 1.2, 0.1)
        c5_plus = st.slider("% C5+ (Heavy Ends):", 0.1, 5.0, 1.0, 0.1)
        co2 = st.slider("% CO2:", 0.0, 10.0, 1.8, 0.1)
        n2 = st.slider("% N2:", 0.0, 10.0, 1.2, 0.1)
        
        comp_dict = {'C1': c1, 'C2': c2, 'C3': c3, 'iC4': ic4, 'nC4': nc4, 'C5+': c5_plus, 'CO2': co2, 'N2': n2, 'H2S': 0.0}
        total_molar = sum(comp_dict.values())

    with col_c2:
        st.markdown(f"### Total Molar: **{round(total_molar, 2)}%**")
        
        if abs(total_molar - 100.0) > 0.01:
            st.warning("⚠️ Ajuste los deslizadores para que la suma molar sea exactamente 100.0%")
        else:
            mw, sg_gas, pcs = calcular_propiedades_gas(comp_dict)
            st.success("✅ Cromatografía Válida")
            
            g1, g2, g3 = st.columns(3)
            g1.metric("Peso Mol.", f"{mw} g/mol")
            g2.metric("Grav. Específica", f"{sg_gas}")
            g3.metric("PCS", f"{pcs} BTU/SCF")
            
            # Gráfico de barras interactivo cromatográfico
            df_gas = pd.DataFrame(list(comp_dict.items()), columns=['Componente', '% Molar'])
            fig_bar = px.bar(
                df_gas, x='Componente', y='% Molar', 
                color='% Molar', 
                title="Cromatograma de Gas Natural (GPA 2261)",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 4: CONTROL DE CALIDAD ISO 17025 (INTERACTIVO)
# -----------------------------------------------------------------------------
elif opcion_modulo == "4. Control de Calidad Dinámico (ISO 17025)":
    st.markdown('<div class="main-header">📈 Aseguramiento de Calidad Analítica (ISO 17025)</div>', unsafe_allow_html=True)
    
    c_q1, c_q2 = st.columns([1, 2])
    
    with c_q1:
        st.subheader("Parámetros del Material de Referencia")
        mrc_nom = st.number_input("Valor Certificado del MRC (Patrón):", value=0.8500, format="%.4f", step=0.001)
        desv_est = st.number_input("Desviación Estándar Aceptada (s):", value=0.0015, format="%.4f", step=0.0001)
        
        st.markdown("---")
        st.subheader("Simular Inserción de Muestra")
        
        # Slider interactivo para simular el valor medio en el laboratorio hoy
        dato_hoy = st.slider(
            "Medición del Analista HOY:", 
            min_value=float(mrc_nom - 5 * desv_est), 
            max_value=float(mrc_nom + 5 * desv_est), 
            value=float(mrc_nom + 0.0010), 
            step=0.0001,
            format="%.4f"
        )

    with c_q2:
        np.random.seed(12)
        datos_base = list(np.random.normal(mrc_nom, desv_est, 14))
        datos_completos = datos_base + [dato_hoy]
        
        fig_shewhart = generar_grafico_shewhart(datos_completos, mrc_nom, desv_est)
        st.plotly_chart(fig_shewhart, use_container_width=True)
        
        lcs = mrc_nom + 3 * desv_est
        lci = mrc_nom - 3 * desv_est
        
        if dato_hoy > lcs or dato_hoy < lci:
            st.error("🚨 **ALERTA CALIDAD (Reglas de Westgard):** Punto fuera de límites de control (±3s). Instrumento descalibrado. Repetir prueba.")
        else:
            st.success("✅ **ENSAYO VÁLIDO:** El sistema analítico opera bajo control estadístico.")
