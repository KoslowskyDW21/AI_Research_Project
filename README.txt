### Minesweeper Backtracking Solver

### Overview
This program contains methods to solve minesweeper boards using backtracking and cutset conditioning
There is a class Board which represents a minesweeper board, which is comprised of BoardSpots
Methods SolveBacktracking and SolveCutsetConditioning will run the given algorithms, printing data about the runtime
Method testAlgorithm is called at runtime and runs multiple instances of the above methods with several different boards

### Prerequisites
- Python 3.x

### Running the Program
1. Ensure all the necessary files (`minesweeper.py` and any other required files) are in the same directory.
2. Open a terminal or command prompt.
3. Run the file minesweeper.py through VSCode or similar IDE
OR
Using a command window, navigate to the directory containing the files and run the following command:
   python minesweeper.py

By default, this will solve for a small 3x4 board with 3 mines
To change, go to line 512 in the code, which looks like this:
board = smallBoard()
smallBoard() can be replaced with other functions for additional testing:

smallBoardIncorrect()
Gives a 3x4 board with 3 mines that is not a valid board state

mediumBoard()
Gives a 10x10 board with 6 mines
Neither algorithm will solve this in a reasonable time

mediumBoardPartiallySolved()
This is the medium board with 3 mines already placed
Backtracking will solve this in a few minutes, cutset conditioning will not

createRandomBoard(n, m, k)
Creates an n x m board with k randomly placed mines
Ability for our algorithms to solve these in a reasonable time varies drastically depending on the placement of the mines
