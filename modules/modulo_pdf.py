import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

def generar_pdf_protocolo_analitico(datos_estudiante, resultados_ensayo):
    """
    Genera un archivo PDF binario en memoria con el Protocolo Analítico de Laboratorio.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )
    
    label_style = ParagraphStyle('Label', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#1E293B"))
    value_style = ParagraphStyle('Value', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#334155"))
    
    story = []
    
    # 1. Encabezado Institucional
    story.append(Paragraph("IPCL MENFA - LABORATORIO DE ENSAYOS OIL & GAS", title_style))
    story.append(Paragraph("Protocolo Analítico de Control de Calidad | ISO/IEC 17025", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#3B82F6"), spaceAfter=15))
    
    # 2. Datos del Estudiante / Muestra
    f_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    info_data = [
        [
            Paragraph("Analista / Estudiante:", label_style), Paragraph(datos_estudiante.get('nombre', 'N/A'), value_style),
            Paragraph("Fecha de Ensayo:", label_style), Paragraph(f_actual, value_style)
        ],
        [
            Paragraph("Legajo / DNI:", label_style), Paragraph(datos_estudiante.get('legajo', 'N/A'), value_style),
            Paragraph("Módulo:", label_style), Paragraph(datos_estudiante.get('modulo', 'N/A'), value_style)
        ],
        [
            Paragraph("Yacimiento / Muestra:", label_style), Paragraph(datos_estudiante.get('muestra', 'Campo MENFA - Pozo 101'), value_style),
            Paragraph("Estado:", label_style), Paragraph(datos_estudiante.get('estado', 'Evaluado'), value_style)
        ]
    ]
    
    t_info = Table(info_data, colWidths=[120, 150, 100, 150])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(t_info)
    story.append(Spacer(1, 15))
    
    # 3. Tabla de Resultados del Ensayo
    story.append(Paragraph("Resultados de Medición y Evaluación", title_style))
    
    headers = [Paragraph("Parámetro Ensayado", label_style), Paragraph("Valor Obtenido", label_style), Paragraph("Límite / Esp.", label_style), Paragraph("Dictamen", label_style)]
    table_data = [headers]
    
    for row in resultados_ensayo:
        table_data.append([
            Paragraph(str(row[0]), value_style),
            Paragraph(str(row[1]), value_style),
            Paragraph(str(row[2]), value_style),
            Paragraph(str(row[3]), value_style)
        ])
        
    t_res = Table(table_data, colWidths=[180, 120, 110, 110])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]))
    
    story.append(t_res)
    story.append(Spacer(1, 30))
    
    # 4. Bloque de Firmas y Validación
    story.append(Paragraph("Firmas de Conformidad", title_style))
    story.append(Spacer(1, 20))
    
    firma_data = [
        [Paragraph("__________________________________<br/>Firma del Estudiante", label_style),
         Paragraph("__________________________________<br/>Fabricio Pizzolato<br/>Instructor IPCL MENFA", label_style)]
    ]
    t_firma = Table(firma_data, colWidths=[260, 260])
    t_firma.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
    
    story.append(t_firma)
    
    # Construcción final del PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
