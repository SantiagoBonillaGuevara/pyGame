# menu.py
import pygame, sys
from configuracion import set_dificultad, set_opcion, get_opcion
from juego import iniciar_juego

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego")
fuente = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 100, 255)
GRIS = (180, 180, 180)

def dibujar_boton(texto, x, y, ancho, alto, activo):
    color = AZUL if activo else GRIS
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    texto_render = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_render, (x + 20, y + 10))
    return pygame.Rect(x, y, ancho, alto)

def menu_dificultad():
    while True:
        pantalla.fill((20, 20, 20))
        mouse_pos = pygame.mouse.get_pos()

        titulo = fuente.render("Selecciona la dificultad", True, BLANCO)
        pantalla.blit(titulo, (220, 50))

        boton_facil = dibujar_boton("Fácil", 300, 150, 200, 50, pygame.Rect(300, 150, 200, 50).collidepoint(mouse_pos))
        boton_media = dibujar_boton("Media", 300, 230, 200, 50, pygame.Rect(300, 230, 200, 50).collidepoint(mouse_pos))
        boton_dificil = dibujar_boton("Difícil", 300, 310, 200, 50, pygame.Rect(300, 310, 200, 50).collidepoint(mouse_pos))
        boton_volver = dibujar_boton("Volver", 300, 390, 200, 50, pygame.Rect(300, 390, 200, 50).collidepoint(mouse_pos))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if click:
            if boton_facil.collidepoint(mouse_pos):
                set_dificultad("Fácil")
                return
            elif boton_media.collidepoint(mouse_pos):
                set_dificultad("Media")
                return
            elif boton_dificil.collidepoint(mouse_pos):
                set_dificultad("Difícil")
                return
            elif boton_volver.collidepoint(mouse_pos):
                return
        
        pygame.display.flip()
        clock.tick(60)

def menu_principal():
    while True:
        pantalla.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()
        click = False

        boton_jugar = dibujar_boton("Jugar", 300, 150, 200, 50, pygame.Rect(300, 150, 200, 50).collidepoint(mouse_pos))
        boton_dificultad = dibujar_boton("Dificultad", 300, 230, 200, 50, pygame.Rect(300, 230, 200, 50).collidepoint(mouse_pos))
        boton_opciones = dibujar_boton("Opciones", 300, 310, 200, 50, pygame.Rect(300, 310, 200, 50).collidepoint(mouse_pos))
        boton_salir = dibujar_boton("Salir", 300, 390, 200, 50, pygame.Rect(300, 390, 200, 50).collidepoint(mouse_pos))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if click:
            if boton_jugar.collidepoint(mouse_pos):
                iniciar_juego()
            elif boton_dificultad.collidepoint(mouse_pos):
                menu_dificultad()
            elif boton_opciones.collidepoint(mouse_pos):
                menu_opciones()
            elif boton_salir.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def menu_opciones():
    opciones = ["personaje", "enemigos", "balas", "fondo", "sonido"]
    estilos = ["Arcade", "Mario", "Doom"]
    seleccion = {tipo: get_opcion(tipo) for tipo in opciones}

    while True:
        pantalla.fill((40, 40, 40))
        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        titulo = fuente.render("Opciones de Personalización", True, BLANCO)
        pantalla.blit(titulo, (160, 40))

        y_base = 120
        for i, tipo in enumerate(opciones):
            texto = fuente.render(f"{tipo.capitalize()}: {seleccion[tipo]}", True, BLANCO)
            pantalla.blit(texto, (200, y_base + i * 60))

            boton_izq_rect = pygame.Rect(120, y_base + i * 60, 50, 40)
            boton_der_rect = pygame.Rect(550, y_base + i * 60, 50, 40)

            boton_izq = dibujar_boton("<", 120, y_base + i * 60, 50, 40, boton_izq_rect.collidepoint(mouse_pos))
            boton_der = dibujar_boton(">", 550, y_base + i * 60, 50, 40, boton_der_rect.collidepoint(mouse_pos))

            if click:
                if boton_izq_rect.collidepoint(mouse_pos):
                    idx = estilos.index(seleccion[tipo])
                    seleccion[tipo] = estilos[(idx - 1) % len(estilos)]
                    break  # para evitar múltiples cambios en un solo clic
                elif boton_der_rect.collidepoint(mouse_pos):
                    idx = estilos.index(seleccion[tipo])
                    seleccion[tipo] = estilos[(idx + 1) % len(estilos)]
                    break

        boton_guardar_rect = pygame.Rect(300, 500, 200, 50)
        boton_guardar = dibujar_boton("Guardar", 300, 500, 200, 50, boton_guardar_rect.collidepoint(mouse_pos))

        if click and boton_guardar_rect.collidepoint(mouse_pos):
            for tipo in opciones:
                set_opcion(tipo, seleccion[tipo])
            return

        pygame.display.flip()
        clock.tick(60)
