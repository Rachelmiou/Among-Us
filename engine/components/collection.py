import json
import pygame

import engine.entity
from ..object_manager import ObjectManager
from ..component import Component

class Collection(Component):
    name = "Collection"
    def __init__(self) -> None:
        super().__init__()
        self.entities = {}
        self.objects = ObjectManager()
        self.isStatic = True

    def initialize(self, data) -> None:
        self.entities.clear()
        with open(data) as sceneFile:
            data = json.load(sceneFile)
            for key in data:
                objData = data[key]
                if key == 'freeze':
                    self.entity.freezePlayer = True
                if key == 'entities':
                    for entityName in objData:
                        entity = engine.entity.Entity()
                        entity.parent = self.entity
                        entity.loadEntity(entityName, objData[entityName])
                        self.entities[entityName] = entity
                        self.objects.addObject(entityName, entity)
    
    def destroy(self):
        for entity in self.entities.values():
            entity.destroy()
        
    def removeObject(self, entity):
        if entity in self.entities:
            print("found")
            self.entities[entity].destroy()
            del self.entities[entity]

    def update(self) -> None:
        if self.entities is not None and self.entity is not None:
            for entity in self.entities.values():
                entity.update()
    
    def draw(self, screen: pygame.Surface, offset: list) -> None:
        if self.entities is not None and self.entity is not None:
            position = self.entity.position
            if not self.isStatic:
                position[0] -= offset[0]
                position[1] -= offset[1]
                
            for entity in self.entities.values():
                entity.draw(screen, position)