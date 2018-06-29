import pygame
import random
import numpy as np
from game_environment.Game import Game

# value iteration
width = 5
height = 5

# set up game
game = Game(width, height)
game.start()
learning = False

MOVE_EVENT, t = pygame.USEREVENT+1, 250
pygame.time.set_timer(MOVE_EVENT, t)


def draw(canvas):
    canvas.fill((255, 255, 255))

    game.draw_cells(canvas)

    if learning:
        pygame.draw.circle(canvas, (46, 155, 236), game.cells[game.agent.pos[0]][game.agent.pos[1]].rect.center,
                           10)


def explore(epsilon, alpha, gamma, r):
    current_state = game.agent.pos

    rand = random.uniform(0, 1)
    to_exit = False
    reward = 0
    a = None

    if game.grid_world.is_exit(current_state):
        to_exit = True

        if current_state in game.grid_world.good_p:
            reward = 1
        elif current_state in game.grid_world.bad_p:
            reward = -1

    else:
        reward = r

        if rand < epsilon:
            a = random.randint(0, len(game.grid_world.actions) - 1)
        else:
            q_actions = game.grid_world.qvalues[:, current_state[0], current_state[1]]
            a = np.argmax(q_actions)

        game.agent.move(game.grid_world.actions[a])

    sample = (current_state, a, reward, game.agent.pos)

    game.grid_world.update_qvalue(sample, gamma, alpha, to_exit)

    if to_exit:
        game.agent.pos = game.grid_world.rand_pos()


# update game
def learn():
    alpha_creep = 0.0 * (int(game.runs) // int(1000))
    explore(0.5 - alpha_creep, 0.1, 0.9, -0.1)
    game.runs += 1


def stop_learn():
    policy = game.grid_world.q_extract_policy()
    for i in range(0, len(game.cells)):
        for j in range(0, len(game.cells[i])):
            direct = policy[i, j]
            char_to_add = ""
            if game.grid_world.is_wall((i + 1, j + 1)):
                char_to_add = ""
            elif game.grid_world.is_exit((i, j)):
                char_to_add = ""
            elif direct == 0:
                char_to_add = "C"
            elif direct == 1:
                char_to_add = "B"
            elif direct == 2:
                char_to_add = "D"
            elif direct == 3:
                char_to_add = "A"
            elif direct == 4:
                char_to_add = "G"
            elif direct == 5:
                char_to_add = "E"
            elif direct == 6:
                char_to_add = "F"
            elif direct == 7:
                char_to_add = "H"

            game.cells[i][j].label = game.font.render(char_to_add, 1, (0, 0, 0))


while not game.stopped:
    draw(game.gameDisplay)
    if learning:
        learn()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(game.grid_world.qvalues)
            game.stopped = True

        # if event.type == MOVE_EVENT:

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            r_pos = (pos[0], pos[1], 1, 1)
            game.drag = True
            game.check(r_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            game.drag = False

        elif event.type == pygame.MOUSEMOTION:
            if game.drag:
                pos = event.pos
                r_pos = (pos[0], pos[1], 1, 1)
                game.check(r_pos)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game.new_grid(game.grid_world)
                learning = True
            elif event.key == pygame.K_c:
                game.clear()
                learning = False
                game.grid_world = None
            elif event.key == pygame.K_d:
                game.d_pressed = True
            elif event.key == pygame.K_s:
                learning = False
                stop_learn()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                game.d_pressed = False

    pygame.display.update()
    game.clock.tick(60)
