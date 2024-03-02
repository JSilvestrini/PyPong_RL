import shape
import pygame as py
import time
import random
from enum import Enum
import numpy as np

from pygame.locals import (
    QUIT
)

py.init()

class PongGame:
    def __init__(self, WIDTH, HEIGHT):
        self.screen = py.display.set_mode((WIDTH, HEIGHT))
        self.w = WIDTH
        self.h = HEIGHT
        self.reset()

    def intercept(self, PADDLE, player):
        # if ball + dimension <= paddle.position + dimension
        if player:
            if ((PADDLE.getPosition()[0]) <= (self.BALL.getPosition()[0] - self.BALL.getDimensions()[0]) <= (PADDLE.getPosition()[0] + PADDLE.getDimensions()[0])): # potential x intercept
                under = (PADDLE.getPosition()[1] + PADDLE.getDimensions()[1]) >= (self.BALL.getPosition()[1] - self.BALL.getDimensions()[0])
                over = (PADDLE.getPosition()[1]) <= (self.BALL.getPosition()[1] + self.BALL.getDimensions()[0])
                if (under and over and (self.BALL.getDirection() == shape.Direction.TOWARDS)):
                    ballVelocity = self.BALL.getVelocity()
                    self.BALL.setVelocity((-1.02 * ballVelocity[0], 1.02 * (PADDLE.getVelocity()[1] + ballVelocity[1])))
                    self.BALL.changeDirection()
                    #self.reward += .15

        else:
            if ((PADDLE.getPosition()[0]) <= (self.BALL.getPosition()[0] + self.BALL.getDimensions()[0]) <= (PADDLE.getPosition()[0] + PADDLE.getDimensions()[0])): # potential x intercept
                under = (PADDLE.getPosition()[1] + PADDLE.getDimensions()[1]) >= (self.BALL.getPosition()[1] - self.BALL.getDimensions()[0])
                over = (PADDLE.getPosition()[1]) <= (self.BALL.getPosition()[1] + self.BALL.getDimensions()[0])
                if (under and over and (self.BALL.getDirection() == shape.Direction.AWAY)):
                    ballVelocity = self.BALL.getVelocity()
                    self.BALL.setVelocity((-1.02 * ballVelocity[0], 1.02 * (PADDLE.getVelocity()[1] + ballVelocity[1])))
                    self.BALL.changeDirection()

    def updateUI(self):
        self.screen.fill((0, 0, 0))
        self.PADDLE2.updatePosition(self.CURR_TIME - self.PREV_TIME)
        self.PADDLE.updatePosition(self.CURR_TIME - self.PREV_TIME)
        self.BALL.updatePosition(self.CURR_TIME - self.PREV_TIME)
        self.PADDLE2.setVelocity((0, self.BALL.getVelocity()[1]))
        py.draw.circle(self.screen, (255, 255, 255), self.BALL.getPosition(), self.BALL.getDimensions()[0])
        x, y, w, h = self.PADDLE.getPosition()[0], self.PADDLE.getPosition()[1], self.PADDLE.getDimensions()[0], self.PADDLE.getDimensions()[1]
        py.draw.rect(self.screen, (255, 255, 255), py.Rect(x, y, w, h))
        x2, y2, w2, h2 = self.PADDLE2.getPosition()[0], self.PADDLE2.getPosition()[1], self.PADDLE2.getDimensions()[0], self.PADDLE2.getDimensions()[1]
        py.draw.rect(self.screen, (255, 255, 255), py.Rect(x2, y2, w2, h2))

    def reset(self):
        self.score = 0
        self.running = True
        self.CURR_TIME = time.time()
        self.PREV_TIME = time.time()
        self.BALL = shape.Entity((540, 540), shape.Shape.CIRCLE, (15, 15))
        hVel = random.randrange(-15,15)
        if hVel == 0:
            hVel + 5
        self.BALL.setVelocity((random.randrange(15, 30) * 15, hVel * 15))
        #self.BALL.setVelocity((random.randrange(15, 30) * 15, 0))
        self.BALL.setDirection(shape.Direction.AWAY)
        self.PADDLE = shape.Entity((100, 540), shape.Shape.RECTANGLE, (25, 150))
        self.PADDLE2 = shape.Entity((self.w - 125, 540 - 75), shape.Shape.RECTANGLE, (25, 150))
        self.PADDLE2.setVelocity((0, self.BALL.getVelocity()[1]))
        self.frameIteration = 0
        self.reward = 0
    
    def move(self, action):
        if np.array_equal(action, [1, 0]):
            self.PADDLE.increaseVelocity((0, -15))
        elif np.array_equal(action, [0, 1]):
            self.PADDLE.increaseVelocity((0, 15))
        else:
            self.PADDLE.setVelocity((0, 0))

    def extraRewards(self):
        # In line with ball - Positive .5
        under = (self.PADDLE.getPosition()[1] + self.PADDLE.getDimensions()[1]) >= (self.BALL.getPosition()[1] - self.BALL.getDimensions()[0])
        over = (self.PADDLE.getPosition()[1]) <= (self.BALL.getPosition()[1] + self.BALL.getDimensions()[0])
        prevDistance = min(max(self.BALL.getPosition()[1], self.PADDLE.getPreviousPosition()[1]) - min(self.BALL.getPosition()[1],self.PADDLE.getPreviousPosition()[1]), 
                        max(self.BALL.getPosition()[1], self.PADDLE.getPreviousPosition()[1] + self.PADDLE.getDimensions()[1]) - min(self.BALL.getPosition()[1], self.PADDLE.getPreviousPosition()[1] + self.PADDLE.getDimensions()[1]))
        currDistance = min(max(self.BALL.getPosition()[1], self.PADDLE.getPosition()[1]) - min(self.BALL.getPosition()[1],self.PADDLE.getPosition()[1]), 
                        max(self.BALL.getPosition()[1], self.PADDLE.getPosition()[1] + self.PADDLE.getDimensions()[1]) - min(self.BALL.getPosition()[1], self.PADDLE.getPosition()[1] + self.PADDLE.getDimensions()[1]))

        if (under and over):
            self.reward += .1
        # Staying still while not in line - Minus .5
        elif (self.PADDLE.getPreviousPosition()[1] == self.PADDLE.getPosition()[1]):
            self.reward -= .25
        # Move to the ball - Positive .4
        if (prevDistance > currDistance):
            self.reward += .1
        # Staying on edge - Minus .5
        if (self.PADDLE.getPosition()[1] < 80) or (self.PADDLE.getPosition()[1] + self.PADDLE.getDimensions()[1] > self.h - 80):
            self.reward -= .25


    def play_step(self, action):
        self.frameIteration += 1
        self.CURR_TIME = time.time()
        for event in py.event.get():
            if event.type == QUIT:
                    self.running = False

        self.move(action)
        self.updateUI()
        self.intercept(self.PADDLE, True)
        self.intercept(self.PADDLE2, False)
        self.extraRewards()

        self.PREV_TIME = self.CURR_TIME
        py.display.flip()

        if (self.BALL.getPosition()[0] - self.BALL.getDimensions()[0] <= 0) or (self.frameIteration > 40000):
            self.reward = -3
            self.running = False
        if (self.BALL.getPosition()[0] + self.BALL.getDimensions()[0] >= self.h):
            s = self.score + 1
            self.reward += (3 * self.score)
            self.reset()
            self.score = s

        return self.running, self.score, self.reward
