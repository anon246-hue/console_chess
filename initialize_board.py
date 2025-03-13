from pydantic import BaseModel
from enum import Enum
from typing import Dict, Tuple, Any

class PieceType(str, Enum):
    PAWN = "p"
    KING = "K"
    QUEEN = "Q"
    KNIGHT = 'N'
    ROOK = 'R'
    BISHOP = 'B'

class PieceStatus(str, Enum):
    ACTIVE = "active"
    CAPTURED = "captured"

class PieceColor(str, Enum):
    WHITE = "white"
    BLACK = "black"

class ChessPiece(BaseModel):
    piece_type: PieceType
    is_active: bool

class board(BaseModel):
    {
        'piece': {'piece_type' : PieceType, 'status': PieceStatus}
    }

class ChessPiece(BaseModel):
    name: str  # Unique identifier for the piece
    piece_type: PieceType
    color: PieceColor
    position: Tuple[int, int]  # (row, col) format
    is_active: bool = True

    def display(self) -> str:
            """Return a display-friendly representation of the piece."""
            return self.piece_type.value #if self.color == PieceColor.WHITE else self.piece_type.value.lower()

#class ChessBoard(BaseModel):
#    pieces: Dict[Tuple[int, int], ChessPiece]  # Map positions to pieces
class ChessBoard(BaseModel):
    #pieces: Dict[str, ChessPiece]  # Map positions to pieces
    pieces: Dict[Tuple[int, int], ChessPiece]  # Map positions to pieces

    def display(self) -> None:
        """Prints the chessboard in a readable format."""
        board = [["." for _ in range(8)] for _ in range(8)]  # Initialize empty board
        
        #for (row, col), piece in self.pieces.items():
        #    board[row][col] = piece.display()
        for piece in self.pieces.values():
            row, col = piece.position
            board[row][col] = piece.display()


        print("\n  a b c d e f g h")
        print("  ---------------")
        for i, row in enumerate(reversed(board)):  # Print from row 8 to 1
            print(f"{8 - i} {' '.join(row)} {8 - i}")
        print("  ---------------")
        print("  a b c d e f g h\n")



initial_pieces = {
    # White pieces
    #(0,0): ChessPiece(name="white_rook_1", piece_type=PieceType.ROOK, color=PieceColor.WHITE, position=(0, 0)),
    #"white_knight_1": ChessPiece(name="white_knight_1", piece_type=PieceType.KNIGHT, color=PieceColor.WHITE, position=(0, 1)),
    #"white_bishop_1": ChessPiece(name="white_bishop_1", piece_type=PieceType.BISHOP, color=PieceColor.WHITE, position=(0, 2)),
    #"white_queen": ChessPiece(name="white_queen", piece_type=PieceType.QUEEN, color=PieceColor.WHITE, position=(0, 3)),
    #"white_king": ChessPiece(name="white_king", piece_type=PieceType.KING, color=PieceColor.WHITE, position=(0, 4)),
    #"white_bishop_2": ChessPiece(name="white_bishop_2", piece_type=PieceType.BISHOP, color=PieceColor.WHITE, position=(0, 5)),
    #"white_knight_2": ChessPiece(name="white_knight_2", piece_type=PieceType.KNIGHT, color=PieceColor.WHITE, position=(0, 6)),
    #"white_rook_2": ChessPiece(name="white_rook_2", piece_type=PieceType.ROOK, color=PieceColor.WHITE, position=(0, 7)),

    (0, 0): ChessPiece(name="white_rook_1", piece_type=PieceType.ROOK, color=PieceColor.WHITE, position=(0, 0)),
    (0, 1): ChessPiece(name="white_knight_1", piece_type=PieceType.KNIGHT, color=PieceColor.WHITE, position=(0, 1)),
    (0, 2): ChessPiece(name="white_bishop_1", piece_type=PieceType.BISHOP, color=PieceColor.WHITE, position=(0, 2)),
    (0, 3): ChessPiece(name="white_queen", piece_type=PieceType.QUEEN, color=PieceColor.WHITE, position=(0, 3)),
    (0, 4): ChessPiece(name="white_king", piece_type=PieceType.KING, color=PieceColor.WHITE, position=(0, 4)),
    (0, 5): ChessPiece(name="white_bishop_2", piece_type=PieceType.BISHOP, color=PieceColor.WHITE, position=(0, 5)),
    (0, 6): ChessPiece(name="white_knight_2", piece_type=PieceType.KNIGHT, color=PieceColor.WHITE, position=(0, 6)),
    (0, 7): ChessPiece(name="white_rook_2", piece_type=PieceType.ROOK, color=PieceColor.WHITE, position=(0, 7)),


    # White pawns
    **{
        (1, i): ChessPiece(
            name=f"white_pawn_{i+1}", piece_type=PieceType.PAWN, color=PieceColor.WHITE, position=(1, i)
        ) for i in range(8)
    },

    # Black pieces
    #"black_rook_1": ChessPiece(name="black_rook_1", piece_type=PieceType.ROOK, color=PieceColor.BLACK, position=(7, 0)),
    #"black_knight_1": ChessPiece(name="black_knight_1", piece_type=PieceType.KNIGHT, color=PieceColor.BLACK, position=(7, 1)),
    #"black_bishop_1": ChessPiece(name="black_bishop_1", piece_type=PieceType.BISHOP, color=PieceColor.BLACK, position=(7, 2)),
    #"black_queen": ChessPiece(name="black_queen", piece_type=PieceType.QUEEN, color=PieceColor.BLACK, position=(7, 3)),
    #"black_king": ChessPiece(name="black_king", piece_type=PieceType.KING, color=PieceColor.BLACK, position=(7, 4)),
    #"black_bishop_2": ChessPiece(name="black_bishop_2", piece_type=PieceType.BISHOP, color=PieceColor.BLACK, position=(7, 5)),
    #"black_knight_2": ChessPiece(name="black_knight_2", piece_type=PieceType.KNIGHT, color=PieceColor.BLACK, position=(7, 6)),
    #"black_rook_2": ChessPiece(name="black_rook_2", piece_type=PieceType.ROOK, color=PieceColor.BLACK, position=(7, 7)),

    (7, 0): ChessPiece(name="black_rook_1", piece_type=PieceType.ROOK, color=PieceColor.BLACK, position=(7, 0)),
    (7, 1): ChessPiece(name="black_knight_1", piece_type=PieceType.KNIGHT, color=PieceColor.BLACK, position=(7, 1)),
    (7, 2): ChessPiece(name="black_bishop_1", piece_type=PieceType.BISHOP, color=PieceColor.BLACK, position=(7, 2)),
    (7, 3): ChessPiece(name="black_queen", piece_type=PieceType.QUEEN, color=PieceColor.BLACK, position=(7, 3)),
    (7, 4): ChessPiece(name="black_king", piece_type=PieceType.KING, color=PieceColor.BLACK, position=(7, 4)),
    (7, 5): ChessPiece(name="black_bishop_2", piece_type=PieceType.BISHOP, color=PieceColor.BLACK, position=(7, 5)),
    (7, 6): ChessPiece(name="black_knight_2", piece_type=PieceType.KNIGHT, color=PieceColor.BLACK, position=(7, 6)),
    (7, 7): ChessPiece(name="black_rook_2", piece_type=PieceType.ROOK, color=PieceColor.BLACK, position=(7, 7)),

    # Black pawns
    **{
        (6, i): ChessPiece(
            name=f"black_pawn_{i+1}", piece_type=PieceType.PAWN, color=PieceColor.BLACK, position=(6, i)
        ) for i in range(8)
    },
}
