# Meg Ermer and Kelvin Feitosa
# CPTR 215 A, Final Project
# History:
#	4 Dec: Added front end
#	Rest of history in github
# Sources:
#	Find key given value in handle_click: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
#	Square colors from Chess.com

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
        
        self.restart_button_state = "N/A"
        
            
        # Styling:
#         white = "#C19B6C"
#         black = "#312624"
        white = "#EEEED4"
        black = "#7C955C"
        font_size = "font-size: 26pt"
        border = "border-radius: 2px; border: 1px solid gray"
            
        self.squares = dict()
        for number in "87654321":
            for letter in "abcdefgh":
                current_square = f"{letter}{number}"
                self.squares[current_square] = QPushButton("")
                self.squares[current_square].setFixedSize(48, 48)
                self.squares[current_square].clicked.connect(self.handle_click)
                self.squares[current_square].setText(self.game.board.pieces[current_square].image)
                if (ord(letter) + int(number)) % 2 == 0:
                    self.squares[current_square].setStyleSheet(f"{font_size}; {border}; background-color: {black}")
                else:
                    self.squares[current_square].setStyleSheet(f"{font_size}; {border}; background-color: {white}")
        
#         layout = QGridLayout()
#         column = 0
#         row = 0
#         for key in self.squares:
#             layout.addWidget(self.squares[key], row, column)
#             if column == 7:
#                 row += 1
#                 column = 0
#             else:
#                 column += 1
                
        # Row label creations
        self.row8 = QLabel("8")
        self.row7 = QLabel("7")
        self.row6 = QLabel("6")
        self.row5 = QLabel("5")
        self.row4 = QLabel("4")
        self.row3 = QLabel("3")
        self.row2 = QLabel("2")
        self.row1 = QLabel("1")
        
        # Column label creations
        self.col_a = QLabel("     a")
        self.col_b = QLabel("     b")
        self.col_c = QLabel("     c")
        self.col_d = QLabel("     d")
        self.col_e = QLabel("     e")
        self.col_f = QLabel("     f")
        self.col_g = QLabel("     g")
        self.col_h = QLabel("     h")
        
        # Sets the layout
        layout = QGridLayout()
        
        layout.addWidget(self.row8, 0, 0)
        layout.addWidget(self.row7, 1, 0)
        layout.addWidget(self.row6, 2, 0)
        layout.addWidget(self.row5, 3, 0)
        layout.addWidget(self.row4, 4, 0)
        layout.addWidget(self.row3, 5, 0)
        layout.addWidget(self.row2, 6, 0)
        layout.addWidget(self.row1, 7, 0)
        
        layout.addWidget(self.col_a, 8, 1)
        layout.addWidget(self.col_b, 8, 2)
        layout.addWidget(self.col_c, 8, 3)
        layout.addWidget(self.col_d, 8, 4)
        layout.addWidget(self.col_e, 8, 5)
        layout.addWidget(self.col_f, 8, 6)
        layout.addWidget(self.col_g, 8, 7)
        layout.addWidget(self.col_h, 8, 8) 
        
        column = 1
        row = 0
        for key in self.squares:
            layout.addWidget(self.squares[key], row, column)
            if column == 8:
                row += 1
                column = 1
            else:
                column += 1
        
        self.new_game = QPushButton("Offer Draw")
        self.new_game.setStyleSheet("background-color: #d3d3d3; font-size: 12pt; font-weight: normal; border-radius: 8px; border: 1px solid gray;")
        self.new_game.setFixedSize(90, 45)

        self.new_game.clicked.connect(self.restart)
        
        
        self.announcement = QLabel("")
        self.announcement.setStyleSheet(f"font-size: 16pt; font-weight: bold;")
        self.announcement.setFixedSize(120, 45)
        
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.announcement)
        info_layout.addWidget(self.new_game)
        
        outer_layout = QVBoxLayout()
        outer_layout.addLayout(layout)
        outer_layout.addLayout(info_layout)
        
        widget = QWidget()
        widget.setLayout(outer_layout)
        widget.setStyleSheet("background-color: #d2e7d6;")
        self.setCentralWidget(widget)
        
        
    def restart(self):
        if self.restart_button_state == "N/A":
            self.restart_button_state = "Confirm"
            self.new_game.setText("Confirm\nDraw?")
            self.new_game.setStyleSheet("background-color: #d3d3d3; font-size: 13pt; font-weight: bold; border-radius: 8px; border: 1px solid gray;")
            
        elif self.restart_button_state == "Confirm":
            self.click_state = "Paused"
            self.announcement.setText("DRAW")
            self.restart_button_state = "New Game"
            self.new_game.setStyleSheet("background-color: #d3d3d3; font-size: 12pt; font-weight: normal; border-radius: 8px; border: 1px solid gray;")
            self.new_game.setText("New Game")
        
        elif self.restart_button_state == "New Game":
            self.announcement.setText("")
            self.restart_button_state = "N/A"
            self.new_game.setText("Offer Draw")
            self.click_state = "Unselected"
            
            self.game = ChessGame()
            for square in self.squares:
                self.squares[square].setText(self.game.board.pieces[square].image)
        
    def handle_click(self):
#         clicked_square = self.sender()
        key_list = list(self.squares.keys())
        val_list = list(self.squares.values())
        target = val_list.index(self.sender())
        board = self.game.board.pieces
        if self.click_state != "Paused":
            self.restart_button_state = "N/A"
            self.new_game.setText("Offer Draw")
            self.new_game.setStyleSheet("background-color: #d3d3d3; font-size: 12pt; font-weight: normal; border-radius: 8px; border: 1px solid gray;")
        if self.click_state == "Paused":
            pass
        elif self.click_state == "Unselected":
            print("Unselected state entered")
            if isinstance(board[key_list[target]], Piece) and\
               board[key_list[target]].side == self.game.board.turn:
                self.select_square(key_list, target)
            else:
                print("Nothing is still selected: {self.click_state}")
                
        elif self.click_state == "Square selected":
            print(f"Square is selected {self.selected_square}")
            if key_list[target] == self.selected_square:
                self.unselect_square()
                print(f"Piece unselected - click state: {self.click_state}")
                print(f"Selected square: {self.selected_square}")
            else:
                print(self.game.legal_moves(self.selected_square))
                if key_list[target] in self.game.legal_moves(self.selected_square):
                    print(f"This is a legal move: moving {key_list[target]}")
                    # Backend Move
                    self.game.board.move(self.selected_square, key_list[target])
                    # Update frontend squares
                    for square in self.squares:
                        self.squares[square].setText(board[square].image)
                    # Check for mates
                    mate_status = self.game.check_mates()
                    print(f"Mate status: {mate_status}")
                    if mate_status != False:
                        self.click_state = "Paused"
                        if mate_status[0] == "Stalemate":
                            self.announcement.setText("Stalemate!")
                        elif mate_status[0] == "Checkmate":
                            self.announcement.setText(f"{'Black' if mate_status[1] == Side.W else 'White'} wins!")
                        self.restart_button_state = "New Game"
                        self.new_game.setText("New Game")
                    else:
                        self.unselect_square()
                try:
                    if board[key_list[target]].side ==\
                       board[self.selected_square].side:
                        print(f"Selecting different piece of same team: ")
                        self.select_square(key_list, target)
                    else:
                        self.unselect_square()
                except:
                    pass
#                 self.unselect_square()
                
    def select_square(self, key_list, target):
#         possible_moves = self.game.legal_moves(key_list[target])
        self.click_state = "Square selected"
        self.selected_square = key_list[target]
        print(f"self.selected_square: {self.selected_square}")
    def unselect_square(self):
        print("unselect_square entered")
        self.selected_square = ""
        self.click_state = "Unselected"


class Side(Enum):
    W = 0
    B = 1
    
class ChessGame:
    def __init__(self):
        """ Creates a ChessGame object with a board
        >>> game = ChessGame()
        >>> print(type(game))
        <class '__main__.ChessGame'>
        >>> print(type(game.board))
        <class '__main__.Board'>
        """
        self.board = Board()
        self.timer = ...
#         self.turn = Side.W
        self.legal_columns = "abcdefgh"
        self.legal_rows = "12345678"
        self.king_moveset = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        self.knight_moveset = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2]]
    # Secondary Helper Methods
    def increment_key(self, key: str, amounts: list[int]) -> str:
        """ Increments the key of a chess square
        >>> game = ChessGame()
        >>> game.increment_key('b1', [2, 0])
        'd1'
        >>> game.increment_key('c4', [4, 4])
        'g8'
        """
        return self.increment_column(key, amounts[0]) + self.increment_row(key, amounts[1])
    def increment_column(self, key: str, amount: int) -> str:
        """ Increments the column of a chess square
        >>> game = ChessGame()
        >>> game.increment_column('a1', 4)
        'e'
        >>> game.increment_column('d4', 2)
        'f'
        """
        return chr(ord(key[0]) + amount)
    def increment_row(self, key: str, amount: int) -> str:
        """ Increments the row of a chess square
        >>> game = ChessGame()
        >>> game.increment_row('a1', 4)
        '5'
        >>> game.increment_row('g5', 2)
        '7'
        """
        return str(int(key[1]) + amount)
    def check_space(self, key_of_piece: str, target_key: str, board: dict = None) -> list[str]:
        """ Checks to see if the space is on the board
        >>> game = ChessGame()
        >>> game.board.move('a2', 'a4')
        >>> game.board.move('b7', 'b5')
        >>> game.check_space('a4', 'b5')
        ['b5', 'capture']
        >>> game.board.move('e1', 'e4')
        >>> game.board.move('f2', 'f3')
        >>> game.check_space('f3', 'e4')
        
        >>> game.check_space('e4', 'e5')
        ['e5']
        """
        board = self.board.pieces if board == None else board
        if target_key[0] in self.legal_columns and target_key[1] in self.legal_rows:
            if isinstance(board[target_key], Piece):
                if board[target_key].side != self.board.turn:
                    return [target_key, "capture"]
                return None # Square has a piece of the same side
            else:
                return [target_key] # If square is an Empty
        else:
            raise ValueError("Provided target is not a valid key")
    
    # Primary Helper Methods
    def cardinal(self, key_of_piece: str, board: dict = None) -> list[str]:
        """ Returns "legal moves" in cardinal directions
        >>> game = ChessGame()
        >>> game.cardinal('g2')
        ['g3', 'g4', 'g5', 'g6', 'g7']
        >>> game.cardinal('a1')
        []
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
        """ Returns legal moves in diaganol directions
        >>> game = ChessGame()
        >>> game.diagonal('d2')
        ['e3', 'f4', 'g5', 'h6', 'c3', 'b4', 'a5']
        >>> game.diagonal('g1')
        []
        """
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
        ''' Validates a move if it is a capture or empty space.
        >>> game = ChessGame()
        >>> game.check_moves_in_moveset('h1', [[1, 2], [2, 1]])
        []
        >>> game.board.move('h1', 'h3')
        >>> game.check_moves_in_moveset('h3', [[1, 2], [2, 1]])
        []
        '''
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
        >>> game.board.turn = Side.W
        >>> game.legal_moves('d3')
        ['d4', 'd5', 'd6', 'd7', 'e3', 'f3', 'g3', 'h3', 'c3', 'b3', 'a3', 'e4', 'f5', 'g6', 'h7', 'c4', 'b5', 'a6']
        >>> game = ChessGame()
        >>> game.board.move('e1', 'e3')
        >>> game.board.move('h7', 'h6')
        >>> game.legal_moves('e3')
        ['e4', 'f4', 'f3', 'd3', 'd4']
        >>> game  = ChessGame()
        >>> game.board.move('f1', 'f3')
        >>> game.board.move('a7', 'a6')
        >>> game.board.move('g1', 'g3')
        >>> game.board.move('h7', 'h6')
        >>> game.legal_moves('e1')
        King hasn't moved and not in check
        Queen side threat found
        Queen side threat found
        Queen side threat found
        ['g1', 'f1']
        >>> game = ChessGame()
        >>> game.board.move('a1', 'a4')
        >>> game.board.move('h7', 'h6')
        >>> game.legal_moves('a4')
        ['a5', 'a6', 'a7', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'a3']
        >>> game.board.move('c1', 'e3')
        >>> game.board.move('c7', 'c5')
        >>> game.legal_moves('e3')
        ['f4', 'g5', 'h6', 'd4', 'c5']
        >>> game.legal_moves('g1')
        ['f3', 'h3']
        >>> game.legal_moves('h2')
        Checking pawn move:
        ['g3']
        Now checking en passant
        ['h3', 'h4']
        >>> game.legal_moves('h4')
        []
        """
        legal_columns = "abcdefgh"
        legal_rows = "12345678"
        side = self.board.pieces[key_of_piece].side if isinstance(self.board.pieces[key_of_piece], Piece) else self.board.turn
        # verify key passed in is a valid key
        if len(key_of_piece) != 2 or (key_of_piece[0] not in legal_columns) or (key_of_piece[1] not in legal_rows):
            raise ValueError("Provided key is not a valid chess square")
        
        legal_move_list = []
        checked_legal_move_list = []
        # Logic Switch (?) Check appropriate possible moves for each Piece type
        if isinstance(self.board.pieces[key_of_piece], King):
            moveset = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            castling_moveset = [[2, 0], [-2, 0]]
            legal_move_list += self.check_moves_in_moveset(key_of_piece, moveset)
#             print(self.king_check(side))
            if (not self.board.pieces[key_of_piece].has_moved) and len(self.king_check(side)) == 0: # King Hasn't Moved & isn't in check
                print("King hasn't moved and not in check")
                king_side_rook = self.increment_key(key_of_piece, [3, 0])
                queen_side_rook = self.increment_key(key_of_piece, [-4, 0])
                rooks = [king_side_rook, queen_side_rook]
                
                king_side_check_squares = [self.increment_key(key_of_piece, move)\
                                           for move in [[2, 0], [1, 0]]]
                queen_side_check_squares = [self.increment_key(key_of_piece, move)\
                                            for move in [[-1, 0], [-2, 0], [-3, 0]]]
                check_squares = [king_side_check_squares, queen_side_check_squares]
                
                king_side_castle_threats = 0
                queen_side_castle_threats = 0
                
                # Terrible sequence of nested ifs that I would in retrospect structure differently
                # but it looks kinda cool so I'm just leaving it cause screw it
                for rook, squares in zip(rooks, check_squares):
                    if isinstance(self.board.pieces[rook], Rook):
                        if not self.board.pieces[rook].has_moved:
                            for square in squares:
                                if not (isinstance(self.board.pieces[square], Empty) and
                                   len(self.king_check(side, self.board.pieces, square)) == 0):
                                    if rook == king_side_rook:
                                        king_side_castle_threats += 1
                                        print("King side threat found")
                                    else:
                                        queen_side_castle_threats += 1
                                        print("Queen side threat found")
                if king_side_castle_threats == 0:
                    checked_legal_move_list.append('g1' if side == Side.W else 'g8')
                if queen_side_castle_threats == 0:
                    checked_legal_move_list.append('c1' if side == Side.W else 'c8')
                            
                            
                                
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
#             print("Pawn check entered")
            side = self.board.pieces[key_of_piece].side
            direction = 1 if side == Side.W else -1
            ext_moveset = [[1, direction], [-1, direction]] # Capture squares
            enp_moveset = [[1, 0], [-1, 0]]
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
                move_key = self.increment_key(key_of_piece, pos_move)
                try:
                    move = self.check_space(key_of_piece, move_key)
                    print("Checking pawn move:")
                    print(move)
                except:
                    move = False
                if move == False or move == None:
                    pass
                # En Passant
                elif len(move) == 1: 
                    print("Now checking en passant")
                    if self.board.pieces[key_of_piece].enp != False:
                        try:
                            enp_move = self.increment_key(move_key, [0, direction * -1])
                            enp_move_check = self.check_space(key_of_piece, enp_move)
                            if enp_move_check == None:
                                pass
                            elif len(enp_move_check) == 2 and enp_move_check[1] == "capture" and\
                               isinstance(self.board.pieces[enp_move], Pawn) and\
                               self.board.pieces[enp_move].times_moved == 1 and\
                               self.board.last_move[1] == enp_move:
                                legal_move_list.append(move_key)
                                self.board.pieces[key_of_piece].enp.append(move_key)
                        except:
                            print("En passant check died")
                # Normal Capture
                elif len(move) == 2 and move[1] == "capture":
                    
                    legal_move_list += move[:1]
                    
        else:
            legal_move_list = []
            
        for move in legal_move_list:
            simulation = self.board.pieces.copy()
            simulation[move] = simulation[key_of_piece]
            simulation[key_of_piece] = Empty()
            if len(self.king_check(side, simulation, move if isinstance(self.board.pieces[key_of_piece], King) else None)) == 0:
                checked_legal_move_list.append(move)
                
        return checked_legal_move_list
    
    def king_check(self, side: Side, board: dict = None, king_pos: str = None) -> list[str]:
        """
        returns keys of pieces that are putting the king in check. if returns an empty list, king
        is not in check
        >>> game = ChessGame()
        >>> game.board.move('e2', 'd3')
        >>> game.board.move('h8', 'e6')
        >>> game.board.move('f8', 'a5')
        >>> game.board.move('d2', 'h6')
        >>> game.board.move('f7', 'f2')
        >>> game.board.move('h2', 'h3')
        >>> game.king_check(Side.W)
        ['e6', 'a5', 'f2']
        >>> game.board.move('d1', 'h5')
        >>> game.board.move('b2', 'd7')
        >>> game.board.move('h1', 'e7')
        >>> game.king_check(Side.B)
        ['e7', 'h5', 'd7']
        """
        board = self.board.pieces if board == None else board
        threats = []
        if king_pos == None: king_pos = self.board.white_king_pos if side == Side.W else self.board.black_king_pos
        # Check cardinals for Rook & Queen
        for square in self.cardinal(king_pos, board):
            if isinstance(board[square], Rook) or isinstance(board[square], Queen):
                if board[square].side != self.board.turn: #CHANGING THIS
                    threats.append(square)
        # Check diagonals for Bishop & Queen
        for square in self.diagonal(king_pos, board):
            if isinstance(board[square], Bishop) or isinstance(board[square], Queen):
                if board[square].side != self.board.turn: #CHANGING THIS
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
    def check_mates(self):
        """
        Checks if the current side is in check, if so looks for legal moves. If none found, it's checkmate for
        opposing side. If current side is not in check, looks for legal moves. If none found, it's stalemate.
        """
        def legal_move_exists(side, board):
            for square in board:
                if isinstance(board[square], Empty):
                    pass
                elif board[square].side != side:
                    pass
                elif len(self.legal_moves(square)) != 0:
                    return True # As soon as a legal move is found
            return False # If no legal moves found
        
        side = self.board.turn
        board = self.board.pieces
        # If current side is in check
        if len(self.king_check(side)) != 0:
            checkmate = False if legal_move_exists(side, board) else True
            return False if not checkmate else ["Checkmate", side]
        # If current side not in check, check for stalemate
        else:
            stalemate = False if legal_move_exists(side, board) else True
            return False if not stalemate else ["Stalemate", side]
            

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
        self.turn = Side.W
        self.last_move = []
    def move(self, start_pos, end_pos):
        """
        Executes a move on the backend board dictionary. Moves the piece at dictionary key 'start_pos' to the square 'end_pos'.
        After executing move, updates turn tracking instance variables self.turn and self.last_move.
        Any piece can be moved anywhere at any time if called from the shell or a script.
        If move is manually called to move a king to a castling square, the rook will also me moved if the king hadn't moved previously.
        Expected usage is to execute a move already verified by ChessGame()'s legal_moves() method.
        En Passant specifically is only possible with the extra setup provided through legal_moves 's check for en passant
        """
        # Castling here:
        if isinstance(self.pieces[start_pos], King) and not self.pieces[start_pos].has_moved:
            if end_pos == 'g1':
                self.pieces['f1'] = self.pieces['h1']
                self.pieces['h1'] = Empty()
            elif end_pos == 'c1':
                self.pieces['d1'] = self.pieces['a1']
                self.pieces['a1'] = Empty()
            elif end_pos == 'g8':
                self.pieces['f8'] = self.pieces['h8']
                self.pieces['h8'] = Empty()
            elif end_pos == 'c8':
                self.pieces['d8'] = self.pieces['a8']
                self.pieces['a8'] = Empty()
        self.pieces[start_pos].has_moved = True
        self.pieces[start_pos].times_moved += 1
        # If move is a capture (end_pos not an Empty)
        if isinstance(self.pieces[end_pos], Empty) == False:
            self.captured.append(self.pieces[end_pos])
        # Executes Move
        self.pieces[end_pos] = self.pieces[start_pos]
        self.pieces[start_pos] = Empty()
        # Check for En Passant and Promotion
        if isinstance(self.pieces[end_pos], Pawn):
            # If not en passant check for promotion
            enp = True
            if self.pieces[end_pos].enp == False:
                enp = False
            elif len(self.pieces[end_pos].enp) == 0:
                enp = False
            if not enp:
                if (self.turn == Side.W and end_pos[1] == "8") or\
                   (self.turn == Side.B and end_pos[1] == "1"):
                    print("Pawn Promoted")
                    times_moved = self.pieces[end_pos].times_moved
                    self.pieces[end_pos] = Queen(self.turn)
                    self.pieces[end_pos].times_moved = times_moved
                    
            # If capture is En Passant
            elif end_pos in self.pieces[end_pos].enp:
                # Capture other pawn
                other_pawn = end_pos[0] + str(int(end_pos[1]) + (1 if self.turn == Side.B else -1))
                self.captured.append(self.pieces[other_pawn])
                self.pieces[other_pawn] = Empty()
                # Reset en passant instance variable for that pawn
                self.pieces[end_pos].enp = False
        # Update position of kings in instance variables for check checks
        if isinstance(self.pieces[end_pos], King):
            if self.pieces[end_pos].side == Side.W:
                self.white_king_pos = end_pos
            else:
                self.black_king_pos = end_pos
        # Update turn tracking instance variables
        self.last_move = [start_pos, end_pos]
        self.turn = Side.W if self.turn == Side.B else Side.B
        

class Piece:
    def __init__(self, side):
        self.has_moved = False
        self.times_moved = 0
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
        self.enp = []
    
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