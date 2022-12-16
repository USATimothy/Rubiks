# Rubiks
Solve a Rubiks cube and a related Rubiks globe in Matlab, Julia, and python

The Rubiks cube and globe are puzzles with movable attached pieces. The pieces can be rotated relative to each other,
with one configuration (proper continents, or one-color faces) being the solution.

The Rubiks cube is a cube with 20 movable pieces (3x3x3, minus the center piece and the centers of the 6 faces).
The Rubiks globe is a globe split into North/South, East/West, and Atlantic/Pacific hemispheres for a total of 8 movable pieces.
A Rubiks globe is mathematically equivalent to a Rubiks cube with all the edge pieces in place, and only the corners needing adjustment.

The Rubiks globe can be solved with a brute-force breadth-first algorithm.
Unlike the globe, the cube cannot be solved by checking a tree of all possible moves for a branch that reaches the solution.
However, some combinations of 4-8 moves can be filtered to find combinations that move only 2-4 pieces while returning the others to their
pre-combination positions. By stringing together move combinations, one can sequentially move the pieces to the correct place.
