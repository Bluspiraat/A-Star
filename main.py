from a_star import AStar

if __name__ == '__main__':
    x, y = 80, 160
    z_scalar = 0.2
    algorithm = AStar(x, y, z_scalar, 10, 1, 0, 0.3, 100000, 0.3)
    algorithm.find_path(0, x*y-1)
    algorithm.plot_elevation()
    algorithm.display()
