# modules/modulo_evaluacion.py
import random

def generar_caso_examen():
    """
    Genera parámetros aleatorios para un caso práctico de laboratorio.
    """
    casos = [
        {
            "id": 1,
            "titulo": "Evaluación de Crudo en Cabecera",
            "api_obs": round(random.uniform(22.0, 35.0), 1),
            "temp_f": round(random.uniform(70.0, 100.0), 1),
            "t1": round(random.uniform(0.1, 1.5), 2),
            "t2": round(random.uniform(0.1, 1.5), 2),
            "limite_bsw": 0.5
        },
        {
            "id": 2,
            "titulo": "Control de Calidad de Inyección de Agua",
            "ph": round(random.uniform(6.5, 8.5), 1),
            "temp_c": round(random.uniform(25.0, 60.0), 1),
            "tds": random.randint(5000, 30000),
            "ca_ppm": random.randint(200, 1000),
            "alk_ppm": random.randint(300, 1200)
        }
    ]
    return random.choice(casos)
