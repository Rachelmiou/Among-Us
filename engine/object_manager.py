
from xml.dom.minidom import Entity
from .singleton import Singleton


@Singleton
class ObjectManager(object):

    def __init__(self) -> None:
        self.objects = {}
    
    def clear(self) -> None:
        self.objects = {}

    def getPlayer(self):
        player = [self.objects[p] for p in self.objects if self.objects[p].isPlayer]
        if len(player) > 0:
            return player[0]
        return None

    def getPlayers(self, isAlive: bool):
        return [self.objects[p] for p in self.objects if self.objects[p].isPlayer and self.objects[p].isAlive == isAlive]    

    def addObject(self, objectName: str, object: Entity) -> None:
        self.objects[objectName] = object

    def removeObject(self, objectName: str) -> None:
        if objectName in self.objects.keys():
            self.objects[objectName].destroy()
            self.objects.pop(objectName)
    
    def getObject(self, objectName: str) -> Entity | None:
        if not objectName in self.objects:
            return None
        return self.objects[objectName]