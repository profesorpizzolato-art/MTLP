import numpy as np
import plotly.graph_objects as go

def generar_grafico_shewhart(valores_historicos, valor_referencia_mrc, desviacion_estandar):
    """
    Genera un Gráfico de Control de Shewhart (ISO 17025) interactivo con Plotly.
    """
    lcs = valor_referencia_mrc + 3 * desviacion_estandar
    lci = valor_referencia_mrc - 3 * desviacion_estandar
    las = valor_referencia_mrc + 2 * desviacion_estandar
    lai = valor_referencia_mrc - 2 * desviacion_estandar

    fig = go.Figure()

    # Puntos medidos
    muestras = list(range(1, len(valores_historicos) + 1))
    fig.add_trace(go.Scatter(x=muestras, y=valores_historicos, mode='lines+markers', name='Valor Medido', line=dict(color='blue')))

    # Líneas de Control
    fig.add_hline(y=valor_referencia_mrc, line_dash="solid", line_color="green", annotation_text="Media (MRC)")
    fig.add_hline(y=lcs, line_dash="dash", line_color="red", annotation_text="LCS (+3s)")
    fig.add_hline(y=lci, line_dash="dash", line_color="red", annotation_text="LCI (-3s)")
    fig.add_hline(y=las, line_dash="dot", line_color="orange", annotation_text="LAS (+2s)")
    fig.add_hline(y=lai, line_dash="dot", line_color="orange", annotation_text="LAI (-2s)")

    fig.update_layout(
        title="Gráfico de Control de Shewhart (Aseguramiento de Calidad)",
        xaxis_title="Número de Ensayo / Día",
        yaxis_title="Resultado del MRC",
        template="plotly_white"
    )
    return fig
