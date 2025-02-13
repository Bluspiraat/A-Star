class Node:
    def __init__(self, x, y, accessible):
        self.x = x
        self.y = y
        self.accessible = accessible
        self.visited = False
        self.neighbours = []
        self.heuristic = 0
        self.path_cost = 10000
        self.estimate = self.heuristic + self.path_cost
        self.path_element = False
        self.status = 0  # 0 unexplored, 1 explored, 2 part of path, 3, start, 4 end
        self.parent = None

    def update_estimate(self):
        self.estimate = self.heuristic + self.path_cost

    def update_path_cost(self, cost):
        self.path_cost = cost
        self.estimate = self.heuristic + self.path_cost

    def update_heuristic(self, heuristic):
        self.heuristic = heuristic
        self.estimate = self.heuristic + self.path_cost
