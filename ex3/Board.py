__author__ = 'Vegard'
from math import pow, sqrt
from heapq import heapify, heappop, heappush
import glob
class Board:

    def __init__(self, file):
        self.board = []
        #Reads in file, saves A and B values, and creates new nodes in a matrix
        with open(file) as fil:
            linjer = fil.readlines()
            self.gridHeight = len(linjer)

            for x, linje in enumerate(linjer):

                self.board.append([])
                self.gridLength = len(linje)
                for y, char in enumerate(linje):
                    if char =="\n":
                        pass

                    self.board[x].append(Node(x, y, char))

                    if char=="A":
                        self.start = (x, y)
                    if char=="B":
                        self.goal = (x, y)




    def heuristic(self, cell):
        return abs(cell.x-self.goal[0]) + abs(cell.y-self.goal[1])


    def bestFirstSearch(self):
        self.closed = []
        self.opened = []
        heapify(self.opened)
        startNode = self.board[self.start[0]][self.start[1]]
        gCost = 0
        hCost = self.heuristic(startNode)
        totalCost = gCost+hCost
        startNode.g = gCost
        startNode.f = totalCost
        heappush(self.opened, (startNode.f, startNode))
        while len(self.opened):

            node = heappop(self.opened)[1]

            self.closed.append(node)
            #Return with node if it is the final solution
            if node.x==self.goal[0] and node.y==self.goal[1]:
                return self.printPath(node)


            for neighbour in self.generateSuccessors(node):

                node.children.append(neighbour)
                if neighbour not in self.closed and neighbour.cost!="#":

                    if (neighbour.f, neighbour) not in self.opened:

                        self.updateCell(neighbour, node)
                        heappush(self.opened, (neighbour.f, neighbour))
                    elif node.g+neighbour.cost<neighbour.g:
                        self.updateCell(neighbour, node)
                        if neighbour in self.closed:
                            self.propagateImprovements(neighbour)


    def updateCell(self, neighbour, node):

        neighbour.parent = node

        neighbour.g= node.g+ neighbour.cost
        hCost = self.heuristic(neighbour)

        neighbour.f = neighbour.g+hCost



    def printPath(self, node):
        temp = node

        while(temp.parent.x!=self.start[0] or temp.parent.y!= self.start[1]):
            temp = temp.parent

            self.board[temp.x][temp.y] = '-'

        #Print the board to console

        board = ''
        for y in range(0, len(self.board)):
            row = ''
            for x in range(0, len(self.board[y])):

                if str(self.board[y][x]) == "-":
                    row += "-"
                elif (self.board[y][x].symbol =="A" or self.board[y][x].symbol=="B"):
                    row += self.board[y][x].symbol
                elif self.board[y][x] in self.closed:
                    row += "x"
                elif (self.board[y][x].f, self.board[y][x]) in self.opened:
                    row +="*"
                else:
                    row += str(self.board[y][x])
            board += row + '\n'
        print(board)

    def propagateImprovements(self, node):
        for barn in node.barn:
            if node.g+barn.cost<barn.g:
                barn.parent = node
                barn.g = node.g+barn.cost
                barn.f = barn.g+self.heuristic(barn)
                self.propagateImprovements(barn)


    def generateSuccessors(self, node):
        children = []
        x, y = node.x, node.y
        if x >0:
            children.append(self.board[x-1][y])
        if y >0:
            children.append(self.board[x][y-1])
        if x<self.gridHeight-1:
            children.append(self.board[x+1][y])
        if y<self.gridLength-1:
            children.append(self.board[x][y+1])
        return children







class Node:

    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        if cost=="w":
            self.cost = 100
        elif cost=="m":
            self.cost=50
        elif cost=="f":
            self.cost=10
        elif cost=="g":
            self.cost=5
        elif cost=="r":
            self.cost=1
        elif cost=="#":
            self.cost = cost
        else:
            self.cost = 1
        self.symbol = cost
        self.parent = None
        self.children = []
        self.g = 0
        self.h = 0
        self.f = 0


    def __eq__(self, other):
        return self.x==other.x and self.y==other.y

    def __lt__(self, other):
        return self.g - other.g

    def __repr__(self):
        return str(self.symbol)




if __name__ == '__main__':
    boards = glob.glob("boards/board*")

    for boardFile in boards:

        print(boardFile)
        board = Board(boardFile)
        board.bestFirstSearch()
