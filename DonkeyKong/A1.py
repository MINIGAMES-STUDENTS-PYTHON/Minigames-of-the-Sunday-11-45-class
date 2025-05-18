import pygame
import random
import sys
import os 

# Incializacion
pygame.init()
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Donkey Kong Extendido") 
clock = pygame.time.Clock()
FPS = 60
GRAVEDAD = 0.6 

# Colores 
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255,0, 0)
VERDE = (0, 255, 0)
ROSA = (255, 182, 193)
AMARILLO = (255, 255, 0)
MARRON = (139, 69, 19)

# Fuentes y Sonidos
pygame.mixer.init()
fuente = pygame.font.SysFont("Arial", 30)

# Clases 
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 45))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.center = (100, ALTO - 70)
        self.vel_y = 0 
        self.vidas = 3
        self.puntos = 0
        self.en_suelo = False 

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5 
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
        if teclas[pygame.K_SPACE]:
            self.vel_y = -12
            self.en_suelo = False 

        self.vel_y += GRAVEDAD 
        self.rect.y += self.vel_y

        colisiones = pygame.sprite.spritecollide(self, plataforma, False)
        if colisiones:
            for plataforma in colisiones:
                if self.vel_y > 0:
                    self.rect.bottom = plataforma.rect.top 
                    self.en_suelo = True 
                    self.vel_y = 0 

        if self.rect.top > ALTO:
            self.vidas -= 1 
            self.rect.center = (100, ALTO - 70)
            self.vel_y = 0

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

class Barril(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(MARRON)
        self.rect = self.image.rect_rect()
        self.rect.x = 50 
        self.rect.y = 60 
        self.vel_x = random.choice([3, 4])
        self.vel_y = 0 

    def update(self):
        self.rect.x += self.vel_x 
        self.vel_y += GRAVEDAD
        self.rect_y += self.vel_y 

        colisiones = pygame.sprite.spritecollide(self, plataforma, False)
        if colisiones:
            for plataforma in colisiones:
                if self.vel_y > 0:
                    self.rect.bottom = plataforma.rect.top 
                    self.vel_y = 0 
                    self.vel_x *= -1

        if self.rect.top > ALTO:
            self.kill()

class Donkey(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 90)

class Princesa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(ROSA)
        self.rect = self.image.get_rect()
        self.rect.center = (750, 80)


# Grupos
jugador = Jugador()
donkey = Donkey()
pricesa = Princesa()

jugadores = pygame.sprite.Group()
jugadores.add(jugador)

donkeys = pygame.sprite.Group()
donkeys.add(donkey)

princesas = pygame.sprite.Group()
princesas.add(princesa)

plataformas = pygame.sprite.Group()
barriles = pygame.sprite.Group()

# Crear plataformas (alternando de izquierda y derecha)
for i in range(6):
    if i %2 == 0:
        plataformas.add(Plataforma(0, ALTO - i * 100, 650, 15))
    else:
        plataformas.add(Plataforma(150, ALTO - i * 100, 650, 15))

# Plataforma final donde esta la princesa 
plataformas.add(Plataforma(700, 60, 100, 20))

# Menu de incio 
def mostrar_menu():
    VENTANA.fill(NEGRO)
    texto = fuente.render("DONKEY KONG EXTENDIDO", True, AMARILLO)
    texto2 = fuente.render("Presiona ENTER para jugar", True, BLANCO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 60))
    VENTANA.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 ))
    pygame.display.flip()

    esperando = True 
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False 

# Juego 
def juego():
    tiempo_barril = 0 
    corriendo = True 
    while corriendo:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Lanzar Barriles cada cierto tiempo 
        tiempo_barril += 1 
        if tiempo_barril >= 100:
            tiempo_barril = 0 
            nuevo = Barril()
            barriles.add(nuevo)
        
        jugadores.update()
        barriles.update()

        # Colision con barriles 
        if pygame.sprite.spritecollideany(jugador, barriles):
            jugador.vidas -= 1 
            jugador.rect.center = (100, ALTO - 70)
            if jugador.vidas <= 0:
                return "perdiste"
            
        # Llegar a la princesa 
        if pygame.sprite.spritecollideany(jugador, princesas):
            return "ganaste"
        
        # Dibujar todo 
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
    texto = fuente.render(mensaje + " Presiona ENTER para volver a jugar", True, BLANCO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 ))
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