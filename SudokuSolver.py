class SudokuGrid()

    digits = '123456789'
    cols = 'ABCDEFGHI'
    rows = '123456789'
  
    def __init__(self, grid):
        self.grid = grid
        self.squares = [c + r for c in self.cols for r in self.rows]
        self.unitlist = [[self.MakeGrid(self.cols, row) for row in self.rows] + 
                         [self.MakeGrid(col, self.rows) for col in self.cols] + 
                         [self.MakeGrid(c, r) for c in ('ABC','DEF','GHI') for r in ('123','456','789')]]
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)
        self.peers = dict(s, set(sum(self.units[s],[])) - set([s])) for s in self.squares)
                         
    def MakeGrid(self,column,row):
        return [c + r for c in column for r in row]
        
