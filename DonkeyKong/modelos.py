import pygame
import random
from variables import AZUL, ALTO, GRAVEDAD, VERDE, MARRON, ROJO, ROSA

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

    def set_plataformas(self, plataformas):
        self.plataformas = plataformas

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = -12
            self.en_suelo = False

        self.vel_y += GRAVEDAD
        self.rect.y += self.vel_y

        colisiones = pygame.sprite.spritecollide(self, self.plataformas, False)
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

class Barril(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(MARRON)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 60
        self.vel_x = random.choice([3, 4])
        self.vel_y = 0

    def set_plataformas(self, plataformas):
        self.plataformas = plataformas

    def update(self):
        self.rect.x += self.vel_x
        self.vel_y += GRAVEDAD
        self.rect.y += self.vel_y

        colisiones = pygame.sprite.spritecollide(self, self.plataformas, False)
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