import numpy as np

n_columns = 6
n_rows = 6

actions = []

# create four different actions
for i in range(0, 4):
    if i == 0:
        actions.append(np.array([[0, 0.8, 0], [0.1, 0, 0.1], [0, 0, 0]]))
    else:
        # each action is a 90 degree rotation of the previously defined action
        current_action = actions[i - 1]
        rotated = np.rot90(current_action)
        actions.append(np.array(rotated))


# convolution operator when performing action at a certain state/cell
def convolve(f, g, s=1):
    # F to be convoled with G with stride length s

    # dimensions of F and G.
    l, w = f.shape
    n = g.shape[1]

    sums = []
    o_dim1, o_dim2 = (0, 0)  # dimensions of resulting matrix
    for row in range(0, l - n + 1, s):
        o_dim1 += 1
        for col in range(0, w - n + 1, s):
            if row == 0:
                o_dim2 += 1

            f_sub = f[row:row + n, col:col + n]  # get subset of F
            product = np.sum(np.multiply(f_sub, g))
            sums.append(product)

    return np.array(sums).reshape((int(o_dim1), int(o_dim2)))


def value_iteration(values, gamma, rs, max_iteration):
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
        max_values = np.zeros((n_rows, n_columns))
        optimal_policy = np.zeros((n_rows, n_columns))

        # loop through actions available
        for a in range(0, len(actions)):
            a_values = convolve(ex_values, actions[a])

            # only add the values associated with the action that provide the greatest values
            greater = a_values > max_values
            max_values[greater] = a_values[greater]
            optimal_policy[greater] = (a + 1)

        max_values[0, n_columns - 1] = 1
        max_values[1, n_columns - 1] = -1
        max_values[4, 1] = 1

        # re-pad the values array
        padded_values = np.zeros((n_rows + 2, n_columns + 2))
        padded_values[1:n_rows + 1, 1:n_columns + 1] = max_values
        padded_values[0, 1:n_columns + 1] = max_values[0, :]
        padded_values[n_rows + 1, 1:n_columns + 1] = max_values[n_rows - 1, :]
        padded_values[1:n_rows + 1, 0] = max_values[:, 0]
        padded_values[1:n_rows + 1, n_columns + 1] = max_values[:, n_columns - 1]

        values = padded_values
        p = optimal_policy
        if iteration == max_iteration - 1:
            values = max_values
    np.zeros((n_rows, n_columns))

    return values, p


state_values, policy = value_iteration(np.zeros((n_rows + 2, n_columns + 2)), 1, 0, 100)
policy_string = ""

# display policy with arrows
for i in range(0, n_rows):
    for j in range(0, n_columns):
        direct = policy[i, j]
        char_to_add = ""

        if direct == 1:
            char_to_add = " ↑"

        elif direct == 2:
            char_to_add = " ←"

        elif direct == 3:
            char_to_add = " ↓"

        elif direct == 4:
            char_to_add = " →"

        policy_string = policy_string + char_to_add

    policy_string = policy_string + "\n"

print(state_values)
print(policy_string)
