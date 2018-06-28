import numpy as np

class Agent:

    def __init__(self, grid):
        self.environment = grid
        self.pos = (0, 0)




    def move(self, action):

        # choose new state given action
        test = np.arange(0, action.size).reshape(action.shape)
        lens = [len(row) for row in action]
        p = [np.sum(row) for row in action]

        new_arr = np.concatenate(np.asarray(test))
        new_p = np.repeat(np.divide(p, lens), lens)

        num = np.random.choice(new_arr, p=new_p)
        index = np.where(test==num)
        new_pos = (index[0][0], index[1][0])
        self.pos = new_pos


