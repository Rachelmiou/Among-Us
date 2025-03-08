import pygame
from ..component import Component

class TextDisplay(Component):
    name = "TextDisplay"
    def __init__(self) -> None:
        super().__init__()
        self.text = None
        self.size = 32
        self.offset = None
        self.color = None
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def initialize(self, data) -> None:
        if 'text' in data:
            self.text = data['text']
        if 'size' in data:
            self.size = data['size']
        if 'offset' in data:
            self.offset = data['offset']
        if 'color' in data:
            self.color = data['color']
        
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
    
    def draw(self, screen: pygame.Surface, offset: list) -> None:
        if self.text is not None and self.entity is not None:
            textRender = self.font.render(self.text, True, self.color)

            textRect = textRender.get_rect()
            textRect.center = (self.entity.position[0] + self.offset[0] - offset[0], self.entity.position[1] + self.offset[1] - offset[0])

            screen.blit(textRender, textRect)