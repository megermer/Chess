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
        self.pieces = dict(a1=Rook(W),   a2=Pawn(W), a3=Empty(), a4=Empty(), a5=Empty(), a6=Empty(), a7=Pawn(B), a8=Rook(B),
                           b1=Knight(W), b2=Pawn(W), b3=Empty(), b4=Empty(), b5=Empty(), b6=Empty(), b7=Pawn(B), b8=Knight(B),
                           c1=Bishop(W), c2=Pawn(W), c3=Empty(), c4=Empty(), c5=Empty(), c6=Empty(), c7=Pawn(B), c8=Bishop(B),
                           d1=Queen(W),  d2=Pawn(W), d3=Empty(), d4=Empty(), d5=Empty(), d6=Empty(), d7=Pawn(B), d8=Queen(B),
                           e1=King(W),   e2=Pawn(W), e3=Empty(), e4=Empty(), e5=Empty(), e6=Empty(), e7=Pawn(B), e8=King(B),
                           f1=Bishop(W), f2=Pawn(W), f3=Empty(), f4=Empty(), f5=Empty(), f6=Empty(), f7=Pawn(B), f8=Bishop(B),
                           g1=Knight(W), g2=Pawn(W), g3=Empty(), g4=Empty(), g5=Empty(), g6=Empty(), g7=Pawn(B), g8=Knight(B),
                           h1=Rook(W),   h2=Pawn(W), h3=Empty(), h4=Empty(), h5=Empty(), h6=Empty(), h7=Pawn(B), h8=Rook(B))
    def move(piece, position):
        pass

class Piece:
    def __init__(self, side):
        self.has_moved = False
    def legal_moves(self):
        pass
    
class King(Piece):
    def __init__(self, side):
        self.image = ""
        self.value = ?
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

class Empty(Piece):
    pass