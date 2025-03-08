import pygame
from random import randint

from .button import Button
from .text_display import TextDisplay

import engine.entity
from ..object_manager import ObjectManager
from ..event_manager import EventManager
from ..component import Component

class Keypad(Component):
    name = "Keypad"
    def __init__(self) -> None:
        super().__init__()
        self.display: engine.entity.Entity = None
        self.keys = []
        self.code = []
        self.pressed = []

    def initialize(self, data) -> None:
        objectManager = ObjectManager()
        self.keys.clear()
        size = 4
        if 'display' in data:
            self.display = objectManager.getObject(data['display'])

        if 'keys' in data:
            for key in data['keys']:
                keyObj: engine.entity.Entity = objectManager.getObject(key)
                keyBtn: Button = keyObj.getComponent("Button")
                if keyBtn is not None:
                    self.keys.append(keyObj)
                    keyBtn.setKeypad(self)

        if 'size' in data:
            size = data['size']
        
        for i in range(size):
            self.code.append(randint(1,9))
        
        self.updateDisplay()

    def destroy(self):
        for button in self.keys:
            button.destroy()
    
    def pressButton(self, button):
        self.pressed.append(button)

        for i in range(len(self.pressed)):
            if self.code[i] != self.pressed[i]:
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

        display = [str(i) for i in self.code]
        for i in range(len(self.pressed)):
            display[i] = '*'

        textComponent.text = ' '.join(display)