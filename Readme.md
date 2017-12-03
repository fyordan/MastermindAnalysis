# How to run:

Currently the code is in a very simple state. You can play a game against
the computer by running the python script and inputing your moves or guesses.

Once you play a move, you will see an output of the form
Out: (a, b) where a is how many symbols are correct,
and b is how many symbols AND their position are correct. The game ends when b = 3.

The moves are represented as a string made up from the characters S, T, and C.
S = square, T = triangle, C = circle

All of the settings (such as distribution sequences are drawn from, or verbosity) are hard coded.

If verbosity is set to True, the likelihood of all still possible sequences are printed.

# TODO:
- Add logging support so multiple games can be played and the data can be seen after the fact.
- Visualize data trends, such as confidence in solution, and likelihood of moves being winning moves.
- Make simple AI to play game.


