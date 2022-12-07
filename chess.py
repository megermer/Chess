# Meg Ermer and Kelvin Feitosa
# CPTR 215 A, Final Project
# History:
#	4 Dec: Added front end
# (Kelvin) 12/4/2022: Fixed secondary helper methods in legal_moves, implemented Pawn & Knight checks. Only King checks remain
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
        self.click_state = "Unselected"   
        self.selected_square = ""
            
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
                    self.squares[current_square].setStyleSheet(f"font-size: 25pt; background-color: {black}")
                else:
                    self.squares[current_square].setStyleSheet(f"font-size: 25pt; background-color: {white}")
                
        
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
        if self.click_state == "Unselected":
            possible_moves = self.game.legal_moves(key_list[target])
            self.click_state = "Square selected"
            self.selected_square = key_list[target]
            print(f"Clicked square: {key_list[target]}") # Testing purposes
            print(f"Legal moves: {possible_moves}") #Testing purposes
        elif self.click_state == "Square selected":
            if key_list[target] == self.selected_square:
                print(f"self.selected_square: {self.selected_square}")
                print(f"key_list[target]: {key_list[target]}")
                self.selected_square = ""
                self.click_state = "Unselected"
                print(f"Selected square: {self.click_state}") #Testing purposes
            else:
                print("else entered")
                if key_list[target] in self.game.legal_moves(self.selected_square):
                    self.game.board.move(self.selected_square, key_list[target])
                    for square in self.squares:
                        self.squares[square].setText(self.game.board.pieces[square].image)

#                     print(self.game.board.pieces)
                self.selected_square = ""
                self.click_state = "Unselected"
                
                
                
            


class Side(Enum):
    W = 0
    B = 1
    
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.timer = ...
        self.turn = Side.W
        self.legal_columns = "abcdefgh"
        self.legal_rows = "12345678"
    # Secondary Helper Methods
    def increment_key(self, key: str, amounts: list[int]) -> str:
        return self.increment_column(key, amounts[0]) + self.increment_row(key, amounts[1])
    def increment_column(self, key: str, amount: int) -> str:
        return chr(ord(key[0]) + amount)
    def increment_row(self, key: str, amount: int) -> str:
        return str(int(key[1]) + amount)
    def check_space(self, key_of_piece: str, target_key: str) -> list[str]:
        if target_key[0] in self.legal_columns and target_key[1] in self.legal_rows:
            if isinstance(self.board.pieces[target_key], Piece):
                if self.board.pieces[target_key].side != self.board.pieces[key_of_piece].side:
                    return [target_key, "capture"]
                return None
            else:
                return [target_key]
        else:
            raise ValueError("Provided target is not a valid key")
    
    # Primary Helper Methods
    def cardinal(self, key_of_piece: str) -> list[str]:
        """
        returns "legal moves" in cardinal directions
        """
        north = "1234567"
        south = "2345678"
        east = "abcdefg"
        west = "bcdefgh"
        cardinal_move_list = []
        for direction in [north, east, south, west]: # North, East, South, West
            current_key = key_of_piece
            current_row = key_of_piece[1] # number
            current_column = key_of_piece[0] # letter
            while (current_row if "2" in direction else current_column) in direction:
                target_key = ((current_column + self.increment_row(current_key, 1 if direction[0] == "1" else -1)) if "2" in direction else\
                              (self.increment_column(current_key, 1 if direction[0] == "a" else -1) + current_row))
                current_key = self.check_space(key_of_piece, target_key)
                if current_key == None: break
                cardinal_move_list.append(current_key[0])
                if len(current_key) > 1: break
                current_key = current_key[0] # Turn current key from a list back to a string
                current_row = current_key[1] # number
                current_column = current_key[0] # letter
        return cardinal_move_list

    def diagonal(self, key_of_piece: str) -> list[str]:
        north = "1234567"
        south = "2345678"
        east = "abcdefg"
        west = "bcdefgh"
        vertical_move_list = []
        for interordinal in [[north, east], [south, east], [south, west], [north, west]]:
            current_key = key_of_piece
            current_row = current_key[1] # number
            current_column = current_key[0] # letter
            while (current_column in interordinal[1]) and (current_row in interordinal[0]):
                target_key = self.increment_column(current_key, 1 if interordinal[1] == east else -1)\
                             + self.increment_row(current_key, 1 if interordinal[0] == north else -1)
                current_key = self.check_space(key_of_piece, target_key)
                if current_key == None: break
                vertical_move_list.append(current_key[0])
                if len(current_key) > 1: break
                current_key = current_key[0] # Turn current key from a list back to a string
                current_row = current_key[1] # number
                current_column = current_key[0] # letter
        return vertical_move_list
    def legal_moves(self, key_of_piece: str) -> list[str]:
        """
        >>> game = ChessGame()
        >>> game.board.move('d1', 'd3')
        >>> game.legal_moves('d3')
        ['d4', 'd5', 'd6', 'd7', 'e3', 'f3', 'g3', 'h3', 'c3', 'b3', 'a3', 'e4', 'f5', 'g6', 'h7', 'c4', 'b5', 'a6']
        """
        legal_columns = "abcdefgh"
        legal_rows = "12345678"
        
        # verify key passed in is a valid key
        if len(key_of_piece) != 2 or (key_of_piece[0] not in legal_columns) or (key_of_piece[1] not in legal_rows):
            raise ValueError(f"This space is not a valid chess square")
        
        legal_move_list = []
        
        # Logic Switch (?) Check appropriate possible moves for each Piece type
        if isinstance(self.board.pieces[key_of_piece], King):
            legal_move_list.append()
        elif isinstance(self.board.pieces[key_of_piece], Queen):
            legal_move_list += self.cardinal(key_of_piece) + self.diagonal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Rook):
            legal_move_list += self.cardinal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Bishop):
            legal_move_list += self.diagonal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Knight):
            moveset = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2]]
            for move in moveset:
                target_key = self.increment_key(key_of_piece, move)
                try:
                    validity = self.check_space(key_of_piece, target_key)
                    if validity != None: legal_move_list += validity[:1]
                except:
                    pass
        elif isinstance(self.board.pieces[key_of_piece], Pawn):
            side = self.board.pieces[key_of_piece].side
            direction = 1 if side == Side.W else -1
            ext_moveset = [[1, direction], [-1, direction]] # Capture squares
            # Check normal forward moves
            moves = [[0, direction]]
            # Check     
            if (side == Side.W and key_of_piece[1] == "2") or (side == Side.B and key_of_piece[1] == "7"):
                moves.append([0, direction * 2]) # Can move 2 sqares if still on home square
            for pos_move in moves:
                move = self.check_space(key_of_piece, self.increment_key(key_of_piece, pos_move))
                if move != None and len(move) == 1:
                    legal_move_list += move
            # Check Captures
            for pos_move in ext_moveset:
                try:
                    move = self.check_space(key_of_piece, self.increment_key(key_of_piece, pos_move))
                    if len(move) == 2 and move[1] == "capture":
                        legal_move_list += move[:1]
                except:
                    pass 
        else:
            legal_move_list = []
        return legal_move_list
    def king_check(self, side: Side) -> list[str]:
        """
        returns keys of pieces that are putting the king in check
        >>> game = ChessGame()
        >>> game.board.move('e2', 'd3')
        >>> game.board.move('h8', 'e6')
        >>> game.board.move('f8', 'a5')
        >>> game.board.move('d2', 'h6')
        >>> game.king_check(Side.W)
        ['e6', 'a5']
        """
        threats = []
        king_pos = self.board.white_king_pos if side == Side.W else self.board.black_king_pos
        for square in self.cardinal(king_pos):
            if isinstance(self.board.pieces[square], Rook) or isinstance(self.board.pieces[square], Queen):
                if self.board.pieces[square].side != side:
                    threats.append(square)
        for square in self.diagonal(king_pos):
            if isinstance(self.board.pieces[square], Bishop) or isinstance(self.board.pieces[square], Queen):
                if self.board.pieces[square].side != side:
                    threats.append(square)
        # Threats from knights here
        
        # Threats from pawns here
        
        return threats

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
        self.white_king_pos = "e1"
        self.black_king_pos = "e8"
    def move(self, start_pos, end_pos):
        # If move is a capture (end_pos not an Empty)
        if isinstance(self.pieces[end_pos], Empty) == False:
            self.captured.append(self.pieces[end_pos])
        self.pieces[end_pos] = self.pieces[start_pos]
        self.pieces[start_pos] = Empty()
        # Update position of kings in instance variables for check checks
        if isinstance(self.pieces[end_pos], King):
            if self.pieces[end_pos].side == Side.W:
                self.white_king_pos = end_pos
            else:
                self.black_king_pos = end_pos

class Piece:
    def __init__(self, side):
        self.has_moved = False
        self.side = side
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
    import doctest
    doctest.testmod()
    
    app = QApplication(sys.argv)
    app.setStyleSheet("QPushButton{font-size: 80pt}")
    window = MainWindow()
    window.show()
    app.exec()