import pygame
from engine.entity import Entity
from engine.scene import Scene
from engine.input_manager import InputManager
from engine.collision_manager import CollisionManager
from engine.event_manager import EventManager
from engine.components import Collection

pygame.init()
pygame.display.set_caption("Among Them")

# variables
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
scene = Scene()
inputManager = InputManager()
collisionManager = CollisionManager()
eventManager = EventManager()

scene.loadScene("scenes/menu.json")
inputManager.addPressed(pygame.K_ESCAPE, lambda: pygame.event.post(pygame.event.Event(pygame.QUIT, {})))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    inputManager.update()
    scene.update()
    collisionManager.update()
    scene.draw(screen)
    clock.tick(60)