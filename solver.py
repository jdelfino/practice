def solve(board):
    made_progress = True
    while(made_progress):
        made_progress = False
        for cell in board.cells():
            for strat in [identity, exclusion, pointer, exclusive_tuples]:
                if strat(board, cell):
                    made_progress = True
        
def identity(board, cell):
    if len(cell.possibles) == 1:
        board.setnum(next(iter(cell.possibles)), cell)
        return True
    
def exclusion(board, cell):
    for p in cell.possibles:
        for unit in [board.row(cell.row), board.col(cell.col), board.box(cell.box)]:
            if not any((x != cell and p in x.possibles) for x in unit):
                board.setnum(p, cell)
                return True

def exclusive_tuples(board, cell):
    rval = False
    
    identical_row = [x for x in board.row(cell.row) if x.possibles == cell.possibles]
    if len(identical_row) == len(cell.possibles):
        #exclusive, remove these from the rest of the row
        for r in board.row(cell.row):
            if r not in identical_row:
                r.possibles -= cell.possibles
                rval = True
                
    identical_col = [x for x in board.col(cell.col) if x.possibles == cell.possibles]
    if len(identical_col) == len(cell.possibles):
        #exclusive, remove these from the rest of the col
        for r in board.col(cell.col):
            if r not in identical_col:
                r.possibles -= cell.possibles
                rval = True
                
    identical_box = [x for x in board.box(cell.box) if x.possibles == cell.possibles]
    if len(identical_box) == len(cell.possibles):
        #exclusive, remove these from the rest of the box
        for r in board.box(cell.box):
            if r not in identical_box:
                r.possibles -= cell.possibles
                rval = True

    return rval

def pointer(board, cell):
    rval = False
    box = list(board.box(cell.box))

    for candidate in cell.possibles:
        cando = [x for x in box if candidate in x.possibles]

        if len(set(x.row for x in cando)) == 1:
            row_to_clear = cando[0].row
            rest = [x for x in board.row(row_to_clear) if candidate in x.possibles]
            for r in rest:
                if r.row == row_to_clear and r.box != cell.box:
                    r.possibles.discard(candidate)
                    rval = True

        if len(set(x.col for x in cando)) == 1:
            col_to_clear = cando[0].col
            rest = [x for x in board.col(col_to_clear) if candidate in x.possibles]
            for r in rest:
                if r.col == col_to_clear and r.box != cell.box:
                    r.possibles.discard(candidate)
                    rval = True

    return rval

def bootstrap_possibles(board, cell):
    if board[cell.row][cell.col].num:
        return set([board[cell.row][cell.col].num])
    row_poss = set(x.num for x in board.row(cell.row))
    col_poss = set(x.num for x in board.col(cell.col))
    box_poss = set(x.num for x in board.box(cell.box))
    return set(range(1,10)) - row_poss - col_poss - box_poss        

class Cell:
    def __init__(self, row_, col_, num=None, possibles=None):
        self.row = row_
        self.col = col_
        self.box = (row_ / 3) * 3 + (col_ / 3)
        self.num = num
        self.possibles = set(possibles) if possibles else set(range(1,10))

    def __str__(self):
        return "(" + str(self.row) + "," + str(self.col) + "," + str(self.box) + ") " + str(self.num) + " [" + str(list(self.possibles)) + "]"
    
class Board:
    def __init__(self, board=None):
        if not board:
            self._board = set(Cell(j, i) for i in range(9) for j in range(9))
        else:
            self._board = set(Cell(j, i, board[j][i]) for i in range(9) for j in range(9))

        for row in self.rows():
            for cell in row:
                cell.possibles = bootstrap_possibles(self, cell)

    def setnum(self, num, cell):
        cell.num = num
        cell.possibles = set()
        self.clear_possibles(cell)

    def cells(self):
        for r in self.rows():
            for c in sorted(r, key=lambda x:x.col):
                yield c

    def cell(self, rownum, colnum):
        return self._board[rownum][colnum]

    def row(self, num):
        return (x for x in self._board if x.row == num)

    def rows(self):
        return (self.row(x) for x in range(9))
    
    def col(self, num):
        return (x for x in self._board if x.col == num)
    
    def box(self, boxnum):
        return (x for x in self._board if x.box == boxnum)
    
    def _do_for_all_units(self, fun, cell):
        for r in self.row(cell.row):
            fun(r)
        for c in self.col(cell.col):
            fun(c)
        for b in self.box(cell.box):
            fun(b)

    def clear_possibles(self, cell):
        self._do_for_all_units(lambda x: x.possibles.discard(cell.num), cell)
    
    def __getitem__(self, index):
        # ahh performance
        return sorted(self.row(index), key=lambda x:x.col)

def print_board(board):
    for c in board.cells():
        if c.col == 0 and c.row % 3 == 0:
            print '-' * 25
        if c.col % 3 == 0:
            print("|"),
        print(c.num or '_'),
        if c.col == 8:
            print "|"
    print '-' * 25

def easy_board():
    return [[6,    None, None, 1,    None, 8,    2,    None, 3   ],
            [None, 2,    None, None, 4,    None, None, 9,    None],
            [8,    None, 3,    None, None, 5,    4,    None, None],
            [5,    None, 4,    6,    None, 7,    None, None, 9   ],
            [None, 3,    None, None, None, None, None, 5,    None],
            [7,    None, None, 8,    None, 3,    1,    None, 2   ],
            [None, None, 1,    7,    None, None, 9,    None, 6   ],
            [None, 8,    None, None, 3,    None, None, 2,    None],
            [3,    None, 2,    9,    None, 4,    None, None, 5   ]]

def hard_board():
    return [[None, 6, 5, None, 3, None, 2, None, None],
            [2, None, 4, None, None, None, None, None, 3],
            [None, None, None, None, None, None, None, 1, None],
            [None, None, 1, 7, 5, None, None, None, None],
            [8, None, None, None, None, None, None, None, 1],
            [None, None, None, None, 4, 9, 7, None, None],
            [None, 8, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, 8, None, 6],
            [None, None, 9, None, 1, None, 5, 7, None]]

def medium_board():
    return [[None, None, 6, 2, 4, None, None, 3, None],
            [None, 3, None, None, None, None, None, 9, None],
            [2, None, None, None, None, None, None, 7, None],
            [5, None, None, 8, None, None, None, 2, None],
            [None, None, 1, None, None, None, 6, None, None],
            [None, 2, None, None, None, 3, None, None, 7],
            [None, 5, None, None, None, None, None, None, 3],
            [None, 9, None, None, None, None, None, 8, None],
            [None, 1, None, None, 6, 2, 5, None, None]]
            
def main():
    #b = Board(hard_board())
    #b = Board(easy_board())
    b = Board(medium_board())
    print_board(b)
    solve(b)
    print_board(b)
    
if __name__ == '__main__':
    main()
    
