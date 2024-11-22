from z3 import Solver, Int, If, And, Or, sat, Sum

grid_size = 9
grid = [[0] * grid_size for _ in range(grid_size)]
pairs = {
    1: [(1, 1), (1, 7)],
    2: [(2, 1), (8, 8)],
    3: [(1, 6), (5, 4)],
    4: [(3, 6), (8, 0)],
    5: [(3, 1), (5, 7)],
}

# Map colors to numbers
color_map = {color: idx + 1 for idx, color in enumerate(pairs.keys())}

# Place fixed start and end points in the grid
for color, positions in pairs.items():
    for x, y in positions:
        grid[x][y] = color_map[color]

    

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

def findPaths(grid, pairs, color_map):
    ans = {}
    for color in pairs.keys():
        p=finalPath(color,grid,"",pairs[color])
        ans[color] = p

    return ans

solved_grid = solve_flow_with_paths(grid, grid_size, pairs, color_map)

ans=findPaths(solved_grid, pairs, color_map)


for color, paths in ans.items():
    path=paths[0]
    for x, y in path:
        grid[x][y] = color_map[color]

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