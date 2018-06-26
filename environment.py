import GridWorld as Gw
import time

'''
total_time = 0
for test in range(0,100):
    # create a grid world
    grid_world = Gw.GridWorld(20, 20, 3, 3, 3)

    # perform value iteration to decide upon best policy
    time_start = time.clock()
    grid_world.policy_iteration(1, -0, 1000, 4)
    time_elapsed = (time.clock() - time_start)
    total_time += time_elapsed

print(total_time/100)

total_time = 0
for test in range(0,100):


print(total_time/100)
'''


#create a grid world
grid_world = Gw.GridWorld(10, 10, 1, 1, 1)

# perform value iteration to decide upon best policy
grid_world.policy_iteration(1, -0.01, 100, 30)


state_values, policy = grid_world.values[1:grid_world.height + 1, 1:grid_world.width + 1], grid_world.policy

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
            char_to_add = " ⬤"
        elif state_values[i, j] == -1 and grid_world.is_exit(i, j):
            char_to_add = " ◯"
        elif direct == 0:
            char_to_add = " ↑"
        elif direct == 1:
            char_to_add = " ←"
        elif direct == 2:
            char_to_add = " ↓"
        elif direct == 3:
            char_to_add = " →"
        elif direct == 4:
            char_to_add = " ↗"
        elif direct == 5:
            char_to_add = " ↖"
        elif direct == 6:
            char_to_add = " ↙"
        elif direct == 7:
            char_to_add = " ↘"

        policy_string += char_to_add

    policy_string += "\n"

print(state_values)
print(policy_string)
