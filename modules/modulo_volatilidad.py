# modules/modulo_volatilidad.py

def calcular_rvr_estimada(api_corregido: float, temp_operativa_f: float) -> float:
    """
    Estima la Presión de Vapor Reid (RVR/RVP en psi) según API y Temperatura.
    """
    # Aproximación semi-empírica para crudos
    rvr_base = (api_corregido / 10.0) ** 1.35
    factor_temp = (temp_operativa_f / 60.0) ** 0.8
    rvr_psi = round(rvr_base * factor_temp * 0.18, 2)
    return rvr_psi

def evaluar_flash_point(flash_point_c: float, limite_seguridad_c: float = 60.0):
    """
    Evalúa la seguridad por Punto de Inflamación (ASTM D93).
    """
    if flash_point_c < 23.0:
        categoria = "Líquido Inflamable Clase I (Alto Riesgo)"
        apto = False
    elif flash_point_c < limite_seguridad_c:
        categoria = "Líquido Combustible Clase II (Riesgo Moderado)"
        apto = False
    else:
        categoria = "Líquido Combustible Clase III (Apto Seguro)"
        apto = True
        
    return apto, categoria
