import json
import pygame

import engine.entity
from ..object_manager import ObjectManager
from ..component import Component
from .collision import Collision

class Room(Component):
    name = "Room"
    def __init__(self) -> None:
        super().__init__()
        self.entities = []

    def initialize(self, data) -> None:
        self.entities.clear()
        for key in data:
            objData = data[key]
            if key == 'shapes':
                for collision in objData:
                    component = Collision()
                    component.setEntity(self.entity)
                    component.initialize(collision)
                    self.entities.append(component)