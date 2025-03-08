import copy
import time
import itertools
from typing import Tuple

numAllocations = 0
numTestsRun = 0
numBoardsSolved = 0

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

    def addMine(self, x, y):
        self.board[y][x].value = -1
        for i in range(x-1, x+2):
            if i >= 0 and i < self.boardWidth:
                for j in range(y-1, y+2):
                    if j >= 0 and j < self.boardHeight and not self.board[j][i].isMine():
                        self.board[j][i].value += 1

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
    
    def getSpot(self, x, y):
        return self.board[y][x]

    def toggleFlag(self, x, y):
        global numAllocations
        if not self.getSpot(x, y).selected:
            self.getSpot(x, y).flagged = not self.getSpot(x, y).flagged
            if self.getSpot(x, y).flagged:
                self.numFlags += 1
            else:
                self.numFlags -= 1
        numAllocations += 1

    def deepCopy(self):
        return copy.deepcopy(self)

    def getFlagPlacements(self):
        return [(x, y) for y in range(self.boardHeight) for x in range(self.boardWidth) if self.board[y][x].flagged]
    
    def flagsAroundLocation(self, x, y):
        mine_count = 0
        for i in range(x-1, x+2):
            if i >= 0 and i < self.boardWidth:
                for j in range(y-1, y+2):
                    if j >= 0 and j < self.boardHeight and self.getSpot(i, j).flagged:
                        if not (i == x and j == y):
                            mine_count += 1
        return mine_count
    
    def isViablePath(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if self.getSpot(x, y).selected:
                    mine_count = self.flagsAroundLocation(x, y)
                    if mine_count > self.getSpot(x, y).value:
                        return False
        return True

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
    mineCoordinates = [(0, 0), (1, 1), (3, 2)]
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

def backtrack(board, x=0, y=0, verbosity=0):
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
        
        # try every possible move
        for y in range(board.boardHeight):
            for x in range(board.boardWidth):
                if(not (board.getSpot(x, y).selected or board.getSpot(x, y).flagged)):
                    boardCopy = board.deepCopy()
                    boardCopy.toggleFlag(x, y)
                    if boardCopy.isViablePath():
                        if verbosity > 0:
                            print("Flagged spot at " + str(x) + ", " + str(y))
                        result = backtrack(boardCopy, x, y, verbosity)
                        if result:
                            return result
                    elif verbosity > 1:
                        print("Attempted to flag spot at " + str(x) + ", " + str(y) + " but it is inconsistent")
                        print(boardCopy)


        # no moves found
        if verbosity > 0:
            print("No solution found on this path. Backtracking...")
        return None

def solveBacktracking(board, verbosity=0):
    global numAllocations
    global numBoardsSolved

    numAllocations = 0
    print("Starting board:")
    print(board)
    start_time = time.time()
    answer = backtrack(board, verbosity=verbosity)
    end_time = time.time()
    if answer:
        print("Flag locations:")
        print(answer)
        numBoardsSolved += 1
    else:
        print("No solution found.")
    print("Number of allocations: " + str(numAllocations))
    print("Elapsed time: {:.4f} seconds".format(end_time - start_time))

# Author: Jeff Krug
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

    for x in range(0, board.boardWidth):
        numCells: int = 0
        for y in range(0, board.boardHeight):
            if board.board[y][x].flagged or board.board[y][x].selected and board.board[y][x].value >= 0:
                numCells += 1
        if maxRevealedCols <= numCells: col = x
        maxRevealedCols= max(maxRevealedCols, numCells)

    return ("row", row) if maxRevealedRows >= maxRevealedCols else ("col", col)

# Author: Jeff Krug
def subBoard(board: boardClass, row: int = -1, col: int = -1) -> list[boardClass]:
    board1: boardClass
    board2: boardClass

    if row > -1:
        rows1: int = row
        rows2: int = board.boardHeight - 1 - rows1

        mines1: list[Tuple[int, int]] = [(x, y) for (x, y) in board.mineCoords if y < rows1]
        mines2: list[Tuple[int, int]] = [(x, y - row - 1) for (x, y) in board.mineCoords if y > rows1]

        board1 = boardClass(board.boardWidth, rows1, len(mines1))
        for x in range(board1.boardWidth):
            for y in range(board1.boardHeight):
                board1.board[y][x] = board.board[y][x]

        board2 = boardClass(board.boardWidth, rows2, len(mines2))
        for x in range(board2.boardWidth):
            for y in range(board2.boardHeight):
                board2.board[y][x] = board.board[y + row + 1][x]

        print(len(mines2))
        print(board.board[2][5].value)
    else:
        cols1: int = col
        cols2: int = board.boardWidth - 1 - cols2
        mines1: list[Tuple[int, int]] = [(x, y) for (x, y) in board.mineCoords if x < cols1]
        mines2: list[Tuple[int, int]] = [(x - col - 1, y) for (x, y) in board.mineCoords if x > cols1]

        board1 = boardClass(cols1, board.boardHeight, len(mines1), mines1)
        board1 = boardClass(cols2, board.boardHeight, len(mines2), mines2)

    return [board1, board2]

def solveCutsetConditioning(board: boardClass, verbosity: int):
    answer

    cutset: Tuple[str, int] = findCutset(board)
    subBoards: list[boardClass] = subBoard(board, row=cutset[1]) if cutset[0] == "row" else subBoard(board, col=cutset[1])

    print(subBoards[0])
    print(subBoards[1])

    print(cutset)

    emptyCells: list[int] = []
    x: int
    y: int

    if cutset[0] == "row":
        y = cutset[1]

        for x in range(board.boardWidth):
            if board.board[y][x].selected: emptyCells.append(x)
        
        numMines = len([(x1, y1) for (x1, y1) in board.mineCoords if y1 == y])

        if numMines == 0:
            pass          
        elif len(emptyCells) == numMines:
            for cell in emptyCells:
                board.toggleFlag(cell, y)
        
        subAnswer1 = backtrack(subBoards[0], verbosity=verbosity)
        subAnswer2 = backtrack(subBoards[1], verbosity=verbosity)
        
        

    # else:
    #     x = cutset[1]

    #     for y in range(board.boardHeight):
    #         if board.board[y][x].selected: emptyCells.append(y)

    print(answer)
    

def testAllBoards(boardWidth, boardHeight, numMines, verbosity=0, timeout=10):
    global numTestsRun
    global numBoardsSolved
    numTestsRun = 0
    numBoardsSolved = 0

    all_positions = [(x, y) for x in range(boardWidth) for y in range(boardHeight) if (x, y) != (0, 0)]
    mine_combinations = itertools.combinations(all_positions, numMines)

    for mineCoordinates in mine_combinations:
        board = boardClass(boardWidth, boardHeight, numMines, mineCoordinates)
        board.makeMove(0, 0)
        print("Testing board with mines at:", mineCoordinates)
        solveBacktracking(board, verbosity)
        print("\n")
        numTestsRun += 1

def testAlgorithms():
    """
    print("Testing backtracking on the following 4 by 3 board:")
    solveBacktracking(smallBoard())

    print("Testing backtracking on the following 4 by 3 invalid board:")
    #solveBacktracking(smallBoardIncorrect())

    
    print("Testing backtracking on the following 10 by 10 board:")
    solveBacktracking(mediumBoard(), 2)

    print("Testing backtracking on the following 10 by 10 board:")
    solveBacktracking(mediumBoardPartiallySolved())
    """
    
    print("Solving all combinations of 4 by 4 boards with 3 mines:")
    testAllBoards(4, 4, 3, 2)
    print("Number of tests run:", numTestsRun)
    print("Precentage of boards solved:", numBoardsSolved/numTestsRun)


# testAlgorithms()
board: boardClass = mediumBoard()
print(board)
solveCutsetConditioning(board, 0)
