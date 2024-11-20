
import json
grid = [
    ['p', 0, 0, 0, 'b', 0, 0, 'p'],
    ['y', 0, 0, 0, 0, 0, 'o', 0],
    [0, 0, 'b', 0, 'g', 0, 'g', 0],
    [0, 0, 0, 0, 'l', 0, 'm', 0],
    [0, 'r', 0, 0, 'r', 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ['l', 'y', 0, 'o', 'm', 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

pairs = {
    'p': [(0,0),(0,7)],
    'b':[(0,4),(2,2)],
    'o':[(1,6),(7,3)],
    'g':[(2,4),(2,6)],
    'l':[(3,4),(6,0)],
    'm':[(3,6),(6,4)],
    'r':[(4,1),(4,3)],
    'y':[(0,0),(6,1)]
}

# sort paris keys accouding to distance
pairs = dict(sorted(pairs.items(), key=lambda x: abs(x[1][0][0] - x[1][1][0]) + abs(x[1][0][1] - x[1][1][1])))


initial_state = {color: [pairs[color][0]] for color in pairs}
overall_history = []

annotaions = {
    'p':1,
    'b':2,
    'o':3,
    'g':4,
    'l':5,
    'm':6,
    'r':7,
    'y':8

}

class FlowFreeGame:

    def __init__(self, grid, pairs):
        self.grid = grid
        self.pairs = pairs
        self.state = initial_state.copy()
        self.colors = list(self.pairs.keys())
        self.paths = {color: [pairs[color][0]] for color in self.colors}
        self.color_idx = 0
        self.current_color = self.colors[self.color_idx]
        self.done = False
        self.states_history = [] 
        self.solution_found = False

        

   

        

    def is_valid_move(self, position,color):
        x, y = position
        if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid[0]):
            return False
        elif self.grid[x][y] == color:
            return True
        elif self.grid[x][y] != 0 :
            return False
        return True


    def dfs(self, color_idx, current_position):
        if color_idx == len(self.colors):
            print("All colors connected successfully.")
            return True

        color = self.colors[color_idx]
        _, end = self.pairs[color]
        x, y = current_position

        if (x, y) == end:
            # print(f"Color {color} connected successfully.")
            return self.dfs(color_idx + 1, self.pairs[self.colors[color_idx + 1]][0] if color_idx + 1 < len(self.colors) else None)

        visited = set(self.paths[color])

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (x + dx, y + dy)

            if new_position in visited:
                continue
            if self.is_valid_move(new_position, color):
                self.grid[new_position[0]][new_position[1]] = color
                self.paths[color].append(new_position)
                if self.dfs(color_idx, new_position):
                    return True
                self.grid[new_position[0]][new_position[1]] = 0
                self.paths[color].pop()

        return False


    def draw_solution(self,grid, solution):
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
        print
            

    

    def solve(self):
        if self.dfs(0, self.pairs[self.colors[0]][0]):
            print("Solution found:")
            self.draw_solution(self.grid, self.paths)
        else:
            print("No solution exists.")


game = FlowFreeGame(grid, pairs)
game.solve()







    