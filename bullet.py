import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, style):
        super().__init__()
        self.image = pygame.image.load(f"assets/bullets/{style}Bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()  # Destruye la bala si sale de la pantalla
