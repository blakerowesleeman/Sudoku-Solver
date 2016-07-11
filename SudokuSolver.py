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
        self.peers = dict((s, set(sum(self.units[s],[])) - set([s])) for s in self.squares)
        self.values = {}
                         
    def MakeGrid(self, column, row):
        return [c + r for c in column for r in row]
        
    def ParseGrid(self, grid):
        # Convert grid to dictionary of Squares: Possible Values '1249'
        # Return False if possible values is empty
        self.values = dict((square, self.digits) for square in self.squares)
        for square, digit in self.GridValues(grid).items():
            if digit in self.digits and not AssignValue(self.values, square, digit):
                # Contradition due to false AssignValue result
                return False
        return self.values
    
    def GridValues(self, grid):
        # Return dictionary of Squares: Original Value
        places = [g for g in grid if g in self.digits or g in '0.1']
        assert len(places) == 81
        return dict(zip(self.squares, places))
        
    def AssignValue(self, values, square, digit):
        # other_values stores remaining digits for position = square
        other_values = values[square].replace(digit,'')
        if all(EliminateValue(values, square, digits) for digits in other_values):
            return values
        else:
            # elimination of digits resulted in contradiction
            return False
