import sys
from time import sleep

from game_stats import  GameStats
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class Alien_inavsion():
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игры и создаёт игровые ресурсы."""
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # Создание экземпляров для хранения игровой статистики и панели
        # результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Создание кнопки Play.
        self.play_button = Button(self, 'Play')



    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()


            self.bullets.update()
            if self.stats.game_active:
                self.ship.update()
                self._update_aliens()
                self.update_bullets()
            self._update_screen()

    # Удаление старых снарядов
    def update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.aliens_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов и создания нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """Проверяет, достиг ли флот края экрана, с последующим обновлением
        позиций всех пришельцев во флоте.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            self.sb.prep_life()
            self.stats.life -= 1

        # Проверяет, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            if event.type == pygame.KEYDOWN:
                self.keydown_events(event)
            if event.type == pygame.KEYUP:
                self.keyup_events(event)

    def _check_play_button(self, mouse_pos):
        # Запускает новую игру при нажатии кнопки Play.
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not  self.stats.game_active:
            # Сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()

            self.stats.game_active = True

            pygame.mixer.music.load('звуки/nasa-z_uki-otkrytogo-kosmosa-chast-3.mp3')
            pygame.mixer.music.play(-1)

            # Очистка списков пришельцев и снярядов.
            self.aliens.empty()
            self.bullets.empty()


            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()



    def keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        """Обработка нажатий кнопок, перемещения влево, вправо, стрельба через
        пробел (реагирует на нажатие клавиш)"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        if event.key == pygame.K_SPACE:
            self.fire_bullet()

        """Реагирует на отпускание клавиш."""
    def keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False


        """Обработка выстрелов"""
    def fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            """Создание нового сняряда и включение его в группу bullets."""
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        """Определяет количество рядов, помещяющихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (7 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)



        # создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагиоует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        """Обрабатывает столкновения корабля с пришельцем."""
        # Уменьшение ship_left.
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1

            # Очистка списка пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_life()
            # Пауза.
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.stats.score = 0
            self.stats.life = 3
            self.stats.level = 1
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                    # Происходит то же, что при столкновении с кораблём.
                    self._ship_hit()

                    break


    def _update_screen(self):
        # При каждом проходе цикла перерисовываеться экран.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        # Кнопка Play отображаеться в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

if __name__ == '__main__':
    ai = Alien_inavsion()
    ai.run_game()
