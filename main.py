import pygame as pg
from player import Player
import obstacle
from alien import Alien, Extra
from laser import Laser

import sys
from random import choice, randint


class Game:
    def __init__(self) -> None:
        # игрок
        player_sprite = Player((screen_width // 2, screen_height), (screen_width, screen_height), 5)
        self.player = pg.sprite.GroupSingle(player_sprite)
        self.lives = 3
        self.score = 0

        # загорождение 
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pg.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(screen_width / 15, screen_height - 100, self.obstacle_x_positions)

        # пришельцы
        self.aliens = pg.sprite.Group()
        self.aliens_lasers = pg.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1
        
        # extra корабль
        self.extra = pg.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)

    def create_obstacle(self, x_start: int, y_start: int, offset_x: int) -> None:
        """
        создает загорождение вокруг игрока

        Args:
            x_start (int): начальная координата по x
            y_start (int): начальная координата по y
            offset_x (int): смещение
        """
        for row_index, row  in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    # Проходимся циклом по форме и строим блок, если элемент равен "x"
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)
    
    def create_multiple_obstacles(self, x_start: int, y_start: int, offset: list) -> None:
        """
        создает загородки вокруг игрока

        Args:
            x_start (int): начальная координата по x
            y_start (int): начальная координата по y
            offset (list): список смещений каждого загорождения
        """
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows: int, cols: int, x_distance: int = 60, y_distance: int = 48, x_offset: int = 70, y_offset: int = 100) -> None:
        """
        создает флот кораблей

        Args:
            rows (int): количество столбцов
            cols (int): количество колонн
            x_distance (int, optional): Расстояние для каждого пришельца по x. Defaults to 60.
            y_distance (int, optional): Расстояние для каждого пришельца по y. Defaults to 48.
            x_offset (int, optional): Расстояние между пришельцами по x. Defaults to 70.
            y_offset (int, optional): Расстояние между пришельцами по y. Defaults to 100.
        """
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                
                if row_index == 0:
                    color = 'yellow'
                elif 1 <= row_index <= 2:
                    color = 'green'
                else:
                    color = 'red'
                alien_sprite = Alien(color, x, y, screen_width)
                self.aliens.add(alien_sprite)
    
    def alien_position_checker(self) -> None:
        """
        проверка положение пришельца, как только один из них
        касается границы – весь флот меняет направление в другую сторону
        """
        for alien in self.aliens.sprites():
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(1)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(1)
    
    def alien_move_down(self, distance: int) -> None:
        """
        смешение пришельца вниз на заданное количество координат

        Args:
            distance (int): дистанция для смещение по y
        """
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance
    
    def alien_shoot(self) -> None:
        """
        выстрел пришельца по игроку, выбирается случайный пришелец и происходит выстрел
        """
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, -5, screen_height)        
            self.aliens_lasers.add(laser_sprite)

    def extra_alien_timer(self) -> None:
        """
        проверка таймера и спавн корабля extra
        """
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def collsions_checks(self) -> None:
        """
        проверка всех столкновений в игре
        """
        # лазеры игрока
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # столкновение с блоками защиты
                if pg.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # столновение с пришельцами
                if pg.sprite.spritecollide(laser, self.aliens, True):
                    laser.kill()
                    # если пришельцы заканчивается – спавн следующих
                    if len(self.aliens) == 0:
                        self.alien_setup(rows = 6, cols = 8)

        # лазеры пришельцев
        if self.aliens_lasers:
            for laser in self.aliens_lasers:
                # столкновение с блоками защиты
                if pg.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # столкновение с игроком
                if pg.sprite.spritecollide(laser, self.player, False):
                    laser.kill() 
                    # механика здоровья
                    self.lives -= 1
                    print(f'Lives: {self.lives}')

                    # проверка на проигрыш, когда кончаются жизни
                    if self.lives <= 0:
                        print('game over')
                        pg.quit()
                        sys.exit()                       

    def run(self) -> None:
        """
        обновление всех спрайтов 
        отрисовка на экране
        """
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.aliens_lasers.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collsions_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.aliens_lasers.draw(screen)
        self.extra.draw(screen)
        

if __name__ == '__main__':
    # инициализация
    pg.init()
    
    # параметры разрешения 
    screen_width = 600
    screen_height = 600
    screen = pg.display.set_mode((screen_width, screen_height))

    # счетчик кадров
    clock = pg.time.Clock()
    
    # заголовок окна и иконка
    pg.display.set_caption("Space Invaders")
    icon = pg.image.load('sprites/green.png').convert_alpha()
    pg.display.set_icon(icon)

    # объект игры
    game = Game()

    # таймер для выстрела пришельца
    ALIENLASER = pg.USEREVENT + 1
    pg.time.set_timer(ALIENLASER, 800)

    # игрокой цикл
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == ALIENLASER:
                game.alien_shoot()

        
        screen.fill((30, 30, 30))
        game.run()

        pg.display.flip()
        clock.tick(60)