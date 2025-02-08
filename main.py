from a_star import AStar

if __name__ == '__main__':
    x, y = 80, 80
    algorithm = AStar(x, y, 10, 1, 0.2, 0.3, 0.4)
    algorithm.find_path(0, x*y-1)
    algorithm.display()
