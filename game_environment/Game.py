import pygame
from core.GridWorld import GridWorld
from game_environment.cell import Cell
from game_environment.Agent import Agent


class Game:

    def __init__(self, width, height):
        self.world_h = 300
        self.world_w = 400
        self.width = width
        self.height = height

        self.stopped = False
        self.d_pressed = False
        self.drag = False

        self.cells = []
        self.cell_color = (220, 220, 220)

        self.objects = []

        self.active = [0, 0, 0]

        self.gameDisplay = pygame.display.set_mode((self.world_w, self.world_h + 125))
        self.agent = None
        self.grid_world = None

        self.runs = 0

        pygame.init()

        self.font = pygame.font.SysFont("monospace", 5)
        self.clock = pygame.time.Clock()

    def start(self):

        cell_w = self.world_w / self.width
        cell_h = self.world_h / self.height

        self.font = pygame.font.Font("assets/Arrows.ttf", int(min([cell_w, cell_h])))
        pygame.display.set_caption('Grid world')

        wall_check = Cell(pygame.Rect(20, self.world_h + 10, 20, 20))
        good_check = Cell(pygame.Rect(20, self.world_h + 40, 20, 20), (119, 219, 41))
        bad_check = Cell(pygame.Rect(20, self.world_h + 70, 20, 20), (212, 58, 58))

        self.objects.append(wall_check)
        self.objects.append(good_check)
        self.objects.append(bad_check)

        for row in range(0, self.height):
            new_row = []
            for col in range(0, self.width):
                g_cell = Cell(pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h), self.cell_color)
                g_cell.filled = False
                new_row.append(g_cell)

            self.cells.append(new_row)

    def draw_cells(self, canvas):
        for i in range(0, len(self.cells)):
            for j in range(0, len(self.cells[i])):
                current_cell = self.cells[i][j]

                if current_cell.filled:
                    pygame.draw.rect(canvas, current_cell.color, current_cell.rect)
                else:
                    pygame.draw.rect(canvas, self.cell_color, current_cell.rect, 1)

                canvas.blit(current_cell.label, (current_cell.rect.left, current_cell.rect.top))

        for ob in range(0, len(self.objects)):
            if self.objects[ob].filled and self.active[ob] == 1:
                pygame.draw.rect(canvas, self.objects[ob].color, self.objects[ob].rect)
            else:
                pygame.draw.rect(canvas, self.objects[ob].color, self.objects[ob].rect, 1)

    def clear(self):
        for i in range(0, len(self.cells)):
            for j in range(0, len(self.cells[i])):
                current_cell = self.cells[i][j]

                current_cell.color = self.cell_color
                current_cell.label = self.font.render("", 1, (0, 0, 0))
                current_cell.filled = False

    def check(self, rect_pos):
        a = self.active.copy()

        for o in range(0, len(self.objects)):
            if self.objects[o].rect.contains(rect_pos):
                a = [0, 0, 0]
                a[o] = 1
                self.objects[o].filled = True

        if 1 in self.active:
            for i in range(0, len(self.cells)):
                for j in range(0, len(self.cells[i])):
                    if self.cells[i][j].rect.contains(rect_pos):
                        if self.d_pressed:
                            self.cells[i][j].color = self.cell_color
                            self.cells[i][j].filled = False
                        else:
                            self.cells[i][j].color = (self.objects[self.active.index(1)]).color
                            self.cells[i][j].filled = True
                        return

        self.active = a

    def new_grid(self, grid=None):
        wall_pos = []
        good_pos = []
        bad_pos = []

        for i in range(0, len(self.cells)):
            for j in range(0, len(self.cells[i])):
                if self.cells[i][j].color == (0, 0, 0):
                    wall_pos.append((i, j))
                elif self.cells[i][j].color == (119, 219, 41):
                    good_pos.append((i, j))
                elif self.cells[i][j].color == (212, 58, 58):
                    bad_pos.append((i, j))

        # create a grid world
        self.grid_world = GridWorld(self.height, self.width, good_pos, bad_pos, wall_pos)
        self.agent = Agent(self.grid_world)


        if grid is not None:
            self.grid_world.values = grid.values
            self.grid_world.policy = grid.policy
            self.grid_world.qvalues = grid.qvalues
            self.agent = Agent(grid)

