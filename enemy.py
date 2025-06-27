import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, velocidad, style):
        super().__init__()
        self.image = pygame.image.load(f"assets/enemies/{style}Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 760)
        self.rect.y = random.randint(-450, -40)
        self.velocidad = velocidad

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y > 600:
            self.rect.y = -40
            self.rect.x = random.randint(0, 760)
