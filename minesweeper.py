import numpy as np
import random


class Minesweeper:
    def __init__(self, size=10, mines=10) -> None:
        self.size = size
        self.mines = mines
        self.visibleBoard = np.zeros(shape=(self.size, self.size))
        self.createBoard()

    def createBoard(self):
        self.makeNewBoardWithMines()
        self.setMineNumbersBoard()

    def makeNewBoardWithMines(self):
        self.board = np.zeros(shape=(self.size, self.size))
        bombs = 0
        while bombs < self.mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.board[row][col] != -1:
                bombs += 1
                self.board[row][col] = -1

    def setMineNumbersBoard(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != -1:
                    self.board[row][col] = self.setMinesNumAdjacentToIt(
                        row, col)

    def setMinesNumAdjacentToIt(self, row, col):
        # neighbor postions
        neighborPositions = [[-1, -1], [-1, 0], [-1, 1],  # top
                             [0, -1],           [0, 1],   # left and right
                             [1, -1],  [1, 0],  [1, 1]]   # bot
        minesNum = 0
        for i in range(len(neighborPositions)):
            mRow = row + neighborPositions[i][0]
            mCol = col + neighborPositions[i][1]
            if mRow >= 0 and mCol >= 0 and mRow < self.size and mCol < self.size:
                if self.board[mRow][mCol] == -1:
                    minesNum += 1
        return minesNum

    def click(self, row, col):
        self.visibleBoard[row][col] = 1
        if self.board[row][col] == -1:
            return False  # fail
        elif self.board[row][col]:
            return True

        # neighbor postions
        neighborPositions = [[-1, -1], [-1, 0], [-1, 1],  # top
                             [0, -1],           [0, 1],   # left and right
                             [1, -1],  [1, 0],  [1, 1]]   # bot
        for i in range(len(neighborPositions)):
            mRow = row + neighborPositions[i][0]
            mCol = col + neighborPositions[i][1]
            if mRow >= 0 and mCol >= 0 and mRow < self.size and mCol < self.size:
                if self.visibleBoard[mRow][mCol] == 0:
                    self.click(mRow, mCol)

        return True

    def winCondition(self):
        counter = 0  # number of cells visible.
        for row in range(self.size):
            for col in range(self.size):
                if self.visibleBoard[row][col] != 0:
                    counter += 1
        # if everything is visible but the mines.
        winCondition = (self.size * self.size) - self.mines
        if counter < winCondition:
            return False
        else:
            return True

    def setAllVisible(self):
        for row in range(self.size):
            for col in range(self.size):
                self.visibleBoard[row][col] = 1

    def __str__(self) -> str:
        # col number
        outputString = "     "
        for i in range(self.size):
            if i >= 10:
                outputString += "" + str(i) + "  "
            else:
                outputString += "" + str(i) + "   "

        # big line
        outputString += "\n----"
        for i in range(self.size):
            outputString += "----"
        outputString += "\n"
        for row in range(self.size):
            # row number
            if row >= 10:
                outputString += str(row) + " | "
            else:
                outputString += str(row) + "  | "

            for col in range(self.size):
                if self.visibleBoard[row][col] == 0:
                    outputString += "  | "
                else:
                    if self.board[row][col] == -1:
                        outputString += "* | "
                    elif self.board[row][col] == 0:
                        outputString += "  | "
                    else:
                        outputString += str(int(self.board[row][col])) + " | "
            outputString += "\n"

        # big line
        outputString += "----"
        for i in range(self.size):
            outputString += "----"
        outputString += "\n"
        return outputString


def start():
    minesweeper = Minesweeper(12, 14)

    validClick = True
    while validClick and (not minesweeper.winCondition()):
        print(minesweeper)

        print("Select which cell would you like to reveal")
        userInput = input("Row: ")
        userInput2 = input("Col: ")
        mRow = int(userInput)
        mCol = int(userInput2)
        print("You selected:", mRow, mCol)
        if mRow < 0 or mCol < 0 or mRow >= minesweeper.size or mCol >= minesweeper.size:
            print("Invalid input.")
            continue

        validClick = minesweeper.click(mRow, mCol)

    if validClick:
        print("WEE! You won.")
    else:
        print("You lost.")
    minesweeper.setAllVisible()
    print(minesweeper)


start()
