import pygame
from ..component import Component

class Animation(Component):
    name = "Animation"
    def __init__(self) -> None:
        super().__init__()
        self.images = {}
        self.state = None
        self.frame = 0
        self.frameRate = 5
        self.frameTimer = 0
        self.sprite = None
        self.direction = 1

    def initialize(self, data) -> None:
        self.sprite = self.entity.getComponent("Sprite")
        for name in data:
            self.images[name] = []
            for file in data[name]:
                self.images[name].append(pygame.image.load(file))
    
    def update(self):
        if self.sprite is not None and self.state in self.images:
            if self.frame >= len(self.images[self.state]):
                self.frame = 0
            
            self.frameTimer += 1

            if self.frameTimer == self.frameRate:
                self.sprite.image = pygame.transform.flip(self.images[self.state][self.frame], self.direction != 1, False)
                self.frame += 1
                self.frameTimer = 0