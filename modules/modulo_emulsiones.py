import numpy as np

def calcular_eficiencia_deshidratacion(bsw_inicial, bsw_final):
    """
    Calcula el porcentaje de separación / eficiencia del tratamiento químico.
    """
    if bsw_inicial <= 0:
        return 0.0
    eficiencia = ((bsw_inicial - bsw_final) / bsw_inicial) * 100.0
    return round(max(0.0, eficiencia), 2)

def calcular_costo_tratamiento(caudal_crudo_m3d, dosis_ppm, costo_quimico_usd_l, densidad_quimico_kg_l=1.0):
    """
    Calcula el consumo volumétrico diario de demulsificante y el costo asociado.
    dosis_ppm = Litros de químico por millón de Litros de emulsion / m3 de químico por millón de m3.
    1 ppm = 1 mL/m3 = 0.001 L/m3.
    """
    volumen_quimico_diario_l = caudal_crudo_m3d * (dosis_ppm / 1000.0)
    costo_diario_usd = volumen_quimico_diario_l * costo_quimico_usd_l
    costo_por_m3_crudo = costo_diario_usd / caudal_crudo_m3d if caudal_crudo_m3d > 0 else 0.0
    
    return round(volumen_quimico_diario_l, 2), round(costo_diario_usd, 2), round(costo_por_m3_crudo, 3)
