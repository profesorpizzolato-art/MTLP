# modules/modulo_calidad.py
import numpy as np

def generar_grafico_shewhart(n_muestras: int = 15, media_referencia: float = 28.5, std_dev: float = 0.3) -> tuple[list, float, float, float, float, float]:
    """
    Simula o procesa datos para una Carta de Control Shewhart (ISO 17025).
    Retorna: (datos, media, ucl, lcl, uwl, lwl)
    """
    try:
        n_puntos = int(n_muestras)
        media_ref = float(media_referencia)
        s = float(std_dev)
    except (ValueError, TypeError):
        n_puntos, media_ref, s = 15, 28.5, 0.3

    # Generación de datos sintéticos con semilla fija para reproducibilidad
    np.random.seed(42)
    datos = np.random.normal(media_ref, s, n_puntos)
    
    # Induce una desviación puntual controlada para fines pedagógicos
    if n_puntos >= 9:
        datos[8] = media_ref + (s * 3.1)

    ucl = media_ref + (3 * s)
    lcl = media_ref - (3 * s)
    uwl = media_ref + (2 * s)
    lwl = media_ref - (2 * s)
    
    datos_lista = [round(float(x), 2) for x in datos]
    
    return datos_lista, round(media_ref, 2), round(ucl, 2), round(lcl, 2), round(uwl, 2), round(lwl, 2)
