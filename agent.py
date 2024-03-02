import torch
from pong import PongGame
import random
import numpy as np
from collections import deque
import shape
from model import LinearQNet, QTrainer
from helper import plot, plotRewards
import math

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class agent:
    def __init__(self):
        self.number_games = 0
        self.epsilon = 80 # controls randomness
        self.gamma = 0.90 # discount, smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(13, 256, 2)
        self.trainer = QTrainer(self.model, LEARNING_RATE, self.gamma)
        self.maxDistance = 0

    def getState(self, game):
        # paddle direction (either up or down based on velocity)
        # ball direction (either up or down compared to player)
        # ball movement (either up or down based on velocity)
        # ball direction (towards or away)
        pv = game.PADDLE.getVelocity()
        pp = game.PADDLE.getPosition()
        pd = game.PADDLE.getDimensions()
        bv = game.BALL.getVelocity()
        bd = game.BALL.getDirection()
        bp = game.BALL.getPosition()
        bdi = game.BALL.getDimensions()
        topOfBall = bp[1] - bdi[1]
        bottomOfBall = bp[1] + bdi[1]
        topOfPaddle = pp[1]
        bottomOfPaddle = pp[1] + pd[1]

        state = [
            # [moving up, moving down, not moving]
            pv[1] < 0,
            pv[1] > 0,
            pv[1] == 0,

            # position of ball to paddle
            # [above paddle, below paddle, straight]
            (bottomOfBall < topOfPaddle),
            (topOfBall > bottomOfPaddle),
            ((topOfBall <= bottomOfPaddle) and (bottomOfBall >= topOfPaddle)),

            # ball movement [up, down, straight]
            bv[1] < 0,
            bv[1] > 0,
            bv[1] == 0,

            # ball direction [away, to]
            bd == shape.Direction.AWAY,
            bd == shape.Direction.TOWARDS
        ]

        state = np.array(state, dtype = int)
        normDistance = math.dist((pp[0] + pd[0], pp[1] + (pp[1] / 2)), bp)
        self.maxDistance = max(self.maxDistance, normDistance)
        normDistance = normDistance / self.maxDistance
        normAngle = (math.degrees(math.atan2((pp[1] + (pp[1] / 2) - bp[1]), (pp[0] + pd[0]) - bp[0])) + 180) /360

        finState = np.concatenate([state, [normDistance, normAngle]])
        return finState

    def remember(self, state, action, reward, nextState, done):
        # done is going to be reverse
        self.memory.append((state, action, reward, nextState, done))

    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            miniSample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            miniSample = self.memory

        states, actions, rewards, nextStates, dones = zip(*miniSample)
        self.trainer.trainStep(states, actions, rewards, nextStates, dones)

    def trainShortMemory(self, state, action, reward, nextState, done):
        # done is going to be reverse
        self.trainer.trainStep(state, action, reward, nextState, done)

    def getAction(self, state):
        # random moves: exploration vs exploitation
        self.epsilon -= 1
        potentialMove = [0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 1)
            potentialMove[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            potentialMove[move] = 1
        return potentialMove


def train():
    scores = []
    averageScores = []
    totalScore = 0
    bestScore = 0

    a = agent()
    try:
        a.model.load()
    except:
        print("Error Loading Model")
    game = PongGame(1080, 1080)

    while True:
        # get old state
        stateOld = a.getState(game)
        # get move
        move = a.getAction(stateOld)
        # perform
        running, score, reward = game.play_step(move)
        # new state
        stateNew = a.getState(game)
        # short
        a.trainShortMemory(stateOld, move, reward, stateNew, running)
        # remember
        a.remember(stateOld, move, reward, stateNew, running)

        if running == False:
            # train long, plot results
            game.reset()
            a.number_games += 1
            a.trainLongMemory()

            if score > bestScore:
                bestScore = score
                a.model.save()
            
            print("Game: ", a.number_games, "Score: ", score, "Record: ", bestScore)
            scores.append(score)
            totalScore += score
            averageScores.append(totalScore / a.number_games)
            plot(scores, averageScores)

if __name__ == "__main__":
    train()

'''
1. Create Pong
    a. Need paddle                                  - done
    b. Need to move                                 - done
    c. Need ball                                    - done
    d. Make ball move                               - done
    e. Let paddle hit ball                          - done
    f. Ball bounces off wall                        - done
2. Outputs                                          - done
    a. Track Position, Velocity, and Direction:     - done
        1. Ball                                     - done
        2. Paddle                                   - done
    b. Track Volley Count                           - done
3. Begin AI work                                    - working on
'''