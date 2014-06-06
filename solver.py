import copy
import time
import argparse

class Unsolvable(Exception):
    def __str__(self):
        return "UnsolvableException"
    
class Mistake(Exception):
    def __init__(self, unit):
        super(Mistake, self).__init__()
        self.unit = unit
    def __str__(self):
        return "MistakeException\n" + '\n'.join([str(x) for x in self.unit])
    
def only_choice(board, cell):
    if len(cell.possibles) == 1:
        board.setnum(next(iter(cell.possibles)), cell)
        return True
    
def single_possibility(board, cell):
    for p in cell.possibles:
        for unit in [board.row(cell.row), board.col(cell.col), board.box(cell.box)]:
            if not any((x != cell and p in x.possibles) for x in unit):
                board.setnum(p, cell)
                return True

def exclusive_tuples(board, cell):
    rval = False

    for collection in [board.row(cell.row), board.col(cell.col), board.box(cell.box)]:
        identical = [x for x in collection if x.possibles == cell.possibles]
        if len(identical) == len(cell.possibles):
            #exclusive, remove these from the rest of the row
            for other_cell in collection:
                if other_cell not in identical_row:
                    other_cell.possibles -= cell.possibles
                    rval = True

    return rval

def pointer(board, cell):
    rval = False
    box = list(board.box(cell.box))

    for candidate in cell.possibles:
        have_candidate = [x for x in box if candidate in x.possibles]

        if len(set(x.row for x in have_candidate)) == 1:
            # all of these possibles are in the same row, which means that
            # this number will not appear outside of this box in this row
            rest = [x for x in board.row(cell.row) if candidate in x.possibles and x.box != cell.box]
            for r in rest:
                r.possibles.discard(candidate)
                rval = True

        if len(set(x.col for x in have_candidate)) == 1:
            rest = [x for x in board.col(cell.col) if candidate in x.possibles and x.box != cell.box]
            for r in rest:
                r.possibles.discard(candidate)
                rval = True

    return rval

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
            self._board = set(Cell(num / 9, num % 9, int(val) if val != '.' else None) for num, val in enumerate(board))

        for row in self.rows():
            for cell in row:
                if cell.num:
                    continue
                row_poss = set(x.num for x in self.row(cell.row))
                col_poss = set(x.num for x in self.col(cell.col))
                box_poss = set(x.num for x in self.box(cell.box))
                cell.possibles = set(range(1,10)) - row_poss - col_poss - box_poss

    def setnum(self, num, cell):
        mycell = self.cell(cell.row, cell.col)
        mycell.num = num
        mycell.possibles = set()
        self.clear_possibles(mycell)

    def cells(self):
        for r in self.rows():
            for c in sorted(r, key=lambda x:x.col):
                yield c

    def cell(self, rownum, colnum):
        return [x for x in self._board if x.row == rownum and x.col == colnum][0]

    def row(self, num):
        return (x for x in self._board if x.row == num)

    def rows(self):
        return (self.row(x) for x in range(9))
    
    def col(self, num):
        return (x for x in self._board if x.col == num)

    def cols(self):
        return (self.col(x) for x in range(9))
    
    def box(self, boxnum):
        return (x for x in self._board if x.box == boxnum)

    def boxes(self):
        return (self.box(x) for x in range(9))
    
    def _do_for_all_units(self, fun, cell):
        for r in self.row(cell.row):
            fun(r)
        for c in self.col(cell.col):
            fun(c)
        for b in self.box(cell.box):
            fun(b)

    def clear_possibles(self, cell):
        self._do_for_all_units(lambda x: x.possibles.discard(cell.num), cell)

    def solvable(self):
        return all(x.possibles or x.num for x in self.cells())
    
    def solved(self):
        try:
            self.check()
        except Mistake:
            return False
        return all(x.num for x in self.cells())
        
    def check(self):
        for unit_collection in [self.rows(), self.cols(), self.boxes()]:
            for unit in unit_collection:
                unit = [x for x in unit if x]
                if sorted(list(set(unit))) != sorted(unit):
                    raise Mistake(unit)
        return True

    def __str__(self):
        rval = ""
        for c in self.cells():
            if c.col == 0 and c.row % 3 == 0:
                rval += '-' * 13 + '\n'
            if c.col % 3 == 0:
                rval += "|"
            rval += (str(c.num) if c.num else '.')
            if c.col == 8:
                rval += "|" + "\n"
        rval += '-' * 13
        return rval

def solve(board):
    do_it_the_smart_way(board)
    
    while not board.solved():
        board = guess(board)

    board.check()
    return board
    
def guess(board):
    print "I have to guess..."
    #print board
    original_board = copy.deepcopy(board)

    to_guess = None
    for cell in sorted(original_board.cells(), key=lambda x:len(x.possibles)):
        if len(cell.possibles) >= 2:
            to_guess = cell
            break
    
    for option in list(to_guess.possibles):
        #print "Trying %s in %s" % (option, to_guess)
        board.setnum(option, to_guess)
        try:
            board = solve(board)
        except (Unsolvable, Mistake), e:
            original_board.cell(to_guess.row, to_guess.col).possibles.discard(option)
            board = copy.deepcopy(original_board)
        else:
            return board

    raise Unsolvable
        
def do_it_the_smart_way(board):
    made_progress = True
    while(made_progress):
        made_progress = False

        if not board.solvable():
            raise Unsolvable
        
        for cell in board.cells():
            for strat in [only_choice, single_possibility, pointer, exclusive_tuples]:
                if strat(board, cell):
                    made_progress = True

def noisy_solve(board):
    print "SOLVING"
    print board
    tick = time.time()
    try:
        board = solve(board)
    except Mistake, e:
        print "Found a mistake! This is probably a bug..."
        print e
    except Unsolvable:
        print "Looks like this puzzle is unsolvable, sorry!"
    else:
        print "SOLVED in %.2f seconds" % (time.time() - tick)
    print board
    
def main():
    parser = argparse.ArgumentParser(description='Solve a sudoku puzzle')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--filename', metavar='Filename', help="Name of file containing puzzles to solve")
    group.add_argument('-p', '--puzzle', metavar='Inline puzzle', help="Specify a puzzle on the command line as a single string with no line breaks, using '.' for empty squares")
    args = parser.parse_args()

    if args.filename:
        total_tick = time.time()
        count = 0
        for line in open(args.filename):
            print line
            noisy_solve(Board(line.strip()))
            count += 1
        print "SOLVED %s puzzles in %.2f seconds" % (count, time.time() - total_tick)

    if args.puzzle:
        noisy_solve(Board(args.puzzle))
        
if __name__ == '__main__':
    main()
    
