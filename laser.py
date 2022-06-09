import pygame as pg


class Laser(pg.sprite.Sprite):
    def __init__(self, pos, speed, screen_height) -> None:
        super().__init__()
        self.image = pg.image.load('sprites/laser.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.screen_height = screen_height
    
    def destroy(self) -> None:
        if self.rect.y > self.screen_height + 50 or self.rect.y < -50:
            self.kill()

    def update(self) -> None:
        self.rect.y -= self.speed
        self.destroy()
