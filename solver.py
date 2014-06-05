def solve(board):
    made_progress = True
    while(made_progress):
        made_progress = False
        for cell in board.cells():
            print cell
            if len(cell.possibles) == 1:
                board.setnum(next(iter(cell.possibles)), cell)
                made_progress = True
            else:
                for p in cell.possibles:
                    if _check(board, cell, p):
                        made_progress = True
                        break

def _check(board, cell, poss):
    for unit in [board.row(cell.row), board.col(cell.col), board.box(cell.row, cell.col)]:
        if not any((x != cell and poss in x.possibles) for x in unit):
            board.setnum(poss, cell)
            return True
        
def identity(self, board, cell):
    if len(cell.possibles) == 1:
        return cell.num

def bootstrap_possibles(board, row, col):
    if board[row][col].num:
        return set([board[row][col].num])
    row_poss = set(x.num for x in board.row(row))
    col_poss = set(x.num for x in board.col(col))
    box_poss = set(x.num for x in board.box(row, col))
    return set(range(1,10)) - row_poss - col_poss - box_poss        

def boxnum(rownum, colnum):
    return (rownum / 3) * 3 + (colnum / 3)

class Cell:
    def __init__(self, row_, col_, num=None, possibles=None):
        self.row = row_
        self.col = col_
        self.box = boxnum(row_, col_)
        self.num = num
        self.possibles = set(possibles) if possibles else set(range(1,10))

    def __str__(self):
        return "(" + str(self.row) + "," + str(self.col) + ") " + str(self.num) + " [" + str(list(self.possibles)) + "]"
    
class Board:
    def __init__(self, board=None):
        if not board:
            self._board = set(Cell(j, i) for i in range(9) for j in range(9))
        else:
            self._board = set(Cell(j, i, board[j][i]) for i in range(9) for j in range(9))

        for row in self.rows():
            for cell in row:
                cell.possibles = bootstrap_possibles(self, cell.row, cell.col)

    def setnum(self, num, cell):
        print "SETNUM", cell
        cell.num = num
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
    
    def box(self, rownum, colnum):
        return (x for x in self._board if x.box == boxnum(rownum, colnum))
    
    def _do_for_all_units(self, fun, rownum, colnum):
        for r in self.row(rownum):
            fun(r)
        for c in self.col(colnum):
            fun(c)
        for b in self.box(rownum, colnum):
            fun(b)

    def clear_possibles(self, cell):
        self._do_for_all_units(lambda x: x.possibles.discard(cell.num), cell.row, cell.col)
    
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
            
def main():
    b = Board(hard_board())
    print_board(b)
    solve(b)
    print_board(b)
    
if __name__ == '__main__':
    main()
    
