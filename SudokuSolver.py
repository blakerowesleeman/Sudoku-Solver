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
        if all(self.EliminateValue(values, square, d) for d in other_values):
            return values
        else:
            # elimination of digits resulted in contradiction
            return False
            
    def EliminateValue(self, values, square, digit):
        if d not in values[square]:
            return values
        # remove digit
        values[square] = values[square].replace(digit,'')
        if len(values[square]) == 0:
            return False # for contradiction
        elif len(values[square]) == 1:
            remaining_digit = values[square]
            if not all(self.EliminateValue(values, s, remaining_digit) for s in self.peers[square])
                return False # for contradiction somewhere in peers of square
        
        # check all units of square for existance of 1 digit and then Eliminate from peers
        for unit in self.units[square]:
            digitplaces = [sq for sq in unit if digit in self.values[sq]]
            if len(digitplaces) == 0:
                return False # for contradiction
            elif len(digitplaces) == 1:
                if not(self.AssignValue(values, digitplaces[0], digit)):
                    return False
        
        return values
    
