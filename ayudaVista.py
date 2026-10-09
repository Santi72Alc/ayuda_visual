import pygame
import random
import array
import config
import calibrador

# 1. Inicialización de Pygame y audio
pygame.init()
pygame.mixer.init(frequency=config.FRECUENCIA_AUDIO_HZ, size=-16, channels=1)

# 2. Configuración de pantalla
info = pygame.display.Info()
pantalla = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
pygame.display.set_caption(config.TITULO_VENTANA)
reloj = pygame.time.Clock()

# 3. Fuentes
fuente_info = pygame.font.SysFont(
    config.NOMBRE_FUENTE, config.TAMANO_FUENTE_INFO, bold=True
)
fuente_letra_cuadro = pygame.font.SysFont(config.NOMBRE_FUENTE, 36, bold=True)


# 4. Generación procedural de audio
def generar_tono(frecuencia, duracion_ms):
    num_muestras = int(config.FRECUENCIA_AUDIO_HZ * (duracion_ms / 1000.0))
    buf = array.array("h")
    periodo = config.FRECUENCIA_AUDIO_HZ / frecuencia
    for i in range(num_muestras):
        valor = 16000 if (i % periodo) < (periodo / 2) else -16000
        buf.append(valor)
    return pygame.mixer.Sound(buffer=buf)


pitido_acierto = generar_tono(config.FRECUENCIA_PITIDO_HZ, config.DURACION_PITIDO_MS)
pitido_fallo = generar_tono(300, 250)

# Conjunto de letras para fijación de nitidez
LETRAS_CENTRO_CUADRADO = "ABCDEFGHJKLMNPQRSTUVWXYZ"

# 5. Estado de la sesión
dioptrias_objetivo = getattr(config, "DIOPTRIAS_INICIALES", 1.0)
dioptrias_actuales = float(dioptrias_objetivo)
modo_terapia = config.MODO_INICIAL
rectangulo_objetivo = random.choice(config.POSICIONES)

# Diccionario de letras independientes para cada cuadro
iconos_letras_cuadrados = {
    pos: random.choice(LETRAS_CENTRO_CUADRADO) for pos in config.POSICIONES
}


def cambiar_objetivo():
    global rectangulo_objetivo, iconos_letras_cuadrados
    rectangulo_objetivo = random.choice(config.POSICIONES)
    iconos_letras_cuadrados = {
        pos: random.choice(LETRAS_CENTRO_CUADRADO) for pos in config.POSICIONES
    }


def evaluar_respuesta(respuesta_usuario):
    global dioptrias_objetivo
    max_d = getattr(config, "DIOPTRIAS_MAXIMAS", 90.0)
    min_d = getattr(config, "DIOPTRIAS_MINIMAS", 0.0)
    paso = getattr(config, "PASO_DIOPTRIAS", 0.5)

    if respuesta_usuario == rectangulo_objetivo:
        pitido_acierto.play()
        dioptrias_objetivo = min(max_d, dioptrias_objetivo + paso)
    else:
        pitido_fallo.play()
        dioptrias_objetivo = max(min_d, dioptrias_objetivo - paso)

    cambiar_objetivo()


def dibujar_hud():
    max_d = getattr(config, "DIOPTRIAS_MAXIMAS", 90.0)
    lineas = [
        f"Modo: {modo_terapia} [Teclas C / D]",
        f"Disparidad / Carga visual: {dioptrias_actuales:.1f} Δ (Máx: {max_d:.1f} Δ)",
        "------------------------------------",
        "Respuesta: Flechas [ARRIBA / ABAJO / IZQ / DER]",
        "Cambiar posición y letras: [TAB]",
        "Recuperar fusión (Reset a 1.0 Δ): [Barra Espaciadora]",
        "Calibrar gafas: [K]",
        "Salir: [ESC]",
    ]

    y = 20
    for linea in lineas:
        img_texto = fuente_info.render(linea, True, config.COLOR_TEXTO)
        pantalla.blit(img_texto, (20, y))
        y += 26


def dibujar_escena():
    global dioptrias_actuales

    velocidad_suavizado = 0.20
    dioptrias_actuales += (
        dioptrias_objetivo - dioptrias_actuales
    ) * velocidad_suavizado

    pantalla.fill((0, 0, 0))

    ancho_p, alto_p = pantalla.get_size()
    cx, cy = ancho_p // 2, alto_p // 2

    # Anclaje de Fusión Central (Solo círculo de fijación despejado)
    pygame.draw.circle(
        pantalla, config.COLOR_CIRCULO, (cx, cy), config.RADIO_CIRCULO, 2
    )

    coords = {
        "ARRIBA": (0, -config.POSICION_RECT_ARRIBA),
        "ABAJO": (0, config.POSICION_RECT_ABAJO),
        "IZQUIERDA": (-config.POSICION_RECT_IZQ, 0),
        "DERECHA": (config.POSICION_RECT_DER, 0),
    }

    # Bloques con +5px de tamaño extra
    ancho_r = config.ANCHO_RECT + 5
    alto_r = config.ALTO_RECT + 5

    px_por_dioptria = getattr(config, "PX_POR_DIOPTRIA", 10.0)
    disparidad_px = dioptrias_actuales * px_por_dioptria

    surf_izq = pygame.Surface((ancho_p, alto_p))
    surf_der = pygame.Surface((ancho_p, alto_p))
    surf_izq.fill((0, 0, 0))
    surf_der.fill((0, 0, 0))

    for pos, (dx, dy) in coords.items():
        posX = cx + dx
        posY = cy + dy

        disp_pos = disparidad_px if pos == rectangulo_objetivo else 0
        offset = disp_pos / 2.0

        if modo_terapia == "CONVERGENCIA":
            offset_izq = +offset
            offset_der = -offset
        else:
            offset_izq = -offset
            offset_der = +offset

        # Generamos el render de la letra en negro
        txt_cuadro = fuente_letra_cuadro.render(
            iconos_letras_cuadrados[pos], True, (0, 0, 0)
        )

        # Ojo Izquierdo
        rect_bloque_izq = pygame.Rect(0, 0, ancho_r, alto_r)
        rect_bloque_izq.center = (int(posX + offset_izq), int(posY))
        pygame.draw.rect(surf_izq, config.COLOR_CAPA_IZQ, rect_bloque_izq, 0)
        rect_txt_izq = txt_cuadro.get_rect(center=rect_bloque_izq.center)
        surf_izq.blit(txt_cuadro, rect_txt_izq)

        # Ojo Derecho
        rect_bloque_der = pygame.Rect(0, 0, ancho_r, alto_r)
        rect_bloque_der.center = (int(posX + offset_der), int(posY))
        pygame.draw.rect(surf_der, config.COLOR_CAPA_DER, rect_bloque_der, 0)
        rect_txt_der = txt_cuadro.get_rect(center=rect_bloque_der.center)
        surf_der.blit(txt_cuadro, rect_txt_der)

    # Superposición aditiva
    pantalla.blit(surf_izq, (0, 0), special_flags=pygame.BLEND_ADD)
    pantalla.blit(surf_der, (0, 0), special_flags=pygame.BLEND_ADD)

    dibujar_hud()
    pygame.display.flip()


# 6. Bucle Principal
ejecutando = True
while ejecutando:
    reloj.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif evento.key == pygame.K_SPACE:
                dioptrias_objetivo = 1.0
            elif evento.key == pygame.K_TAB:
                cambiar_objetivo()
            elif evento.key == pygame.K_c:
                modo_terapia = "CONVERGENCIA"
            elif evento.key == pygame.K_d:
                modo_terapia = "DIVERGENCIA"
            elif evento.key == pygame.K_k:
                calibrador.calibrar_pantalla(pantalla)
                config.cargar_configuracion()
            elif evento.key == pygame.K_UP:
                evaluar_respuesta("ARRIBA")
            elif evento.key == pygame.K_DOWN:
                evaluar_respuesta("ABAJO")
            elif evento.key == pygame.K_LEFT:
                evaluar_respuesta("IZQUIERDA")
            elif evento.key == pygame.K_RIGHT:
                evaluar_respuesta("DERECHA")

    dibujar_escena()

pygame.quit()
