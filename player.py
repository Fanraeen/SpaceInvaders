import pygame as pg
from laser import Laser


class Player(pg.sprite.Sprite):
    def __init__(self, pos: tuple, screen_size: tuple, speed: int) -> None:
        """
        инициализация класса игрока

        Args:
            pos (tuple): начальная позиция игрока
            screen_size (tuple): размер экрана (x, y)
            speed (int): скорость игрока, перемещения по пикселям в один цикл
        """
        super().__init__()
        
        # распаковка разрешения экрана
        self.screen_width, self.screen_height = screen_size

        # загрузка спрайта и установка координат
        self.image = pg.image.load('sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)

        self.speed = speed
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 400
        
        # группа спрайтов для лазеров игрока
        self.lasers = pg.sprite.Group()
    
    def get_input(self) -> None:
        """
        метод для отслеживаия нажатий клавиш, изменяет положения игрока
        """
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            if self.rect.right < self.screen_width:
                self.rect.x += self.speed
    
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            if self.rect.left > 0:
                self.rect.x -= self.speed
 
        if keys[pg.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pg.time.get_ticks()
        
        if keys[pg.K_m]:
            self.laser_cooldown = 0

    def recharge(self) -> None:
        """
        перезарядка игрока, проверка таймера, можно ли сделать следующий выстрел
        """
        if not self.ready:
            current_time = pg.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self) -> None:
        """
        выстрел, добавление лазера в группу лазеров игрока
        """
        self.lasers.add(Laser(self.rect.center, 5, self.screen_height))

    def update(self) -> None:
        """
        обновление всех данных об игроке
        """
        self.get_input()
        self.recharge()
        self.lasers.update()