"""
Scenes hold objects and display them to the screen
"""
import json
import pygame
from random import choice

from .entity import Entity
from .object_manager import ObjectManager
from .event_manager import EventManager, Events
from .collision_manager import CollisionManager
from .scene_manager import SceneManager
from .input_manager import InputManager

class Scene (object):
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.updatable = {}
        self.drawable = {}
        self.topLayer = {}
        self.events = EventManager()
        self.collision = CollisionManager()
        self.camera = None
        self.collision.scene = self
        self.dimensions = [0,0]
        self.minigames = 0
        self.minigameGoal = 2
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.coneSize = 150
        self.showVisonCone = False
        self.showMinigameCompletion = False

        self.backgroundColor = (0, 0, 0)
        SceneManager().scene = self
        InputManager().clear()
        InputManager().addPressed(pygame.K_e, self.activateInteration)
        EventManager().clear()
        ObjectManager().clear()
        CollisionManager().clear()

    # Load the scene file and present it
    def loadScene(self, filename: str):
        self.reset()

        with open(filename) as sceneFile:
            data = json.load(sceneFile)
            for key in data:
                objData = data[key]
                if key == 'entities':
                    for entityName in objData:
                        entity = Entity()
                        entity.loadEntity(entityName, objData[entityName])
                        self.addObject(entityName, entity)

                if key == 'stage':
                    if 'backgroundColor' in objData:
                        self.backgroundColor = objData['backgroundColor']
                    if 'camera' in objData:
                        self.camera = objData['camera']
                    if 'goal' in objData:
                        self.minigameGoal = objData['goal']
                    if 'showVisonCone' in objData:
                        self.showVisonCone = objData['showVisonCone']
                    if 'showMinigameCompletion' in objData:
                        self.showMinigameCompletion = objData['showMinigameCompletion']
                
                if key == 'events':
                    for eventName in objData:
                        eventData = objData[eventName]
                        event = Events[eventData['type']](eventName, self)
                        event.initialize(eventData['value'])
                        self.events.addEvent(eventName, event.trigger)

        players = ObjectManager().getPlayers(True)
        if len(players) > 0:
            # make someone an imposter
            players[0].isImposter = True # choice(players).isImposter = True

    def activateInteration(self):
        player = ObjectManager().getPlayer()
        if player is not None:
            if player.interactionTrigger is not None:
                self.events.triggerEvent(player.interactionTrigger)
            elif player.killTrigger is not None:
                self.events.triggerEvent(player.killTrigger)

    def clearTrigger(self):
        player = ObjectManager().getPlayer()
        if player is not None:
            player.setTrigger(None)

    def freezePlayer(self, val: bool):
        player = ObjectManager().getPlayer()
        component = player.getComponent("Movement")
        if component is not None:
            component.isFrozen = val

    def addObject(self, name: str, object: Entity):
        ObjectManager().addObject(name, object)

        if 'update' in dir(object):
            self.updatable[name] = object
        
        if 'draw' in dir(object):
            if object.isMinigame:
                self.topLayer[name] = object
            else:
                self.drawable[name] = object
    
    def removeObject(self, name: str):
        ObjectManager().removeObject(name)

        if name in self.updatable.keys():
            self.updatable.pop(name)

        if name in self.drawable.keys():
            self.drawable.pop(name)

        if name in self.topLayer.keys():
            self.topLayer.pop(name)
    
    def completeMinigame(self):
        self.minigames+=1
        # activate win function

    # update all objects in scene
    def update(self):
        for object in self.updatable.values():
            object.update()

    def getOffset(self):
        offset = [0,0]
        if self.camera is not None:
            camera = ObjectManager().getObject(self.camera)
            offset = [camera.position[0] - self.dimensions[0], camera.position[1] - self.dimensions[1]]
        
        return offset

    # display all objects on the screen surface
    def draw(self, screen: pygame.Surface):
        # Fill background with solid color
        screen.fill(self.backgroundColor)

        self.dimensions = [screen.get_width()/2, screen.get_height()/2]
        offset = self.getOffset()

        # Draw Base Layer
        for object in self.drawable.values():
            object.draw(screen, offset)

        # Draw Vision Cone
        if self.showVisonCone:
            visionCone = pygame.Surface([self.dimensions[0] * 2, self.dimensions[1] * 2], pygame.SRCALPHA)
            visionCone.fill((0,0,0))
            rect = pygame.Rect(self.dimensions[0] - self.coneSize, self.dimensions[1] - self.coneSize, self.coneSize * 2 + 64, self.coneSize * 2 + 64)
            pygame.draw.ellipse(visionCone, (0, 0, 0, 0), rect)
            screen.blit(visionCone, visionCone.get_rect())

        # Draw Top Layer
        for object in self.topLayer.values():
            object.draw(screen, offset)

        if self.showMinigameCompletion:
            textRender = self.font.render(f"Minigames complete: {self.minigames}", True, (255, 255, 255))
            textRect = textRender.get_rect()
            screen.blit(textRender, textRect)
            
        player = ObjectManager().getPlayer()
        if player is not None and player.isImposter:
            textRender = self.font.render(f"You are the Imposter", True, (255, 255, 255))
            textRect = textRender.get_rect()
            textRect.top = 30
            screen.blit(textRender, textRect)

        players = ObjectManager().getPlayers(True)
        if len(players) == 2:
            # Load the Imposter win screen
            self.loadScene("scenes/imposterWin.json")

        if self.minigames >= self.minigameGoal:
            # Load the crew win screen
            self.loadScene("scenes/crewWin.json")

        pygame.display.flip()