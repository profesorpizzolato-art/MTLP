# modules/modulo_gas.py

def calcular_propiedades_gas(c1: float = 85.0, c2: float = 7.0, c3: float = 3.0, co2: float = 3.0, n2: float = 2.0) -> tuple[float, float, float]:
    """
    Calcula Peso Molecular (PM), Gravedad Específica (SG) y Poder Calorífico Superior (PCS en BTU/p³)
    para una mezcla cromatográfica básica.
    """
    try:
        # Conversión explícita a float para evitar TypeError por tipos incompatibles
        c1_f = float(c1)
        c2_f = float(c2)
        c3_f = float(c3)
        co2_f = float(co2)
        n2_f = float(n2)
        
        total = c1_f + c2_f + c3_f + co2_f + n2_f
        
        if total <= 0:
            return 0.0, 0.0, 0.0
        
        # Fracciones molares normalizadas
        y_c1 = c1_f / total
        y_c2 = c2_f / total
        y_c3 = c3_f / total
        y_co2 = co2_f / total
        y_n2 = n2_f / total
        
        # Pesos moleculares (g/mol)
        pm = (y_c1 * 16.04) + (y_c2 * 30.07) + (y_c3 * 44.10) + (y_co2 * 44.01) + (y_n2 * 28.01)
        
        # Gravedad Específica respecto al Aire (PM Aire = 28.96 g/mol)
        sg = pm / 28.96
        
        # Poder Calorífico Superior (PCS) base seca (BTU/scf)
        pcs = (y_c1 * 1010.0) + (y_c2 * 1773.0) + (y_c3 * 2516.0)
        
        return round(pm, 2), round(sg, 3), round(pcs, 1)

    except Exception:
        # Fallback seguro para evitar que la app crashee en Streamlit
        return 0.0, 0.0, 0.0
