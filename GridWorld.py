import numpy as np
import random
import MDP_helper as Helper


class GridWorld:

    def __init__(self, height: int, width: int, good_n, bad_n, wall_n):
        self.width = width
        self.height = height
        self.wall_n = wall_n

        self.good_p = good_n
        self.bad_p = bad_n
        self.wall_p = wall_n
        self.actions = Helper.def_actions()

        self.values = np.zeros((height + 2, width + 2))
        self.prev_values = np.zeros((height + 2, width + 2))
        self.policy = np.zeros((height, width))

        self.count = 0
        if isinstance(good_n, int):
            for pg in range(0, good_n):
                self.good_p.append((random.randint(0, height - 1), random.randint(0, width - 1)))
        if isinstance(bad_n, int):
            for pb in range(0, bad_n):
                self.bad_p.append((random.randint(0, height - 1), random.randint(0, width - 1)))
        if isinstance(wall_n, int):
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
    def convolve(self, f: np.ndarray, g, s=1) -> np.ndarray:
        # F to be convoled with G with stride length s

        # dimensions of F and G.
        l, w = f.shape
        n = self.actions[0].shape[0]
        g_is_policy = False
        if g.shape == (self.height, self.width):
            g_is_policy = True

        sums = []
        o_dim1, o_dim2 = (0, 0)  # dimensions of resulting matrix
        for row in range(0, l - n + 1, s):
            o_dim1 += 1
            for col in range(0, w - n + 1, s):
                temp_g = g.copy()

                if g_is_policy:
                    index = int(g[row, col])
                    temp_g = self.actions[index].copy()

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
                                temp_g[center] += temp_g[r - row, c - col]
                                temp_g[r - row, c - col] = 0

                product = np.sum(np.multiply(f_sub, temp_g))
                sums.append(product)

        return np.array(sums).reshape((int(o_dim1), int(o_dim2)))

    def value_iteration(self, gamma, rs, max_iteration):
        p = self.policy.copy()
        iterating = True
        count = 0

        while iterating and count < max_iteration:
            self.prev_values = self.values.copy()
            self.update_values(self.actions, gamma, rs)

            if np.amax(np.absolute(self.prev_values - self.values)) < 0.001 or count >= max_iteration - 1:
                iterating = False
                # loop through actions available
                p = self.extract_policy(gamma, rs)

            else:
                iterating = True
                count += 1

        self.policy = p
        self.count = count

    def policy_iteration(self, gamma, rs, max_iter, value_test):
        iterating = True
        count = 0
        p = self.policy.copy()

        while iterating:
            current_policy = p.copy()
            for test in range(0, value_test):
                self.prev_values = self.values.copy()
                self.update_values([p], gamma, rs)

            p = self.extract_policy(gamma, rs)
            if (p == current_policy).all() or count == max_iter - 1:

                iterating = False

            count += 1

        self.policy = p
        self.count = count*value_test

    def extract_policy(self, gamma, rs):
        ex_values = gamma * self.prev_values + rs
        max_values = self.convolve(ex_values, self.actions[0])
        optimal_policy = np.zeros((self.height, self.width))

        for a in range(1, len(self.actions)):
            a_values = self.convolve(ex_values, self.actions[a])

            # only add the values associated with the action that provide the greatest values
            greater = a_values >= max_values
            max_values[greater] = a_values[greater]
            optimal_policy[greater] = a

        return optimal_policy

    def update_values(self, actions, gamma, rs):
        ex_values = gamma * self.prev_values + rs
        max_values = self.convolve(ex_values, actions[0])

        # loop through actions available and update values accordingly
        if len(actions) > 1:
            for a in range(1, len(actions)):
                a_values = self.convolve(ex_values, actions[a])
                # only add the values associated with the action that provide the greatest values
                greater = a_values >= max_values
                max_values[greater] = a_values[greater]

        # choose positions for good and bad rewards
        for g in range(0, len(self.good_p)):
            max_values[self.good_p[g][0], self.good_p[g][1]] = 1

        for g in range(0, len(self.bad_p)):
            max_values[self.bad_p[g][0], self.bad_p[g][1]] = -1

        # pad the values array

        padded_values = np.zeros((self.height + 2, self.width + 2))
        padded_values[1:self.height + 1, 1:self.width + 1] = max_values
        self.values = padded_values
