import copy
import pickle

letters = "abcdefgh"
numbers = "87654321"
def chess(game: str, move: str):
    try:#if file exists load board
        data = open(game, "rb")
        board = pickle.load(data)
        data.close()

    except FileNotFoundError:#else create new board
        board = Board()

    val = turn(board, move)#excecute move

    if val == True:
        if board.turns == False:
            strings = (board.strblack(), "Black's turn:")

        else:
            strings = (str(board), "White's turn:")

    else:
        if board.turns == True:
            strings = (board.strblack(), "Black's turn:")

        else:
            strings = (str(board), "White's turn:")
    # val = None
    # while val != "End":
    #      print(board)#white's perspective board
    #      val = turn(board, input("white's turn: "))
    #      while val == False:#waits until valid move is given
    #          val = turn(board, input("white's turn: "))
    #      board.turns = True

    #      print(board.strblack())#black's perspective board
    #      val = turn(board, input("black's turn: "))
    #      while val == False:#waits until valid move is given
    #          val = turn(board, input("black's turn: "))
    #      board.turns = False

    #saving board
    data = open(game, "wb")
    pickle.dump(board, data)
    data.close()

    return (board.result, val, strings)

class Piece:
    def __init__(self, color, pos):
        self.c = color
        self.p = pos

class King(Piece):
    def __init__(self, color, pos):
        self.check = False
        self.moved = False #for castling
        super().__init__(color, pos)

    def movementation(self, move: tuple, board, spos: tuple, npred: bool):
        if move in self.reach(board):#normal moves
            if self.c == False:#white
                if board.b[move[0]][move[1]].bcheck == False:#verifies if square is in check
                    if board.b[move[0]][move[1]].o != None:#verifies if square is occupied
                        if board.b[move[0]][move[1]].o.c == True:#verifies if piece on square is black
                            board.b[self.p[0]][self.p[1]].o = None#clears previous position
                            self.p = move#updates position of piece
                            board.b[move[0]][move[1]].o = self#updates ocupation of square
                            return True

                        else:
                            if npred:
                                board.result = spos[1] + " is occupied by a white piece"
                            return False

                    else:
                        board.b[self.p[0]][self.p[1]].o = None#clears previous position
                        self.p = move#updates position of piece
                        board.b[move[0]][move[1]].o = self#updates ocupation of square
                        return True
       
                else:
                    if npred:
                        board.result = "if King is moved to " + spos[1] + " he will be in check"
                    return False

            else:#black
                if board.b[move[0]][move[1]].wcheck == False:#verifies if square is in check
                    if board.b[move[0]][move[1]].o != None:#verifies if square is occupied
                        if board.b[move[0]][move[1]].o.c == False:#verifies if piece on square is white
                            board.b[self.p[0]][self.p[1]].o = None#clears previous position
                            self.p = move#updates position of piece
                            board.b[move[0]][move[1]].o = self#updates ocupation of square
                            return True

                        else:
                            if npred:
                                board.result = spos[1] + " is occupied by a black piece"
                            return False

                    else:
                        board.b[self.p[0]][self.p[1]].o = None#clears previous position
                        self.p = move#updates position of piece
                        board.b[move[0]][move[1]].o = self#updates ocupation of square
                        return True
       
                else:
                    if npred:
                        board.result = "if King is moved to " + spos[1] + " he will be in check"
                    return False

        elif self.moved == False and self.check == False:#castling
            if self.c == False:#if color white
                if move == (7, 6):#small castle
                    if board.b[7][5].bcheck == False and board.b[7][6].bcheck == False and board.b[7][5].o == None and board.b[7][6] and isinstance(board.b[7][7].o, Rook):
                        if board.b[7][7].o.c == False and board.b[7][7].o.moved == False:
                            board.b[self.p[0]][self.p[1]].o = None#clears previous position
                            self.p = move#updates position of piece
                            board.b[move[0]][move[1]].o = self#updates ocupation of square
                            board.b[7][5].o = board.b[7][7].o#updates ocupation of square
                            board.b[7][7].o = None#clears previous position
                            board.b[7][5].o.p = (7, 5)#updates position of piece
                            return True

                elif move == (7, 2):#big castle
                    if board.b[7][3].bcheck == False and board.b[7][2].bcheck == False and board.b[7][1].o == None and board.b[7][2].o == None and board.b[7][3] and isinstance(board.b[7][0].o, Rook):
                        if board.b[7][0].o.c == False and board.b[7][0].o.moved == False:
                            board.b[self.p[0]][self.p[1]].o = None#clears previous position
                            self.p = move#updates position of piece
                            board.b[move[0]][move[1]].o = self#updates ocupation of square
                            board.b[7][3].o = board.b[7][0].o#updates ocupation of square
                            board.b[7][0].o = None#clears previous position
                            board.b[7][3].o.p = (7, 3)#updates position of piece
                            return True

                return False
            else:# if color black
                if move == (0, 6):#small castle
                    if board.b[0][5].wcheck == False and board.b[0][6].wcheck == False and board.b[0][5].o == None and board.b[0][6] and isinstance(board.b[7][7].o, Rook):
                        if board.b[0][7].o.c == True and board.b[0][7].o.moved == False:
                            board.b[self.p[0]][self.p[1]].o = None#clears previous position
                            self.p = move#updates position of piece
                            board.b[move[0]][move[1]].o = self#updates ocupation of square
                            board.b[0][5].o = board.b[7][7].o#updates ocupation of square
                            board.b[0][7].o = None#clears previous position
                            board.b[0][5].o.p = (0, 5)#updates position of piece
                            return True

                elif move == (0, 2):#big castle
                    if board.b[0][3].wcheck == False and board.b[0][2].wcheck == False and board.b[0][1].o == None and board.b[0][2].o == None and board.b[0][3] and isinstance(board.b[0][0].o, Rook):
                        if board.b[0][0].o.c == True and board.b[0][0].o.moved == False:
                            board.b[self.p[0]][self.p[1]].o = None#clears previous position
                            self.p = move#updates position of piece
                            board.b[move[0]][move[1]].o = self#updates ocupation of square
                            board.b[0][3].o = board.b[0][0].o#updates ocupation of square
                            board.b[0][0].o = None#clears previous position
                            board.b[0][3].o.p = (0, 3)#updates position of piece
                            return True

                return False

        else:#invalid move
            if npred:
                board.result = spos[1] + " is an invalid position"
            return False

    def reach(self, board):
        r = []
        for i in range(self.p[0] - 1, self.p[0] + 2):
            for j in range(self.p[1] - 1, self.p[1] + 2):
                if -1 < i < 8 and -1 < j < 8 and not((i, j) == tuple(self.p)):
                    r.append((i, j))
        return r

class Queen(Piece):
    def movementation(self, move: tuple, board, spos: tuple, npred: bool):
        if move in self.reach(board):#valid position
            if board.b[move[0]][move[1]].o != None:#occupied
                if self.c == False:#white
                    if board.b[move[0]][move[1]].o.c == True:#checking color of piece occuping destination
                        board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                        self.p = move#updating piece's position
                        board.b[move[0]][move[1]].o = self#updating square's occupation
                        return True
                    else:
                        if npred:
                            board.result = "Can't capture own piece on " + spos[1]
                        return False
                else:#black
                    if board.b[move[0]][move[1]].o.c == False:#checking color of piece occuping destination
                        board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                        self.p = move#updating piece's position
                        board.b[move[0]][move[1]].o = self#updating square's occupation
                        return True

                    else:
                        if npred:
                            board.result = "Can't capture own piece on " + spos[1]
                        return False

            else:
                board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                self.p = move#updating piece's position
                board.b[move[0]][move[1]].o = self#updating square's occupation
                return True

        else:#invalid position
            if npred:
                board.result = spos[1] + " is an invalid position"
            return False

    def reach(self, board):
        r = []
        #rook range:
        #baixo
        for i in range(self.p[0] + 1, 8):
            if board.b[i][self.p[1]].o != None:
                r.append((i, self.p[1]))
                break
            r.append((i, self.p[1]))
        #cima
        for i in range(self.p[0] - 1, -1, -1):
            if board.b[i][self.p[1]].o != None:
                r.append((i, self.p[1]))
                break
            r.append((i, self.p[1]))
        #direita
        for i in range(self.p[1] + 1, 8):
            if board.b[self.p[0]][i].o != None:
                r.append((self.p[0], i))
                break
            r.append((self.p[0], i))
        #esquerda
        for i in range(self.p[1] - 1, -1, -1):
            if board.b[self.p[0]][i].o != None:
                r.append((self.p[0], i))
                break
            r.append((self.p[0], i))

        #bishop range:
        #direita-baixo
        for i, j in zip(range(self.p[0] + 1, 8), range(self.p[1] + 1, 8)):
            if board.b[i][j].o != None:
                r.append((i, j))
                break
            r.append((i, j))
        #esquerda-baixo
        for i, j in zip(range(self.p[0] + 1, 8), range(self.p[1] - 1, -1, -1)):
            if board.b[i][j].o != None:
                r.append((i, j))
                break
            r.append((i, j))
        #esquerda-cima
        for i, j in zip(range(self.p[0] - 1, -1, -1), range(self.p[1] - 1, -1, -1)):
            if board.b[i][j].o != None:
                r.append((i, j))
                break
            r.append((i, j))
        #direita-cima
        for i, j in zip(range(self.p[0] - 1, -1, -1), range(self.p[1] + 1, 8)):
            if board.b[i][j].o != None:
                r.append((i, j))
                break
            r.append((i, j))
        
        return r

class Bishop(Piece):
    def movementation(self, move: tuple, board, spos: tuple, npred: bool):
        if move in self.reach(board):#valid position
            if board.b[move[0]][move[1]].o != None:#occupied
                if self.c == False:#white
                    if board.b[move[0]][move[1]].o.c == True:#checking color of piece occuping destination
                        board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                        self.p = move#updating piece's position
                        board.b[move[0]][move[1]].o = self#updating square's occupation
                        return True
                    else:
                        if npred:
                            board.result = "Can't capture own piece on " + spos[1]
                        return False
                else:#black
                    if board.b[move[0]][move[1]].o.c == False:#checking color of piece occuping destination
                        board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                        self.p = move#updating piece's position
                        board.b[move[0]][move[1]].o = self#updating square's occupation
                        return True

                    else:
                        if npred:
                            board.result = "Can't capture own piece on " + spos[1]
                        return False

            else:
                board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                self.p = move#updating piece's position
                board.b[move[0]][move[1]].o = self#updating square's occupation
                return True

        else:#invalid position
            if npred:
                board.result = spos[1] + " is an invalid position"
            return False

    def reach(self, board):
        r = []
        #direita-baixo
        for i, j in zip(range(self.p[0] + 1, 8), range(self.p[1] + 1, 8)):
            if board.b[i][j].o != None:
                r.append((i, j))
                break
            r.append((i, j))
        #esquerda-baixo
        for i, j in zip(range(self.p[0] + 1, 8), range(self.p[1] - 1, -1, -1)):
            if board.b[i][j].o != None:
                r.append((i, j))
                break
            r.append((i, j))
        #esquerda-cima
        for i, j in zip(range(self.p[0] - 1, -1, -1), range(self.p[1] - 1, -1, -1)):
            if board.b[i][j].o != None:
                r.append((i, j))
                break
            r.append((i, j))
        #direita-cima
        for i, j in zip(range(self.p[0] - 1, -1, -1), range(self.p[1] + 1, 8)):
            if board.b[i][j].o != None:
                r.append((i, j))
                break
            r.append((i, j))
        
        return r
    
class Knight(Piece):
    def movementation(self, move: tuple, board, spos: tuple, npred: bool):
        if move in self.reach(board):#valid position
            if board.b[move[0]][move[1]].o != None:#occupied
                if self.c == False:#white
                    if board.b[move[0]][move[1]].o.c == True:#checking color of piece occuping destination
                        board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                        self.p = move#updating piece's position
                        board.b[move[0]][move[1]].o = self#updating square's occupation
                        return True
                    else:
                        if npred:
                            board.result = "Can't capture own piece on " + spos[1]
                        return False
                else:#black
                    if board.b[move[0]][move[1]].o.c == False:#checking color of piece occuping destination
                        board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                        self.p = move#updating piece's position
                        board.b[move[0]][move[1]].o = self#updating square's occupation
                        return True

                    else:
                        if npred:
                            board.result = "Can't capture own piece on " + spos[1]
                        return False

            else:
                board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                self.p = move#updating piece's position
                board.b[move[0]][move[1]].o = self#updating square's occupation
                return True

        else:#invalid position
            if npred:
                board.result = spos[1] + " is an invalid position"
            return False

    def reach(self, board):
        r = []
        l = [(self.p[0] + 2, self.p[1] - 1), (self.p[0] + 2, self.p[1] + 1), (self.p[0] - 1, self.p[1] + 2), (self.p[0] + 1, self.p[1] + 2), (self.p[0] - 2, self.p[1] + 1), (self.p[0] - 2, self.p[1] - 1), (self.p[0] + 1, self.p[1] - 2), (self.p[0] - 1, self.p[1] - 2)]
        for i in l:
            if 0 <= i[0] <= 7 and 0 <= i[1] <= 7:
                r.append(i)
        return r

class Rook(Piece):
    def __init__(self, color, pos):
        self.moved = False #for castling
        super().__init__(color, pos)

    def movementation(self, move: tuple, board, spos: tuple, npred: bool):
        if move in self.reach(board):#valid position
            if board.b[move[0]][move[1]].o != None:#occupied
                if self.c == False:#white
                    if board.b[move[0]][move[1]].o.c == True:#checking color of piece occuping destination
                        board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                        self.p = move#updating piece's position
                        board.b[move[0]][move[1]].o = self#updating square's occupation
                        return True
                    else:
                        if npred:
                            board.result = "Can't capture own piece on " + spos[1]
                        return False
                else:#black
                    if board.b[move[0]][move[1]].o.c == False:#checking color of piece occuping destination
                        board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                        self.p = move#updating piece's position
                        board.b[move[0]][move[1]].o = self#updating square's occupation
                        return True

                    else:
                        if npred:
                            board.result = "Can't capture own piece on " + spos[1]
                        return False

            else:
                board.b[self.p[0]][self.p[1]].o = None#freeing previous spot
                self.p = move#updating piece's position
                board.b[move[0]][move[1]].o = self#updating square's occupation
                return True

        else:#invalid position
            if npred:
                board.result = spos[1] + " is an invalid position"
            return False

    def reach(self, board):
        r = []
        #baixo
        for i in range(self.p[0] + 1, 8):
            if board.b[i][self.p[1]].o != None:
                r.append((i, self.p[1]))
                break
            r.append((i, self.p[1]))
        #cima
        for i in range(self.p[0] - 1, -1, -1):
            if board.b[i][self.p[1]].o != None:
                r.append((i, self.p[1]))
                break
            r.append((i, self.p[1]))
        #direita
        for i in range(self.p[1] + 1, 8):
            if board.b[self.p[0]][i].o != None:
                r.append((self.p[0], i))
                break
            r.append((self.p[0], i))
        #esquerda
        for i in range(self.p[1] - 1, -1, -1):
            if board.b[self.p[0]][i].o != None:
                r.append((self.p[0], i))
                break
            r.append((self.p[0], i))
        return r

class Pawn(Piece):
    def __init__(self, color, pos):
        self.da = False#double advance for en passant
        self.pro = False#promotion
        super().__init__(color, pos)

    def movementation(self, move: tuple, board, spos: tuple, npred: bool):#to do promotion
        if self.c == False:#white
            if move[0] < self.p[0]:#is moving forward
                if self.p[0] - move[0] == 1:#1 square forward
                    if self.p[1] == move[1]:#move forward
                        if board.b[move[0]][move[1]].o == None:#not occupied
                            board.b[self.p[0]][self.p[1]].o = None#free's actual position
                            board.b[move[0]][move[1]].o = self#updates occupation of new position
                            self.p = move#updates piece's position
                            if move[0] == 0:
                                self.pro = True

                            return True

                        else:#occupied
                            if npred:
                                board.result = spos[1] + " is already occupied"
                            return False

                    elif (self.p[1] - move[1] == 1 or self.p[1] - move[1] == -1):#capturing
                        if board.b[move[0]][move[1]].o != None:#normal capturing
                            if board.b[move[0]][move[1]].o.c == True:#piece on new position is black
                                board.b[self.p[0]][self.p[1]].o = None#free's actual position
                                board.b[move[0]][move[1]].o = self#updates occupation of new position
                                self.p = move#updates piece's position
                                if move[0] == 0:
                                    self.pro = True

                                return True

                            else:#piece on new position is white
                                if npred:
                                    board.result = " Can't capture own piece"
                                return False
                        
                        elif isinstance(board.b[move[0] + 1][move[1]].o, Pawn):#en passant
                            if board.b[move[0] + 1][move[1]].o.c == True and board.b[move[0] + 1][move[1]].o.da == True:
                                board.b[move[0] + 1][move[1]].o = None
                                board.b[self.p[0]][self.p[1]].o = None#free's actual position
                                board.b[move[0]][move[1]].o = self#updates occupation of new position
                                self.p = move#updates piece's position
                                return True

                            else:#invalid position
                                if npred:
                                    board.result = spos[1] + " is an invalid position"
                                return False

                        else:#invalid position
                            if npred:
                                board.result = spos[1] + " is an invalid position"
                            return False

                elif move[0] == 4 and self.p[0] == 6 and move[1] == self.p[1] and board.b[5][move[1]].o == None and board.b[4][move[1]].o == None:#double advancement
                    board.b[self.p[0]][self.p[1]].o = None#free's actual position
                    board.b[move[0]][move[1]].o = self#updates occupation of new position
                    self.p = move#updates piece's position
                    self.da = True#double advance = True
                    return self

                else:#invalid position
                    if npred:
                        board.result = spos[1] + "is an invalid postion"
                    return False
            
            else:#invalid position
                if npred:
                    board.result = spos[1] + " is an invalid position"
                return False

        else:#black
            if move[0] > self.p[0]:#is moving forward
                if self.p[0] - move[0] == -1:#1 square forward
                    if self.p[1] == move[1]:#move forward
                        if board.b[move[0]][move[1]].o == None:#not occupied
                            board.b[self.p[0]][self.p[1]].o = None#free's actual position
                            board.b[move[0]][move[1]].o = self#updates occupation of new position
                            self.p = move#updates piece's position
                            if move[0] == 7:
                                self.pro = True

                            return True

                        else:#occupied
                            if npred:
                                board.result = spos[1] + " is already occupied"
                            return False

                    elif (self.p[1] - move[1] == 1 or self.p[1] - move[1] == -1):#capturing
                        if board.b[move[0]][move[1]].o != None:#normal capturing
                            if board.b[move[0]][move[1]].o.c == False:#piece on new position is white
                                board.b[self.p[0]][self.p[1]].o = None#free's actual position
                                board.b[move[0]][move[1]].o = self#updates occupation of new position
                                self.p = move#updates piece's position
                                if move[0] == 7:
                                    self.pro = True

                                return True

                            else:#piece on new position is black
                                if npred:
                                    board.result = "Can't capture own piece"
                                return False
                        
                        elif isinstance(board.b[move[0] - 1][move[1]].o, Pawn):#en passant
                            if board.b[move[0] - 1][move[1]].o.c == True and board.b[move[0] - 1][move[1]].o.da == True:
                                board.b[move[0] - 1][move[1]].o = None
                                board.b[self.p[0]][self.p[1]].o = None#free's actual position
                                board.b[move[0]][move[1]].o = self#updates occupation of new position
                                self.p = move#updates piece's position
                                return True

                            else:#invalid position
                                if npred:
                                    board.result = spos[1] + " is an invalid position"
                                return False

                        else:#invalid position
                            if npred:
                                board.result = spos[1] + " is an invalid position"
                            return False
                    else:#invalid position
                        if npred:
                            board.result = spos[1] + " is an invalid position"
                        return False

                elif move[0] == 3 and self.p[0] == 1 and move[1] == self.p[1] and board.b[2][move[1]].o == None and board.b[3][move[1]].o == None:#double advancement
                    board.b[self.p[0]][self.p[1]].o = None#free's actual position
                    board.b[move[0]][move[1]].o = self#updates occupation of new position
                    self.p = move#updates piece's position
                    self.da = True#double advance = True
                    return self

                else:#invalid position
                    if npred:
                        board.result = spos[1] + " is an invalid postion"
                    return False
            
            else:#invalid position
                if npred:
                    board.result = spos[1] + " is an invalid position"
                return False

    def reach(self, board):
        r = []
        if self.c == False:
            if self.p[1] != 0:
                r.append((self.p[0] - 1, self.p[1] - 1))
            
            if self.p[1] != 7:
                r.append((self.p[0] - 1, self.p[1] + 1))

        else:
            if self.p[1] != 0:
                r.append((self.p[0] + 1, self.p[1] - 1))
            
            if self.p[1] != 7:
                r.append((self.p[0] + 1, self.p[1] + 1))

        return r

class Square:
    def __init__(self, color, occupied):
        self.c = color
        self.o = occupied
        self.wcheck = False #check in favor of white
        self.bcheck = False #check in favor of black

class Board:
    def __init__(self):
        self.ep = False
        self.ep1 = False
        self.movements = []
        self.turns = False
        #creation of all the pieces
        self.br0 = Rook(True, [0, 0]); self.bkn0 = Knight(True, [0, 1]); self.bb0 = Bishop(True, [0,2]); self.bq = Queen(True, [0, 3]); self.bk = King(True, [0, 4]); self.bb1 = Bishop(True, [0, 5]); self.bkn1 = Knight(True, [0, 6]); self.br1 = Rook(True, [0, 7])
        self.bp0 = Pawn(True, [1, 0]); self.bp1 = Pawn(True, [1, 1]); self.bp2 = Pawn(True, [1, 2]); self.bp3 = Pawn(True, [1, 3]); self.bp4 = Pawn(True, [1, 4]); self.bp5 = Pawn(True, [1, 5]); self.bp6 = Pawn(True, [1, 6]); self.bp7 = Pawn(True, [1, 7])
        self.wp0 = Pawn(False, [6, 0]); self.wp1 = Pawn(False, [6, 1]); self.wp2 = Pawn(False, [6, 2]); self.wp3 = Pawn(False, [6, 3]); self.wp4 = Pawn(False, [6, 4]); self.wp5 = Pawn(False, [6, 5]); self.wp6 = Pawn(False, [6, 6]); self.wp7 = Pawn(False, [6, 7])
        self.wr0 = Rook(False, [7, 0]); self.wkn0 = Knight(False, [7, 1]); self.wb0 = Bishop(False, [7,2]); self.wq = Queen(False, [7, 3]); self.wk = King(False, [7, 4]); self.wb1 = Bishop(False, [7, 5]); self.wkn1 = Knight(False, [7, 6]); self.wr1 = Rook(False, [7, 7])
        #creation of all the squares
        self.a8 = Square(False, self.br0); self.b8 = Square(True, self.bkn0); self.c8 = Square(False, self.bb0); self.d8 = Square(True, self.bq); self.e8 = Square(False, self.bk); self.f8 = Square(True, self.bb1); self.g8 = Square(False, self.bkn1); self.h8 = Square(True, self.br1)
        self.a7 = Square(True, self.bp0); self.b7 = Square(False, self.bp1); self.c7 = Square(True, self.bp2); self.d7 = Square(False, self.bp3); self.e7 = Square(True, self.bp4); self.f7 = Square(False, self.bp5); self.g7 = Square(True, self.bp6); self.h7 = Square(False, self.bp7)
        self.a6 = Square(False, None); self.b6 = Square(True, None); self.c6 = Square(False, None); self.d6 = Square(True, None); self.e6 = Square(False, None); self.f6 = Square(True, None); self.g6 = Square(False, None); self.h6 = Square(True, None)
        self.a5 = Square(True, None); self.b5 = Square(False, None); self.c5 = Square(True, None); self.d5 = Square(False, None); self.e5 = Square(True, None); self.f5 = Square(False, None); self.g5 = Square(True, None); self.h5 = Square(False, None)
        self.a4 = Square(False, None); self.b4 = Square(True, None); self.c4 = Square(False, None); self.d4 = Square(True, None); self.e4 = Square(False, None); self.f4 = Square(True, None); self.g4 = Square(False, None); self.h4 = Square(True, None)
        self.a3 = Square(True, None); self.b3 = Square(False, None); self.c3 = Square(True, None); self.d3 = Square(False, None); self.e3 = Square(True, None); self.f3 = Square(False, None); self.g3 = Square(True, None); self.h3 = Square(False, None)
        self.a2 = Square(False, self.wp0); self.b2 = Square(True, self.wp1); self.c2 = Square(False, self.wp2); self.d2 = Square(True, self.wp3); self.e2 = Square(False, self.wp4); self.f2 = Square(True, self.wp5); self.g2 = Square(False, self.wp6); self.h2 = Square(True, self.wp7)
        self.a1 = Square(True, self.wr0); self.b1 = Square(False, self.wkn0); self.c1 = Square(True, self.wb0); self.d1 = Square(False, self.wq); self.e1 = Square(True, self.wk); self.f1 = Square(False, self.wb1); self.g1 = Square(True, self.wkn1); self.h1 = Square(False, self.wr1)
        #creation of the board
        self.b = [[self.a8, self.b8, self.c8, self.d8, self.e8, self.f8, self.g8, self.h8], [self.a7, self.b7, self.c7, self.d7, self.e7, self.f7, self.g7, self.h7], [self.a6, self.b6, self.c6, self.d6, self.e6, self.f6, self.g6, self.h6], [self.a5, self.b5, self.c5, self.d5, self.e5, self.f5, self.g5, self.h5], [self.a4, self.b4, self.c4, self.d4, self.e4, self.f4, self.g4, self.h4], [self.a3, self.b3, self.c3, self.d3, self.e3, self.f3, self.g3, self.h3], [self.a2, self.b2, self.c2, self.d2, self.e2, self.f2, self.g2, self.h2], [self.a1, self.b1, self.c1, self.d1, self.e1, self.f1, self.g1, self.h1]]
        
        self.result = None #match result

    def __str__(self):
        """returns printable version of white's perspective board"""
        out = ""
        wletters = ["▫️", "A ", "  B ", "  C ", "  D ", "  E ", "  F ", "  G ", "  H"]
        n = 8
        for i in wletters:
            out += str(i)
        out += "\n"
        for lists in self.b:
            out += str(n) + "  "
            for element in lists:
                if element.o == None:
                    if element.c == False:
                        out += "⬜"
                    else:
                        out += "⬛"

                elif isinstance(element.o, King):
                    if element.o.c == False:
                        out += "🤴🏻"
                    else:
                        out += "🤴🏿"

                elif isinstance(element.o, Queen):
                    if element.o.c == False:
                        out += "👸🏻"
                    else:
                        out += "👸🏿"

                elif isinstance(element.o, Bishop):
                    if element.o.c == False:
                        out += "🧙🏻‍♂️"
                    else:
                        out += "🧙🏿‍♂️"

                elif isinstance(element.o, Knight):
                    if element.o.c == False:
                        out += "🦄"
                    else:
                        out += "🐴"

                elif isinstance(element.o, Rook):
                    if element.o.c == False:
                        out += "💂🏻"
                    else:
                        out += "💂🏿"

                elif isinstance(element.o, Pawn):
                    if element.o.c == False:
                        out += "🧑🏻‍🌾"
                    else:
                        out += "🧑🏿‍🌾"
            out += "\n"
            n -= 1
        return out

    def strblack(self):
        """returns printable version of black's perspective board"""
        out = ""
        bboard = copy.deepcopy(self.b)
        bletters = ["▪️", "H ", "  G ", "  F ", "  E ", "  D ", "  C ", "  B ", "  A"]
        n = 1
        bboard.reverse()
        for i in bletters:
            out += str(i)
        out += "\n"
        for lists in bboard:
            lists.reverse()
            out += str(n) + "  "
            for element in lists:
                if element.o == None:
                    if element.c == False:
                        out += "⬜"
                    else:
                        out += "⬛"

                elif isinstance(element.o, King):
                    if element.o.c == False:
                        out += "🤴🏻"
                    else:
                        out += "🤴🏿"

                elif isinstance(element.o, Queen):
                    if element.o.c == False:
                        out += "👸🏻"
                    else:
                        out += "👸🏿"

                elif isinstance(element.o, Bishop):
                    if element.o.c == False:
                        out += "🧙🏻‍♂️"
                    else:
                        out += "🧙🏿‍♂️"

                elif isinstance(element.o, Knight):
                    if element.o.c == False:
                        out += "🦄"
                    else:
                        out += "🐴"

                elif isinstance(element.o, Rook):
                    if element.o.c == False:
                        out += "💂🏻"
                    else:
                        out += "💂🏿"

                elif isinstance(element.o, Pawn):
                    if element.o.c == False:
                        out += "🧑🏻‍🌾"
                    else:
                        out += "🧑🏿‍🌾"
            out += "\n"
            n += 1
        return out

    def __contains__(self, item: str):
        """verifies if item is in board, item must be in lowercase"""

        if isinstance(item, str):
            for lists in self.b:
                for squares in lists:
                    if str(squares) == item:
                        return True
            return False
        
        else:
            self.result = "item must be type string"
            return None

    def moves(self, apos: tuple, dpos: tuple, spos: tuple, npred = True):
        """moves the pieces if movements and checks if the moves are valid updates the board"""
        #excecute movements
        if isinstance(self.b[apos[0]][apos[1]].o, King):
            val = self.b[apos[0]][apos[1]].o.movementation(dpos, self, spos, npred)

        elif isinstance(self.b[apos[0]][apos[1]].o, Queen):
            val = self.b[apos[0]][apos[1]].o.movementation(dpos, self, spos, npred)

        elif isinstance(self.b[apos[0]][apos[1]].o, Bishop):
            val = self.b[apos[0]][apos[1]].o.movementation(dpos, self, spos, npred)

        elif isinstance(self.b[apos[0]][apos[1]].o, Knight):
            val = self.b[apos[0]][apos[1]].o.movementation(dpos, self, spos, npred)

        elif isinstance(self.b[apos[0]][apos[1]].o, Rook):
            val = self.b[apos[0]][apos[1]].o.movementation(dpos, self, spos, npred)

        elif isinstance(self.b[apos[0]][apos[1]].o, Pawn):
            val = self.b[apos[0]][apos[1]].o.movementation(dpos, self, spos, npred)
            if val == True:
                if self.b[dpos[0]][dpos[1]].o.pro == True:
                    choice = input("1: 👸   2: 💂‍♂️\n3: 🧙‍♂️   4: 🐴")
                    while choice not in "1234":
                        choice = input("1: 👸   2: 💂‍♂️\n3: 🧙‍♂️   4: 🐴")

                    if choice == "1":
                        self.b[dpos[0]][dpos[1]].o = Queen(self.b[dpos[0]][dpos[1]].o.c, self.b[dpos[0]][dpos[1]].o.p)

                    elif choice == "2":
                        self.b[dpos[0]][dpos[1]].o = Rook(self.b[dpos[0]][dpos[1]].o.c, self.b[dpos[0]][dpos[1]].o.p)

                    elif choice == "3":
                        self.b[dpos[0]][dpos[1]].o = Bishop(self.b[dpos[0]][dpos[1]].o.c, self.b[dpos[0]][dpos[1]].o.p)

                    else:
                        self.b[dpos[0]][dpos[1]].o = Knight(self.b[dpos[0]][dpos[1]].o.c, self.b[dpos[0]][dpos[1]].o.p)
            
            elif isinstance(val, Pawn):
                self.ep1 = val
                val = True

        else:
            self.result = "There is no piece at " + spos[0]
            val = False
        #saves movements
        self.movements.append(spos)

        #updates en passant possibilities
        if isinstance(self.ep, Pawn):
            self.ep.da = False
            self.ep = self.ep1

        #updates board
        #sets wcheck and bcheck to False
        for i in self.b:
            for j in i:
                j.wcheck = False
                j.bcheck = False

        #updates wcheck and bcheck with the new values
        for i in self.b:
            for j in i:
                if j.o != None:
                    if j.o.c == False:
                        for x in j.o.reach(self):
                            self.b[x[0]][x[1]].wcheck = True

                    else:
                        for x in j.o.reach(self):
                            self.b[x[0]][x[1]].bcheck = True

        #updates kings checks
        if self.b[self.wk.p[0]][self.wk.p[1]].bcheck == True:
            self.wk.check = True

        if self.b[self.bk.p[0]][self.bk.p[1]].wcheck == True:
            self.bk.check = True

        #checks if king is in check after movement
        if (self.turns == False and self.wk.check == True) or (self.turns == True and self.bk.check == True):
            self.result = "Your king is in check"
            val = False

        #analises all possible movements for the next turn and determines if draws or checkmates
        if npred and val:
            valm = False
            pboard = copy.deepcopy(self)

            #5 repetitive moves
            if len(self.movements) >= 10:
                if self.movements[-1] == self.movements[-3][::-1] == self.movements[-5] == self.movements[-7][::-1] == self.movements[-9] and self.movements[-2] == self.movements[-4][::-1] == self.movements[-6] == self.movements[-8][::-1] == self.movements[-10]:
                    self.result = "Last 5 moves where identical, Draw"
                    return "End"

            #deadpositions
            wpieces = []
            bpieces = []
            for i in self.b:
                for j in i:
                    if j.o != None:
                        if j.o.c == False:
                            wpieces.append(j.o)
                        
                        else:
                            bpieces.append(j.o)
            winsuf = True
            wknight = True
            wbishopc0 = False
            wbishopc1 = False
            binsuf = False
            bknight = False
            bbishopc0 = False
            bbishopc1 = False
            if len(wpieces) <= 3 and len(bpieces) <= 3:
                for i in wpieces:#white
                    if not (isinstance(i, King) or isinstance(i, Bishop) or isinstance(i, Knight)):
                        winsuf = False
                        break

                    elif isinstance(i, Bishop):
                        if self.b[i.p[0]][i.p[1]].c == False:
                            wbishopc0 = True

                        else:
                            wbishopc1 = True

                    elif isinstance(i, Knight):
                        wknight = True
                    
                if (wknight and (wbishopc0 or wbishopc1)) or (wbishopc0 and wbishopc1):
                    winsuf = False
                
                for i in bpieces:#black
                    if not (isinstance(i, King) or isinstance(i, Bishop) or isinstance(i, Knight)):
                        binsuf = False
                        break

                    elif isinstance(i, Bishop):
                        if self.b[i.p[0]][i.p[1]].c == False:
                            bbishopc0 = True

                        else:
                            bbishopc1 = True

                    elif isinstance(i, Knight):
                        bknight = True
                    
                if (bknight and (bbishopc0 or bbishopc1)) or (bbishopc0 and bbishopc1):
                    binsuf = False

                if winsuf and binsuf:
                    self.result = "entered a dead position, Draw"
                    return "End"

            #other cases
            if self.turns == False:#black's turn prediction
                for i in pboard.b:
                    for j in i:
                        if j.o != None:
                            if j.o.c == True:                                      
                                if isinstance(j.o, Pawn):
                                    for i in ((j.o.p[0] + 1, j.o.p[1]), (j.o.p[0] + 1, j.o.p[1] + 1), (j.o.p[0] + 1, j.o.p[0] - 1), (j.o.p[0] + 2, j.o.p[1])):
                                        nspos = (letters[j.o.p[1]] + numbers[j.o.p[0]], letters[i[1]] + numbers[i[0]])
                                        if pboard.moves(j.o.p, i, nspos, npred = False):
                                            valm = True
                                            break

                                else:
                                    possibilities = j.o.reach(pboard)                                    
                                    for i in possibilities:
                                        nspos = (letters[j.o.p[1]] + numbers[j.o.p[0]], letters[i[1]] + numbers[i[0]])
                                        if pboard.moves(j.o.p, i, nspos, npred = False):
                                            valm = True
                                            break
                        if valm:
                            break

                    if valm:
                        break

                if self.bk.check == True and valm == False:
                    self.result = "Checkmate, 🏆🤴🏻"
                    return "End"

                elif valm == False:
                    self.result = "No more possible moves for black, Draw"
                    return "End"

            else:#white's turn prediction
                for i in pboard.b:
                    for j in i:
                        if j.o != None:
                            if j.o.c == False:                                      
                                if isinstance(j.o, Pawn):
                                    for i in ((j.o.p[0] - 1, j.o.p[1]), (j.o.p[0] - 1, j.o.p[1] + 1), (j.o.p[0] - 1, j.o.p[0] - 1), (j.o.p[0] - 2, j.o.p[1])):
                                        nspos = (letters[j.o.p[1]] + numbers[j.o.p[0]], letters[i[1]] + numbers[i[0]])
                                        if pboard.moves(j.o.p, i, nspos, npred = False):
                                            valm = True
                                            break

                                else:
                                    possibilities = j.o.reach(pboard)                                    
                                    for i in possibilities:
                                        nspos = (letters[j.o.p[1]] + numbers[j.o.p[0]], letters[i[1]] + numbers[i[0]])
                                        if pboard.moves(j.o.p, i, nspos, npred = False):
                                            valm = True
                                            break
                        if valm:
                            break

                    if valm:
                        break
                
                if self.wk.check == True and valm == False:
                    self.result = "Checkmate, 🏆🤴🏿"
                    return "End"

                elif valm == False:
                    self.result = "No more possible moves for white, Draw"
                    return "End"

        return val

def turn(board: Board, move: str):
    """if move is valid: excecutes the moves and returns True. else: doesnt excecute the moves and returns False"""

    if not isinstance(move, str):#verifies if move is a string
        board.result = "input must be like example \"e2 e4\"\n"
        return False

    move.lower()#turns move into lowercase
    if move == "draw":
        if len(board.movements) >= 6:
                if board.movements[-1] == board.movements[-3][::-1] == board.movements[-5] and board.movements[-2] == board.movements[-4][::-1] == board.movements[-6]:
                    board.result = "Last 5 moves where identical, Draw"
                    return "End"

        else:
            response = input("a: accept\nb: reject")
            if response == "a":
                board.result = "Draw"
                return "End"

            else:
                board.result = "request rejected, game continues"
                return False

    elif move == "resign":
        if board.turns == False:
            board.result = "White resigns, 🏆🤴🏿"
        
        else:
            board.result = "Black resings, 🏆🤴🏻"

        return "End"

    else:
        spos = move.split()#positions in string format

        if (spos[0][0] not in letters and spos[0][1] not in numbers) or (spos[1][0] not in letters and spos[1][1] not in numbers):
            if spos[0][0] not in letters and spos[0][1] not in numbers:
                board.result = spos[0] + " is not on the board\n"
            
            if spos[1][0] not in letters and spos[1][1] not in numbers:
                board.result = spos[1] + " is not on the board\n"

            return False

        apos = (numbers.index(spos[0][1]), letters.index(spos[0][0]))#old position in index format
        dpos = (numbers.index(spos[1][1]), letters.index(spos[1][0]))#new position in index format

        oldboard = copy.deepcopy(board)#saves old board, so that if move turns out to be invalid it can be undone

        val = board.moves(apos, dpos, spos, oldboard)
        if val == False:
            board = oldboard
        
        return val

chess("", "")