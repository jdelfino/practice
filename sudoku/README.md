This is a sudoku solver written in Python. It's not really commented, and not really optimized for performance. It was written mostly as an exercise to remind me how to use Python after being away from it for 6 months.

It uses some simple strategies:
- "this square can only be N"
- "no other square in this unit can be N"
- "pointers" (http://www.sudoku-solutions.com/solvingInteractions.php) 
- "exclusive tuples" (http://www.thonky.com/sudoku/naked-pairs-triples-quads/)

When those strategies are exhausted, it resorts to taking a guess, then making as much progress without guessing again as possible.

If you want a much more elegant, faster version of this, check out http://norvig.com/sudoku.html.