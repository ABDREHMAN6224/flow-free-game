import numpy as np
import json
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0,0],
    [0, 0, 0, 0, 0, 0, 0, 0,0],
    [0, 0, 0, 0, 0, 0, 0, 0,0],
    [0, 0, 0, 0, 0, 0, 0, 0,0],
    [0, 0, 0, 0, 0, 0, 0, 0,0],
    [0, 0, 0, 0, 0, 0, 0, 0,0],
    [0, 0, 0, 0, 0, 0, 0, 0,0],
    [0, 0, 0, 0, 0, 0, 0, 0,0],
    [0, 0, 0, 0, 0, 0, 0, 0,0],
]

pairs = {
    'b': [(0, 7), (6,5)],
    'r': [(0, 8), (4,3)],
    'g': [(1, 7), (5,3)],
    'y': [(0, 0), (6,6)],
    'o': [(4,5), (7,1)],

}

# sort paris keys accouding to distance
pairs = dict(sorted(pairs.items(), key=lambda x: abs(x[1][0][0] - x[1][1][0]) + abs(x[1][0][1] - x[1][1][1])))


initial_state = {color: [pairs[color][0]] for color in pairs}
overall_history = []

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

        # print(self.paths[color])

        
        visited = set(self.paths[color])
        new_positions = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]]) + np.array([x, y])
        new_positions_list = new_positions.tolist()
        new_positions = sorted(new_positions_list, key=lambda x: abs(x[0] - end[0]) + abs(x[1] - end[1]))



        for new_position in new_positions:
            new_position = tuple(new_position)
            if new_position in visited:
                continue
            if self.is_valid_move(new_position, color):
                self.grid[new_position[0]][new_position[1]] = color
                self.paths[color].append(new_position)
                # visited.add(new_position)
                if self.dfs(color_idx, new_position):
                    return True
                self.grid[new_position[0]][new_position[1]] = 0
                self.paths[color].pop()
                # visited.remove(new_position)

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
        for color in self.pairs:
            start, end = self.pairs[color]
            self.grid[start[0]][start[1]] = color
            self.grid[end[0]][end[1]] = color


        if self.dfs(0, self.pairs[self.colors[0]][0]):
            print("Solution found:")
            self.draw_solution(self.grid, self.paths)
        else:
            print("No solution exists.")


game = FlowFreeGame(grid, pairs)
game.solve()







    