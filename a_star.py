import math
from grid import Grid
import pygame


class AStar:
    def __init__(self, x, y, z_scalar, cell_size, border, block_chance, path_weight, heuristic_weight):
        self.grid = Grid(x, y, z_scalar, cell_size, border)
        self.grid.block_cells_random(block_chance)
        self.path_weight = path_weight
        self.heuristic_weight = heuristic_weight

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
                self.trace_path(start_index, goal_index)
                self.grid.nodes[start_index].status = 3
                self.grid.nodes[goal_index].status = 4
                print(f'The length of the closed list is {len(closed_list)}')
                break
            open_list.remove(current_node)
            current_node.visited = True
            current_node.status = 1
            closed_list.append(current_node)
            for neighbour in current_node.neighbours:
                if not neighbour.visited and neighbour.accessible:
                    cost_to_neighbour = current_node.path_cost + self.path_weight
                    if cost_to_neighbour < neighbour.estimate:
                        neighbour.update_path_cost(cost_to_neighbour)
                        neighbour.parent = current_node
                    if neighbour not in open_list:
                        open_list.append(neighbour)

    def update_heuristics(self, end_node):
        for node in self.grid.nodes:
            node.update_heuristic(math.sqrt((node.x - end_node.x)**2 + (node.y - end_node.y)**2)*self.heuristic_weight)

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
        while current_node is not start_node:
            current_node.status = 2
            current_node = current_node.parent
