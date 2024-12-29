from z3 import Solver, Int, If, And, Or, sat, Sum

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
    for r, c in positions:
        grid[r][c] = color_map[color]

    

# Solver function
def solve_flow_with_paths(grid, size, pairs, color_map):
    B = [[Int(f'B_{i}_{j}') for j in range(size)] for i in range(size)]
    solver = Solver()

    # Constraint 1: Each cell is either 0 or one of the color indices
    for i in range(size):
        for j in range(size):
            solver.add(Or(B[i][j] == 0, Or([B[i][j] == color_idx for color_idx in color_map.values()])))

    # Constraint 2: Fixed positions must have their assigned color
    for i in range(size):
        for j in range(size):
            if grid[i][j] != 0:
                solver.add(B[i][j] == grid[i][j])

    #  Constraint : Flow continuity for each color
    for i in range(size):
        for j in range(size):
            same_neighbours = Sum([If(B[i][j] == B[k][l], 1, 0)
                                      for k in range(size) for l in range(size) if
                                      abs(k - i) + abs(l - j) == 1])
            
             
            if grid[i][j] != 0:
                solver.add(Sum(same_neighbours) == 1)
            else:
                solver.add(Or(Sum(same_neighbours) == 2, B[i][j] == 0))   

            


    # Solve the constraints
    if solver.check() == sat:
        model = solver.model()
        solution = [[model[B[i][j]].as_long() for j in range(size)] for i in range(size)]
        return solution
    else:
        return None

def is_valid_move(matrix, visited, current_position, next_position,no):
    i, j = next_position
    # return 0 <= i < len(matrix) and 0 <= j < len(matrix[0]) and not visited[i][j] and matrix[i][j] == no
    if 0 <= i < len(matrix) and 0 <= j < len(matrix[0]):
        if not visited[i][j] and matrix[i][j] == no:
            return True
    
    return False

def dfs(matrix, visited, current_position, target_position, path, all_paths,no):
    i, j = current_position
    visited[i][j] = True
    path.append(current_position)
    if current_position == target_position:
        all_paths.append(path.copy())
    else:
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_position = (i + di, j + dj)
            if is_valid_move(matrix, visited, current_position, next_position,no):
                dfs(matrix, visited, next_position, target_position, path, all_paths,no)

    path.pop()
    visited[i][j] = False


def finalPath(no,matrix,coord,positionsonmap):

    num = sum(row.count(no) for row in matrix)
    M = len(matrix)
    N = len(matrix[0])

    visited = [[False for _ in range(N)] for _ in range(M)]
    path = []
    all_paths = []
    src = pairs[no][0]
    dest = pairs[no][1]
    dfs(matrix, visited, src, dest, path, all_paths,no)
    
    return all_paths

def buildPath(src, dest, colorIndex, grid):
    queue = [src]
    visited = set()
    parent = {}
    while queue:
        current = queue.pop(0)
        if current == dest:
            break
        i, j = current
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_position = (i + di, j + dj)
            if 0 <= next_position[0] < len(grid) and 0 <= next_position[1] < len(grid[0]) and grid[next_position[0]][next_position[1]] == colorIndex and next_position not in visited:
                queue.append(next_position)
                visited.add(next_position)
                parent[next_position] = current
    path = []
    current = dest
    while current != src:
        path.append(current)
        current = parent[current]
    path.append(src)
    path.reverse()
    return path

def findPaths(grid, pairs, color_map):
    ans = {}
    for color in pairs.keys():
        # p=finalPath(color,grid,"",pairs[color])
        # ans[color] = p
        src, dest = pairs[color]
        colorIndex = color_map[color]
        path = buildPath(src, dest, colorIndex, grid)
        ans[color] = path

    return ans


if __name__ == '__main__':
    solved_grid = solve_flow_with_paths(grid, grid_size, pairs, color_map)

    print(solved_grid)

    ans=findPaths(solved_grid, pairs, color_map)

    print(ans)

    for color, path in ans.items():
        for r, c in path:
            grid[r][c] = color

    def draw_solution(grid):
            """
            draws 2d grid with proper spacing to show paths of colors
            """
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 0:
                        print("  ", end="")
                    else:
                        print(f"{grid[i][j]} ", end="")
                print()
            print()

    draw_solution(grid)