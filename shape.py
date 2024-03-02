import pygame as py
from enum import Enum

WIDTH = 1080
HEIGHT = 1080

class Direction(Enum):
    TOWARDS = True
    AWAY = False

class Shape(Enum):
    CIRCLE = True
    RECTANGLE = False

class Entity:
    def __init__(self, position, shape, dimensions):
        self.position = position
        self.velocity = (0, 0)
        self.previous_position = (0, 0)
        self.direction = Direction.AWAY
        self.shape = Shape(shape)
        self.dimensions = dimensions
        self.volley = 0

        if self.shape == Shape.RECTANGLE:
            x = 0
        elif self.shape == Shape.CIRCLE:
            x = 0

    def getPosition(self):
        return self.position
    def getVelocity(self):
        return self.velocity
    def getPreviousPosition(self):
        return self.previous_position
    def getDirection(self):
        return self.direction
    def getShape(self):
        return self.shape
    def getDimensions(self):
        return self.dimensions
    def bounce(self):
        # calculate the bouncing of the ball
        # update position
        # update the velocity
        # update direction
        # can use this code for paddle collision
        if self.position[0] + self.dimensions[0] >= WIDTH:
            self.velocity = (-1 * self.velocity[0], self.velocity[1])
            self.position = (WIDTH - self.dimensions[0], self.position[1])
            self.changeDirection()
        if self.position[1] + self.dimensions[0] >= HEIGHT:
            self.velocity = (self.velocity[0], -1 * self.velocity[1])
            self.position = (self.position[0], HEIGHT - self.dimensions[0])
        if self.position[1] <= self.dimensions[0]:
            self.velocity = (self.velocity[0], -1 * self.velocity[1])
            self.position = (self.position[0], self.dimensions[0])

    def updatePosition(self, time):
        self.previous_position = self.position
        self.position = (self.position[0] + (self.velocity[0] * time), self.position[1] + (self.velocity[1] * time))

        if self.shape == Shape.RECTANGLE:
            if self.position[0] > WIDTH - self.dimensions[0]:
                self.position = (WIDTH - self.dimensions[0], HEIGHT)

            if self.position[1] > HEIGHT - self.dimensions[1]:
                self.position = (self.position[0], HEIGHT - self.dimensions[1])
                self.velocity = (0, 0)

            if self.position[0] <= 0:
                self.position = (0, self.position[1])

            if self.position[1] <= 0:
                self.position = (self.position[0], 0)
                self.velocity = (0, 0)
        
        if self.shape == Shape.CIRCLE:
            border = 0 <= self.position[0] < (WIDTH - self.dimensions[0]) and 0 <= self.position[1] < (HEIGHT - self.dimensions[1])
            if not border:
                self.bounce()

    def increaseVelocity(self, n):
        self.velocity = (self.velocity[0] + n[0], self.velocity[1] + n[1])
        if self.shape == Shape.RECTANGLE:
            if self.velocity[1] > 350:
                self.velocity = (self.velocity[0], 350)
            if self.velocity[1] < -350:
                self.velocity = (self.velocity[0], -350)
    def setVelocity(self, n):
        self.velocity = n
        if self.shape == Shape.CIRCLE:
            if self.velocity[0] > 800:
                self.velocity = (800, self.velocity[1])
            if self.velocity[0] < -800:
                self.velocity = (-800, self.velocity[1])
            if self.velocity[1] > 400:
                self.velocity = (self.velocity[0], 400)
            if self.velocity[1] < -400:
                self.velocity = (self.velocity[0], -400)
    def changeDirection(self):
        if self.direction == Direction.TOWARDS:
            self.direction = Direction.AWAY
        else:
            self.direction = Direction.TOWARDS
    def setDirection(self, dir):
        self.direction = dir

    def incrementVolley(self):
        self.volley += 1