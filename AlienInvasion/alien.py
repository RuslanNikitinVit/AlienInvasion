
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс представляющий одного пришельца."""
    def __init__(self, ai_game):
        """Инициализирует пришельца и задаёт его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображение пришельца и назначение атрибута rect.
        self.image = pygame.image.load('image/pngwing.com (3).png')
        self.rect = self.image.get_rect()


        # Каждый новый пришелец появляеться в левом верхнем углу экрана.
        self.rect.y = self.rect.height
        self.rect.x = self.rect.width


        # Сохранение точной горизотальной поверхности пришельца.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возращает True, если пришелец находиться у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    def update(self):
        """Перемещает пришельца вправо илив влево."""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x

