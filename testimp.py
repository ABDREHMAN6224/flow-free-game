from a import solve_flow_with_paths

grid_size = 10
grid = [[0] * grid_size for _ in range(grid_size)]
pairs = {
    1: [(1, 1), (1, 7)],
    2: [(2, 1), (8, 8)],
    3: [(1, 6), (5, 4)],
    4: [(3, 6), (8, 0)],
    5: [(3, 1), (5, 7)],
}

pairs =  {
    'yellow': [(2, 7), (3, 2)],
    'cyan': [(3, 1), (3, 8)],
    'orange': [(4, 1), (8, 3)],
    'green': [(4, 5), (8, 1)],
    'purple': [(4, 6), (6, 3)],
    'blue': [(4, 8), (8, 9)],
    'pink': [(5, 5), (6, 4)],
    'red': [(6, 2), (9, 9)],
    'mehroon': [(7, 9), (9, 1)]
}

pairs = {'a': [(1, 1), (5, 1)],
    'b': [(1, 2), (5, 6)],
    'c': [(2, 2), (3, 6)],
    'd': [(2, 3), (9, 0)],
    'e': [(5, 0), (6, 9)],
    'f': [(5, 3), (7, 5)],
    'g': [(6, 3), (7, 4)],
    'h': [(6, 6), (8, 8)],
    'i': [(6, 7), (9, 4)],
    'j': [(7, 1), (8, 6)],
    'k': [(7, 3), (8, 2)]
}

# Map colors to numbers
color_map = {color: idx + 1 for idx, color in enumerate(pairs.keys())}

# Place fixed start and end points in the grid
for color, positions in pairs.items():
    for x, y in positions:
        grid[x][y] = color_map[color]

print(grid, pairs, color_map, sep='\n\n')
solved = solve_flow_with_paths(grid, 10, pairs, color_map)
