import pygame
from ..component import Component
from ..input_manager import InputManager

class Movement(Component):
    name = "Movement"
    def __init__(self) -> None:
        super().__init__()
        self.speed = 0
        self.velocity = [0,0]
        self.isFrozen = False
        self.animation = None
    
    def initialize(self, data) -> None:
        inputSystem = InputManager()
        inputSystem.addHeld(pygame.K_w, self.moveUp)
        inputSystem.addHeld(pygame.K_a, self.moveLeft)
        inputSystem.addHeld(pygame.K_s, self.moveDown)
        inputSystem.addHeld(pygame.K_d, self.moveRight)

        if 'speed' in data:
            self.speed = data['speed']
        
        self.animation = self.entity.getComponent("Animation")
        print(self.animation)
    
    def moveUp(self):
        if not self.isFrozen:
            self.velocity[1] = -self.speed

    def moveLeft(self):
        if not self.isFrozen:
            self.velocity[0] = -self.speed

    def moveDown(self):
        if not self.isFrozen:
            self.velocity[1] = self.speed

    def moveRight(self):
        if not self.isFrozen:
            self.velocity[0] = self.speed

    def update(self) -> None:
        if self.entity is not None:
            self.entity.position[0] += self.velocity[0]
            self.entity.position[1] += self.velocity[1]

            if self.animation is not None:
                self.animation.state = "idle"
                divisor = abs(self.velocity[0])
                if divisor > 0:
                    self.animation.direction = self.velocity[0] / divisor
                if divisor > 0 or abs(self.velocity[1]) > 0:
                    self.animation.state = "walk"
        
        self.velocity = [0,0]