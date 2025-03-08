from .button import Button
from .collection import Collection
from .collision import Collision
from .movement import Movement
from .room import Room
from .sprite import Sprite
from .text_display import TextDisplay
from .keypad import Keypad
from .vending import Vending
from .meeting import Meeting
from .animation import Animation

ComponentTypes = {
    "button": Button,
    "collection": Collection,
    "keypad": Keypad,
    "movement": Movement,
    "room": Room,
    "sprite": Sprite,
    "text": TextDisplay,
    "collision": Collision,
    "vending": Vending,
    "meeting": Meeting,
    "animation": Animation
}