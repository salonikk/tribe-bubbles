import sys, threading, time
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from random import randint

# if you change CELL_COUNT, be sure that initial
# patterns in constructor are still valid
CELL_COUNT = 10
CELL_SIZE = 50
GRID_ORIGINX = 100
GRID_ORIGINY = 100
W_WIDTH = 700
W_HEIGHT = 700


class TribeBubbles(QWidget):

  def __init__(self):
    super().__init__()
    self.__board = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
    self.setWindowTitle('Tribe Bubbles')
    self.setGeometry(300, 300, W_WIDTH, W_HEIGHT)
    self.score1 = 0
    self.mult1 = 0
    self.h1 = False
    self.v1 = False
    self.d11 = False
    self.d21 = False
    self.score2 = 0
    self.mult2 = 0
    self.h2 = False
    self.v2 = False
    self.d12 = False
    self.d22 = False
    self.turn = 0
    self.draw = 0
    self.show()

  def GameOver(self):
    count = 0
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          if self.__board[r][c] == -1:
              count +=1
    if count == 0:
        return True


  def paintEvent(self, event):
    qp = QPainter()

    blackPen = QPen(QBrush(Qt.black), 1)
    qp.begin(self)

    # clear the background
    qp.fillRect(event.rect(), Qt.white)

    qp.setPen(blackPen)

    # draw each cell
    qp.drawText(10,20, "Rules: player 1 is red and player 2 is black. Alternate clicking empty spaces to place your colored circles")
    qp.drawText(10,40, "in the squares. Player 2 begins. Increase your score by getting at leat 4 squares in a row.")
    qp.drawText(10,60, "If you create multiple lines at once, you get extra points! The computer will randomly place blockers.")
    qp.drawText(10, 80, "If you would like to pass your turn, click a blue blocker. Good luck!")
    for r in range(len(self.__board)):
      for c in range(len(self.__board[r])):
        qp.drawRect(GRID_ORIGINX + c * CELL_SIZE, GRID_ORIGINY + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.__board[r][c] == 1:
          redPen = QPen(QBrush(Qt.red), 2)
          qp.setPen(redPen)
          qp.drawEllipse(GRID_ORIGINX + c * CELL_SIZE + 3, GRID_ORIGINY + r * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6)
          qp.setPen(blackPen)
        if self.__board[r][c] == 3:
          blackPen = QPen(QBrush(Qt.black), 1)
          qp.setPen(blackPen)
          qp.drawEllipse(GRID_ORIGINX + c * CELL_SIZE + 3, GRID_ORIGINY + r * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6)
          qp.setPen(blackPen)
        if self.__board[r][c] == 2:
             bluePen = QPen(QBrush(Qt.blue), 3)
             qp.setPen(bluePen)
             brush = QBrush(Qt.blue, Qt.SolidPattern)
             qp.setBrush(brush)
             qp.drawRect(GRID_ORIGINX + c * CELL_SIZE + 3, GRID_ORIGINY + r * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6)
             qp.setBrush(Qt.white)
             qp.setPen(blackPen)
        scorestringp1= "player 1 score: " + str(self.score1)
        multstringp1 = "X " + str(self.mult1)
        qp.drawText(275, 620, scorestringp1)
        if self.mult1 == 0:
            qp.drawText(400, 620, "X 1")
        else:
            qp.drawText(400, 620, multstringp1)

        scorestringp2= "player 2 score: " + str(self.score2)
        multstringp2 = "X " + str(self.mult2)
        qp.drawText(275, 660, scorestringp2)
        if self.mult2 == 0:
            qp.drawText(400, 660, "X 1")
        else:
            qp.drawText(400, 660, multstringp2)
    if self.GameOver() is True:
        whitePen = QPen(QBrush(Qt.white), 3)
        qp.setPen(blackPen)
        brush2 = QBrush(Qt.white, Qt.SolidPattern)
        qp.setBrush(brush2)
        qp.drawRect(250, 250, 200, 200)
        qp.setFont(QFont("Arial", 30))
        if self.score1 > self.score2:
                qp.drawText(260,350, "Player 1 wins!")
        if self.score2 > self.score1:
                qp.drawText(260,350, "Player 2 wins!")
        else:
                qp.drawText(280, 320, "Tie Game!")
                qp.drawText(280, 400, "Play Again!")
    qp.end()


  def mousePressEvent(self, event):
        self.turn = (self.turn + 1) % 2
        self.__x = event.x()
        self.__y = event.y()
        row = (event.y() - GRID_ORIGINY) // CELL_SIZE
        col = (event.x() - GRID_ORIGINX) // CELL_SIZE
        if self.turn == 0:
            if 0 <= row < CELL_COUNT and 0 <= col < CELL_COUNT:
                if self.__board[row][col] == -1:
                    self.__board[row][col] = 1
                    self.disappear1()
                    randrow = randint(0, len(self.__board) -1)
                    randcol = randint(0, len(self.__board) - 1)
                    randsquare = self.__board[randrow][randcol]
                    if randsquare == 2:
                        randrow = randint(0, len(self.__board) -1)
                        randcol = randint(0, len(self.__board) - 1)
                        randsquare = self.__board[randrow][randcol]
                    self.__board[randrow][randcol] = 2
            else:
                pass
        elif self.turn == 1:
            if 0 <= row < CELL_COUNT and 0 <= col < CELL_COUNT:
                if self.__board[row][col] == -1:
                    self.__board[row][col] = 3
                    self.disappear2()
                    randrow = randint(0, len(self.__board) -1)
                    randcol = randint(0, len(self.__board) - 1)
                    randsquare = self.__board[randrow][randcol]
                    if randsquare == 2:
                        randrow = randint(0, len(self.__board) -1)
                        randcol = randint(0, len(self.__board) - 1)
                        randsquare = self.__board[randrow][randcol]
                    #self.__board[randrow][randcol] = 2
        if self.GameOver() is True:
            print("gameover")
            draw = 1
        self.update()


  def disappear1(self):
    dis1 = []
    self.mult1 = 0
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          #horizontal
          if c <= (len(self.__board)-1-3):
              if self.__board[r][c] == 1 and self.__board[r][c+1] == 1 and self.__board[r][c+2] == 1 and self.__board[r][c+3] == 1:
                  self.h1 = True
                  for i in range(0, 9):
                      if c + i < 10:
                          if self.__board[r][c + i] == 1:
                              dis1.append((r, c+i))
                          else:
                              break
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          #vertical
          if r <= (len(self.__board)-1-3):
            if self.__board[r][c] == 1 and self.__board[r+1][c] == 1 and self.__board[r+2][c] == 1 and self.__board[r+3][c] == 1:
                   self.v1 = True
                   for i in range(0, 9):
                       if r + i < 10:
                            if self.__board[r+i][c] == 1:
                                dis1.append((r+i, c))
                            else:
                                break
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          #diagonal
          if r <= (len(self.__board)-1-3) and c <= (len(self.__board)-1-3):
            if self.__board[r][c] == 1 and self.__board[r+1][c+1] == 1 and self.__board[r+2][c+2] == 1 and self.__board[r+3][c+3] == 1:
                   self.d11 = True
                   for i in range(0, 9):
                       if r + i < 10 and c + i < 10:
                            if self.__board[r+i][c+i] == 1:
                                dis1.append((r+i, c+i))
                            else:
                                break
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          if r <= (len(self.__board)-1+3) and c <= (len(self.__board)-1-3):
            if self.__board[r][c] == 1 and self.__board[r-1][c+1] == 1 and self.__board[r-2][c+2] == 1 and self.__board[r-3][c+3] == 1:
                   self.d21 = True
                   for i in range(0, 9):
                       if r - i < 10 and c + i < 10:
                            if self.__board[r-i][c+i] == 1:
                                dis1.append((r-i, c+i))
                            else:
                                break

    if self.h1 == True:
        self.mult1 +=1
        self.h1 = False
    if self.v1 == True:
        self.mult1 +=1
        self.v1 = False
    if self.d11 == True:
        self.mult1 +=1
        self.d11 = False
    if self.d21 == True:
        self.mult1 +=1
        self.d21 = False

    dis1 = list(set(dis1))
    for element in dis1:
        self.score1 += self.mult1*1
        r1, c1 = element
        self.__board[r1][c1] = -1

  def disappear2(self):
    dis2 = []
    self.mult2 = 0
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          #horizontal
          if c <= (len(self.__board)-1-3):
              if self.__board[r][c] == 3 and self.__board[r][c+1] == 3 and self.__board[r][c+2] == 3 and self.__board[r][c+3] == 3:
                  self.h2 = True
                  for i in range(0, 9):
                      if c + i < 10:
                          if self.__board[r][c + i] == 3:
                              dis2.append((r, c+i))
                          else:
                              break
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          #vertical
          if r <= (len(self.__board)-1-3):
            if self.__board[r][c] == 3 and self.__board[r+1][c] == 3 and self.__board[r+2][c] == 3 and self.__board[r+3][c] == 3:
                   self.v2 = True
                   for i in range(0, 9):
                       if r + i < 10:
                            if self.__board[r+i][c] == 3:
                                dis2.append((r+i, c))
                            else:
                                break
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          #diagonal
          if r <= (len(self.__board)-1-3) and c <= (len(self.__board)-1-3):
            if self.__board[r][c] == 3 and self.__board[r+1][c+1] == 3 and self.__board[r+2][c+2] == 3 and self.__board[r+3][c+3] == 3:
                   self.d12 = True
                   for i in range(0, 9):
                       if r + i < 10 and c + i < 10:
                            if self.__board[r+i][c+i] == 3:
                                dis2.append((r+i, c+i))
                            else:
                                break
    for r in range(0, len(self.__board)):
      for c in range(0, len(self.__board)):
          if r <= (len(self.__board)-1+3) and c <= (len(self.__board)-1-3):
            if self.__board[r][c] == 3 and self.__board[r-1][c+1] == 3 and self.__board[r-2][c+2] == 3 and self.__board[r-3][c+3] == 3:
                   self.d22 = True
                   for i in range(0, 9):
                       if r - i < 10 and c + i < 10:
                            if self.__board[r-i][c+i] == 3:
                                dis2.append((r-i, c+i))
                            else:
                                break

    if self.h2 == True:
        self.mult2 +=1
        self.h2 = False
    if self.v2 == True:
        self.mult2 +=1
        self.v2 = False
    if self.d12 == True:
        self.mult2 +=1
        self.d12 = False
    if self.d22 == True:
        self.mult2 +=1
        self.d22 = False

    dis2 = list(set(dis2))
    for element in dis2:
        self.score2 += self.mult2*1
        r2, c2 = element
        self.__board[r2][c2] = -1







if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = TribeBubbles()
  sys.exit(app.exec_())
