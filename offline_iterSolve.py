import pygame
from game_environment.Game import Game

# value iteration
width = 5
height = 5
gamma = 1
rs = -0.01
value_tests = 4

# set up game
game = Game(width, height)
game.start()


def draw(canvas):
    canvas.fill((255, 255, 255))

    game.draw_cells(canvas)


# policy iteration ----- offline MDP solving
def perform_alg(grid=None):
    game.new_grid(grid)

    game.grid_world.policy_iteration(gamma, rs, 1000, value_tests)
    state_values, policy = game.grid_world.values[1:height + 1, 1:width + 1], game.grid_world.policy

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

    return game.grid_world


# update game
while not game.stopped:
    draw(game.gameDisplay)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
                if game.runs == 0:
                    game.grid_world = perform_alg()
                else:
                    value_tests = 1
                    game.grid_world = perform_alg(game.grid_world)

                game.runs += 1
            elif event.key == pygame.K_c:
                game.clear()
                game.grid_world = None
                game.runs = 0
                value_tests = 4
            elif event.key == pygame.K_d:
                game.d_pressed = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                game.d_pressed = False

    pygame.display.update()
    game.clock.tick(60)
