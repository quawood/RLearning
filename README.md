# Markov Decision Processes
Playing around with reinforcement learning

The problem tackled currently in this project is a generalization of the problem outlined in Lecture 8 and 9 of CS188Spring2013 on Markov Decision Processes 

The problem is as follows:
* There exists an agent in a mxn dimensional grid world.
* There are cells within this grid world that give high positive reward and high negative reward upon leaving them
* Leaving a any ordinary cell to any other ordinary cell gives a certain reward as well
* An agent can choose from a series of actions within the grid world. These actions can be stochastic (the intended action is not always taken)
* Given that you want to maximum the reward collected by an agent in the grid world, what are the optimal actions to take on each grid?


This problem was solved using value iteration, which is an iterative process which uses the Belmann equation to determine the expected reward from acting optimally from a certain cell.
Having calculated these values for each cell, the actions that produced these values were chosen to determine which action should be taken within each cell


Currently, there is a crude version of a virtual environmet where positions walls, rewards, and penalties can be modified easily.

![alt text](https://github.com/quawood/RLearning/blob/master/images/current1.png)
![alt text](https://github.com/quawood/RLearning/blob/master/images/current2.png)

Issues/next steps:
* add sliders for gamma value, living reward, and dimensions of environment
* actual reinforcement learning in grid world
