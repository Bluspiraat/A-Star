import colorsys

import opensimplex

from nodes import Node
import pygame
import random
from opensimplex import OpenSimplex


class Grid:
    def __init__(self, width, height, z_scalar, cell_size, border):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.border = border
        self.nodes = self.create_nodes()
        self.__determine_neighbours()
        self.__determine_z(z_scalar)
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

    def __determine_z(self, scalar):
        noise = OpenSimplex(43)
        grid = {}
        for node in self.nodes:
            grid[node.x, node.y] = node
        for key in grid.keys():
            x, y = key
            grid[key].z = (noise.noise2(x * scalar, y * scalar) + 1) * 128  # Map from [-1, 1] to [0, 255]

    def create_nodes(self):
        nodes = []
        for i in range(self.height):
            for j in range(self.width):
                nodes.append(Node(i, j, 0, True))
        return nodes

    def display(self):
        self.screen.fill((0, 0, 0))
        for node in self.nodes:
            x = node.x * self.cell_size + self.border
            y = node.y * self.cell_size + self.border
            width = self.cell_size - 2 * self.border
            height = self.cell_size - 2 * self.border
            color = pygame.Color(0)
            color.hsva = (node.z/2, 100, 100, 100)
            pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.display.flip()

    def block_cells_random(self, chance):
        for node in self.nodes:
            if random.random() < chance:
                node.accessible = False
