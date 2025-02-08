import math
import numpy as np
from grid import Grid
import pygame
import matplotlib.pyplot as plt


class AStar:
    def __init__(self, x, y, z_scalar, cell_size, border, block_chance, path_weight, vertical_weight, heuristic_weight):
        self.grid = Grid(x, y, z_scalar, cell_size, border)
        self.grid.block_cells_random(block_chance)
        self.path_weight = path_weight
        self.vertical_weight = vertical_weight
        self.heuristic_weight = heuristic_weight
        self.path = None

    def display(self):
        running = True
        while running:
            self.grid.display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    def find_path(self, start_index, goal_index):
        self.initial_conditions(start_index, goal_index)
        goal = self.grid.nodes[goal_index]
        open_list = [self.grid.nodes[start_index]]
        closed_list = []
        while len(open_list) > 0:
            current_node = sorted(open_list, key=lambda node: node.estimate)[0]
            if current_node == goal:
                path_length = self.trace_path(start_index, goal_index)
                self.grid.nodes[start_index].status = 3
                self.grid.nodes[goal_index].status = 4
                print(
                    f'Total nodes = {self.grid.width * self.grid.height}, the path length is {path_length} and the explored number of nodes is {len(closed_list)}')
                break
            open_list.remove(current_node)
            current_node.visited = True
            current_node.status = 1
            closed_list.append(current_node)
            for neighbour in current_node.neighbours:
                if not neighbour.visited and neighbour.accessible:
                    cost_to_neighbour = current_node.path_cost + self.__euclidean_distance(current_node,
                                                                                           neighbour) * self.path_weight
                    if cost_to_neighbour < neighbour.estimate:
                        neighbour.update_path_cost(cost_to_neighbour)
                        neighbour.parent = current_node
                    if neighbour not in open_list:
                        open_list.append(neighbour)

    def update_heuristics(self, end_node):
        for node in self.grid.nodes:
            node.update_heuristic(self.__euclidean_distance(node, end_node) * self.heuristic_weight)

    def __euclidean_distance(self, start, end):
        return math.sqrt(
            (start.x - end.x) ** 2 + (start.y - end.y) ** 2 + (start.z - end.z) ** 2 * self.vertical_weight)

    def initial_conditions(self, start, goal):
        start_node = self.grid.nodes[start]
        start_node.accessible = True
        start_node.update_path_cost(0)
        goal_node = self.grid.nodes[goal]
        goal_node.accessible = True
        self.update_heuristics(goal_node)

    def trace_path(self, start_index, goal_index):
        current_node = self.grid.nodes[goal_index]
        start_node = self.grid.nodes[start_index]
        path = []
        while current_node is not start_node:
            current_node.status = 2
            current_node = current_node.parent
            path.append(current_node)
        path.append(start_node)
        self.path = path
        return len(path)

    def get_height_map(self):
        return [node.z for node in reversed(self.path)]

    def plot_elevation(self):
        plt.figure(figsize=(18, 6))
        plt.plot(self.get_height_map())
        plt.title(f'Std of data is {np.std(self.get_height_map())} and the total elevation is {sum(self.get_height_map())}')
        plt.savefig('Height_map.png')
