import copy
import time

numAllocations = 0

class boardSpot(object):
    value = 0
    selected = False
    flagged = False

    def __init__(self):
        self.selected = False

    def __str__(self):
        return str(boardSpot.value)

    def isMine(self):
        return boardSpot.value == -1:
    
    def getValue(self):
        return boardSpot.value


class boardClass(object):
    def __init__(self, m_boardWidth, m_boardHeight, m_numMines, mineCoordinates=None):
        self.board = [[boardSpot() for i in range(m_boardWidth)] for j in range(m_boardHeight)]
        self.boardWidth = m_boardWidth
        self.boardHeight = m_boardHeight
        self.numMines = m_numMines
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

    numAllocations = 0
    print("Starting board:")
    print(board)
    start_time = time.time()
    answer = backtrack(board, verbosity=verbosity)
    end_time = time.time()
    if answer:
        print("Flag locations:")
        print(answer)
    else:
        print("No solution found.")
    print("Number of allocations: " + str(numAllocations))
    print("Elapsed time: {:.4f} seconds".format(end_time - start_time))

def testAlgorithms():
    print("Testing backtracking on the following 4 by 3 board:")
    solveBacktracking(smallBoard())

    print("Testing backtracking on the following 4 by 3 invalid board:")
    solveBacktracking(smallBoardIncorrect())

    """
    print("Testing backtracking on the following 10 by 10 board:")
    solveBacktracking(mediumBoard(), 2)"""

    print("Testing backtracking on the following 10 by 10 board:")
    solveBacktracking(mediumBoardPartiallySolved())


testAlgorithms()