import pygame


class Cell:

    def __init__(self, rect, color=(0, 0, 0)):

        self.color = color
        self.filled = False
        self.rect = rect

        font = pygame.font.SysFont("monospace", 15)
        self.label = font.render("", 1, (0, 0, 0))
