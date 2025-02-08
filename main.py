from a_star import AStar

if __name__ == '__main__':
    x, y = 50, 50
    algorithm = AStar(x, y, 10, 1, 0, 0.3, 0.4)
    algorithm.display()
