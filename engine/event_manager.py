from .singleton import Singleton
import pygame
import engine.entity
import engine.components
import engine.object_manager

@Singleton
class EventManager(object):
    def __init__(self) -> None:
        self.events = {}
    
    def clear(self) -> None:
        self.events.clear()

    def addEvent(self, name, function) -> None:
        self.events[name] = function

    def removeEvent(self, name) -> None:
        if name in self.events.keys():
            self.events.pop(name)
    
    def triggerEvent(self, name, *args, **kwargs):
        if name in self.events.keys():
            self.events[name](args, kwargs)

class Event(object):
    name = "Event"

    def __init__(self, name, scene):
        self.eventName = name
        self.scene = scene

    def getEventName(self):
        return self.eventName

    def getScene(self):
        return self.scene

    def initialize(self, data):
        pass

    def trigger(self, *args, **kwargs):
        pass

class StartMinigame(Event):
    name = "startMinigame"
    
    def __init__(self, name, scene):
        super().__init__(name, scene)
        self.isOpen = False
        self.sceneName = ""
        self.eventManager = EventManager()

    def initialize(self, data):
        self.sceneName = data

    def trigger(self, *args, **kwargs):
        if not self.isOpen:
            self.isOpen = True
            # load keypad into scene

            self.eventManager.removeEvent(self.eventName)
            self.eventManager.addEvent("closeMinigame", self.OnComplete)

            keypadObj = engine.entity.Entity()
            keypadObj.isMinigame = True
            collectionComponent = engine.components.Collection()
            keypadObj.addComponent(collectionComponent)
            collectionComponent.initialize(self.sceneName)
            self.scene.freezePlayer(keypadObj.freezePlayer)
            self.scene.addObject(self.eventName, keypadObj)
        
    def OnComplete(self, *args, **kwargs):
        self.eventManager.removeEvent("closeMinigame")
        self.scene.clearTrigger()
        self.scene.freezePlayer(False)
        self.scene.removeObject(self.eventName)
        self.isOpen = False
        if len(args[0]) > 0:
            if args[0][0] == True:
                self.scene.completeMinigame()
            else:
                self.eventManager.addEvent(self.eventName, self.trigger)  
          
class LoadScene(Event):
    name = "loadScene"
    
    def __init__(self, name, scene):
        super().__init__(name, scene)

    def initialize(self, data):
        self.sceneName = data

    def trigger(self, *args, **kwargs):
        self.scene.loadScene(self.sceneName)

class QuitGame(Event):
    name = "quitGame"
    def trigger(self, *args, **kwargs):
        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
            
class KillPlayer(Event):
    name = "killPlayer"
    def trigger(self, *args, **kwargs):
        Players = engine.object_manager.ObjectManager().getPlayers(True)
        imposter = [p for p in Players if p.isImposter][0]

        if imposter is not None and imposter.target is not None:
            imposter.target.kill()

Events = {
    "startMinigame": StartMinigame,
    "loadScene": LoadScene,
    "quitGame": QuitGame,
    "killPlayer": KillPlayer
}