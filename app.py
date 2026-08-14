import sys
import os
import io

# Inyección del directorio raíz al PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Importación de submódulos locales
from modules.modulo_crudo import calcular_api_corregido, calcular_bsw, evaluar_conformidad_crudo
from modules.modulo_agua import calcular_sst, calcular_indice_langelier
from modules.modulo_gas import calcular_propiedades_gas
from modules.modulo_calidad import generar_grafico_shewhart
from modules.modulo_emulsiones import calcular_eficiencia_deshidratacion, calcular_costo_tratamiento
from modules.modulo_viscosidad import calcular_viscosidad_temperatura, evaluar_clasificacion_viscosidad
from modules.modulo_salinidad import calcular_ptb_sales, evaluar_conforme_sales
from modules.modulo_pdf import generar_pdf_protocolo_analitico

# Configuración de página
st.set_page_config(
    page_title="Simulador interactivo de Laboratorio | IPCL MENFA",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
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
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BARRA LATERAL
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/petroleum-press.png", width=70)
st.sidebar.title("LAB-PETRO MENFA 2.0")

st.sidebar.subheader("👤 Datos del Alumno")
nombre_estudiante = st.sidebar.text_input("Nombre y Apellido:", value="Estudiante MENFA")
legajo_estudiante = st.sidebar.text_input("DNI / Legajo:", value="UTN-2026")

st.sidebar.markdown("---")
opcion_modulo = st.sidebar.radio(
    "Seleccione Módulo de Trabajo:",
    [
        "1. Crudo: Deshidratación y Centrifugado",
        "2. Agua: Tratamiento e Incrustación",
        "3. Gas Natural: Cromatografía y Mezcla",
        "4. Control de Calidad Dinámico (ISO 17025)",
        "5. Emulsiones y Química Deshidratante",
        "6. Rheología y Viscosimetría de Crudos",
        "7. Determinación de Sales en Crudo (PTB)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Autoría y Desarrollo:**  
Fabricio Pizzolato  
*IPCL MENFA / Formación Técnica Oil & Gas*
""")

datos_estudiante = {
    'nombre': nombre_estudiante,
    'legajo': legajo_estudiante,
    'modulo': opcion_modulo,
    'muestra': 'Muestra Campo IPCL-1',
    'estado': 'Ensayo Finalizado'
}

def exportar_reportes(resultados_tabla, prefijo_archivo):
    st.markdown("---")
    with st.expander("📄 Exportar Protocolo Analítico y Datos"):
        pdf_bytes = generar_pdf_protocolo_analitico(datos_estudiante, resultados_tabla)
        c_exp1, c_exp2 = st.columns(2)
        c_exp1.download_button(
            label="📥 Descargar Protocolo en PDF",
            data=pdf_bytes,
            file_name=f"Protocolo_{prefijo_archivo}_{legajo_estudiante}.pdf",
            mime="application/pdf"
        )
        df_export = pd.DataFrame(resultados_tabla, columns=["Parámetro", "Valor Obtenido", "Límite / Referencia", "Dictamen"])
        buffer_excel = io.BytesIO()
        df_export.to_excel(buffer_excel, index=False)
        buffer_excel.seek(0)
        c_exp2.download_button(
            label="📊 Descargar Datos en Excel",
            data=buffer_excel,
            file_name=f"Datos_{prefijo_archivo}_{legajo_estudiante}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# -----------------------------------------------------------------------------
# MÓDULO 1: PETRÓLEO CRUDO
# -----------------------------------------------------------------------------
if opcion_modulo == "1. Crudo: Deshidratación y Centrifugado":
    st.markdown('<div class="main-header">🧪 Módulo 1: Calidad de Crudo y Deshidratación</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⚙️ Ensayo (ASTM D1298 / D4007)")
        api_obs = st.slider("°API Observado:", 10.0, 50.0, 28.5, 0.1)
        temp_f = st.slider("Temperatura (°F):", 50.0, 140.0, 85.0, 1.0)
        t1 = st.slider("Agua+Sed. Tubo 1 (mL):", 0.0, 5.0, 0.3, 0.05)
        t2 = st.slider("Agua+Sed. Tubo 2 (mL):", 0.0, 5.0, 0.3, 0.05)
        limite_contrato = st.number_input("Límite BS&W (%):", 0.1, 3.0, 0.5, 0.1)

    with col2:
        st.subheader("📊 Resultados")
        api_60, sg_60 = calcular_api_corregido(api_obs, temp_f)
        bsw_total = calcular_bsw(t1, t2)
        conforme, clasif = evaluar_conformidad_crudo(api_60, bsw_total, limite_contrato)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("°API (60°F)", f"{api_60}")
        m2.metric("Gravedad Esp.", f"{sg_60}")
        m3.metric("BS&W", f"{bsw_total}%")

        if conforme:
            st.success(f"✅ APTO | {clasif}")
        else:
            st.error(f"❌ RECHAZADO | BS&W > {limite_contrato}%")

        fig_pie = px.pie(names=['Petróleo Neto', 'BS&W'], values=[max(0.0, 100.0 - bsw_total), bsw_total], hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    exportar_reportes([
        ["°API Corregido (60°F)", f"{api_60} °API", "ASTM 5A", "OK"],
        ["Gravedad Específica", f"{sg_60}", "-", clasif],
        ["BS&W Total", f"{bsw_total} %", f"Máx {limite_contrato}%", "APTO" if conforme else "RECHAZADO"]
    ], "Crudo")

# -----------------------------------------------------------------------------
# MÓDULO 2: AGUA DE INYECCIÓN
# -----------------------------------------------------------------------------
elif opcion_modulo == "2. Agua: Tratamiento e Incrustación":
    st.markdown('<div class="main-header">💧 Módulo 2: Fisicoquímica de Agua e Índice de Langelier</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⚙️ Análisis de Gravimetría y Química")
        vol_ml = st.number_input("Volumen Filtrado (mL):", 100, 1000, 500, 50)
        p_ini = st.number_input("Peso Filtro Seco (mg):", 100.0, 5000.0, 1050.0, 10.0)
        p_fin = st.number_input("Peso Filtro + Residuo (mg):", 100.0, 5000.0, 1085.0, 10.0)
        
        st.markdown("---")
        ph = st.slider("pH del Agua:", 4.0, 10.0, 7.8, 0.1)
        temp_c = st.slider("Temperatura Operativa (°C):", 10.0, 90.0, 45.0, 1.0)
        tds = st.number_input("TDS (ppm):", 500, 100000, 15000, 1000)
        ca_ppm = st.number_input("Calcio Ca2+ (ppm):", 50, 5000, 400, 50)
        alk_ppm = st.number_input("Alcalinidad Total (ppm):", 50, 5000, 600, 50)

    with col2:
        st.subheader("📊 Diagnóstico de Agua")
        sst = calcular_sst(vol_ml, p_ini, p_fin)
        lsi, diag = calcular_indice_langelier(ph, temp_c, tds, ca_ppm, alk_ppm)
        
        m1, m2 = st.columns(2)
        m1.metric("SST (Sólidos Suspendidos)", f"{sst} ppm")
        m2.metric("Índice LSI (Langelier)", f"{lsi}")

        if lsi > 0.5:
            st.warning(f"⚠️ {diag}")
        elif lsi >= -0.5:
            st.success(f"✅ {diag}")
        else:
            st.error(f"🚨 {diag}")

        df_gauge = pd.DataFrame({"Parámetro": ["pH Actual", "LSI Index"], "Valor": [ph, lsi]})
        fig_bar = px.bar(df_gauge, x="Parámetro", y="Valor", color="Parámetro", text_auto=True)
        st.plotly_chart(fig_bar, use_container_width=True)

    exportar_reportes([
        ["Sólidos Suspendidos (SST)", f"{sst} mg/L", "Máx. 50 mg/L", "OK" if sst <= 50 else "EXCEDIDO"],
        ["Índice de Langelier (LSI)", f"{lsi}", "-0.5 a +0.5", diag]
    ], "Agua")

# -----------------------------------------------------------------------------
# MÓDULO 3: GAS NATURAL
# -----------------------------------------------------------------------------
elif opcion_modulo == "3. Gas Natural: Cromatografía y Mezcla":
    st.markdown('<div class="main-header">🔥 Módulo 3: Cromatografía y Poder Calorífico de Gas</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⚙️ Composición Molar (% mol)")
        c1 = st.slider("Metano (C1):", 50.0, 98.0, 85.0, 0.5)
        c2 = st.slider("Etano (C2):", 0.0, 15.0, 7.0, 0.5)
        c3 = st.slider("Propano (C3):", 0.0, 10.0, 3.0, 0.5)
        co2 = st.slider("Dióxido de Carbono (CO2):", 0.0, 10.0, 3.0, 0.5)
        n2 = st.slider("Nitrógeno (N2):", 0.0, 10.0, 2.0, 0.5)

    with col2:
        st.subheader("📊 Propiedades Térmicas")
        pm, sg, pcs = calcular_propiedades_gas(c1, c2, c3, co2, n2)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("PM Mezcla", f"{pm} g/mol")
        m2.metric("Grav. Específica", f"{sg}")
        m3.metric("PCS (Poder Cal.)", f"{pcs} BTU/p³")

        df_croma = pd.DataFrame({
            "Componente": ["Metano (C1)", "Etano (C2)", "Propano (C3)", "CO2", "N2"],
            "Molar %": [c1, c2, c3, co2, n2]
        })
        fig_croma = px.bar(df_croma, x="Componente", y="Molar %", color="Componente", text_auto=True)
        st.plotly_chart(fig_croma, use_container_width=True)

    exportar_reportes([
        ["Peso Molecular Mezcla", f"{pm} g/mol", "16.0 - 22.0", "CONFORME"],
        ["Gravedad Específica (Aire=1)", f"{sg}", "0.55 - 0.75", "CONFORME"],
        ["Poder Calorífico Superior", f"{pcs} BTU/p³", "Min. 950 BTU/p³", "APTO COMERCIAL"]
    ], "Gas")

# -----------------------------------------------------------------------------
# MÓDULO 4: CONTROL DE CALIDAD ISO 17025
# -----------------------------------------------------------------------------
elif opcion_modulo == "4. Control de Calidad Dinámico (ISO 17025)":
    st.markdown('<div class="main-header">📈 Módulo 4: Gráficos de Control Shewhart (ISO 17025)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("⚙️ Parámetros de Control")
        n_puntos = st.slider("Cantidad de Muestras Evaluar:", 10, 30, 15, 1)
        media_ref = st.number_input("Valor de Referencia (Patrón):", 10.0, 100.0, 28.5, 0.1)
        desv_std = st.number_input("Desviación Estándar (s):", 0.05, 2.0, 0.3, 0.05)

    with col2:
        st.subheader("📊 Carta de Control Analítica")
        datos, media, ucl, lcl, uwl, lwl = generar_grafico_shewhart(n_puntos, media_ref, desv_std)
        
        fig_cc = go.Figure()
        x_axis = list(range(1, n_puntos + 1))
        fig_cc.add_trace(go.Scatter(x=x_axis, y=datos, mode='lines+markers', name='Lectura'))
        fig_cc.add_hline(y=media, line_dash="solid", line_color="green", annotation_text="Media")
        fig_cc.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL (+3s)")
        fig_cc.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL (-3s)")
        fig_cc.add_hline(y=uwl, line_dash="dot", line_color="orange", annotation_text="UWL (+2s)")
        fig_cc.add_hline(y=lwl, line_dash="dot", line_color="orange", annotation_text="LWL (-2s)")
        
        st.plotly_chart(fig_cc, use_container_width=True)

    exportar_reportes([
        ["Media del Sistema", f"{media}", f"{media_ref}", "EN CONTROL"],
        ["Límite Superior Control (UCL)", f"{ucl}", "+3s", "LÍMITE MÁX"],
        ["Límite Inferior Control (LCL)", f"{lcl}", "-3s", "LÍMITE MÍN"]
    ], "Calidad")

# -----------------------------------------------------------------------------
# MÓDULO 5: EMULSIONES Y QUÍMICA
# -----------------------------------------------------------------------------
elif opcion_modulo == "5. Emulsiones y Química Deshidratante":
    st.markdown('<div class="main-header">🧪 Módulo 5: Dosificación Química y Tratamiento de Emulsiones</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⚙️ Parámetros de Operación")
        bsw_in = st.slider("BS&W Entrada (Crudo Bruto %):", 5.0, 60.0, 25.0, 1.0)
        bsw_out = st.slider("BS&W Salida (Tratado %):", 0.1, 5.0, 0.4, 0.1)
        caudal = st.number_input("Caudal de Planta (m³/día):", 50, 5000, 1200, 50)
        dosis = st.slider("Dosis Química Desemulsionante (ppm):", 10, 300, 45, 5)
        costo_l = st.number_input("Costo Aditivo (USD/Litro):", 1.0, 20.0, 3.5, 0.5)

    with col2:
        st.subheader("📊 Balance Operativo")
        efic = calcular_eficiencia_deshidratacion(bsw_in, bsw_out)
        litros_d, costo_d = calcular_costo_tratamiento(dosis, caudal, costo_l)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Eficiencia", f"{efic}%")
        m2.metric("Consumo Química", f"{litros_d} L/día")
        m3.metric("Costo Diario", f"${costo_d} USD")

        if efic >= 95.0:
            st.success("✅ **TRATAMIENTO EFICIENTE Y OPTIMIZADO**")
        else:
            st.warning("⚠️ **INSUFICIENTE SEPARACIÓN**: Ajustar temperatura o dosis química")

    exportar_reportes([
        ["Eficiencia de Deshidratación", f"{efic} %", "Min 95.0 %", "ÓPTIMA" if efic >= 95 else "A JUSTAR"],
        ["Consumo Diario Aditivo", f"{litros_d} L/día", f"Dosis: {dosis} ppm", "OK"],
        ["Costo Operativo Diario", f"${costo_d} USD", "-", "EVALUADO"]
    ], "Emulsiones")

# -----------------------------------------------------------------------------
# MÓDULO 6: VISCOSIMETRÍA
# -----------------------------------------------------------------------------
elif opcion_modulo == "6. Rheología y Viscosimetría de Crudos":
    st.markdown('<div class="main-header">🧪 Módulo 6: Viscosimetría y Curva Rheológica (ASTM D341)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⚙️ Curva Walther (ASTM D341)")
        v1 = st.number_input("Viscosidad Medida 1 (cP):", 1.0, 5000.0, 450.0, 10.0)
        t1 = st.number_input("Temperatura Medición 1 (°C):", 10.0, 100.0, 20.0, 1.0)
        v2 = st.number_input("Viscosidad Medida 2 (cP):", 1.0, 5000.0, 85.0, 5.0)
        t2 = st.number_input("Temperatura Medición 2 (°C):", 10.0, 100.0, 50.0, 1.0)
        t_obj = st.slider("Temperatura Operativa Objetivo (°C):", 5.0, 90.0, 35.0, 1.0)

    with col2:
        st.subheader("📊 Estimación de Fluidez")
        v_est = calcular_viscosidad_temperatura(v1, t1, v2, t2, t_obj)
        cat, rec = evaluar_clasificacion_viscosidad(v_est)
        
        st.metric("Viscosidad Estimada", f"{v_est} cP", delta=f"@ {t_obj} °C")
        st.info(f"**Categoría:** {cat}\n\n**Recomendación:** {rec}")

        # Gráfico dinámico de perfil de temperatura
        temps = np.linspace(10, 80, 20)
        viscs = [calcular_viscosidad_temperatura(v1, t1, v2, t2, t) for t in temps]
        df_visc = pd.DataFrame({"Temperatura (°C)": temps, "Viscosidad (cP)": viscs})
        fig_visc = px.line(df_visc, x="Temperatura (°C)", y="Viscosidad (cP)", markers=True)
        st.plotly_chart(fig_visc, use_container_width=True)

    exportar_reportes([
        [f"Viscosidad a {t_obj}°C", f"{v_est} cP", "ASTM D341", cat],
        ["Diagnóstico de Bombeabilidad", cat, "-", rec]
    ], "Viscosidad")

# -----------------------------------------------------------------------------
# MÓDULO 7: SALES EN CRUDO
# -----------------------------------------------------------------------------
elif opcion_modulo == "7. Determinación de Sales en Crudo (PTB)":
    st.markdown('<div class="main-header">🧂 Módulo 7: Contenido de Sales Electrométrico (ASTM D3230)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⚙️ Parámetros de Mediciones Conductimétricas")
        cond = st.number_input("Conductividad Medida (µS/cm):", 1.0, 500.0, 48.0, 1.0)
        temp_c = st.slider("Temperatura de Celda (°C):", 15.0, 40.0, 25.0, 0.5)
        lim_ptb = st.number_input("Límite de Entrega (PTB):", 1.0, 50.0, 10.0, 1.0)

    with col2:
        st.subheader("📊 Resultado Analítico")
        ptb = calcular_ptb_sales(cond, temp_c)
        es_conforme, msj = evaluar_conforme_sales(ptb, lim_ptb)
        
        m1, m2 = st.columns(2)
        m1.metric("Sales Totales", f"{ptb} PTB")
        m2.metric("Límite Especificado", f"{lim_ptb} PTB")

        if es_conforme:
            st.success(f"✅ **{msj}**")
        else:
            st.error(f"🚨 **{msj}**")

    exportar_reportes([
        ["Sales Totales (PTB)", f"{ptb} PTB", f"Máx {lim_ptb} PTB", "CONFORME" if es_conforme else "NO CONFORME"],
        ["Conductividad Corregida", f"{cond} µS/cm", "@ 25°C", "EVALUADO"]
    ], "Salinidad")
    
