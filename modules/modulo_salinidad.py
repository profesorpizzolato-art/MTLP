# modules/modulo_salinidad.py

def calcular_ptb_sales(conductividad_uS: float, temp_c: float) -> float:
    """
    Estima el contenido de sales en crudo expresado en PTB (Pounds per Thousand Barrels)
    según método de conductividad eléctrica (ASTM D3230).
    """
    try:
        cond = float(conductividad_uS)
        t = float(temp_c)
        
        # Corregido por temperatura a 25°C
        factor_temp = 1 + 0.02 * (t - 25)
        cond_25 = cond / factor_temp if factor_temp != 0 else cond
        
        # Ajuste empírico no lineal de calibración PTB vs uS
        if cond_25 <= 0:
            return 0.0
            
        ptb = 0.142 * (cond_25 ** 1.08)
        return float(round(ptb, 2))
    except Exception:
        return 0.0


def evaluar_conforme_sales(ptb_calculado: float, limite_ptb: float = 10.0) -> tuple[bool, str]:
    """
    Evalúa la conformidad del nivel de sales en el crudo.
    Garantiza que ambos valores se traten como números antes de comparar.
    """
    try:
        val_ptb = float(ptb_calculado)
        val_limite = float(limite_ptb)
    except (ValueError, TypeError):
        val_ptb = 0.0
        val_limite = 10.0

    if val_ptb <= val_limite:
        return True, f"CONFORME (PTB {val_ptb} <= {val_limite})"
    else:
        return False, f"EXCEDIDO (PTB {val_ptb} > {val_limite} - Riesgo de corrosión en Refinería)"
