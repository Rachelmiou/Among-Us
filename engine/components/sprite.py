import pygame
from ..component import Component

class Sprite(Component):
    name = "Sprite"
    def __init__(self) -> None:
        super().__init__()
        self.image = None
        self.size = None

    def initialize(self, data) -> None:
        if 'image' in data:
            self.image = pygame.image.load(data['image'])
        if 'size' in data:
            self.size = data['size']
    
    def draw(self, screen: pygame.Surface, offset: list) -> None:
        if self.image is not None and self.entity is not None:
            image = self.image

            if self.size is not None:
                image = pygame.transform.scale(image, self.size)
            
            image = pygame.transform.rotate(image, self.entity.rotation)

            if not self.entity.isAlive:
                colorImage = pygame.Surface(self.size).convert_alpha()
                colorImage.fill((255,0,0))
                image.blit(colorImage, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            
            position = [self.entity.position[0] - offset[0], self.entity.position[1] - offset[1]]
            screen.blit(image, position)