import pygame
from ..component import Component
from ..collision_manager import CollisionManager
from math import sqrt, hypot

class Collision(Component):
    name = "Collision"
    def __init__(self) -> None:
        super().__init__()
        self.shape = None
        self.size = None
        self.static = False
        self.trigger = None
        self.offset = [0,0]
        self.sceneOffset = [0,0]

    def initialize(self, data) -> None:
        if 'size' in data:
            self.size = data['size']

        if 'shape' in data:
            self.shape = data['shape']

        if 'offset' in data:
            self.offset = data['offset']

        if 'static' in data:
            self.static = data['static']

        if 'trigger' in data:
            self.trigger = data['trigger']

        CollisionManager().addCollision(self)

    def dot(u, v) -> list:
        return [u[0] * v[0] + u[1] * v[1]]

    def getPosition(self):
        position = [self.entity.position[0] + self.offset[0], self.entity.position[1] + self.offset[1]]
        return position
    
    def getSize(self):
        if self.shape == "circle":
            return [self.size[0] * 2, self.size[0] * 2]
        
        return [self.size[0], self.size[1]]

    def boxBox(box1, box2) -> [bool, list, list]:
        position = box1.getPosition()
        otherPosition = box2.getPosition()

        box1Size = box1.getSize()
        box2Size = box2.getSize()

        box1Bounds = [position[0], position[1], position[0]+box1Size[0], position[1]+box1Size[1]]
        box2Bounds = [otherPosition[0], otherPosition[1], otherPosition[0]+box2Size[0], otherPosition[1]+box2Size[1]]

        if box1Bounds[0] >= box2Bounds[2] or box1Bounds[2] <= box2Bounds[0] or box1Bounds[1] >= box2Bounds[3] or box1Bounds[3] <= box2Bounds[1]:
            return [False, []]

        leftRight = box2Bounds[2] - box1Bounds[0]
        rightLeft = box2Bounds[0] - box1Bounds[2]
        
        topBottom = box2Bounds[3] - box1Bounds[1]
        bottomTop = box2Bounds[1] - box1Bounds[3]

        minX = 0
        if abs(leftRight) < abs(rightLeft):
            minX = leftRight
        else:
            minX = rightLeft
            
        minY = 0
        if abs(topBottom) < abs(bottomTop):
            minY = topBottom
        else:
            minY = bottomTop

        if abs(minX) < abs(minY):
            minY = 0
        else:
            minX = 0

        return [True, [minX / 2, minY / 2]]

    def boxCircle(box, circle) -> [bool, list]:
        result = Collision.boxBox(box, circle)

        if not result[0]:
            return result

        position = box.getPosition()
        otherPosition = circle.getPosition()
        otherPosition[0] += circle.size[0]
        otherPosition[1] += circle.size[0]

        points = [
            position,                                       # TL
            
            [position[0] + box.size[0] / 2, position[1]],   # T
            [position[0] + box.size[0], position[1]],       # TR

            [position[0], position[1] + box.size[1] / 2],   # L
            [position[0], position[1] + box.size[1]],       # BL

            [position[0] + box.size[0], position[1] + box.size[1] / 2], # R
            [position[0] + box.size[0], position[1] + box.size[1]],     # BR

            [position[0] + box.size[0] / 2, position[1] + box.size[1] / 2] # B
        ]

        for point in points:
            restitution = [point[0] - otherPosition[0], point[1] - otherPosition[1]]
            result = hypot(restitution[0], restitution[1])
            if result < circle.size[0]:
                restitution = [restitution[0] / 8, restitution[1] / 8]
                return [True, restitution]
        
        return [False, []]
    
    def checkCollision(self, other, scene) -> [bool, list]:
        if (self.size is None or self.shape is None) or (other.size is None or other.shape is None):
            return [False, []]
        
        self.sceneOffset = [0,0]
        if scene is not None:
            self.sceneOffset = scene.getOffset()
        
        # Box and Circle
        if self.shape == "box" and other.shape == "box":
            return Collision.boxBox(self, other)

        elif self.shape == "box" and other.shape == "circle":
            return Collision.boxCircle(self, other)

        elif self.shape == "circle" and other.shape == "box":
            return Collision.boxCircle(other, self)

        elif self.shape == "circle" and other.shape == "circle":
            collisionDist = self.size[0] + other.size[0]
            position = self.getPosition()
            otherPosition = other.getPosition()
            actualX = position[0] - otherPosition[0]
            actualY = position[1] - otherPosition[1]

            actualDist = hypot(actualX, actualY)
            return [actualDist < collisionDist, [actualX / 2, actualY / 2]]
        
        return [False, []]

    # def draw(self, screen, offset):
    #     position = self.getPosition()
    #     position[0] -= offset[0]
    #     position[1] -= offset[1]

    #     if self.shape == "circle":
    #         pygame.draw.circle(screen, (255, 0, 0), (position[0] + self.size[0], position[1] + self.size[0]), self.size[0])

    #     if self.shape == "box":
    #         points = [
    #             position,
    #             [position[0], position[1] + self.size[1]],
    #             [position[0] + self.size[0], position[1]],
    #             [position[0] + self.size[0], position[1] + self.size[1]],
    #             [position[0] + self.size[0]/2, position[1] + self.size[1]/2]
    #         ]
    #         for i in range(len(points)):
    #             point = points[i]
    #             pygame.draw.circle(screen, (255, 0, 0), point, 2)