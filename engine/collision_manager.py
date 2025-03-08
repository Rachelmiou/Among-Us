from .singleton import Singleton
from .event_manager import EventManager
from .object_manager import ObjectManager

@Singleton
class CollisionManager(object):

    def __init__(self) -> None:
        self.dynamicObjects = []
        self.staticObjects = []
        self.contacts = {}
        self.eventManager = EventManager()
        self.scene = None
    
    def clear(self) -> None:
        self.staticObjects.clear()
        self.dynamicObjects.clear()

    def addCollision(self, object) -> None:
        if not object.static:
            self.dynamicObjects.append(object)
            return
        self.staticObjects.append(object)
    
    def collideWithList(self, dynamic, list):
        for reactor in list:
            if dynamic != reactor:
                self.collideWith(dynamic, reactor)

    def collideWith(self, dynamic, reactor):
        names = [dynamic.entity.name, reactor.entity.name]
        names.sort()
        collisionName = '-'.join(names)

        result = dynamic.checkCollision(reactor, self.scene)
        if result[0]:
            isTouching = collisionName in self.contacts
            self.contacts[collisionName] = True
            if not dynamic.static and dynamic.trigger is None:
                if reactor.trigger is None:
                    if reactor.static:
                        result[1][0] *= 2
                        result[1][1] *= 2
                    dynamic.entity.position[0] += result[1][0]
                    dynamic.entity.position[1] += result[1][1]
                else:
                    if not isTouching:
                        if dynamic.entity.isPlayer:
                            dynamic.entity.setTrigger(reactor.trigger)

            if not reactor.static and reactor.trigger is None:
                if dynamic.trigger is None:
                    if dynamic.static:
                        result[1][0] *= 2
                        result[1][1] *= 2
                    reactor.entity.position[0] -= result[1][0]
                    reactor.entity.position[1] -= result[1][1]
                else:
                    if not isTouching:
                        if reactor.entity.isPlayer:
                            reactor.entity.setTrigger(dynamic.trigger)
        else:
            if collisionName in self.contacts:
                self.eventManager.triggerEvent("closeMinigame", False)
                entities = collisionName.split('-')
                player = ObjectManager().getPlayer()
                if player.name in entities:
                    player.interactionTrigger = None
                del self.contacts[collisionName]

    def update(self):
        # loop through objects
        for dynamic in self.dynamicObjects:
            self.collideWithList(dynamic, self.dynamicObjects)
            self.collideWithList(dynamic, self.staticObjects)
                

        # check if collision
        # move appropriately