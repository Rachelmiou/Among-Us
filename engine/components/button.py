from .sprite import Sprite
from ..input_manager import InputManager
from ..event_manager import EventManager
from ..component import Component

class Button(Component):
    name = "Button"
    def __init__(self) -> None:
        self.keypad = None
        self.bounds = [0,0,0,0]
        self.value = 0
        self.trigger = None
    
    def initialize(self, data) -> None:
        if 'value' in data:
            self.value = data['value']
        if 'trigger' in data:
            self.trigger = data['trigger']

        InputManager().addClickable(self)
        sprite: Sprite = self.entity.getComponent("Sprite")

        if sprite is not None:
            position = self.entity.getPosition()
            self.bounds = [position[0], position[1], position[0] + sprite.size[0], position[1] + sprite.size[1]]
    
    def destroy(self):
        InputManager().removeClickable(self)

    def setKeypad(self, keypad) -> None:
        self.keypad = keypad
    
    def onClick(self, point) -> bool:
        if point[0] >= self.bounds[0] and point[0] <= self.bounds[2] and \
                point[1] >= self.bounds[1] and point[1] <= self.bounds[3]:
            if self.keypad is not None:
                # Check if point is in bounds
                self.keypad.pressButton(self.value)
                return True

            if self.trigger is not None:
                EventManager().triggerEvent(self.trigger)
                return True

            # Run click on keypad if it is
        return False