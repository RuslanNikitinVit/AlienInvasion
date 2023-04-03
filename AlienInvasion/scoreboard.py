import pygame.font


class Scoreboard():
    """Класс для вывода игровой информации"""
    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчёта очков"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Настройка шрифта для вывода cчёта.
        self.text_color = (	248, 248, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка изображений счетов
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_life()
    def prep_score(self):
        """Преобразует текущий счёт в графическое изображение."""
        rounded_score = round(self.stats.score, -1) # -1 означает округление
        # до ближайших десяток, сотен и так далее
        score_str = "{:,}".format(rounded_score)
        # score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color)
        # Вывод счёта в верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счёт в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color,
                                                 self.settings.bg_color)
        # Рекорд выравниваеться по центру верхней стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        #Проверяет появился ли новый рекорд.
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            with open('record.txt', 'w') as file_object:
                file_object.write(str(self.stats.high_score))

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        lev = 'Level '
        level_str = lev + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Уровень выводиться под текущим счётом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.right = self.score_rect.left - 200

    def prep_life(self):
        life_str = str(self.stats.life)
        self.life_image = self.font.render(life_str, True, self.text_color, self.settings.bg_color)

        self.life_rect = self.life_image.get_rect()
        self.life_rect.left = self.screen_rect.left + 20
        self.life_rect.top = 20




    def show_score(self):
        """Выводит текущий счёт и число оставшихся кораблей."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.life_image, self.life_rect)






