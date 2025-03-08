import pygame
from random import randint, choice

from .button import Button
from .text_display import TextDisplay

import engine.entity
from ..object_manager import ObjectManager
from ..event_manager import EventManager
from ..component import Component

class Vending(Component):
    name = "vending"
    def __init__(self) -> None:
        super().__init__()
        self.display: engine.entity.Entity = None
        self.displayItem: engine.entity.Entity = None
        self.keys = []
        self.items = []
        self.code = []
        self.pressed = []

    def initialize(self, data) -> None:
        objectManager = ObjectManager()
        self.keys.clear()
        size = 4
        if 'display' in data:
            self.display = objectManager.getObject(data['display'])
        if 'displayItem' in data:
            self.displayItem = objectManager.getObject(data['displayItem'])

        if 'keys' in data:
            for key in data['keys']:
                keyObj: engine.entity.Entity = objectManager.getObject(key)
                keyBtn: Button = keyObj.getComponent("Button")
                if keyBtn is not None:
                    self.keys.append(keyObj)
                    keyBtn.setKeypad(self)

        if 'items' in data:
            for item in data['items']:
                itemObj: engine.entity.Entity = objectManager.getObject(item)
                self.items.append(itemObj.getComponent("Sprite"))

        if 'size' in data:
            size = data['size']
        
        row = {'A': 0, 'B': 1, 'C': 2}
        self.code = (choice(list(row.keys())), str(randint(1,3)))
        
        if self.displayItem is not None:
            sprite = self.displayItem.getComponent("Sprite")
            item = self.items[row[self.code[0]] * 3 + (int(self.code[1])-1)]
            sprite.image = item.image

        self.updateDisplay()

    def destroy(self):
        for button in self.keys:
            button.destroy()
    
    def pressButton(self, button):
        self.pressed.append(button)

        for i in range(len(self.pressed)):
            if self.code[i] != str(self.pressed[i]):
                self.pressed = []
                break
        
        # We've completed the keypress
        # update display
        self.updateDisplay()
        if len(self.code) == len(self.pressed):
            # We're complete
            EventManager().triggerEvent("closeMinigame", True)
    
    def updateDisplay(self):
        if self.display is None:
            return
        
        textComponent: TextDisplay = self.display.getComponent('TextDisplay')

        if textComponent is None:
            return

        display = ['-' for i in self.code]
        for i in range(len(self.pressed)):
            display[i] = str(self.pressed[i])

        textComponent.text = ''.join(display)