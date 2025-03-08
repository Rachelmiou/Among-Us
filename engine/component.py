from pygame import Surface
import engine.entity

class Component(object):
    name = "Base"
    def __init__(self) -> None:
        self.entity: engine.entity.Entity = None

    def setEntity(self, entity) -> None:
        self.entity = entity

    def getEntity(self):
        return self.entity

    def destroy(self):
        pass

    def initialize(self, data) -> None:
        pass
    
    def update(self) -> None:
        pass
    
    def draw(self, screen: Surface, offset: list) -> None:
        pass