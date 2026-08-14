import math

def calcular_sst(peso_filtro_seco_g, peso_filtro_final_g, volumen_muestra_ml):
    """
    Calcula Sólidos Suspendidos Totales (SST) en mg/L según Standard Methods 2540 D.
    """
    if volumen_muestra_ml <= 0:
        return 0.0
    diferencia_masa_g = peso_filtro_final_g - peso_filtro_seco_g
    sst_mg_l = (diferencia_masa_g * 1_000_000) / volumen_muestra_ml
    return round(sst_mg_l, 2)

def calcular_indice_langelier(ph, temp_c, tds_mg_l, ca_mg_l, alcalinidad_mg_l):
    """
    Aproximación simplificada del Índice de Saturación de Langelier (LSI).
    LSI = pH - pHs
    """
    # Factores empíricos
    A = (math.log10(tds_mg_l) - 1) / 10 if tds_mg_l > 0 else 0
    B = -13.12 * math.log10(temp_c + 273.15) + 34.55
    C = math.log10(ca_mg_l) - 0.4 si_ca_valido if (ca_mg_l := max(ca_mg_l, 1)) else 0
    D = math.log10(alcalinidad_mg_l) if alcalinidad_mg_l > 0 else 0
    
    pKs = 11.0 - A + B
    pKa = 10.3
    pHs = (9.3 + A + B) - (C + D)
    lsi = ph - pHs
    
    tendencia = "Incrustante" if lsi > 0.2 else "Corrosiva" if lsi < -0.2 else "Neutro / Equilibrado"
    return round(lsi, 2), tendencia
