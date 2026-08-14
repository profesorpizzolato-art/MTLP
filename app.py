import sys
import os

# Asegura que el directorio raíz esté en el path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ahora sí realizas las importaciones locales
import streamlit as st
import numpy as np
import pandas as pd

from modules.modulo_crudo import calcular_api_corregido, calcular_bsw, evaluar_conformidad_crudo
from modules.modulo_agua import calcular_sst, calcular_indice_langelier
from modules.modulo_gas import calcular_propiedades_gas
from modules.modulo_calidad import generar_grafico_shewhart
from modules.modulo_emulsiones import calcular_eficiencia_deshidratacion, calcular_costo_tratamiento
from modules.modulo_viscosidad import calcular_viscosidad_temperatura
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
# BARRA LATERAL - NAVEGACIÓN, REGISTRO Y AUTORÍA
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

# Datos base del estudiante para exportación
datos_estudiante = {
    'nombre': nombre_estudiante,
    'legajo': legajo_estudiante,
    'modulo': opcion_modulo,
    'muestra': 'Muestra de Campo IPCL-1',
    'estado': 'Ensayo Finalizado'
}

# -----------------------------------------------------------------------------
# MÓDULO 1: PETRÓLEO CRUDO
# -----------------------------------------------------------------------------
if opcion_modulo == "1. Crudo: Deshidratación y Centrifugado":
    st.markdown('<div class="main-header">🧪 Módulo Interactivo: Calidad de Crudo y Deshidratación</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Parámetros de Prueba (ASTM D1298 / D4007)")
        api_obs = st.slider("°API Observado (Lectura en probeta):", 10.0, 50.0, 28.5, 0.1)
        temp_f = st.slider("Temperatura de Ensayo (°F):", 50.0, 140.0, 85.0, 1.0)
        
        st.markdown("---")
        t1 = st.slider("Agua + Sedimento Tubo 1 (mL):", 0.0, 5.0, 0.3, 0.05)
        t2 = st.slider("Agua + Sedimento Tubo 2 (mL):", 0.0, 5.0, 0.3, 0.05)
        limite_contrato = st.number_input("Límite Contractual BS&W (% v/v):", 0.1, 3.0, 0.5, 0.1)

    with col2:
        st.subheader("📊 Resultados en Tiempo Real")
        api_60, sg_60 = calcular_api_corregido(api_obs, temp_f)
        bsw_total = calcular_bsw(t1, t2)
        conforme, clasificacion = evaluar_conformidad_crudo(api_60, bsw_total, limite_contrato)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("°API Corregido", f"{api_60} °API")
        m2.metric("Gravedad Esp.", f"{sg_60}")
        m3.metric("BS&W Total", f"{bsw_total} %")

        if conforme:
            st.success(f"✅ **CRUDO APTO PARA DESPACHO** | Clasificación: **{clasificacion}**")
        else:
            st.error(f"❌ **RECHAZADO EN TANQUE** | Supera el máximo de {limite_contrato}% BS&W")

        fig_pie = px.pie(
            names=['Petróleo Neto', 'BS&W'],
            values=[max(0.0, 100.0 - bsw_total), bsw_total],
            color_discrete_sequence=['#1E3A8A', '#EF4444'],
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # BLOQUE DE EXPORTACIÓN Y REPORTES
    st.markdown("---")
    with st.expander("📄 Exportar Protocolo Analítico y Datos"):
        dictamen = "APTO DESPACHO" if conforme else "NO CONFORME / RECHAZADO"
        
        resultados_tabla = [
            ["°API Corregido (60°F)", f"{api_60} °API", "Según Tabla ASTM 5A", "OK"],
            ["Gravedad Específica", f"{sg_60}", "-", clasificacion],
            ["Contenido de BS&W", f"{bsw_total} %", f"Máx. {limite_contrato} %", dictamen]
        ]
        
        pdf_bytes = generar_pdf_protocolo_analitico(datos_estudiante, resultados_tabla)
        
        c_exp1, c_exp2 = st.columns(2)
        c_exp1.download_button(
            label="📥 Descargar Protocolo en PDF",
            data=pdf_bytes,
            file_name=f"Protocolo_Crudo_{legajo_estudiante}.pdf",
            mime="application/pdf"
        )
        
        df_export = pd.DataFrame(resultados_tabla, columns=["Parámetro", "Valor Obtenido", "Límite Especificado", "Dictamen"])
        buffer_excel = io.BytesIO()
        df_export.to_excel(buffer_excel, index=False)
        buffer_excel.seek(0)
        
        c_exp2.download_button(
            label="📊 Descargar Datos en Excel",
            data=buffer_excel,
            file_name=f"Datos_Crudo_{legajo_estudiante}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# -----------------------------------------------------------------------------
# RESTO DE LOS MÓDULOS (2 AL 7)
# -----------------------------------------------------------------------------
elif opcion_modulo == "2. Agua: Tratamiento e Incrustación":
    st.markdown('<div class="main-header">💧 Módulo Interactivo: Fisicoquímica y Tratamiento de Agua</div>', unsafe_allow_html=True)
    st.info("Ajuste los parámetros gravimétricos y de LSI para simular la calidad del agua de inyección.")

elif opcion_modulo == "3. Gas Natural: Cromatografía y Mezcla":
    st.markdown('<div class="main-header">🔥 Módulo Interactivo: Cromatografía de Gas Natural</div>', unsafe_allow_html=True)

elif opcion_modulo == "4. Control de Calidad Dinámico (ISO 17025)":
    st.markdown('<div class="main-header">📈 Aseguramiento de Calidad Analítica (ISO 17025)</div>', unsafe_allow_html=True)

elif opcion_modulo == "5. Emulsiones y Química Deshidratante":
    st.markdown('<div class="main-header">🧪 Módulo Interactivo: Emulsiones y Química Deshidratante</div>', unsafe_allow_html=True)

elif opcion_modulo == "6. Rheología y Viscosimetría de Crudos":
    st.markdown('<div class="main-header">🧪 Módulo de Viscosimetría y Rheología de Crudos</div>', unsafe_allow_html=True)

elif opcion_modulo == "7. Determinación de Sales en Crudo (PTB)":
    st.markdown('<div class="main-header">🧂 Módulo de Determinación de Sales en Crudo (ASTM D3230)</div>', unsafe_allow_html=True)
