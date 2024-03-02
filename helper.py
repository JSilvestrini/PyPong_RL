import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, averageScores):
    display.clear_output(wait = True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training - Score")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.plot(scores)
    plt.plot(averageScores)
    plt.ylim(ymin = 0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(averageScores)-1, averageScores[-1], str(averageScores[-1]))
    plt.show(block=False)
    plt.pause(.1)

# make a plot for rewards
def plotRewards(rewards):
    display.clear_output(wait = True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training - Rewards")
    plt.xlabel("Number of Games")
    plt.ylabel("Rewards")
    plt.plot(rewards)
    plt.text(len(rewards)-1, rewards[-1], str(rewards[-1]))
    plt.show(block=False)
    plt.pause(.1)