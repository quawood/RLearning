import numpy as np


def def_actions():
    actions = []

    # create 4 different actions
    for i in range(0, 4):
        if i == 0:
            actions.append(np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]]))
        else:
            # each action is a 90 degree rotation of the previously defined action
            previous_action = actions[i - 1]
            rotated = np.rot90(previous_action)
            actions.append(np.array(rotated))

    # code to add 4 diagonal actions

    for i in range(4, 8):
        if i == 4:
            actions.append(np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]]))
        else:
            # each action is a 90 degree rotation of the previously defined action
            previous_action = actions[i - 1]
            rotated = np.rot90(previous_action)
            actions.append(np.array(rotated))

    return actions
