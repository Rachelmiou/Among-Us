
from xml.dom.minidom import Entity
from .singleton import Singleton


@Singleton
class SceneManager(object):

    def __init__(self) -> None:
        self.scene = None
    
    def clear(self) -> None:
        self.scene = None