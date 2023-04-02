class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self): # Инициализация настроек игры.
        # Назначение цвета фона
        self.bg_color = ('black')
        self.screen_width = 1200
        self.screen_height = 800
        self.ship_speed = 1.5
        self.ship_limit = 3

        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = ('red')

        self.bullets_allowed = 3

        # Настройка пришельцев

        self.fleet_drop_speed = 10


       # темп ускорения игры
        self.speedup = 1.3
        # увеличение очков
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.1
        # fleet_direction = 1 обозначает движение вправо; а -1 -влево.
        self.fleet_direction = 1

        # Подсчёт очков
        self.aliens_points = 50


    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.bullet_speed *= self.speedup
        self.alien_speed *= self.speedup

        self.aliens_points  = int(self.aliens_points * self.score_scale)