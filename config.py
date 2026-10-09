import json
import os

NOMBRE_FUENTE = "DejaVu Sans"
TITULO_VENTANA = "Terapia Visual Anaglifa"
COLOR_FONDO = (0, 0, 0)
COLOR_CIRCULO = (128, 128, 128)
COLOR_TEXTO = (200, 200, 200)

FRECUENCIA_AUDIO_HZ = 44100
FRECUENCIA_PITIDO_HZ = 880
DURACION_PITIDO_MS = 150

TAMANO_FUENTE_INFO = 18
RADIO_CIRCULO = 40

ANCHO_RECT = 80
ALTO_RECT = 80

POSICION_RECT_ARRIBA = 180
POSICION_RECT_ABAJO = 180
POSICION_RECT_IZQ = 240
POSICION_RECT_DER = 240

POSICIONES = ["ARRIBA", "ABAJO", "IZQUIERDA", "DERECHA"]

MODO_INICIAL = "CONVERGENCIA"
DISPARIDAD_INICIAL_C = 20
DISPARIDAD_MINIMA = 0
DISPARIDAD_MAXIMA = 120
PASO_DISPARIDAD = 6
PX_A_DIOPTRIAS = 0.1

# Valores por defecto
COLOR_CAPA_IZQ = (0, 255, 255)  # Cian/Azul (Ojo Izquierdo)
COLOR_CAPA_DER = (255, 0, 0)  # Rojo (Ojo Derecho)

# --- CONFIGURACIÓN DE DIOPTRIAS PRISMA ---
DIOPTRIAS_MAXIMAS = 90.0  # Límite máximo de dioptrías
DIOPTRIAS_MINIMAS = 0.0  # Límite mínimo
PASO_DIOPTRIAS = 0.5  # Salto por acierto/fallo
PX_POR_DIOPTRIA = 10.0  # Píxeles por cada dioptría prisma

ARCHIVO_CONFIG = "config.json"


def guardar_configuracion():
    datos = {
        "COLOR_CAPA_IZQ": list(COLOR_CAPA_IZQ),
        "COLOR_CAPA_DER": list(COLOR_CAPA_DER),
    }
    try:
        with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
    except Exception as e:
        print(f"Error al guardar {ARCHIVO_CONFIG}: {e}")


def cargar_configuracion():
    global COLOR_CAPA_IZQ, COLOR_CAPA_DER
    if os.path.exists(ARCHIVO_CONFIG):
        try:
            with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if "COLOR_CAPA_IZQ" in datos:
                    COLOR_CAPA_IZQ = tuple(datos["COLOR_CAPA_IZQ"])
                if "COLOR_CAPA_DER" in datos:
                    COLOR_CAPA_DER = tuple(datos["COLOR_CAPA_DER"])
        except Exception as e:
            print(f"Error al cargar {ARCHIVO_CONFIG}: {e}")


# Carga automática al importar el módulo
cargar_configuracion()
