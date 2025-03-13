#start board at 0,0 or 1,1
#add enum for status: active/captured


board_init_dict = {
    'white': {
        'pawn1': {'x':1,'y':2,'status':'Active', },
        'pawn2': {'x':2,'y':2,'status':'Active'},
        'pawn3': {'x':3,'y':2,'status':'Active'},
        'pawn4': {'x':4,'y':2,'status':'Active'},
        'pawn5': {'x':5,'y':2,'status':'Active'},
        'pawn6': {'x':6,'y':2,'status':'Active'},
        'pawn7': {'x':7,'y':2,'status':'Active'},
        'pawn8': {'x':8,'y':2,'status':'Active'},
        'rook1': {'x':1,'y':1,'status':'Active'},
        'knight1': {'x':2,'y':1,'status':'Active'},
        'bishop1': {'x':3,'y':1,'status':'Active'},
        'queen': {'x':4,'y':1,'status':'Active'},
        'king': {'x':5,'y':1,'status':'Active'},
        'rook2': {'x':6,'y':1,'status':'Active'},
        'knight2': {'x':7,'y':1,'status':'Active'},
        'bishop2': {'x':8,'y':1,'status':'Active'},
    },
    'black': {
        'pawn1': {'x':1,'y':7,'status':'Active'},
        'pawn2': {'x':2,'y':7,'status':'Active'},
        'pawn3': {'x':3,'y':7,'status':'Active'},
        'pawn4': {'x':4,'y':7,'status':'Active'},
        'pawn5': {'x':5,'y':7,'status':'Active'},
        'pawn6': {'x':6,'y':7,'status':'Active'},
        'pawn7': {'x':7,'y':7,'status':'Active'},
        'pawn8': {'x':8,'y':7,'status':'Active'},
        'rook1': {'x':1,'y':8,'status':'Active'},
        'knight1': {'x':2,'y':8,'status':'Active'},
        'bishop1': {'x':3,'y':8,'status':'Active'},
        'queen': {'x':4,'y':8,'status':'Active'},
        'king': {'x':5,'y':8,'status':'Active'},
        'rook2': {'x':6,'y':8,'status':'Active'},
        'knight2': {'x':7,'y':8,'status':'Active'},
        'bishop2': {'x':8,'y':8,'status':'Active'},
    }
}

#basic logic to use for move constraints
#move_constraints: 
#rooks - current x or y coordinate
#bishop - current cordinate +-1x, +-1y
#knight
#queen - all above
#king - any coordnate +1
#pawns - y +1, or capture

#adds
#for each turn get list of all piece movement options and validity
    #can easier use this for validations
    #and checking if king is in path of them


class Chess():
    def __init__(self,board=board_init_dict):
        self.board = board
        self.turn = 'white'
        self.log=[]
    
    def check_boundary():

    def check_piece_movement(self,piece, new_x, new_y):
        
        #check if selected piece can move to new coordinates

        if new_x > 8 or new_x < 1: #check board boundaries
            raise Exception("movement is off board")
        if new_y > 8 or new_y < 1:
            raise Exception("movement is off board")
        
        current_x = self.board[self.turn][piece]['x']
        current_y = self.board[self.turn][piece]['y']
        x_diff = current_x - new_x
        y_diff = current_y - new_y

        if piece == 'king':
            movement_type = 'single'
            ...

        elif piece == 'queen':
            ...

        elif piece[:-1] == 'pawn':
            movement_type = 'single'
            if x_diff == 1 and y_diff == 0:
                return True, movement_type
            #also check for first pawn move for double
            #check for pawn capture diagonal
            #check en pessant?? woof
        
        elif piece[:-1] == 'rook':
            if current_x == new_x or current_y == new_y:
                movement_type = 'straight'
                return True, movement_type

        elif piece[:-1] == 'bishop':
            x_diff = current_x - new_x
            y_diff = current_y - new_y
            movement_type = 'diagonal'
            if x_diff == y_diff:
                return True,movement_type

        elif piece[:-1] == 'knight':
            if ( abs(x_diff) == 1 and abs(y_diff) == 2 ) or ( abs(x_diff) == 2 and abs(y_diff) == 1 ):
                movement_type = 'knight'
                return True, movement_type
        else:
            print('Movement is invalid')
            #show valid moavements for piece
        
    def check_squares(self,piece, new_x, new_y, movement_type):
        #check if current team or opponent occupies any squares along path to desired square
        #Steps
        #turn current board cords into list
        #get lsit of spaces traversed for movement
        #check for item in list, if match then error

        current_x = self.board[self.turn][piece]['x']
        current_y = self.board[self.turn][piece]['y']

        current_board = self.board
        board_cords = []
        for k,v in current_board['white'].items():
            x = v['x']
            y = v['y']
            board_cords.append([x,y])

        for k,v in current_board['black'].items():
            x = v['x']
            y = v['y']
            board_cords.append([x,y])

        traversed_squares = []
        if movement_type == 'straight':
            if new_x == current_x:
                for num in range(current_y, new_y):
                    traversed_squares.append([current_x,num])
            if new_y == current_y:
                for num in range(current_x, new_x):
                    traversed_squares.append([num,current_y])
        
        elif movement_type == 'diagonal':
            #feels like im missing somehtng here
            x_diff = current_x - new_x
            y_diff = current_y - new_y

            for num in range(current_y, new_y):
                traversed_squares.append([current_x+1,current_y+1])

            ...
        else:
            ...

        for squares in traversed_squares:
            if squares in board_cords:
                return False

    def is_active_piece(self,piece): #check is piece captured, T/F to use in turns
        current_team = self.turn
        current_status = self.board[current_team][piece]['status']

        if current_status == 'Active':
            return True

        else:
            print("Sorry, this piece has been captured")
            return False

    def check_capture(self, new_x, new_y): #check if opposing team has piece there, if so update dict to capture
        current_team = self.turn
        current_board = self.board[current_team]
        
        for k,v in current_board.items():
            if new_x == v['x'] and new_y == v['y'] and v['status'] == 'Active': #check for not king too
                
                if current_team == 'whte':
                     update_team = 'black'
                else:
                     update_team = 'white'
                self.board[update_team][k]['status'] = 'Captured'

                return True, self.board[update_team][k], update_team
        #where to update baord for current move piece status
        #maybe do all at once

    def update_board(self,piece, new_x, new_y):
        #if all checks passes, finally update baord and user turn
        current_board = self.board
        current_board[self.turn][piece]['x'] = new_x
        current_board[self.turn][piece]['y'] = new_y
    
    def add_to_log(self,piece, new_x, new_y):
        log_item = [self.turn,piece, new_x,new_y]
        self.log.append(log_item)
        
    
    def king_constraints():
        #is king in check, or will the move place/keep king in check
        #use earlier functions like check squares/movements
        #check if current move places own king in check
        #check draw if king cannot move
        ...
    
    def vizualize_board(self):
        #use list of lists of coordinates to display
        current_board = self.board
        board_cords = []
        for k,v in current_board['white'].items():
            x = v['x']
            y = v['y']
            board_cords.append([x,y])

        for k,v in current_board['black'].items():
            x = v['x']
            y = v['y']
            board_cords.append([x,y])
        print(board_cords)
        
        
    def turn(self, piece, new_x, new_y):
        if not self.is_active_piece(piece):
            raise Exception("Piece has been captured")

        valid_movement, movement_type = self.check_piece_movement(piece, new_x, new_y)
        if valid_movement:
            raise Exception("movement is invalid")

        if not self.check_squares(piece, new_x, new_y):
            raise Exception("Move runs into existing piece")
        
        capture, captured_piece, captured_team = self.check_capture(new_x, new_y)
        if capture:
            print(f'Captured {captured_team}s {captured_piece}')



        self.update_board(piece, new_x, new_y)
        self.add_to_log(piece, new_x, new_y)
        
        if self.turn == 'white': #probably better way, setting team for next turn
            self.turn = 'black'
        else:
            self.turn = 'white'

        print(f'{self.turn}s turn to move')
