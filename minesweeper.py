import numpy as np
import random


class Minesweeper:
    def __init__(self, size=10, mines=10) -> None:
        self.size = size  # size of the board col == rows
        self.mines = mines  # number of mines
        # all is not visible
        self.visibleBoard = np.zeros(shape=(self.size, self.size))
        self.createBoard()  # create the board with mines and the numbers.

    def createBoard(self):
        # create the board and set the mines randomly
        self.makeNewBoardWithMines()
        # add the numbers of neighboring mines in each cell.
        self.setMineNumbersBoard()

    def makeNewBoardWithMines(self):
        self.board = np.zeros(shape=(self.size, self.size))
        bombs = 0
        while bombs < self.mines:
            # select a random cell
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.board[row][col] != -1:  # if mine is not already placed.
                bombs += 1
                self.board[row][col] = -1

    def setMineNumbersBoard(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != -1:  # not if cell is a mine
                    # set the number of mines neighboring the mine
                    self.board[row][col] = self.setMinesNumAdjacentToIt(
                        row, col)

    def setMinesNumAdjacentToIt(self, row, col):
        # neighbor postions
        neighborPositions = [[-1, -1], [-1, 0], [-1, 1],  # top
                             [0, -1],           [0, 1],   # left and right
                             [1, -1],  [1, 0],  [1, 1]]   # bot
        minesNum = 0
        # visit each neighbor position
        for i in range(len(neighborPositions)):
            mRow = row + neighborPositions[i][0]
            mCol = col + neighborPositions[i][1]
            if mRow >= 0 and mCol >= 0 and mRow < self.size and mCol < self.size:  # valid neighbor
                if self.board[mRow][mCol] == -1:  # if there is a mine, then add to counter
                    minesNum += 1

        return minesNum

    def click(self, row, col):
        self.visibleBoard[row][col] = 1

        if self.board[row][col] == -1:
            return False  # fail. Clicked on a mine.
        elif self.board[row][col]:
            return True

        # neighbor postions
        neighborPositions = [[-1, -1], [-1, 0], [-1, 1],  # top
                             [0, -1],           [0, 1],   # left and right
                             [1, -1],  [1, 0],  [1, 1]]   # bot
        # visit each neighbor position
        for i in range(len(neighborPositions)):
            mRow = row + neighborPositions[i][0]
            mCol = col + neighborPositions[i][1]
            if mRow >= 0 and mCol >= 0 and mRow < self.size and mCol < self.size:  # valid neighbor
                if self.visibleBoard[mRow][mCol] == 0:
                    self.click(mRow, mCol)

        return True

    # You win when all the visible cells + mines == size * size
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

    # Set the board all visible
    def setAllVisible(self):
        for row in range(self.size):
            for col in range(self.size):
                self.visibleBoard[row][col] = 1

    # string representation of the class. Shows the board visible atm.
    def __str__(self) -> str:
        # col number
        outputString = "     "
        for i in range(self.size):
            if i >= 10:  # check when columns is two digits
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
            if row >= 10:  # check when rows is two digits
                outputString += str(row) + " | "
            else:
                outputString += str(row) + "  | "

            for col in range(self.size):
                # shows the board if cell is visible
                if self.visibleBoard[row][col] == 0:
                    outputString += "  | "
                else:
                    if self.board[row][col] == -1:  # mine representation
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
    minesweeper = Minesweeper(12, 14)  # 12x12 14 mines

    validClick = True
    while validClick and (not minesweeper.winCondition()):
        print(minesweeper)  # prints the state of the board

        print("Select which cell would you like to reveal")
        userInput = input("Row: ")
        userInput2 = input("Col: ")

        try:
            mRow = int(userInput)
            mCol = int(userInput2)
        except ValueError:  # check if user types a number
            print("That's not an int.")
            continue

        print("You selected:", mRow, mCol)

        # row and col should be valid.
        if mRow < 0 or mCol < 0 or mRow >= minesweeper.size or mCol >= minesweeper.size:
            print("Invalid input. Type numbers between 0 and",
                  minesweeper.size - 1)
            continue

        # click on the row and col selected.
        validClick = minesweeper.click(mRow, mCol)

    if validClick:
        print("WEE! You won.")
    else:
        print("You lost.")

    minesweeper.setAllVisible()  # everything is visible
    print(minesweeper)  # print all the board


start()  # the beginning. :)
