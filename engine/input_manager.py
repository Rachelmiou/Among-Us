import pygame
from .singleton import Singleton

class Key(object):
        def __init__(self) -> None:
            self.pressed = None
            self.held = None
            self.released = None

            self.currentState = False

        def update(self, state):
            if not self.currentState and state:
                if not self.pressed is None:
                    self.pressed()
            
            if self.currentState and state:
                if not self.held is None:
                    self.held()
            
            if self.currentState and not state:
                if not self.released is None:
                    self.released()
                
            self.currentState = state

@Singleton
class InputManager(object):

    def __init__(self) -> None:
        self.keyList = {}
        self.clickable = []
        self.oldDown = False
    
    def clear(self) -> None:
        self.keyList = {}
        self.clickable = []
    
    def addPressed(self, keyCode, function):
        if not keyCode in self.keyList.keys():
            self.keyList[keyCode] = Key()
        
        self.keyList[keyCode].pressed = function
    
    def addHeld(self, keyCode, function):
        if not keyCode in self.keyList.keys():
            self.keyList[keyCode] = Key()
        
        self.keyList[keyCode].held = function
    
    def addReleased(self, keyCode, function):
        if not keyCode in self.keyList.keys():
            self.keyList[keyCode] = Key()
        
        self.keyList[keyCode].released = function
    
    def addClickable(self, clickable) -> None:
        self.clickable.append(clickable)

    def removeClickable(self, clickable) -> None:
        if clickable in self.clickable:
            index = self.clickable.index(clickable)
            self.clickable.pop(index)
            

    def update(self):
        pressedKeys = pygame.key.get_pressed()
        for keyCode in self.keyList.keys():
            self.keyList[keyCode].update(pressedKeys[keyCode])
        
        if pygame.mouse.get_pressed()[0] and not self.oldDown:
            for click in self.clickable:
                if click.onClick(pygame.mouse.get_pos()):
                    break
        self.oldDown = pygame.mouse.get_pressed()[0]