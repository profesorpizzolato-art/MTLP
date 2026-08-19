# modules/modulo_evaluacion.py
import random
from modules.modulo_crudo import calcular_api_corregido, calcular_bsw
from modules.modulo_agua import calcular_indice_langelier, calcular_sst
from modules.modulo_gas import calcular_propiedades_gas
from modules.modulo_emulsiones import calcular_eficiencia_deshidratacion, calcular_costo_tratamiento
from modules.modulo_viscosidad import calcular_viscosidad_temperatura
from modules.modulo_salinidad import calcular_ptb_sales
from modules.modulo_volatilidad import calcular_rvr_estimada
from modules.modulo_sara import evaluar_estabilidad_asfaltenos

def generar_caso_examen():
    """
    Genera aleatoriamente 1 de los 30 casos de evaluación práctica para el simulador MENFA.
    """
    id_caso = random.randint(1, 30)
    
    # -------------------------------------------------------------------------
    # MÓDULO 1: CRUDO Y BS&W (CASOS 1 A 4)
    # -------------------------------------------------------------------------
    if id_caso in [1, 2, 3, 4]:
        t1 = round(random.uniform(0.1, 2.0), 2)
        t2 = round(random.uniform(0.1, 2.0), 2)
        api_obs = round(random.uniform(18.0, 38.0), 1)
        temp_f = round(random.uniform(65.0, 105.0), 1)
        bsw_real = calcular_bsw(t1, t2)
        api_60, _ = calcular_api_corregido(api_obs, temp_f)
        
        return {
            "id": id_caso,
            "modulo": "Crudo y Centrifugado",
            "titulo": f"Evaluación de Calidad de Crudo - Muestra N° {id_caso}",
            "enunciado": f"Se analiza una muestra de petróleo en centrífuga ASTM D4007. El tubo 1 marca {t1} mL de sedimento/agua y el tubo 2 marca {t2} mL. La lectura del termohidrómetro fue de {api_obs} °API a {temp_f} °F.",
            "pregunta": "Calcule el porcentaje de BS&W Total (%):",
            "respuesta_correcta": bsw_real,
            "tolerancia": 0.05,
            "unidad": "%",
            "explicacion": f"El BS&W total corresponde a la suma de las lecturas de los dos tubos ({t1} + {t2} = {bsw_real}%). El °API corregido a 60°F es {api_60} °API."
        }

    # -------------------------------------------------------------------------
    # MÓDULO 2: AGUA DE INYECCIÓN Y LSI (CASOS 5 A 8)
    # -------------------------------------------------------------------------
    elif id_caso in [5, 6, 7, 8]:
        ph = round(random.uniform(6.8, 8.4), 2)
        temp_c = round(random.uniform(20.0, 65.0), 1)
        tds = random.randint(3000, 35000)
        ca = random.randint(150, 1200)
        alk = random.randint(200, 1500)
        lsi_real, diag = calcular_indice_langelier(ph, temp_c, tds, ca, alk)
        
        return {
            "id": id_caso,
            "modulo": "Agua de Inyección",
            "titulo": f"Análisis Fisicoquímico de Agua - Muestra N° {id_caso}",
            "enunciado": f"Se reporta un análisis de agua de producción con: pH={ph}, Temp={temp_c} °C, TDS={tds} ppm, Calcio={ca} ppm y Alcalinidad={alk} ppm.",
            "pregunta": "Calcule el Índice de Langelier (LSI) del agua:",
            "respuesta_correcta": lsi_real,
            "tolerancia": 0.15,
            "unidad": "LSI",
            "explicacion": f"El valor de LSI es {lsi_real}. Diagnóstico: {diag}."
        }

    # -------------------------------------------------------------------------
    # MÓDULO 3: GAS NATURAL Y CROMATOGRAFÍA (CASOS 9 A 12)
    # -------------------------------------------------------------------------
    elif id_caso in [9, 10, 11, 12]:
        c1 = round(random.uniform(70.0, 90.0), 1)
        c2 = round(random.uniform(3.0, 12.0), 1)
        c3 = round(random.uniform(1.0, 6.0), 1)
        co2 = round(random.uniform(0.5, 5.0), 1)
        n2 = round(100.0 - (c1 + c2 + c3 + co2), 1)
        pm, sg, pcs = calcular_propiedades_gas(c1, c2, c3, co2, n2)
        
        return {
            "id": id_caso,
            "modulo": "Gas Natural",
            "titulo": f"Cromatografía de Gas de Separador - Muestra N° {id_caso}",
            "enunciado": f"Análisis Molar (% mol): C1={c1}%, C2={c2}%, C3={c3}%, CO2={co2}%, N2={n2}%.",
            "pregunta": "Calcule el Poder Calorífico Superior (PCS) estimado en BTU/p³:",
            "respuesta_correcta": pcs,
            "tolerancia": 15.0,
            "unidad": "BTU/p³",
            "explicacion": f"El Poder Calorífico Superior es {pcs} BTU/p³, con un Peso Molecular de {pm} g/mol y Gravedad Específica {sg}."
        }

    # -------------------------------------------------------------------------
    # MÓDULO 4: CONTROL DE CALIDAD ISO 17025 (CASOS 13 A 16)
    # -------------------------------------------------------------------------
    elif id_caso in [13, 14, 15, 16]:
        media_patron = round(random.uniform(20.0, 40.0), 1)
        s = round(random.uniform(0.2, 0.8), 2)
        ucl_real = round(media_patron + (3 * s), 2)
        
        return {
            "id": id_caso,
            "modulo": "Control de Calidad ISO 17025",
            "titulo": f"Carta de Control Shewhart - Calibración N° {id_caso}",
            "enunciado": f"Se prepara una carta de control para un patrón de referencia con una media histórica de {media_patron} y una desviación estándar (s) de {s}.",
            "pregunta": "Calcule el Límite Superior de Control (UCL = +3s):",
            "respuesta_correcta": ucl_real,
            "tolerancia": 0.05,
            "unidad": "Unidades Analíticas",
            "explicacion": f"El UCL se calcula como Media + 3*s ({media_patron} + 3*{s} = {ucl_real})."
        }

    # -------------------------------------------------------------------------
    # MÓDULO 5: EMULSIONES Y TRATAMIENTO QUÍMICO (CASOS 17 A 20)
    # -------------------------------------------------------------------------
    elif id_caso in [17, 18, 19, 20]:
        caudal = random.randint(300, 3000)
        dosis = random.randint(20, 120)
        costo_unitario = round(random.uniform(2.5, 6.0), 2)
        litros, costo_diario_real = calcular_costo_tratamiento(dosis, caudal, costo_unitario)
        
        return {
            "id": id_caso,
            "modulo": "Emulsiones y Química",
            "titulo": f"Dosificación de Desemulsionante en Batería - Caso N° {id_caso}",
            "enunciado": f"Una batería procesa {caudal} m³/día de fluido bruto. Se dosifican {dosis} ppm de aditivo químico deshidratante. El producto tiene un costo de {costo_unitario} USD/Litro.",
            "pregunta": "Calcule el costo total diario del tratamiento en USD/día:",
            "respuesta_correcta": costo_diario_real,
            "tolerancia": 5.0,
            "unidad": "USD/día",
            "explicacion": f"Para {caudal} m³/día con {dosis} ppm se requieren {litros} L/día. Multiplicado por {costo_unitario} USD/L da ${costo_diario_real} USD/día."
        }

    # -------------------------------------------------------------------------
    # MÓDULO 6: VISCOSIMETRÍA Y RHEOLOGÍA (CASOS 21 A 23)
    # -------------------------------------------------------------------------
    elif id_caso in [21, 22, 23]:
        v1, t1 = 500.0, 20.0
        v2, t2 = 90.0, 50.0
        t_eval = round(random.uniform(30.0, 40.0), 1)
        v_est = calcular_viscosidad_temperatura(v1, t1, v2, t2, t_eval)
        
        return {
            "id": id_caso,
            "modulo": "Rheología y Viscosidad",
            "titulo": f"Estimación de Viscosidad por Curva Walther - Caso N° {id_caso}",
            "enunciado": f"Un crudo presenta {v1} cP a {t1} °C y {v2} cP a {t2} °C (ASTM D341).",
            "pregunta": f"Estime la viscosidad del crudo (en cP) a la temperatura del oleoducto de {t_eval} °C:",
            "respuesta_correcta": v_est,
            "tolerancia": 10.0,
            "unidad": "cP",
            "explicacion": f"Aplicando la doble logarítmica de Walther ASTM D341, la viscosidad proyectada a {t_eval} °C es {v_est} cP."
        }

    # -------------------------------------------------------------------------
    # MÓDULO 7: SALES EN CRUDO (CASOS 24 A 26)
    # -------------------------------------------------------------------------
    elif id_caso in [24, 25, 26]:
        cond = round(random.uniform(15.0, 120.0), 1)
        temp_c = 25.0
        ptb_real = calcular_ptb_sales(cond, temp_c)
        
        return {
            "id": id_caso,
            "modulo": "Salinidad en Crudo",
            "titulo": f"Determinación Conductimétrica de Sales - Muestra N° {id_caso}",
            "enunciado": f"En el ensayo electrométrico ASTM D3230 a 25 °C, la celda registra una conductividad de {cond} µS/cm.",
            "pregunta": "Calcule la concentración de sales en PTB (lb/1000 bbl):",
            "respuesta_correcta": ptb_real,
            "tolerancia": 0.8,
            "unidad": "PTB",
            "explicacion": f"La conductividad de {cond} µS/cm equivale a {ptb_real} PTB de sal en crudo."
        }

    # -------------------------------------------------------------------------
    # MÓDULO 8: VOLATILIDAD Y SEGURIDAD (CASOS 27 Y 28)
    # -------------------------------------------------------------------------
    elif id_caso in [27, 28]:
        api = round(random.uniform(28.0, 42.0), 1)
        temp_f = round(random.uniform(70.0, 110.0), 1)
        rvr_real = calcular_rvr_estimada(api, temp_f)
        
        return {
            "id": id_caso,
            "modulo": "Volatilidad y Seguridad",
            "titulo": f"Estimación de Presión de Vapor Reid (RVR) - Muestra N° {id_caso}",
            "enunciado": f"Se transfiere un crudo liviano/mediano de {api} °API almacenado a una temperatura de {temp_f} °F.",
            "pregunta": "Calcule la Presión de Vapor Reid (RVR/RVP) estimada en psi:",
            "respuesta_correcta": rvr_real,
            "tolerancia": 0.3,
            "unidad": "psi",
            "explicacion": f"La Presión de Vapor Reid estimada para un crudo de {api} °API a {temp_f} °F es {rvr_real} psi."
        }

    # -------------------------------------------------------------------------
    # MÓDULO 9: CARACTERIZACIÓN SARA (CASOS 29 Y 30)
    # -------------------------------------------------------------------------
    else:
        sat = round(random.uniform(35.0, 55.0), 1)
        aro = round(random.uniform(20.0, 35.0), 1)
        res = round(random.uniform(10.0, 20.0), 1)
        asf = round(random.uniform(4.0, 15.0), 1)
        cii_real, diag = evaluar_estabilidad_asfaltenos(sat, aro, res, asf)
        
        return {
            "id": id_caso,
            "modulo": "Caracterización SARA",
            "titulo": f"Análisis de Estabilidad Coloidal - Muestra N° {id_caso}",
            "enunciado": f"Resultados SARA (% peso): Saturados={sat}%, Aromáticos={aro}%, Resinas={res}%, Asfaltenos={asf}%.",
            "pregunta": "Calcule el Índice de Inestabilidad Coloidal (CII):",
            "respuesta_correcta": cii_real,
            "tolerancia": 0.05,
            "unidad": "CII",
            "explicacion": f"El CII es {cii_real}. Expresión: (Saturados + Asfaltenos) / (Aromáticos + Resinas). Diagnóstico: {diag}."
        }
