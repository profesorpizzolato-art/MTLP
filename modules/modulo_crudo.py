import numpy as np

def calcular_api_corregido(api_observado, temp_f):
    """
    Calcula el °API corregido a 60°F usando una aproximación polinómica
    de las tablas ASTM 5A.
    """
    # Factor de corrección aproximado por expansión térmica
    delta_t = temp_f - 60.0
    factor_correccion = 0.054 * delta_t
    api_60 = api_observado - factor_correccion
    
    # Derivación de Specific Gravity (SG)
    sg_60 = 141.5 / (api_60 + 131.5)
    return round(api_60, 2), round(sg_60, 4)

def calcular_bsw(lectura_tubo1, lectura_tubo2):
    """
    Calcula el porcentaje volumétrico de BS&W según ASTM D4007.
    """
    bsw_total = lectura_tubo1 + lectura_tubo2
    return round(bsw_total, 2)

def evaluar_conformidad_crudo(api_60, bsw_total, limite_bsw_contrato=1.0):
    """
    Evalúa la especificación de transferencia de custodia.
    """
    conforme = bsw_total <= limite_bsw_contrato
    clasificacion = "Crudo Liviano" if api_60 >= 31.1 else "Crudo Mediano" if api_60 >= 22.3 else "Crudo Pesado"
    return conforme, clasificacion
