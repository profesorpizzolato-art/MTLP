def calcular_propiedades_gas(composicion_molar):
    """
    Dada una composición molar (dict), calcula Peso Molecular, 
    Gravedad Específica y Poder Calorífico aproximado (BTU/SCF).
    """
    # Pesos moleculares g/mol
    mw_componentes = {
        'C1': 16.04, 'C2': 30.07, 'C3': 44.10,
        'iC4': 58.12, 'nC4': 58.12, 'C5+': 72.15,
        'CO2': 44.01, 'N2': 28.01, 'H2S': 34.08
    }
    
    # Poder calorífico aprox (BTU/SCF)
    pcs_componentes = {
        'C1': 1010, 'C2': 1790, 'C3': 2590,
        'iC4': 3360, 'nC4': 3370, 'C5+': 4000,
        'CO2': 0, 'N2': 0, 'H2S': 637
    }
    
    mw_mezcla = sum((composicion_molar.get(comp, 0) / 100.0) * mw 
                    for comp, mw in mw_componentes.items())
    
    pcs_mezcla = sum((composicion_molar.get(comp, 0) / 100.0) * pcs 
                     for comp, pcs in pcs_componentes.items())
    
    sg_gas = mw_mezcla / 28.9625
    
    return round(mw_mezcla, 2), round(sg_gas, 4), round(pcs_mezcla, 1)
