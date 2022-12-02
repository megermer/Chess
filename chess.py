from enum import Enum

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
        #return cardinal(key_of_piece) + diagonal(key_of_piece)
        
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
        self.image = ""
        self.value = None
        self.moveset = ...

class Queen(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = ""
        self.value = 7

class Rook(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = ""
        self.value = 5

class Bishop(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = ""
        self.value = 3

class Knight(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = ""
        self.value = 3

class Pawn(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.image = ""
        self.value = 1

class Empty:
    pass