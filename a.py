
import json
grid = [
    ['p', 0, 0, 0, 'b', 0, 0,'p'],
    ['y',0, 0, 0, 0, 0, 'o', 0],
    [0, 0, 'b', 0, 'g', 0, 'g',0],
    [0, 0, 0, 0, 'l', 0, 'm',0],
    [0, 'r', 0, 0, 'r', 0, 0,0],
    ['l', 'y', 0, 'o', 'm', 0, 0,0],
    [0,0, 0, 0, 0, 0, 0, 0],
]

pairs = {
    'p': [(0,1),(0,7)],
    'b':[(0,4),(2,2)],
    'o':[(1,6),(5,3)],
    'g':[(2,4),(2,6)],
    'l':[(3,4),(5,3)],
    'm':[(3,6),(5,4)],
    'r':[(4,1),(4,4)],
    'y':[(5,0),(5,1)]

    
}

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
        self.color_idx = 0
        self.current_color = self.colors[self.color_idx]
        self.done = False
        self.states_history = [] 

        

   

        

    def is_valid_move(self, position):
        x, y = position
        if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid[0]):
            return False
        if self.grid[x][y] != 0:
            return False
        return True


    def dfs(self, current_position):
        if self.done:
            reslt = self.state.copy()
            print(reslt)
            print("Done")
            return

        if self.color_idx == len(self.colors):
            print("All colors done")
            self.done = True
            return

        if current_position == self.pairs[self.current_color][1]:
            print(f"Done with {current_position}, target: {self.pairs[self.current_color][1]}, __________")
            self.color_idx += 1
           
            if self.color_idx == len(self.colors):
                self.done = True
                return

            self.current_color = self.colors[self.color_idx]
            self.dfs(self.pairs[self.current_color][0])
            return
        # print(f"Done with {current_position}, target: {self.pairs[self.current_color][1]}")

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (current_position[0] + dx, current_position[1] + dy)
            if new_position == self.pairs[self.current_color][1]:
                print(f"Found target {new_position}")
                self.state[self.current_color].append(new_position)
                self.states_history.append(self.state.copy())
                overall_history.append(json.loads(json.dumps(self.state)))
                self.dfs(new_position)

            elif self.is_valid_move(new_position):
                self.grid[new_position[0]][new_position[1]] = self.current_color
                if not self.done:
                    self.state[self.current_color].append(new_position)
                    self.states_history.append(self.state.copy())
                    overall_history.append(json.loads(json.dumps(self.state)))
                self.dfs(new_position)
                self.grid[new_position[0]][new_position[1]] = 0
                if not self.done:
                    if len(self.state[self.current_color]) > 0:
                        self.state[self.current_color].pop()


    def drawSolution(self, state):
        # print 2d matrix with solution
        for color in state:
            for position in state[color]:
                x, y = position
                self.grid[x][y] = color
        for row in self.grid:
            print(row)
        print("\n\n\n")
        

    

    def solve(self):
        self.dfs(self.pairs[self.current_color][0])
        self.drawSolution(self.state)
        return self.state

game = FlowFreeGame(grid, pairs)
game.solve()

# with open('output.txt', 'w') as f:
#     for state in overall_history:
#         f.write(str(state))
#         f.write('\n')






    