from initialize_board import ChessBoard,ChessPiece,initial_pieces,PieceColor,PieceType
from pydantic import BaseModel
from enum import Enum
from typing import Dict, Tuple, Any


class Chess():
    def __init__(
        self,
        board:ChessBoard = ChessBoard(pieces=initial_pieces),
    ):
        self.board = board
        self.color_turn = PieceColor('white')
        self.log=[]
        self.captured_pieces=[]
    
    def check_boundary(self, new_position):
        new_col = new_position[0]
        new_row = new_position[1]
        if new_col > 7 or new_col < 0: #check board boundaries
            raise Exception("movement is off board")
        if new_row > 7 or new_row < 0:
            raise Exception("movement is off board")
        
        return True
    
    def check_teams_piece(self,current_position): #cehck if current piece matches current team
        current_piece  = self.board.pieces[current_position].color.value
        
        if not current_piece:
            raise Exception("No piece at this position")
        elif current_piece != self.color_turn.value:
            raise Exception("That is not your piece")
        else:
            return True

    ####heavy GPT assist
    def is_straight_line_move(self,piece: ChessPiece, new_position: Tuple[int, int], board: ChessBoard) -> bool:
        """Check if the move is a straight line and if path is clear."""
        row_diff = new_position[0] - piece.position[0]
        col_diff = new_position[1] - piece.position[1]

        if row_diff != 0 and col_diff != 0:
            print('Not a straight line move')
            return False  # Not a straight line move

        step_row = 0 if row_diff == 0 else (1 if row_diff > 0 else -1)
        step_col = 0 if col_diff == 0 else (1 if col_diff > 0 else -1)

        row, col = piece.position
        while (row, col) != new_position:
            row += step_row
            col += step_col
            if (row, col) == new_position:
                break  # Reached destination
            if (row, col) in board.pieces:  # Path blocked
                print('Path blocked')
                return False

        return True

    def is_diagonal_move(self,piece: ChessPiece, new_position: Tuple[int, int], board: ChessBoard) -> bool:
        """Check if the move is diagonal and if path is clear."""
        row_diff = new_position[0] - piece.position[0]
        col_diff = new_position[1] - piece.position[1]

        if abs(row_diff) != abs(col_diff):
            return False  # Not a diagonal move

        step_row = 1 if row_diff > 0 else -1
        step_col = 1 if col_diff > 0 else -1

        row, col = piece.position
        while (row, col) != new_position:
            row += step_row
            col += step_col
            if (row, col) == new_position:
                break  # Reached destination
            if (row, col) in board.pieces:  # Path blocked
                return False

        return True

    def is_valid_pawn_move(self,piece: ChessPiece, new_position: Tuple[int, int], board: ChessBoard) -> bool:
        """Check valid pawn movement."""
        direction = 1 if piece.color == PieceColor.WHITE else -1
        start_row = 1 if piece.color == PieceColor.WHITE else 6
        row_diff = new_position[0] - piece.position[0]
        col_diff = abs(new_position[1] - piece.position[1])

        if col_diff == 0:  # Forward movement
            if row_diff == direction and new_position not in board.pieces:
                return True  # Normal one-square move
            if piece.position[0] == start_row and row_diff == 2 * direction and new_position not in board.pieces:
                return True  # Two-square move from start

        elif col_diff == 1 and row_diff == direction:  # Diagonal capture
            return new_position in board.pieces and board.pieces[new_position].color != piece.color

        return False

    def is_valid_rook_move(self,piece: ChessPiece, new_position: Tuple[int, int], board: ChessBoard) -> bool:
        """Check valid rook movement (straight lines, no jumping over pieces)."""
        return self.is_straight_line_move(piece, new_position, board)

    def is_valid_bishop_move(self,piece: ChessPiece, new_position: Tuple[int, int], board: ChessBoard) -> bool:
        """Check valid bishop movement (diagonal, no jumping over pieces)."""
        return self.is_diagonal_move(piece, new_position, board)

    def is_valid_queen_move(self,piece: ChessPiece, new_position: Tuple[int, int], board: ChessBoard) -> bool:
        """Check valid queen movement (combines rook and bishop logic)."""
        return self.is_straight_line_move(piece, new_position, board) or self.is_diagonal_move(piece, new_position, board)

    def is_valid_knight_move(self,piece: ChessPiece, new_position: Tuple[int, int]) -> bool:
        """Check valid knight movement (L-shape)."""
        row_diff = abs(new_position[0] - piece.position[0])
        col_diff = abs(new_position[1] - piece.position[1])
        return (row_diff, col_diff) in [(2, 1), (1, 2)]

    def is_valid_king_move(self,piece: ChessPiece, new_position: Tuple[int, int]) -> bool:
        """Check valid king movement (one square in any direction)."""
        row_diff = abs(new_position[0] - piece.position[0])
        col_diff = abs(new_position[1] - piece.position[1])
        return max(row_diff, col_diff) == 1

    def is_valid_move(self, current_position: Tuple[int, int], new_position: Tuple[int, int]) -> bool:
        """Check if the piece can legally move to the new position."""
        board = self.board
        if current_position not in board.pieces:
            print('Piece not found')
            return False  # Piece not found

        #piece = board.pieces[piece_name]
        piece = board.pieces[current_position]
        old_position = piece.position
        row_diff = abs(new_position[0] - old_position[0])
        col_diff = abs(new_position[1] - old_position[1])


        # Check if destination is occupied by same color
        destination_piece = self.board.pieces.get(new_position)
        if destination_piece and destination_piece.color == piece.color:
            print("Can't capture own piece")
            return False  # Can't capture own piece

        # Movement rules based on piece type
        if piece.piece_type == PieceType.PAWN:
            return self.is_valid_pawn_move(piece, new_position, board)
        
        elif piece.piece_type == PieceType.ROOK:
            return self.is_valid_rook_move(piece, new_position, board)

        elif piece.piece_type == PieceType.BISHOP:
            return self.is_valid_bishop_move(piece, new_position, board)

        elif piece.piece_type == PieceType.QUEEN:
            return self.is_valid_queen_move(piece, new_position, board)

        elif piece.piece_type == PieceType.KNIGHT:
            return self.is_valid_knight_move(piece, new_position)

        elif piece.piece_type == PieceType.KING:
            return self.is_valid_king_move(piece, new_position)

        return False  # If none match, invalid move
    ######End GPT Assist


    def is_active_piece(self,piece): #DNU
        """Not needed since we are removing pieces from board once captured"""
        current_team = self.turn
        current_status = self.board[current_team][piece]['status']

        if current_status == 'Active':
            return True
        else:
            print("Sorry, this piece has been captured")
            return False
        
    def check_capture(self, new_position: Tuple[int, int]): #check if opposing team has piece there, if so update dict to capture
        
        captured_piece = self.board.pieces.get(new_position)

        if captured_piece:
            self.captured_pieces.append(captured_piece)
            print(f'{self.color_turn.value} Captured {new_position}')
            del self.board.pieces[new_position]

            
    def update_board(self,current_position: Tuple[int, int],new_position: Tuple[int, int]):
        #if all checks passes, finally update baord and user turn
        current_piece = self.board.pieces[current_position]

        del self.board.pieces[current_position] #removed current piece

        updated_piece = current_piece
        updated_piece.position=(new_position)
        self.board.pieces[new_position] = updated_piece #place piece at new position

    
    def add_to_log(self,current_position: Tuple[int, int],new_position: Tuple[int, int]):
        log_item = [self.color_turn.value,current_position, new_position]
        self.log.append(log_item)


    def take_turn(self,current_position: Tuple[int, int],new_position: Tuple[int, int]):
        if self.check_boundary(new_position):
            pass
        if self.check_teams_piece(current_position):
            pass
        if self.is_valid_move(current_position,new_position):
            pass
        self.check_capture(new_position)
        self.update_board(current_position,new_position)
        self.add_to_log(current_position,new_position)

        print(f'{self.color_turn.value} moved {current_position} to {new_position}')

        #update user turn
        if self.color_turn.value == 'white':
            self.color_turn = PieceColor('black')
        else:
            self.color_turn = PieceColor('white')

        print(f'')
    
    def whos_turn_is_it(self):
        print(f'It is {self.color_turn.value}s turn to move')


def create_chess(board = ChessBoard(pieces=initial_pieces)):
    return Chess(ChessBoard(pieces=initial_pieces))