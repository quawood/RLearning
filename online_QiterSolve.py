import pygame
import random
import numpy as np
from core import GridWorld as Gw
from game_environment.Game import Game
from game_environment.Agent import Agent

# value iteration
width = 3
height = 4
gamma = 1
rs = -0.01

# set up game
game = Game(width, height)
game.start()
learning = False
global countgood, countbad


def draw(canvas):
    canvas.fill((255, 255, 255))

    game.draw_cells(canvas)

    if game.agent is not None:
        pygame.draw.circle(canvas, (46, 155, 236), game.cells[game.agent.pos[0] - 1][game.agent.pos[1] - 1].rect.center,
                           10)


def test(epsilon, alpha, gamma, r):
    current_state = game.agent.pos

    rand = random.uniform(0, 1)

    if rand < epsilon:
        a = random.randint(0, len(game.grid_world.actions) - 1)
    else:
        q_actions = game.grid_world.qvalues[:, current_state[0], current_state[1]]
        a = np.argmax(q_actions)

    game.agent.move(game.grid_world.actions[a])
    reward = r
    exit = False
    if current_state in game.grid_world.good_p:
        reward = 1
        exit = True

    elif current_state in game.grid_world.bad_p:
        reward = -1
        exit = True

    sample = (current_state, a, reward, game.agent.pos)

    game.grid_world.update_qvalue(sample, gamma, alpha)

    if exit:
        game.agent.pos = (4, 2)

# update game

def learn(grid=None):
    alpha_creep = 0.01 * (int(game.runs) // int(1000))
    test(0.2 - alpha_creep, 0.1, 1, -0.1)
    game.runs += 1

while not game.stopped:
    draw(game.gameDisplay)

    if learning:
        learn(game.grid_world)
        game.runs += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(game.grid_world.qvalues)
            game.stopped = True

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
                game.new_grid(grid=None)
                learning = True
            elif event.key == pygame.K_c:
                game.clear()
                game.grid_world = None
                value_tests = 4
            elif event.key == pygame.K_d:
                game.d_pressed = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                game.d_pressed = False

    pygame.display.update()
    game.clock.tick(60)

