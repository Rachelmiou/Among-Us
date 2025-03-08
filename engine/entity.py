"""
Entities make up the base form of everything in our world
"""
from typing import Dict
from pygame import Surface
from math import sqrt

from .component import Component
from .components import ComponentTypes
from .object_manager import ObjectManager

class Entity(object):
    def __init__(self) -> None:
        self.name = None
        self.position = [0,0]
        self.parent = None
        self.rotation = 0
        self.enabled = True
        self.isMinigame = False
        self.isPlayer = False
        self.isImposter = False
        self.isAlive = True
        self.interactionTrigger = None
        self.killTrigger = None
        self.freezePlayer = False
        self.target = None

        self.components : Dict[str, Component] = {}

    def loadEntity(self, entityName, entityData) -> None:
        self.name = entityName
        if 'position' in entityData:
            self.position = entityData['position']
        if 'rotation' in entityData:
            self.rotation = entityData['rotation']
        if 'enabled' in entityData:
            self.enabled = entityData['enabled']
        if 'minigame' in entityData:
            self.isMinigame = entityData['minigame']
        if 'isPlayer' in entityData:
            self.isPlayer = entityData['isPlayer']
        if 'isAlive' in entityData:
            self.isAlive = entityData['isAlive']
        
        if 'components' in entityData:
            for component in entityData['components']:
                if component in ComponentTypes:
                    comp = ComponentTypes[component]()
                    self.addComponent(comp)
                    comp.initialize(entityData['components'][component])
        
        if not self.isAlive:
            self.kill()

    def kill(self):
        collision = self.getComponent("Collision")
        self.isAlive = False
        if collision is not None:
            collision.trigger = "startEmergencyMeeting"
            collision.static = True

    def setTrigger(self, trigger):
        self.interactionTrigger = trigger

    def addComponent(self, component: Component) -> None:
        component.setEntity(self)
        self.components[component.__class__.name] = component
    
    def getComponent(self, name) -> Component | None:
        if name in self.components.keys():
            return self.components[name]
        return None

    def destroy(self):
        for name in self.components.keys():
            self.components[name].destroy()
    
    def getPosition(self):
        if self.parent is None:
            return self.position
        
        return [self.parent.position[0] + self.position[0], self.parent.position[1] + self.position[1]]

    def update(self) -> None:
        if not self.enabled:
            return

        for component in self.components.values():
            component.update()
        
        if self.isPlayer and self.isImposter:
            # look for any other player in reach
            players = ObjectManager().getPlayers(True)
            self.killTrigger = None
            self.target = None
            for player in players:
                if player == self:
                    continue

                dX, dY = player.position[0] - self.position[0], player.position[1] - self.position[1]
                dist = sqrt(dX ** 2 + dY ** 2)
                if dist < 150:
                    self.killTrigger = "killPlayer"
                    self.target = player

    def draw(self, screen: Surface, offset: list) -> None:
        if not self.enabled:
            return

        for component in self.components.values():
            component.draw(screen, offset)