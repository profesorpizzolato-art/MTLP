# modules/modulo_emulsiones.py

def calcular_eficiencia_deshidratacion(bsw_entrada: float, bsw_salida: float) -> float:
    """Calcula la eficiencia de separación del tratamiento térmico/químico."""
    try:
        bsw_in = float(bsw_entrada)
        bsw_out = float(bsw_salida)
        if bsw_in <= 0:
            return 0.0
        eficiencia = ((bsw_in - bsw_out) / bsw_in) * 100.0
        return float(round(max(0.0, eficiencia), 2))
    except Exception:
        return 0.0

def calcular_costo_tratamiento(dosis_ppm: float, caudal_m3d: float, costo_litro_usd: float) -> tuple[float, float]:
    """
    Calcula consumo diario de aditivo (L/día) y costo operativo diario (USD/día).
    Fórmula: Litros/día = (dosis_ppm * caudal_m3d) / 1000.0
    """
    try:
        dosis = float(dosis_ppm)
        caudal = float(caudal_m3d)
        costo_l = float(costo_litro_usd)
        
        # 1 m³ de agua/crudo = 1000 L -> dosis (ppm) / 1,000,000 * caudal * 1000 L
        litros_dia = (dosis * caudal) / 1000.0
        costo_dia = litros_dia * costo_l
        
        return round(litros_dia, 2), round(costo_dia, 2)
    except Exception:
        return 0.0, 0.0
