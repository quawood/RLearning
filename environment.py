import GridWorld as Gw
import pygame
import cell


# value iteration
width = 15
height = 15


def perform_alg():
    wall_pos = []
    good_pos = []
    bad_pos = []

    for i in range(0, len(cells)):
        for j in range(0, len(cells[i])):
            if cells[i][j].color == (0, 0, 0):
                wall_pos.append((i, j))
            elif cells[i][j].color == (119, 219, 41):
                good_pos.append((i, j))
            elif cells[i][j].color == (212, 58, 58):
                bad_pos.append((i, j))

    # create a grid world
    grid_world = Gw.GridWorld(height, width, good_pos, bad_pos, wall_pos)
    grid_world.policy_iteration(1, -0.01, 100, 5)
    state_values, policy = grid_world.values[1:height + 1, 1:width + 1], grid_world.policy

    for i in range(0, len(cells)):
        for j in range(0, len(cells[i])):
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

            cells[i][j].label = font.render(char_to_add, 1, (0, 0, 0))


pygame.init()


world_w = 400
world_h = 400
cell_w = world_w/width
cell_h = world_h/height

font = pygame.font.Font("Arrows.ttf", int(min([cell_w, cell_h])))

gameDisplay = pygame.display.set_mode((world_w, world_h + 125))
pygame.display.set_caption('Grid world')
clock = pygame.time.Clock()

stopped = False

active = [0, 0, 0]

objects = []

wall_check = cell.Spot(pygame.Rect(20, world_h + 10, 20, 20))
good_check = cell.Spot(pygame.Rect(20, world_h + 40, 20, 20), (119, 219, 41))
bad_check = cell.Spot(pygame.Rect(20, world_h + 70, 20, 20), (212, 58, 58))
cells = []
cell_color = (220,220,220)
objects.append(wall_check)
objects.append(good_check)
objects.append(bad_check)

# create a bunch of cells of the grid world
for row in range(0, height):
    new_row = []
    for col in range(0, width):
        g_cell = cell.Spot(pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h), cell_color)
        g_cell.filled = False
        new_row.append(g_cell)

    cells.append(new_row)


def draw(canvas, act, objs, clls):
    a = act
    canvas.fill((255, 255, 255))
    count = 0
    for i in range(0, len(clls)):
        for j in range(0, len(clls[i])):
            current_cell = clls[i][j]

            if current_cell.filled:
                pygame.draw.rect(canvas, current_cell.color, current_cell.rect)
            else:
                pygame.draw.rect(canvas, cell_color, current_cell.rect, 1)

            canvas.blit(current_cell.label, (current_cell.rect.left, current_cell.rect.top))
            count += 1

    for ob in range(0, len(objs)):
        if objs[ob].filled and a[ob] == 1:
            pygame.draw.rect(canvas, objs[ob].color, objs[ob].rect)
        else:
            pygame.draw.rect(canvas, objs[ob].color, objs[ob].rect, 1)


while not stopped:
    draw(gameDisplay, active, objects, cells)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopped = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rect_pos = (pos[0], pos[1], 1, 1)

            def check(act):
                a = act

                for o in range(0, len(objects)):
                    if objects[o].rect.contains(rect_pos):
                        a = [0, 0, 0]
                        a[o] = 1
                        objects[o].filled = True
                        return a
                if 1 in act:
                    for i in range(0, len(cells)):
                        for j in range(0, len(cells[i])):

                            if cells[i][j].rect.contains(rect_pos):
                                if event.button == 1:
                                    cells[i][j].color = objects[act.index(1)].color
                                    cells[i][j].filled = True
                                elif event.button == 3:
                                    cells[i][j].color = cell_color
                                    cells[i][j].filled = False

                                return a
                return a
            active = check(active)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                perform_alg()

    pygame.display.update()
    clock.tick(60)
