from a_star import AStar

if __name__ == '__main__':
    x, y = 50, 50
    z_scalar = 0.1
    algorithm = AStar(x, y, z_scalar, 10, 1, 0, 0.3, 0.4)
    algorithm.display()
