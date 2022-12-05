# Meg Ermer and Kelvin Feitosa
# CPTR 215 A, Final Project
# History:
#	4 Dec: Added front end
# Sources:
#	Find key given value in handle_click: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/

from enum import Enum
import sys
#from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QLabel
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess")
        
        self.game = ChessGame()
            
        # Styling:
        white = "#C19B6C"
        black = "#312624"
            
        self.squares = dict()
        for number in "87654321":
            for letter in "abcdefgh":
                current_square = f"{letter}{number}"
                self.squares[current_square] = QPushButton("")
                self.squares[current_square].setFixedSize(45, 45)
                self.squares[current_square].clicked.connect(self.handle_click)
                self.squares[current_square].setText(self.game.board.pieces[current_square].image)
                if (ord(letter) + int(number)) % 2 == 0:
                    self.squares[current_square].setStyleSheet(f"background-color: {black}")
                else:
                    self.squares[current_square].setStyleSheet(f"background-color: {white}")
                
            
        layout = QGridLayout()
        column = 0
        row = 0
        for key in self.squares:
            layout.addWidget(self.squares[key], row, column)
            if column == 7:
                row += 1
                column = 0
            else:
                column += 1
        
                
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def handle_click(self):
        clicked_square = self.sender()
        key_list = list(self.squares.keys())
        val_list = list(self.squares.values())
        target = val_list.index(clicked_square)
        possible_moves = self.game.legal_moves(key_list[target])
        
        print(f"Clicked square: {key_list[target]}")
        print(f"Legal moves: {possible_moves}")


class Side(Enum):
    W = 0
    B = 1
    
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.timer = ...
    def legal_moves(self, key_of_piece: str) -> list[str]:
        legal_move_list = []
        
        def check_space(key_of_piece: str, target_key: str) -> list[str]:
            if isinstance(self.board.pieces[target_key], Piece):
                if self.board.pieces[target_key].side != self.board.pieces[key_of_piece].side:
                    return [target_key, "capture"]
                return None
            else:
                return [target_key]
        
        def cardinal(key_of_piece: str) -> list[str]:
            cardinal_move_list = []
            for direction in ["1234567", "abcdefg", "2345678", "bcdefgh"]: # North, East, South, West
                current_key = [key_of_piece]
                while (current_key[0][1] if "2" in direction else current_key[0][0]) in direction:
                    target_key = ((current_key[0][0] + str(int(current_key[0][1]) + (1 if direction[0] == "1" else -1))) if "2" in direction else\
                                  (chr(ord(current_key[0][0]) + (1 if direction[0] == "a" else -1)) + current_key[0][1]))
                    current_key = check_space(key_of_piece, target_key)
                    if current_key == None: break
                    cardinal_move_list.append(current_key[0])
                    if len(current_key) > 1: break
            return cardinal_move_list

        def diagonal(key_of_piece):
            vertical_move_list = []
            # Northeast
            current_key = [key_of_piece]
            while (current_key[0][0] in "abcdefg") and (current_key[0][1] in "1234567"):
                current_key = check_space(key_of_piece, chr(ord(current_key[0][0]) + 1) + str(int(current_key[0][1]) + 1))
                if current_key == None: break
                vertical_move_list.append(current_key[0])
                if len(current_key) > 1: break
            # Southeast
            current_key = [key_of_piece]
            while (current_key[0][0] in "abcdefg") and (current_key[0][1] in "2345678"):
                current_key = check_space(key_of_piece, chr(ord(current_key[0][0]) + 1) + str(int(current_key[0][1]) - 1))
                if current_key == None: break
                vertical_move_list.append(current_key[0])
                if len(current_key) > 1: break
            # Southwest
            current_key = [key_of_piece]
            while (current_key[0][0] in "bcdefgh") and (current_key[0][1] in "2345678"):
                current_key = check_space(key_of_piece, chr(ord(current_key[0][0]) - 1) + str(int(current_key[0][1]) - 1))
                if current_key == None: break
                vertical_move_list.append(current_key[0])
                if len(current_key) > 1: break
            # Northwest
            current_key = [key_of_piece]
            while (current_key[0][0] in "bcdefgh") and (current_key[0][1] in "1234567"):
                current_key = check_space(key_of_piece, chr(ord(current_key[0][0]) - 1) + str(int(current_key[0][1]) + 1))
                if current_key == None: break
                vertical_move_list.append(current_key[0])
                if len(current_key) > 1: break
            return vertical_move_list
        
        if isinstance(self.board.pieces[key_of_piece], King):
            legal_move_list.append()
        elif isinstance(self.board.pieces[key_of_piece], Queen):
            legal_move_list += cardinal(key_of_piece) + diagonal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Rook):
            legal_move_list += cardinal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Bishop):
            legal_move_list += diagonal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Knight):
            pass
        elif isinstance(self.board.pieces[key_of_piece], Pawn):
            pass
        else:
            legal_move_list = []
        return legal_move_list

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
        self.side = side
    def is_opposite_side(self, key_of_other):
            return self.side != self.board.pieces[key_of_other].side
class King(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2654" if self.side == Side.W else "\u265A"
        self.value = None
        self.moveset = ...

class Queen(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2655" if self.side == Side.W else "\u265B"
        self.value = 7

class Rook(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2656" if self.side == Side.W else "\u265C"
        self.value = 5

class Bishop(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2657" if self.side == Side.W else "\u265D"
        self.value = 3

class Knight(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2658" if self.side == Side.W else "\u265E"
        self.value = 3

class Pawn(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2659" if self.side == Side.W else "\u265F"
        self.value = 1

class Empty:
    def __init__(self):
        self.image = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QPushButton{font-size: 80pt}")
    window = MainWindow()
    window.show()
    app.exec()