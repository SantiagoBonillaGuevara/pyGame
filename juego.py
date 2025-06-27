import pygame
import sys
from configuracion import get_dificultad, get_opcion
from player import Player
from enemy import Enemy
from bullet import Bullet


pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego en marcha")
clock = pygame.time.Clock()

# Colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

def obtener_velocidad():
    dificultad=get_dificultad()
    if dificultad == "Fácil":
        print("el juego esta en facil")
        return 5
    elif dificultad == "Media":
        print("el juego esta en media")
        return 8
    elif dificultad == "Difícil":
        print("el juego esta en dificil")
        return 12
    else:
        return 5  # valor por defecto

def iniciar_juego():

    estilo_personaje = get_opcion("personaje")
    estilo_enemigos = get_opcion("enemigos")
    estilo_balas = get_opcion("balas")
    estilo_fondo = get_opcion("fondo")
    estilo_sonido = get_opcion("sonido")

    fondo = pygame.image.load(f"assets/backgrounds/{estilo_fondo}Back.png").convert()
    fondo = pygame.transform.scale(fondo, (800, 600))  # Asegura que tenga 800x600

    velocidad = obtener_velocidad()
    velocidad_enemigo = velocidad - 2

    pygame.mixer.init()

    # Sonido de fondo
    pygame.mixer.music.load(f"assets/sounds/{estilo_sonido}/Music.mp3")  # o .ogg
    pygame.mixer.music.set_volume(1.1)  # volumen de 0.0 a 1.0

    # Efectos
    sonido_colision = pygame.mixer.Sound(f"assets/sounds/{estilo_sonido}/Damage.mp3")
    sonido_muerte = pygame.mixer.Sound(f"assets/sounds/{estilo_sonido}/GameOver.mp3")
    sonido_disparo = pygame.mixer.Sound(f"assets/sounds/{estilo_sonido}/Shoot.mp3")
    sonido_enemigo_muerto = pygame.mixer.Sound(f"assets/sounds/{estilo_sonido}/Kill.mp3")
    sonido_advanced = pygame.mixer.Sound(f"assets/sounds/{estilo_sonido}/Advance.mp3")

    jugador = Player(400, 500, velocidad, estilo_personaje)
    grupo_jugador = pygame.sprite.Group(jugador)
    grupo_balas = pygame.sprite.Group()
    score = 0
    vidas = 15 - velocidad
    umbral_score = 50

    GENERAR_ENEMIGO = pygame.USEREVENT + 1
    pygame.time.set_timer(GENERAR_ENEMIGO, (5000//velocidad))

    enemigos = pygame.sprite.Group()

    fuente = pygame.font.SysFont(None, 36)

    pygame.mixer.music.play(-1)
    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bala = Bullet(jugador.rect.centerx, jugador.rect.top, estilo_balas)
                    grupo_balas.add(bala)
                    sonido_disparo.play()
            elif event.type == GENERAR_ENEMIGO:
                enemigo = Enemy(velocidad_enemigo, estilo_enemigos)  # Asegúrate de que la clase Enemy esté definida
                enemigos.add(enemigo)

        teclas = pygame.key.get_pressed()
        jugador.update(teclas)
        enemigos.update()
        grupo_balas.update()

        colisionados = pygame.sprite.spritecollide(jugador, enemigos, dokill=True)
        if colisionados:
            sonido_colision.play()
            vidas -= 1
            print(f"¡Colisión! Vidas restantes: {vidas}")
            if vidas <= 0:
                pygame.mixer.music.stop()
                sonido_muerte.play()
                pygame.time.delay(1000)
                print("¡Has perdido!")
                corriendo = False

        colisiones = pygame.sprite.groupcollide(enemigos, grupo_balas, True, True)
        if colisiones:
            sonido_enemigo_muerto.play()
            score += len(colisiones)

        # Aumentar velocidades cada 50 puntos
        if score >= umbral_score:
            sonido_advanced.play()
            velocidad +=1
            velocidad_enemigo +=1
            jugador.set_velocidad(velocidad)
            pygame.time.set_timer(GENERAR_ENEMIGO, (5000//velocidad))
            umbral_score += 50  # Próximo umbral

        # Dibujar
        pantalla.blit(fondo, (0, 0))
        grupo_jugador.draw(pantalla)
        enemigos.draw(pantalla)
        grupo_balas.draw(pantalla)

        # Mostrar vidas
        texto_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 255, 255))
        pantalla.blit(texto_vidas, (10, 10))

        texto_score = fuente.render(f"Puntaje: {score}", True, (255, 255, 255))
        pantalla.blit(texto_score, (10, 40))

        pygame.display.flip()
        clock.tick(60)
