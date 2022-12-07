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
        elif self.click_state == "Square selected":
            if key_list[target] == self.selected_square:
                self.selected_square = ""
                self.click_state = "Unselected"
            else:
                if key_list[target] in self.game.legal_moves(self.selected_square):
                    self.game.board.move(self.selected_square, key_list[target])
                    for square in self.squares:
                        self.squares[square].setText(self.game.board.pieces[square].image)
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
        self.king_moveset = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        self.knight_moveset = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2]]
    # Secondary Helper Methods
    def increment_key(self, key: str, amounts: list[int]) -> str:
        return self.increment_column(key, amounts[0]) + self.increment_row(key, amounts[1])
    def increment_column(self, key: str, amount: int) -> str:
        return chr(ord(key[0]) + amount)
    def increment_row(self, key: str, amount: int) -> str:
        return str(int(key[1]) + amount)
    def check_space(self, key_of_piece: str, target_key: str, board: dict = None) -> list[str]:
        board = self.board.pieces if board == None else board
        if target_key[0] in self.legal_columns and target_key[1] in self.legal_rows:
            if isinstance(board[target_key], Piece):
                if board[target_key].side != board[key_of_piece].side:
                    return [target_key, "capture"]
                return None
            else:
                return [target_key]
        else:
            raise ValueError("Provided target is not a valid key")
    
    # Primary Helper Methods
    def cardinal(self, key_of_piece: str, board: dict = None) -> list[str]:
        """
        returns "legal moves" in cardinal directions
        """
        board = self.board.pieces if board == None else board
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
                current_key = self.check_space(key_of_piece, target_key, board)
                if current_key == None: break
                cardinal_move_list.append(current_key[0])
                if len(current_key) > 1: break
                current_key = current_key[0] # Turn current key from a list back to a string
                current_row = current_key[1] # number
                current_column = current_key[0] # letter
        return cardinal_move_list

    def diagonal(self, key_of_piece: str, board: dict = None) -> list[str]:
        board = self.board.pieces if board == None else board
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
                current_key = self.check_space(key_of_piece, target_key, board)
                if current_key == None: break
                vertical_move_list.append(current_key[0])
                if len(current_key) > 1: break
                current_key = current_key[0] # Turn current key from a list back to a string
                current_row = current_key[1] # number
                current_column = current_key[0] # letter
        return vertical_move_list
    # Useful for King and Rook
    def check_moves_in_moveset(self, key_of_piece: str, moveset: list[list[int]]) -> list[str]:
        valid_moves = []
        for move in moveset:
            target_key = self.increment_key(key_of_piece, move)
            try:
                validity = self.check_space(key_of_piece, target_key)
                if validity != None: valid_moves += validity[:1]
            except:
                pass
        return valid_moves
    def legal_moves(self, key_of_piece: str) -> list[str]:
        """
        >>> game = ChessGame()
        >>> game.board.move('d1', 'd3')
        >>> game.board.pieces['d3'].value
        7
        >>> isinstance(game.board.pieces['d3'], Queen)
        True
        >>> game.legal_moves('d3')
        ['d4', 'd5', 'd6', 'd7', 'e3', 'f3', 'g3', 'h3', 'c3', 'b3', 'a3', 'e4', 'f5', 'g6', 'h7', 'c4', 'b5', 'a6']
        """
        legal_columns = "abcdefgh"
        legal_rows = "12345678"
        side = self.board.pieces[key_of_piece].side if isinstance(self.board.pieces[key_of_piece], Empty) == False else ""
        # verify key passed in is a valid key
        if len(key_of_piece) != 2 or (key_of_piece[0] not in legal_columns) or (key_of_piece[1] not in legal_rows):
            raise ValueError("Provided key is not a valid chess square")
        
        legal_move_list = []
        
        # Logic Switch (?) Check appropriate possible moves for each Piece type
        if isinstance(self.board.pieces[key_of_piece], King):
            moveset = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            legal_move_list += self.check_moves_in_moveset(key_of_piece, moveset)
        elif isinstance(self.board.pieces[key_of_piece], Queen):
            legal_move_list += self.cardinal(key_of_piece) + self.diagonal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Rook):
            legal_move_list += self.cardinal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Bishop):
            legal_move_list += self.diagonal(key_of_piece)
        elif isinstance(self.board.pieces[key_of_piece], Knight):
            moveset = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2]]
            legal_move_list += self.check_moves_in_moveset(key_of_piece, moveset)
        elif isinstance(self.board.pieces[key_of_piece], Pawn):
            print("Pawn check entered")
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
        checked_legal_move_list = []
        for move in legal_move_list:
            simulation = self.board.pieces.copy()
            simulation[move] = simulation[key_of_piece]
            simulation[key_of_piece] = Empty()
            if len(self.king_check(side, simulation)) == 0:
                checked_legal_move_list.append(move)
        return checked_legal_move_list
    def king_check(self, side: Side, board: dict = None, king_pos: str = None) -> list[str]:
        """
        returns keys of pieces that are putting the king in check
        >>> game = ChessGame()
        >>> game.board.move('e2', 'd3')
        >>> game.board.move('h8', 'e6')
        >>> game.board.move('f8', 'a5')
        >>> game.board.move('d2', 'h6')
        >>> game.board.move('f7', 'f2')
        >>> game.king_check(Side.W)
        ['e6', 'a5', 'f2']
        >>> game.board.move('d1', 'h5')
        >>> game.board.move('b2', 'd7')
        >>> game.king_check(Side.B)
        ['h5', 'd7']
        """
        board = self.board.pieces if board == None else board
        threats = []
        king_pos = self.board.white_king_pos if side == Side.W else self.board.black_king_pos
        # Check cardinals for Rook & Queen
        for square in self.cardinal(king_pos):
            if isinstance(board[square], Rook) or isinstance(board[square], Queen):
                if board[square].side != side:
                    threats.append(square)
        # Check diagonals for Bishop & Queen
        for square in self.diagonal(king_pos):
            if isinstance(board[square], Bishop) or isinstance(board[square], Queen):
                if board[square].side != side:
                    threats.append(square)
        # Check for Knights
        for square in self.knight_moveset:
            try:
                key = self.increment_key(king_pos, square)
                piece = board[key]
                if isinstance(piece, Knight) and piece.side != side:
                    threats.append(key)
            except:
                pass
        # Check for Pawns
        direction = 1 if side == Side.W else -1
        pawn_capture_moveset = [[1, direction], [-1, direction]]
        for square in pawn_capture_moveset:
            try:
                key = self.increment_key(king_pos, square)
                piece = board[key]
                if isinstance(piece, Pawn) and piece.side != side:
                    threats.append(key)
            except:
                pass
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
        
    def __repr__(self):
        return f"White King" if self.side == Side.W else f"Black King"

class Queen(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2655" if self.side == Side.W else "\u265B"
        self.value = 7
        
    def __repr__(self):
        return f"White Queen" if self.side == Side.W else f"Black Queen"

class Rook(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2656" if self.side == Side.W else "\u265C"
        self.value = 5
        
    def __repr__(self):
        return f"White Rook" if self.side == Side.W else f"Black Rook"

class Bishop(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2657" if self.side == Side.W else "\u265D"
        self.value = 3
    
    def __repr__(self):
        return f"White Bishop" if self.side == Side.W else f"Black Bishop"

class Knight(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2658" if self.side == Side.W else "\u265E"
        self.value = 3
        
    def __repr__(self):
        return f"White Knight" if self.side == Side.W else f"Black Knight"
    
class Pawn(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = "\u2659" if self.side == Side.W else "\u265F"
        self.value = 1
    
    def __repr__(self):
        return f"White Pawn" if self.side == Side.W else f"Black Pawn"

class Empty:
    def __init__(self):
        self.image = ""
    def __repr__(self):
        return f"Empty"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    app = QApplication(sys.argv)
    app.setStyleSheet("QPushButton{font-size: 80pt}")
    window = MainWindow()
    window.show()
    app.exec()