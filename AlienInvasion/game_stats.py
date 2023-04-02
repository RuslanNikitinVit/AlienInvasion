class GameStats():
    """Отслеживание коллизий для игры Alien Invasion."""


    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        """Игра запускаеться в неактивном состоянии."""
        self.game_active = False
        self.score = 0
        self.level = 1
        self.life = 3
        self.lifes = 3
        # рекорд не должен сбрасываться
        self.high_score = 0
    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
