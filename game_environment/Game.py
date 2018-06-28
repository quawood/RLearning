import pygame

from game_environment.cell import Cell


class Game:

    def __init__(self, width, height):
        self.world_h = 500
        self.world_w = 500
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

        self.runs = 0

        self.pygame = pygame
        self.pygame.init()

        self.font = self.pygame.font.SysFont("monospace", 5)
        self.clock = self.pygame.time.Clock()

    def start(self):

        cell_w = self.world_w / self.width
        cell_h = self.world_h / self.height

        self.font = self.pygame.font.Font("assets/Arrows.ttf", int(min([cell_w, cell_h])))
        self.pygame.display.set_caption('Grid world')

        wall_check = Cell(self.pygame.Rect(20, self.world_h + 10, 20, 20))
        good_check = Cell(self.pygame.Rect(20, self.world_h + 40, 20, 20), (119, 219, 41))
        bad_check = Cell(self.pygame.Rect(20, self.world_h + 70, 20, 20), (212, 58, 58))

        self.objects.append(wall_check)
        self.objects.append(good_check)
        self.objects.append(bad_check)

        for row in range(0, self.height):
            new_row = []
            for col in range(0, self.width):
                g_cell = Cell(self.pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h), self.cell_color)
                g_cell.filled = False
                new_row.append(g_cell)

            self.cells.append(new_row)

    def draw_cells(self, canvas):
        for i in range(0, len(self.cells)):
            for j in range(0, len(self.cells[i])):
                current_cell = self.cells[i][j]

                if current_cell.filled:
                    self.pygame.draw.rect(canvas, current_cell.color, current_cell.rect)
                else:
                    self.pygame.draw.rect(canvas, self.cell_color, current_cell.rect, 1)

                canvas.blit(current_cell.label, (current_cell.rect.left, current_cell.rect.top))

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
