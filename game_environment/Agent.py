import numpy as np
from core.GridWorld import GridWorld


class Agent:

    def __init__(self, grid: GridWorld):
        self.environment = grid
        self.pos = (2, 3)

    def move(self, action):
        valid_action = action.copy()
        center = (1, 1)
        # choose new state given action

        for r in range(0, 3):
            for c in range(0, 3):
                if self.environment.is_wall((r + self.pos[0], c + self.pos[1])):
                    valid_action[center] += valid_action[r, c]
                    valid_action[r, c] = 0

        # choose new state given action
        p = np.ravel(np.sum(valid_action, axis=1))
        test = [0, 1, 2]
        row = np.random.choice(test, p=p)
        index1 = np.where(test == row)[0][0]

        normalized = [i * (1/np.sum(valid_action[index1])) for i in valid_action[index1]]
        col = np.random.choice(test, p=normalized)
        index2 = np.where(test == col)[0][0]

        displace = (index1 - center[0], index2 - center[1])
        new_pos = (self.pos[0] + displace[0], + self.pos[1] + displace[1])
        self.pos = new_pos
