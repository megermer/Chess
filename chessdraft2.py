from enum import Enum

class Side(Enum):
    W = 0
    B = 1
    
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.timer = ...

class Board:
    def __init__(self):
        self.pieces = dict(a1=Rook(Side.W),   a2=Pawn(Side.W), a3=Empty(), a4=Empty(), a5=Empty(), a6=Empty(), a7=Pawn(Side.B), a8=Rook(Side.B),
                           b1=Knight(Side.W), b2=Pawn(Side.W), b3=Empty(), b4=Empty(), b5=Empty(), b6=Empty(), b7=Pawn(Side.B), b8=Knight(Side.B),
                           c1=Bishop(Side.W), c2=Pawn(Side.W), c3=Empty(), c4=Empty(), c5=Empty(), c6=Empty(), c7=Pawn(Side.B), c8=Bishop(Side.B),
                           d1=Queen(Side.W),  d2=Pawn(Side.W), d3=Empty(), d4=Empty(), d5=Empty(), d6=Empty(), d7=Pawn(Side.B), d8=Queen(Side.B),
                           e1=King(Side.W),   e2=Pawn(Side.W), e3=Empty(), e4=Empty(), e5=Empty(), e6=Empty(), e7=Pawn(Side.B), e8=King(Side.B),
                           f1=Bishop(Side.W), f2=Pawn(Side.W), f3=Empty(), f4=Empty(), f5=Empty(), f6=Empty(), f7=Pawn(Side.B), f8=Bishop(Side.B),
                           g1=Knight(Side.W), g2=Pawn(Side.W), g3=Empty(), g4=Empty(), g5=Empty(), g6=Empty(), g7=Pawn(Side.B), g8=Knight(Side.B),
                           h1=Rook(Side.W),   h2=Pawn(Side.W), h3=Empty(), h4=Empty(), h5=Empty(), h6=Empty(), h7=Pawn(Side.B), h8=Rook(Side.B))
        self.captured = []
    def move(self, start_pos, end_pos):
        if isinstance(self.pieces[end_pos], Empty) == False:
            self.captured.append(self.pieces[end_pos])
        self.pieces[end_pos] = self.pieces[start_pos]
        self.pieces[start_pos] = Empty()

class Piece:
    def __init__(self, side):
        self.has_moved = False
    def legal_moves(self):
        pass
    
class King(Piece):
    def __init__(self, side):
        self.image = ""
        self.value = None
        self.moveset = ...

class Queen(Piece):
    def __init__(self, side):
        self.image = ""
        self.value = 7

class Rook(Piece):
    def __init__(self, side):
        self.image = ""
        self.value = 5

class Bishop(Piece):
    def __init__(self, side):
        self.image = ""
        self.value = 3

class Knight(Piece):
    def __init__(self, side):
        self.image = ""
        self.value = 3

class Pawn(Piece):
    def __init__(self, side):
        self.image = ""
        self.value = 1

class Empty:
    pass