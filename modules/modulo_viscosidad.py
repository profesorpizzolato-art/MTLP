import numpy as np

def calcular_viscosidad_temperatura(v1: float, t1_c: float, v2: float, t2_c: float, t_obj_c: float) -> float:
    """
    Estima la viscosidad (cP/cSt) a una temperatura objetivo (t_obj_c)
    usando la relación logarítmica de Walther (ASTM D341).
    """
    try:
        t1_k = t1_c + 273.15
        t2_k = t2_c + 273.15
        t_obj_k = t_obj_c + 273.15

        if t1_k == t2_k or v1 <= 0 or v2 <= 0:
            return float(round(v1, 2))

        log_v1 = np.log10(np.log10(v1 + 0.7))
        log_v2 = np.log10(np.log10(v2 + 0.7))
        log_t1 = np.log10(t1_k)
        log_t2 = np.log10(t2_k)

        b = (log_v1 - log_v2) / (log_t2 - log_t1)
        a = log_v1 + b * log_t1

        log_v_obj = a - b * np.log10(t_obj_k)
        viscosidad_estimada = (10 ** (10 ** log_v_obj)) - 0.7

        if np.isnan(viscosidad_estimada) or np.isinf(viscosidad_estimada):
            raise ValueError("Valor fuera de rango")

        return float(round(viscosidad_estimada, 2))

    except Exception:
        # Respaldo de interpolación semilogarítmica
        try:
            ln_v1 = np.log(v1)
            ln_v2 = np.log(v2)
            slope = (ln_v2 - ln_v1) / (t2_c - t1_c)
            v_fallback = np.exp(ln_v1 + slope * (t_obj_c - t1_c))
            return float(round(v_fallback, 2))
        except Exception:
            return float(round(v1, 2))


def evaluar_clasificacion_viscosidad(viscosidad_cp: float) -> tuple[str, str]:
    if viscosidad_cp > 500:
        return (
            "ALTA VISCOSIDAD",
            "Riesgo de alta pérdida de carga en oleoductos. Se recomienda dilución con nafta o calentamiento."
        )
    elif viscosidad_cp > 150:
        return (
            "VISCOSIDAD MODERADA",
            "Apto para transporte estándar, evaluar uso de reductores de fricción (DRA)."
        )
    else:
        return (
            "FLUIDEZ ÓPTIMA",
            "Excelente bombeabilidad y bajas pérdidas por fricción."
        )
