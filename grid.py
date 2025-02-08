from nodes import Node
import pygame
import random


class Grid:
    def __init__(self, width, height, cell_size, border):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.border = border
        self.nodes = self.create_nodes()
        self.__determine_neighbours()
        self.screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))

    def __determine_neighbours(self):
        grid = {}
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for node in self.nodes:
            grid[node.x, node.y] = node
        for key in grid.keys():
            neighbours = []
            for direction in directions:
                x, y = key
                dx, dy = direction
                neighbour = grid.get((x + dx, y + dy), None)
                if neighbour is not None:
                    neighbours.append(neighbour)
            grid[key].neighbours = neighbours

    def create_nodes(self):
        nodes = []
        for i in range(self.height):
            for j in range(self.width):
                nodes.append(Node(i, j, True))
        return nodes

    def display(self):
        self.screen.fill((0, 0, 0))
        for node in self.nodes:
            x = node.x * self.cell_size + self.border
            y = node.y * self.cell_size + self.border
            width = self.cell_size - 2 * self.border
            height = self.cell_size - 2 * self.border
            if not node.accessible:
                pygame.draw.rect(self.screen, (100, 100, 100), (x, y, width, height))
            elif node.status == 0:
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, width, height))
            elif node.status == 1:
                pygame.draw.rect(self.screen, (255, 153, 0), (x, y, width, height))
            elif node.status == 2:
                pygame.draw.rect(self.screen, (0, 0, 255), (x, y, width, height))
            elif node.status == 3:
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, width, height))
            elif node.status == 4:
                pygame.draw.rect(self.screen, (255, 0, 0), (x, y, width, height))
        pygame.display.flip()

    def block_cells_random(self, chance):
        for node in self.nodes:
            if random.random() < chance:
                node.accessible = False
