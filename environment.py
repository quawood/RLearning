import numpy as np


n_columns = 6
n_rows = 6


actions = []
# create 4 different actions
for i in range(0, 4):
    if i == 0:
        actions.append(np.array([[0, 0.8, 0], [0.1, 0, 0.1], [0, 0, 0]]))
    else:
        # each action is a 90 degree rotation of the previously defined action
        previous_action = actions[i - 1]
        rotated = np.rot90(previous_action)
        actions.append(np.array(rotated))

# code to add 4 diagonal actions

for i in range(4, 8):
    if i == 4:
        actions.append(np.array([[0.1, 0, 0.8], [0, 0, 0], [0, 0, 0.1]]))
    else:
        # each action is a 90 degree rotation of the previously defined action
        previous_action = actions[i - 1]
        rotated = np.rot90(previous_action)
        actions.append(np.array(rotated))


def is_wall(i1: int, i2: int) -> bool:
    wall = False
    if i1 == 0 or i1 == n_rows + 1 or i2 == 0 or i2 == n_columns + 1 or (i1, i2) == (2, 2):
        wall = True

    return wall


def is_exit(i1: int, i2: int) -> bool:
    sink = False
    states = [(0, n_columns - 1), (1, n_columns - 1)]
    for s in range(0, len(states)):
        if (i1, i2) == states[s]:
            sink = True

    return sink


# convolution operator when performing action at a certain state/cell
def convolve(f: np.ndarray, a: int, s=1) -> np.ndarray:
    # F to be convoled with G with stride length s

    # dimensions of F and G.
    g = actions[a]
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
            if is_exit(row + center[0], row + center[1]):
                temp_g = np.zeros((n, n))
            else:
                for r in range(row, row + n):
                    for c in range(col, col + n):
                        if is_wall(r, c):
                            temp_g[center] += g[r - row, c - col]
                            temp_g[r - row, c - col] = 0

            product = np.sum(np.multiply(f_sub, temp_g))
            sums.append(product)

    return np.array(sums).reshape((int(o_dim1), int(o_dim2)))


def value_iteration(values: np.ndarray, gamma: float, rs: float, max_iteration: int) -> (np.ndarray, np.ndarray):
    """
    :param values: value matrix containing the values of each state/cell
    :type values: np.ndarray
    :param gamma: gamma value giving the discount rate
    :type gamma: float
    :param rs: living penalty
    :type rs: float
    :param max_iteration: the maximum iterations of the value iteration algorithm
    :type max_iteration: int
    """
    values = values
    p = np.zeros((n_rows, n_columns))
    for iteration in range(0, max_iteration):

        ex_values = gamma * values + rs
        max_values = convolve(ex_values, 0)
        optimal_policy = np.ones((n_rows, n_columns))

        # loop through actions available
        for a in range(1, len(actions)):
            a_values = convolve(ex_values, a)

            # only add the values associated with the action that provide the greatest values
            greater = a_values >= max_values
            max_values[greater] = a_values[greater]
            optimal_policy[greater] = (a + 1)

        # choose positions for good and bad rewards
        max_values[0, n_columns - 1] = 1
        max_values[1, n_columns - 1] = -1

        # re-pad the values array
        padded_values = np.zeros((n_rows + 2, n_columns + 2))
        padded_values[1:n_rows + 1, 1:n_columns + 1] = max_values

        values = padded_values
        p = optimal_policy
        if iteration == max_iteration - 1:
            values = max_values
    np.zeros((n_rows, n_columns))

    return values, p


state_values, policy = value_iteration(np.zeros((n_rows + 2, n_columns + 2)), 1, -0.01, 100)
policy_string = ""

# display policy with arrows
for i in range(0, n_rows):
    for j in range(0, n_columns):
        direct = policy[i, j]
        char_to_add = ""
        print()
        if is_wall(i+1,j+1):
            char_to_add = " ■"
        elif state_values[i, j] == 1 and is_exit(i, j):
            char_to_add = " •"
        elif state_values[i, j] == -1 and is_exit(i, j):
            char_to_add = " o"
        elif direct == 1:
            char_to_add = " ↑"
        elif direct == 2:
            char_to_add = " ←"
        elif direct == 3:
            char_to_add = " ↓"
        elif direct == 4:
            char_to_add = " →"
        elif direct == 5:
            char_to_add = " ↗"
        elif direct == 6:
            char_to_add = " ↖"
        elif direct == 7:
            char_to_add = " ↙"
        elif direct == 8:
            char_to_add = " ↘"

        policy_string += char_to_add

    policy_string += "\n"

print(state_values)
print(policy_string)
