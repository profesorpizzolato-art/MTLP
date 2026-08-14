def calcular_ptb_sales(conductividad_uS, factor_calibracion=0.85):
    """
    Calcula la concentración de sales en lb/1000 bbl (PTB) según ASTM D3230.
    """
    ptb = conductividad_uS * factor_calibracion
    mg_l_equiv = ptb * 2.85  # Conversión aproximada a mg/L de NaCl en la mezcla
    return round(ptb, 2), round(mg_l_equiv, 1)

def evaluar_conforme_sales(ptb_calculado, limite_ptb=10.0):
    """
    Evalúa si cumple con la especificación de entrega a refinería/oleoducto (típicamente <= 10-20 PTB).
    """
    conforme = ptb_calculado <= limite_ptb
    return conforme
