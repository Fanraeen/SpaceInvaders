import pygame as pg


class Alien(pg.sprite.Sprite):
    def __init__(self, color, x, y, screen_width):
        super().__init__()
        self.image = pg.image.load(f'sprites/{color}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.screen_width = screen_width
        
        if color == 'red': self.value = 100
        elif color == 'green': self.value = 200
        else: self.value = 300 


    def update(self, direction) -> None:
        self.rect.x += direction
        self.rect.y += 0.8


class Extra(pg.sprite.Sprite):
    def __init__(self, side, screen_width) -> None:
        super().__init__()
        self.image = pg.image.load(f'sprites/extra.png').convert_alpha()

        if side == 'right':
            self.speed = -3
            x = screen_width + 50
        else:
            self.speed = 3 
            x = -50

        self.rect = self.image.get_rect(topleft = (x, 100))
    
    def update(self):
        self.rect.x += self.speed
