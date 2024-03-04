# PyPong_RL

## Overview

This collection of files implements a reinforcement learning algorithm that will learn to play Pong (rather poorly). More information about what can be improved can be found starting at [Optimizations and Problems](#optimizations-and-problems).

## Requirements

-   PyTorch
-   PyGame
-   NumPy
-   Matplotlib
-   IPython

## Files

### pong.py

This file contains the actual game environment that the RL AI will play and train in. The game uses PyGame to run, which will be touched on more in the [Optimizations and Problems](#optimizations-and-problems) section as well as the [What I Would Change](#what-i-would-change) section.

This file has functions that will mainly keep track of the current game state, which will allow the agent to gain information for training the model. This file utilizes the shape file to implement the player (RL AI), a ball, and a brute force algorithm that will track the velocity of the ball and try to match it at all times.

### shape.py

This file contains the shapes and the information that they need to be properly placed on the canvas that the game is played on. Most of this class can be refactored or completely rewritten since before (and while) writing it I had little information on how OOP programming was done in Python. This will be touched on more in [What I Would Change](#what-i-would-change).

### agent.py

This file contains all the information that the agent feeds to the model class and also acts as the main file of the collection. This file stores information about the game state, calls the training functions, and will output the chosen move to the game class.

### model.py

This file contains the model that is made using PyTorch. This model uses the [Adam Algorithm](https://pytorch.org/docs/stable/generated/torch.optim.Adam.html) to accomplish this. This file also contains the ability to save a model when it reaches a higher score than a previous iteration as well as loading in models.

### helper.py

This file contains two graphing functions, one of which is unused. The function that is used will plot the average scores as well as the score from each game with the x-axis as the number of games played.

## Optimizations and Problems

**Problem One**

As stated earlier in the overview, this model is rather bad at playing and is exploiting rewards. To solve this the following could be done:

**Potential Fixes**

1. **Remove Rewards that can be Exploited**. In this case, the RL AI gets points for touching the ball and for sitting in front of the ball. The model is then exploiting this by moving from the start point in a random direction and hitting the bottom of the play area, this will allow the RL AI to hit the ball once every few games, meaning that the long term reward beats the punishment that it receives for one, sitting in place, and two, not moving closer to the ball.
2. **Change the System of Rewards Entirely**. Add and remove rewards based on the behavior we want to see. This is contrary to what is said above. In order to rework the rewards, weights and frequency need to be thought about. If the RL AI can hit the ball, maybe make it so that it gets more points than earlier, but make it so that there is a larger punishment for sitting still, but only in certain cases. This fix can be found in the **pong.py** file and can be edited based on preference.
3. **Change the Brute Force Algorithm**. This is also found in the **pong.py** file, but is more subtle. The opponent to the RL AI is an algorithm that will match the velocity of the ball in the vertical direction to ensure that it is always lined upo with the ball. This might be too hard for the RL AI to score against, so to fix it, random moves could be incorporated, and an actual algorithm could be created rather than just velocity matching.

**Problem Two**

This model also takes lots of time to train, anything that can be done to speed it up would help, so the following could be done:

**Potential Fixes**

1. **Threading**. This could allow for multiple agents to work and train at the same time, however, PyGame does not allow for running multiple game displays at the same time. This will be touched on later in [What I Would Change](#what-i-would-change).
2. **Lower-Level Programming**. By saying this, I mean by skipping PyGame entirely since a display is not really needed to train the RL AI. I could either run the training in an array without making drawing calls and functions that would take time to draw on the canvas, or by using a lower-level API to skip past PyGame.

## What I Would Change

1. **Object Oriented Programming**. This was my first time using Python to create classes, so it was weird going from something like C++ to this. In the future I would like to try and make the classes feel more like a C++ class rather than a Python class.
2. **Naming**. This also has to do with point 1. In Python classes to create public and private variables underscores need to be used, so in the future I want to do that more, and implement more getters and setters to prevent trying to directly access member variables.
3. **PyGame Tweaks**. Like stated earlier, using PyGame may be slowing the program down. In order to continue using PyGame, I would have to split the game display into different games, and then have a model play on an individual partition. The only problem this could create that I would have to create a round robin threading solution to make sure that one thread accesses the game, then the next, and so on.
4. **Threading**. In order to implement threading, either point 3 would have to happen, or some other solution that is thread safe would have to be done. My first thought to this would be to use something like OpenGL, which would skip past the PyGame layer, but the problem of "What if OpenGL doesn't work with threading" could still occur. The next solution would be to create arrays and play the game in that instead.
