import copy
import time
import itertools
from typing import Tuple, Set
import random

numAllocations = 0
numTestsRun = 0
numBoardsSolved = 0

# Author: RaemondBW
# class representing a single spot on the board
# value: -1 for mine, 0-8 for number of mines around the spot
# selected: true if the spot has been revealed
# flagged: true if the spot has been flagged as a mine
class boardSpot(object):
    value = 0
    selected = False
    flagged = False
    def __init__(self):
        self.selected = False

    def __str__(self):
        return str(boardSpot.value)

    def isMine(self):
        return boardSpot.value == -1
    
    def getValue(self):
        return boardSpot.value

class boardClass(object):
    # Author: RaemondBW
    # Edited by David Koslowsky and Jeff Krug
    def __init__(self, m_boardWidth, m_boardHeight, m_numMines, mineCoordinates=None):
        self.board = [[boardSpot() for i in range(m_boardWidth)] for j in range(m_boardHeight)]
        self.boardWidth = m_boardWidth
        self.boardHeight = m_boardHeight
        self.numMines = m_numMines
        self.mineCoords = mineCoordinates # Added by Jeff for cutset conditioning purposes
        self.numFlags = 0

        if mineCoordinates:
            for (x, y) in mineCoordinates:
                self.addMine(x, y)

    # Author: RaemondBW
    # Edited by David Koslowsky
    # prints a visualization of the board to the console
    def __str__(self):
        returnString = " "
        divider = "\n---"

        for i in range(0, self.boardWidth):
            divider += "----"
        divider += "\n"

        returnString += divider
        for y in range(0, self.boardHeight):
            for x in range(0, self.boardWidth):
                if self.board[y][x].flagged:
                    returnString += " | *"
                elif self.board[y][x].isMine() and self.board[y][x].selected:
                    returnString += " |" + str(self.board[y][x].value)
                elif self.board[y][x].selected:
                    returnString += " | " + str(self.board[y][x].value)
                else:
                    returnString += " |  "
            returnString += " |"
            returnString += divider
        return returnString

    # Author: RaemondBW
    def addMine(self, x, y):
        self.board[y][x].value = -1
        for i in range(x-1, x+2):
            if i >= 0 and i < self.boardWidth:
                for j in range(y-1, y+2):
                    if j >= 0 and j < self.boardHeight and not self.board[j][i].isMine():
                        self.board[j][i].value += 1

    # Author: RaemondBW
    # Edited by David Koslowsky, adding checks for flags
    # simulates making a move at the given x and y coordinates
    # if there are no mines around the spot, it will recursively reveal all adjacent spots
    # returns true if the move was successful, false if the player hit a mine
    def makeMove(self, x, y):
        if self.board[y][x].flagged:
            print("This spot is flagged. Unflag it first to make a move.")
            return True
        self.board[y][x].selected = True
        if self.board[y][x].value == -1:
            return False
        if self.board[y][x].value == 0:
            for i in range(x-1, x+2):
                if i >= 0 and i < self.boardWidth:
                    for j in range(y-1, y+2):
                        if j >= 0 and j < self.boardHeight and not self.board[j][i].selected:
                            self.makeMove(i, j)
        return True
    
    # Author: David Koslowsky
    def getSpot(self, x, y):
        return self.board[y][x]

    # Author: David Koslowsky
    # flags the spot at the given x and y coordinates
    # if the spot is already flagged, it will unflag it
    # increments the global int numAllocations for metrics
    def toggleFlag(self, x, y):
        global numAllocations
        if not self.getSpot(x, y).selected:
            self.getSpot(x, y).flagged = not self.getSpot(x, y).flagged
            if self.getSpot(x, y).flagged:
                self.numFlags += 1
            else:
                self.numFlags -= 1
        numAllocations += 1

    # Author: David Koslowsky
    # returns a deep copy of the board
    def deepCopy(self):
        return copy.deepcopy(self)

    # Author: David Koslowsky
    # returns a list of Tuples containing x, y coordinates for all the flagged spots on the board
    def getFlagPlacements(self):
        return [(x, y) for y in range(self.boardHeight) for x in range(self.boardWidth) if self.board[y][x].flagged]

    # Author: David Koslowsky
    # returns the number of flags around the given x, y coordinates
    def flagsAroundLocation(self, x, y):
        mine_count = 0
        for i in range(x-1, x+2):
            if i >= 0 and i < self.boardWidth:
                for j in range(y-1, y+2):
                    if j >= 0 and j < self.boardHeight and self.getSpot(i, j).flagged:
                        if not (i == x and j == y):
                            mine_count += 1
        return mine_count
    
    # Author: David Koslowsky
    # returns true if the board is a viable path, meaning that no revealed spot has more flags around it than its value
    def isViablePath(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if self.getSpot(x, y).selected:
                    mine_count = self.flagsAroundLocation(x, y)
                    if mine_count > self.getSpot(x, y).value:
                        return False
        return True

    # Author: David Koslowsky
    # returns true if the board is consistent, meaning that all revealed spots have the correct number of flags around them
    def isConsistent(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if self.getSpot(x, y).selected:
                    mine_count = self.flagsAroundLocation(x, y)
                    if mine_count != self.getSpot(x, y).value:
                        return False
        return True


# Method to create a small board with specific mine coordinates
def smallBoard():
    boardWidth = 4
    boardHeight = 3
    numMines = 3
    mineCoordinates = [(1, 1), (3, 2), (0, 2)]
    board = boardClass(boardWidth, boardHeight, numMines, mineCoordinates)
    board.makeMove(0, 0)
    board.makeMove(3, 0)
    board.toggleFlag(1, 1)
    return board

def smallBoardIncorrect():
    board = smallBoard()
    board.getSpot(0, 0).value = 5
    return board

def mediumBoard():
    boardWidth = 10
    boardHeight = 10
    numMines = 6
    mineCoordinates = [(1, 3), (5, 1), (5, 2), (1, 5), (2, 5), (4, 5), (5, 5)]
    board = boardClass(boardWidth, boardHeight, numMines, mineCoordinates)
    board.makeMove(0, 0)
    return board

def mediumBoardPartiallySolved():
    board = mediumBoard()
    board.toggleFlag(1, 3)
    board.toggleFlag(5, 1)
    board.toggleFlag(5, 2)
    return board

# Author: David Koslowsky
# Backtracking algorithm to solve the minesweeper board
# returns a list of Tuples containing x, y coordinates for all the flagged spots on the board
# if no solution is found, returns None
# verbosity: 0 = no output, 1 = basic output, 2 = detailed output
def backtrack(board, xRange, yRange, verbosity=0):
        if verbosity > 1:
            print("Board state:")
            print(board)

        # base case for when the board has been solved
        if board.numFlags == board.numMines:

            if board.isConsistent():
                print("Solution found:")
                print(board)
                return board.getFlagPlacements()
            else:
                if verbosity > 0:
                    print("Max mines reached, but board is inconsistent. Backtracking...")
                return None
        
        # try placing a flag at every unselected spot on the board
        for y in yRange:
            for x in xRange:
                if(not (board.getSpot(x, y).selected or board.getSpot(x, y).flagged)):
                    boardCopy = board.deepCopy()
                    boardCopy.toggleFlag(x, y)
                    # if the board is still viable, continue the search
                    if boardCopy.isViablePath():
                        if verbosity > 0:
                            print("Flagged spot at " + str(x) + ", " + str(y))
                        result = backtrack(boardCopy, xRange, yRange, verbosity)
                        # if a solution is found, return it up the stack
                        if result:
                            return result
                    elif verbosity > 1:
                        print("Attempted to flag spot at " + str(x) + ", " + str(y) + " but it is inconsistent")
                        print(boardCopy)


        # getting to this point means no solution was found on this path
        if verbosity > 0:
            print("No solution found on this path. Backtracking...")
        return None

# Author: David Koslowsky
# tracks useful data for the backtracking algorithm
# prints out the number of times the board was allocated and the time taken to solve the board
# also prints the starting board and the solved board (if one is found) along with the mine locations
def solveBacktracking(board: boardClass, verbosity=0):
    global numAllocations
    global numBoardsSolved

    numAllocations = 0
    print("Starting board:")
    print(board)
    start_time = time.time()
    answer = backtrack(board, range(board.boardWidth), range(board.boardHeight), verbosity)
    end_time = time.time()
    if answer or answer == []:
        print("Flag locations:")
        print(answer)
        numBoardsSolved += 1
    else:
        print("No solution found.")
    print("Number of allocations: " + str(numAllocations))
    print("Elapsed time: {:.4f} seconds".format(end_time - start_time))

# Author: Jeff Krug
# This is the first step of the algorithm--finding a cutset
# It selects a single row as the cutset--the row with the least number of empty cells
def findCutset(board: boardClass) -> Tuple[str, int]:
    maxRevealedRows: int = -1
    maxRevealedCols: int = -1
    row: int = -1
    col: int = -1

    for y in range(0, board.boardHeight):
        numCells: int = 0
        for x in range(0, board.boardWidth):
            if board.board[y][x].flagged or board.board[y][x].selected and board.board[y][x].value >= 0:
                numCells += 1
        if maxRevealedRows <= numCells: row = y
        maxRevealedRows = max(maxRevealedRows, numCells)

    # I simply ran out of time to implement column cutsets, so I commented out this section of code.

    # for x in range(0, board.boardWidth):
    #     numCells: int = 0
    #     for y in range(0, board.boardHeight):
    #         if board.board[y][x].flagged or board.board[y][x].selected and board.board[y][x].value >= 0:
    #             numCells += 1
    #     if maxRevealedCols <= numCells: col = x
    #     maxRevealedCols= max(maxRevealedCols, numCells)

    # The function returns the number of the row selected
    return ("row", row) if maxRevealedRows >= maxRevealedCols else ("col", col)

# Author: Jeff Krug
# Splits a board into two subboards that can be solved separately
def subBoard(board: boardClass, row: int = -1, col: int = -1) -> list[boardClass]:
    board1: boardClass
    board2: boardClass

    if row > -1:
        # Determine the size of each subboard
        # Each subboard is the large enough to include the cutset, so when it is solved, it
        # can take the cutset into account, but not modify its values
        rows1: int = row + 1
        rows2: int = board.boardHeight - rows1 + 1

        # Determine the number of mines for each subboard
        mines1: list[Tuple[int, int]] = [(x, y) for (x, y) in board.mineCoords if y < rows1 - 1]
        mines2: list[Tuple[int, int]] = [(x, y - row) for (x, y) in board.mineCoords if y >= rows1]

        # Create the boards and fill in the values from the orginal board
        board1 = boardClass(board.boardWidth, rows1, len(mines1))
        for x in range(board1.boardWidth):
            for y in range(board1.boardHeight):
                board1.board[y][x] = board.board[y][x]

        board2 = boardClass(board.boardWidth, rows2, len(mines2))
        for x in range(board2.boardWidth):
            for y in range(1, board2.boardHeight):
                board2.board[y][x] = board.board[y + row][x]

    # The else statement never runs because I removed column functionality
    else:
        cols1: int = col + 1
        cols2: int = board.boardWidth - cols2 + 1
        mines1: list[Tuple[int, int]] = [(x, y) for (x, y) in board.mineCoords if x < cols1]
        mines2: list[Tuple[int, int]] = [(x - col - 1, y) for (x, y) in board.mineCoords if x > cols1]

        board1 = boardClass(cols1, board.boardHeight, len(mines1), mines1)
        for x in range(board1.boardWidth):
            for y in range(board1.boardHeight):
                board1.board[y][x] = board.board[y][x]

        board2 = boardClass(cols2, board.boardHeight, len(mines2), mines2)
        for x in range(1, board2.boardWidth):
            for y in range(board2.boardHeight):
                board2.board[y][x] = board.board[y][x + col]

    return [board1, board2]

# Author: Jeff Krug
# Runs backtracking search on the subboards and combines the answers
def solveRows(board: boardClass, subBoard1: boardClass, subBoard2: boardClass, y: int, verbosity: int) -> list[Tuple[int, int]]:
    # Fill in the cutset with the proper mines for subboard one
    for x1 in range(subBoard1.boardWidth):
        subBoard1.board[subBoard1.boardHeight - 1][x1] = board.board[y][x1]

    # Fill in the cutset with the proper mines for subboard two
    for x2 in range(subBoard2.boardWidth):
        subBoard2.board[0][x2] = board.board[y][x2]

    if verbosity > 1:
        print("Sub-board 1:")
        print(subBoard1)
        print("Sub-board 2:")
        print(subBoard2)

    # Run backtracking search on the first subboard without altering the cutset
    subAnswer1 = backtrack(subBoard1, range(subBoard1.boardWidth), range(subBoard1.boardHeight - 1), verbosity=verbosity)
    # Run backtracking search on the second subboard without altering the cutset
    subAnswer2 = backtrack(subBoard2, range(subBoard2.boardWidth), range(1, subBoard2.boardHeight), verbosity=verbosity)

    # Backtracking search returns None if there are no mines to be found
    # This code sets the answers to an empty list, so the algorithm doesn't crash
    if(subBoard1.numMines == 0):
        subAnswer1 = []
    if(subBoard2.numMines == 0):
        subAnswer2 = []
    
    if verbosity > 1:
        print(subAnswer1)
        print(subAnswer2)

    if subAnswer1 is None or subAnswer2 is None:
        return None

    # Combine answers and remove duplicates
    subAnswers = subAnswer1 + subAnswer2
    minesSet: set[Tuple[int, int]] = set(subAnswers)
    answer = list(minesSet)
    
    return answer

# Author: Jeff Krug
# This code never runs
def solveCols(board: boardClass, subBoard1: boardClass, subBoard2: boardClass, x: int, verbosity: int):
    for y1 in range(subBoard1.boardHeight):
        subBoard1.board[y1][subBoard1.boardWidth - 1] = board.board[y1][x]

    for y2 in range(subBoard2.boardWidth):
        subBoard2.board[y2][0] = board.board[y2][x]

    subAnswer1 = backtrack(subBoard1, verbosity=verbosity)
    subAnswer2 = backtrack(subBoard2, verbosity=verbosity)

    if subAnswer1 is None or subAnswer2 is None:
        return None

    minesSet: Set[Tuple[int, int]] = set()
    minesSet.add((x, y) for (x, y) in subAnswer1)
    minesSet.add((x, y) for (x, y) in subAnswer2)

    answer: list[Tuple[int, int]] = [(x, y) for (x, y) in minesSet]
    return answer

# Author: Jeff Krug
# Runs cutset conditioning on a board of minesweeper to determine if it is 
# solvable
# Algorithm for cutset conditiong: https://www.forns.lmu.build/classes/spring-2019/cmsi-282/lecture-13M.html
def cutsetConditioning(board: boardClass, verbosity: int):
    answer: list[Tuple[int, int]]

    # The cutset is found, and the subboards are generated
    cutset: Tuple[str, int] = findCutset(board)
    subBoards: list[boardClass] = subBoard(board, row=cutset[1]) if cutset[0] == "row" else subBoard(board, col=cutset[1])

    if verbosity > 0:
        print(subBoards[0])
        print(subBoards[1])
        print(cutset)

    emptyCells: list[int] = []
    x: int
    y: int

    if cutset[0] == "row":
        y = cutset[1]

        # Find the number of empty cells in the cutset
        for x in range(board.boardWidth):
            if board.board[y][x].selected: emptyCells.append(x)
        
        numMines = len([(x1, y1) for (x1, y1) in board.mineCoords if y1 == y])
        originalFlags: list[int] = []

        # Keep track of original mines so they don't get removed in the conditioning
        for x in range(len(board.board[y])):
            if board.board[y][x].flagged:
                originalFlags.append(x)

        if verbosity > 0:
            print(numMines)
            print(originalFlags)

        # This if else tree is step two, conditioning the cutset
        # It will test try different combinations of mines depending on how many mines are supposed
        # to be in the cutset
        if numMines - len(originalFlags) == 0:
            pass          
        elif len(emptyCells) == numMines - len(originalFlags):
            for cell in emptyCells:
                if not cell in originalFlags:
                    board.toggleFlag(cell, y)          
        else:
            mineCells = [0 for i in range(len(emptyCells))]

            for i in range(numMines):
                mineCells[i] = 1

            # Find all combinations of mines
            for permutation in itertools.permutations(mineCells, len(emptyCells)):
                for i in range(len(permutation)):
                    if permutation[i] == 1:
                        if not i in originalFlags:
                            board.toggleFlag(i, y)

                # This is step three, solving the rest of the problem
                answer = solveRows(board, subBoards[0], subBoards[1], y, verbosity)

                if answer:
                    return answer

        # This is also step three, and it will run if testing all combinations of mines in the cutset
        # is not necessary
        answer = solveRows(board, subBoards[0], subBoards[1], y, verbosity) 

    return answer

# Author: Jeff Krug
# Tests the runtime of cutset conditioning
def solveCutsetConditioning(board: boardClass, verbosity: int):
    global numAllocations
    global numBoardsSolved

    numAllocations = 0
    print("Starting board:")
    print(board)
    start_time = time.time()
    answer = cutsetConditioning(board, verbosity)
    end_time = time.time()
    if answer or answer == []:
        print("Flag locations:")
        print(answer)
        numBoardsSolved += 1
    else:
        print("No solution found.")
    print("Number of allocations: " + str(numAllocations))
    print("Elapsed time: {:.4f} seconds".format(end_time - start_time))
    cutsetConditioning(board, verbosity)

# Author: David Koslowsky
# creates a random board with the given dimensions and number of mines
# clicks at 0, 0 to reveal some spots
# sample does not include 0, 0 to avoid clicking on a mine
def createRandomBoard(n, m, k):
    all_positions = [(x, y) for x in range(n) for y in range(m) if (x, y) != (0, 0)]
    mine_positions = random.sample(all_positions, k)
    board = boardClass(n, m, k, mine_positions)
    board.makeMove(0, 0)
    return board


def main():
    board = smallBoard()

    # Solve the board using backtracking
    print("Solving with backtracking:")
    solveBacktracking(board, verbosity=0)

    # Solve the board using cutset conditioning
    print("Solving with cutset conditioning:")
    solveCutsetConditioning(board, verbosity=0)

if __name__ == "__main__":
    main()