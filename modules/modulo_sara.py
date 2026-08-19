# modules/modulo_sara.py

def evaluar_estabilidad_asfaltenos(saturados: float, aromaticos: float, resinas: float, asfaltenos: float):
    """
    Calcula el Índice de Inestabilidad Coloidal (CII) para SARA.
    CII = (Saturados + Asfaltenos) / (Aromáticos + Resinas)
    """
    denominador = aromaticos + resinas
    if denominador == 0:
        return 0.0, "Error en fracciones"
    
    cii = round((saturados + asfaltenos) / denominador, 2)
    
    if cii < 0.7:
        diagnostico = "Crudo Estable (Bajo riesgo de precipitación)"
    elif cii <= 0.9:
        diagnostico = "Crudo Moderadamente Inestable (Riesgo Medio)"
    else:
        diagnostico = "Crudo Inestable (Alto riesgo de precipitación de Asfaltenos)"
        
    return cii, diagnostico
