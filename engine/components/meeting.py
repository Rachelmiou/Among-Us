import pygame
from random import randint

from . import Button, Sprite, TextDisplay, Collection

import engine.entity
from ..object_manager import ObjectManager
from ..event_manager import EventManager
from ..scene_manager import SceneManager
from ..component import Component

class Meeting(Component):
    name = "Meeting"
    def __init__(self) -> None:
        super().__init__()
        self.display: engine.entity.Entity = None
        self.keys = []
        self.collection = None
        self.abstain = None

    def initialize(self, data) -> None:
        objectManager = ObjectManager()
        self.collection = self.entity.parent.getComponent(Collection.name)
        self.keys.clear()
        if 'abstain' in data:
            keyObj: engine.entity.Entity = objectManager.getObject(data['abstain'])
            keyBtn: Button = keyObj.getComponent("Button")
            if keyBtn is not None:
                self.abstain = keyObj
                keyBtn.setKeypad(self)

        players = objectManager.getPlayers(True)
        print(players)
        for i in range(len(players)):
            player = players[i]
            x = ((i % 2) * 276) + 32
            y = ((i // 2) * 84) + 32
            buttonObj = engine.entity.Entity()
            buttonObj.position = [x, y]
            buttonObj.name = f"{player.name}_Button"
            
            sprite = Sprite()
            sprite.entity = buttonObj
            sprite.image = pygame.image.load("assets/images/button.png")
            sprite.size = [256, 64]
            buttonObj.addComponent(sprite)

            text = TextDisplay()
            text.entity = buttonObj
            text.text = player.name
            text.offset = [128,32]
            text.color = [255, 255, 255]
            buttonObj.addComponent(text)

            button = Button()
            button.entity = buttonObj
            button.initialize({"value": i})
            button.setKeypad(self)
            buttonObj.addComponent(button)

            objectManager.addObject(buttonObj.name, buttonObj)
            self.keys.append(buttonObj)
            self.collection.entities[buttonObj.name] = buttonObj

    def destroy(self):
        for button in self.keys:
            button.destroy()
        if self.abstain is not None:
            self.abstain.destroy()
    
    def pressButton(self, button):
        players = ObjectManager().getPlayers(True)
        if button == -1:
            # We're complete
            EventManager().triggerEvent("closeMinigame", False)
            
        if button < len(players):
            print(f"killing {players[button].name}")
            SceneManager().scene.removeObject(players[button].name)
            dead = ObjectManager().getPlayers(False)
            for player in dead:
                SceneManager().scene.removeObject(player.name)
            EventManager().triggerEvent("closeMinigame", False)