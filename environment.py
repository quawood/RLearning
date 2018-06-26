import GridWorld as Gw


# create a grid world
grid_world = Gw.GridWorld(20, 20, 3, 3, 5)
grid_world.value_iteration(1, -0.1, 1000)
state_values, policy = grid_world.values, grid_world.policy

# display policy with arrows
policy_string = ""
for i in range(0, grid_world.height):
    for j in range(0, grid_world.width):
        direct = policy[i, j]
        char_to_add = ""
        print()
        if grid_world.is_wall(i + 1, j + 1):
            char_to_add = " ■"
        elif state_values[i, j] == 1 and grid_world.is_exit(i, j):
            char_to_add = " •"
        elif state_values[i, j] == -1 and grid_world.is_exit(i, j):
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
