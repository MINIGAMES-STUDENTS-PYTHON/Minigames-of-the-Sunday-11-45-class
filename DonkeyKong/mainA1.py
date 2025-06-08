import pygame
import random
import sys
from variables import ANCHO, ALTO, NEGRO, AMARILLO, BLANCO, FPS
from modelos import Jugador, Donkey, Princesa, Plataforma, Barril

# Inicialización
pygame.init()
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Donkey Kong Extendido")
clock = pygame.time.Clock()
pygame.mixer.init()
fuente = pygame.font.SysFont("Arial", 30)

# Objetos y grupos
jugador = Jugador()
donkey = Donkey()
princesa = Princesa()

jugadores = pygame.sprite.Group(jugador)
donkeys = pygame.sprite.Group(donkey)
princesas = pygame.sprite.Group(princesa)
plataformas = pygame.sprite.Group()
barriles = pygame.sprite.Group()

# Crear plataformas alternadas
for i in range(6):
    if i % 2 == 0:
        plataformas.add(Plataforma(0, ALTO - i * 100, 650, 15))
    else:
        plataformas.add(Plataforma(150, ALTO - i * 100, 650, 15))
# Plataforma final para la princesa
plataformas.add(Plataforma(700, 60, 100, 20))

# Asignar plataformas
jugador.set_plataformas(plataformas)

def mostrar_menu():
    VENTANA.fill(NEGRO)
    texto = fuente.render("DONKEY KONG EXTENDIDO", True, AMARILLO)
    texto2 = fuente.render("Presiona ENTER para jugar", True, BLANCO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 60))
    VENTANA.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

def juego():
    tiempo_barril = 0
    corriendo = True
    while corriendo:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Generar barril
        tiempo_barril += 1
        if tiempo_barril >= 100:
            tiempo_barril = 0
            nuevo = Barril()
            nuevo.set_plataformas(plataformas)
            barriles.add(nuevo)

        jugadores.update()
        barriles.update()

        # Colisiones
        if pygame.sprite.spritecollideany(jugador, barriles):
            jugador.vidas -= 1
            jugador.rect.center = (100, ALTO - 70)
            if jugador.vidas <= 0:
                return "perdiste"

        if pygame.sprite.spritecollideany(jugador, princesas):
            return "ganaste"

        # Dibujar
        VENTANA.fill(NEGRO)
        plataformas.draw(VENTANA)
        barriles.draw(VENTANA)
        jugadores.draw(VENTANA)
        donkeys.draw(VENTANA)
        princesas.draw(VENTANA)

        texto = fuente.render(f"Vidas: {jugador.vidas} Puntos: {jugador.puntos}", True, BLANCO)
        VENTANA.blit(texto, (10, 10))
        pygame.display.flip()

# Loop principal
while True:
    mostrar_menu()
    resultado = juego()
    VENTANA.fill(NEGRO)
    mensaje = "¡Ganaste!" if resultado == "ganaste" else "Perdiste"
    texto = fuente.render(mensaje + " - ENTER para jugar otra vez", True, BLANCO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jugador.vidas = 3
                jugador.puntos = 0
                jugador.rect.center = (100, ALTO - 70)
                barriles.empty()
                esperando = False