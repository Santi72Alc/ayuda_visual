import pygame
import config


def calibrar_pantalla(pantalla):
    """
    Calibración independiente por ojo (Ajuste directo de intensidad por capa).
    """
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(config.NOMBRE_FUENTE, 18, bold=True)

    # "IZQ" para calibrar solo la capa izquierda, "DER" para la derecha
    ojo_activo = "IZQ"

    en_calibracion = True
    while en_calibracion:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_calibracion = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_k):
                    en_calibracion = False
                elif evento.key == pygame.K_i:
                    ojo_activo = "IZQ"
                elif evento.key == pygame.K_d:
                    ojo_activo = "DER"
                elif evento.key == pygame.K_1:
                    config.COLOR_CAPA_IZQ = (0, 255, 255)  # Cian
                    config.COLOR_CAPA_DER = (255, 0, 0)  # Rojo
                    config.guardar_configuracion()
                elif evento.key == pygame.K_2:
                    config.COLOR_CAPA_IZQ = (0, 255, 0)  # Verde
                    config.COLOR_CAPA_DER = (255, 0, 0)  # Rojo
                    config.guardar_configuracion()

        # Ajuste de intensidad del ojo seleccionado
        teclas = pygame.key.get_pressed()
        paso = 2

        if teclas[pygame.K_UP] or teclas[pygame.K_DOWN]:
            delta = paso if teclas[pygame.K_UP] else -paso

            if ojo_activo == "IZQ":
                # Modifica la intensidad del canal Cian/Azul (G y B)
                r, g, b = config.COLOR_CAPA_IZQ
                g = max(20, min(255, g + delta))
                b = max(20, min(255, b + delta))
                config.COLOR_CAPA_IZQ = (r, g, b)
            else:
                # Modifica la intensidad del canal Rojo (R)
                r, g, b = config.COLOR_CAPA_DER
                r = max(20, min(255, r + delta))
                config.COLOR_CAPA_DER = (r, g, b)

            config.guardar_configuracion()

        # Fondo Negro Puro
        pantalla.fill((0, 0, 0))
        cx, cy = pantalla.get_size()[0] // 2, pantalla.get_size()[1] // 2

        # Mostramos UN solo cuadrado central en función del ojo que estamos calibrando
        rect_prueba = pygame.Rect(cx - 70, cy - 70, 140, 140)

        if ojo_activo == "IZQ":
            pygame.draw.rect(pantalla, config.COLOR_CAPA_IZQ, rect_prueba, 0)
            color_actual = config.COLOR_CAPA_IZQ
        else:
            pygame.draw.rect(pantalla, config.COLOR_CAPA_DER, rect_prueba, 0)
            color_actual = config.COLOR_CAPA_DER

        lineas_texto = [
            "CALIBRACIÓN DIRECTA POR OJO",
            "----------------------------------------------------------------------",
            "PRESETS: [1] Cian/Rojo | [2] Verde/Rojo",
            "SELECCIONAR OJO: [I] Izquierdo (Cian) | [D] Derecho (Rojo)",
            "----------------------------------------------------------------------",
            f"OJO ACTIVO: {'IZQUIERDO' if ojo_activo == 'IZQ' else 'DERECHO'} | Color RGB: {color_actual}",
            "Ajustar Brillo/Intensidad: Mantener Flecha [ARRIBA / ABAJO]",
            "----------------------------------------------------------------------",
            "INSTRUCCIONES:",
            f" 1. Ponte las gafas y cierra el ojo {'DERECHO' if ojo_activo == 'IZQ' else 'IZQUIERDO'}.",
            f" 2. Con el ojo {'IZQUIERDO' if ojo_activo == 'IZQ' else 'DERECHO'}, ajusta con [ARRIBA/ABAJO] hasta que el cuadro",
            "    se vea brillante pero cómodo (sin deslumbrar ni verse apagado).",
            " 3. Pulsa "
            + (
                "'[D]' para cambiar y calibrar el Ojo Derecho."
                if ojo_activo == "IZQ"
                else "'[I]' para volver al Ojo Izquierdo."
            ),
            "----------------------------------------------------------------------",
            "Guardado automático en config.json | Presiona [K] o [ESC] para salir",
        ]

        y = 20
        for lin in lineas_texto:
            if "OJO ACTIVO:" in lin:
                color = (255, 255, 0)
            elif "INSTRUCCIONES:" in lin or "2. Con el ojo" in lin:
                color = (130, 210, 255)
            elif "Guardado automático" in lin:
                color = (100, 255, 100)
            else:
                color = (200, 200, 200)

            img = fuente.render(lin, True, color)
            pantalla.blit(img, (30, y))
            y += 22

        pygame.display.flip()
        reloj.tick(60)
