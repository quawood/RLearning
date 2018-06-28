import pygame
from core import GridWorld as Gw
from game_environment.Game import Game

# value iteration
width = 10
height = 10
gamma = 1
rs = -0.01
value_tests = 4

# set up game
game = Game(width, height)
game.start()


# create a bunch of cells of the grid world
def draw(canvas):
    canvas.fill((255, 255, 255))

    game.draw_cells(canvas)

    for ob in range(0, len(game.objects)):
        if game.objects[ob].filled and game.active[ob] == 1:
            pygame.draw.rect(canvas, game.objects[ob].color, game.objects[ob].rect)
        else:
            pygame.draw.rect(canvas, game.objects[ob].color, game.objects[ob].rect, 1)


# policy iteration ----- offline MDP solving
def perform_alg(grid=None):
    wall_pos = []
    good_pos = []
    bad_pos = []

    for i in range(0, len(game.cells)):
        for j in range(0, len(game.cells[i])):
            if game.cells[i][j].color == (0, 0, 0):
                wall_pos.append((i, j))
            elif game.cells[i][j].color == (119, 219, 41):
                good_pos.append((i, j))
            elif game.cells[i][j].color == (212, 58, 58):
                bad_pos.append((i, j))

    # create a grid world
    grid_world = Gw.GridWorld(height, width, good_pos, bad_pos, wall_pos)

    # if a change is made in environment, give the values and policies to new state to speed up comp.
    if grid is not None:
        grid_world.values = grid.values
        grid_world.policy = grid.policy

    grid_world.policy_iteration(gamma, rs, 1000, value_tests)
    state_values, policy = grid_world.values[1:height + 1, 1:width + 1], grid_world.policy

    for i in range(0, len(game.cells)):
        for j in range(0, len(game.cells[i])):
            direct = policy[i, j]
            char_to_add = ""
            print()
            if grid_world.is_wall(i + 1, j + 1):
                char_to_add = ""
            elif state_values[i, j] == 1 and grid_world.is_exit(i, j):
                char_to_add = ""
            elif state_values[i, j] == -1 and grid_world.is_exit(i, j):
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


    return grid_world


# update game
while not game.stopped:
    draw(game.gameDisplay)

    for event in game.pygame.event.get():
        if event.type == game.pygame.QUIT:
            stopped = True

        elif event.type == game.pygame.MOUSEBUTTONDOWN:
            pos = game.pygame.mouse.get_pos()
            r_pos = (pos[0], pos[1], 1, 1)
            game.drag = True
            game.check(r_pos)

        elif event.type == game.pygame.MOUSEBUTTONUP:
            game.drag = False

        elif event.type == game.pygame.MOUSEMOTION:
            if game.drag:
                pos = event.pos
                r_pos = (pos[0], pos[1], 1, 1)
                game.check(r_pos)

        elif event.type == game.pygame.KEYDOWN:
            if event.key == game.pygame.K_RETURN:
                if game.runs == 0:
                    grid_w = perform_alg()
                else:
                    value_tests = 1
                    grid_w = perform_alg(grid_w)

                game.runs += 1
            elif event.key == game.pygame.K_c:
                game.clear()
                grid_w = None
                value_tests = 4
            elif event.key == game.pygame.K_d:
                d_pressed = True

        elif event.type == game.pygame.KEYUP:
            if event.key == game.pygame.K_d:
                d_pressed = False

    game.pygame.display.update()
    game.clock.tick(60)
