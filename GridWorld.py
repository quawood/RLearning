import numpy as np
import random
import MDP_helper as Helper


class GridWorld:

    def __init__(self, width: int, height: int, good_n: int, bad_n: int, wall_n: int):
        self.width = width
        self.height = height
        self.wall_n = wall_n

        self.good_p = []
        self.bad_p = []
        self.wall_p = []
        self.actions = Helper.def_actions()

        self.values = np.zeros((height + 2, width + 2))
        self.policy = np.zeros((height, width))

        for pg in range(0, good_n):
            self.good_p.append((random.randint(0, height - 1), random.randint(0, width - 1)))
        for pb in range(0, bad_n):
            self.bad_p.append((random.randint(0, height - 1), random.randint(0, width - 1)))
        for pw in range(0, wall_n):
            self.wall_p.append((random.randint(0, height - 1), random.randint(0, width - 1)))

    def is_exit(self, i1: int, i2: int) -> bool:
        sink = False
        states = self.good_p + self.bad_p
        for s in range(0, len(states)):
            if (i1, i2) == states[s]:
                sink = True

        return sink

    def is_wall(self, i1: int, i2: int) -> bool:
        wall = False
        for pw in range(0, len(self.wall_p)):
            if (i1, i2) == (self.wall_p[pw][0] + 1, self.wall_p[pw][1] + 1):
                wall = True
                break

        if not wall:
            if i1 == 0 or i1 == self.height + 1 or i2 == 0 or i2 == self.width + 1:
                wall = True

        return wall

    # convolution operator when performing action at a certain state/cell
    def convolve(self, f: np.ndarray, g: np.ndarray, s=1) -> np.ndarray:
        # F to be convoled with G with stride length s

        # dimensions of F and G.
        l, w = f.shape
        n = g.shape[1]

        sums = []
        o_dim1, o_dim2 = (0, 0)  # dimensions of resulting matrix
        for row in range(0, l - n + 1, s):
            o_dim1 += 1
            for col in range(0, w - n + 1, s):
                temp_g = g.copy()
                if row == 0:
                    o_dim2 += 1

                f_sub = f[row:row + n, col:col + n]  # get subset of F

                center = (int((n - 1) / 2), int((n - 1) / 2))
                # check if action is about to be performed to a wall or in exit state and change the action accordingly
                if self.is_exit(row + center[0], row + center[1]):
                    temp_g = np.zeros((n, n))
                else:
                    for r in range(row, row + n):
                        for c in range(col, col + n):
                            if self.is_wall(r, c):
                                temp_g[center] += g[r - row, c - col]
                                temp_g[r - row, c - col] = 0

                product = np.sum(np.multiply(f_sub, temp_g))
                sums.append(product)

        return np.array(sums).reshape((int(o_dim1), int(o_dim2)))

    def value_iteration(self, actions, gamma: float, rs: float, max_iteration: int):

        values = self.values
        p = np.zeros((self.height, self.width))
        iterating = True
        count = 0

        while iterating and count < max_iteration:
            ex_values = gamma * values + rs
            max_values = self.convolve(ex_values, actions[0])

            # loop through actions available
            if len(actions) > 1:
                for a in range(1, len(self.actions)):
                    a_values = self.convolve(ex_values, actions[a])

                    # only add the values associated with the action that provide the greatest values
                    greater = a_values >= max_values
                    max_values[greater] = a_values[greater]

            # choose positions for good and bad rewards
            for g in range(0, len(self.good_p)):
                max_values[self.good_p[g][0], self.good_p[g][1]] = 1
            for g in range(0, len(self.bad_p)):
                max_values[self.bad_p[g][0], self.bad_p[g][1]] = -1

                # re-pad the values array

            padded_values = np.zeros((self.height + 2, self.width + 2))
            padded_values[1:self.height + 1, 1:self.width + 1] = max_values

            if np.amax(np.absolute(padded_values - values)) < 0.01 or count >= max_iteration - 1:
                values = padded_values
                iterating = False

                optimal_policy = np.ones((self.height, self.width))

                # loop through actions available
                if len(actions) > 1:
                    for a in range(1, len(self.actions)):
                        a_values = self.convolve(ex_values, actions[a])

                        # only add the values associated with the action that provide the greatest values
                        greater = a_values >= max_values
                        max_values[greater] = a_values[greater]
                        optimal_policy[greater] = (a + 1)

                p = optimal_policy

            else:
                values = padded_values
                iterating = True
                count += 1

        self.values = values
        self.policy = p

    def policy_iteration(self, gamma: float, rs: float, max_iter: int, value_test: int):
        iterating = True
        count = 0
        p = np.zeros(self.policy.shape)

        while iterating:
            current_policy = self.policy
            self.value_iteration([self.actions[0]], gamma, rs, value_test)

            ex_values = gamma * self.values + rs
            max_values = self.convolve(ex_values, self.actions[0])
            optimal_policy = np.ones((self.height, self.width))

            # loop through actions available
            for a in range(1, len(self.actions)):
                a_values = self.convolve(ex_values, self.actions[a])

                # only add the values associated with the action that provide the greatest values
                greater = a_values >= max_values
                max_values[greater] = a_values[greater]
                optimal_policy[greater] = (a + 1)

            p = optimal_policy

            if p.all() == current_policy.all() or count == max_iter - 1:
                iterating = False
            count += 1

        self.policy = p



