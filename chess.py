from pprint import pprint
import random
random.seed(42)

class Chess:
    def __init__(self, player1_name, player2_name, grid_len=5, dummy_char='0'):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.p1points = 0
        self.p2points = 0
        # Types of characters = {'P': 'pawn'}
        self.character_types = {}
        # List of character names for each character type = {'P': [P1, P2, P3, P4, P5]}
        self.characters = {}
        # Possible moves = {'P': [F, B, L, R]}
        self.possible_moves = {}
        self.grid = []
        self.dummy_char = dummy_char
        self.grid_len = grid_len
        # For each character type, remaining characters on board
        self.p1_valid_characters = {}
        self.p2_valid_characters = {}
        
        
    def init_grid(self):
        for _ in range(self.grid_len):
            self.grid.append([self.dummy_char for _ in range(self.grid_len)])
        
        
    def add_character(self, character_type, character_type_abbr, character_moves):
        self.character_types[character_type_abbr] = character_type
        self.possible_moves[character_type] = character_moves
        self.p1_valid_characters[character_type] = character_moves
        self.p2_valid_characters[character_type] = character_moves
        
    
    def deploy_player_chars(self, player_name, character_type):
        if player_name == self.player1_name:
            pos = self.grid_len - 1
        else:
            pos = 0
        
        # Randomly initialize 5 player positions
        if player_name == self.player1_name:
            random.shuffle(self.p1_valid_characters[character_type])
            for idx, char in enumerate(self.p1_valid_characters[character_type]):
                self.grid[pos][idx] = player_name + '-' + char
        else:
            random.shuffle(self.p2_valid_characters[character_type])
            for idx, char in enumerate(self.p2_valid_characters[character_type]):
                self.grid[pos][idx] = player_name + '-' + char
           
            
    def play_game(self, player_name, character, move, reset_grid_if_won):
        """Play game

        Args:
            player_name (str): Name of the current player
            character (character name): Character name
            move (str): Move name
            reset_grid_if_won (bool): If any player has won, reset grid or not
        """        
        error_state = ''
        # TODO: Better way of getting character type
        character_type_abbr = character[0]
        character_type = self.character_types[character_type_abbr]
        # Disable try/except if you WANT the error to stop execution of program
        try:
            # Invalid move
            if character_type_abbr not in self.character_types:
                error_state = 'Invalid character type'
                raise Exception('ERROR: ', error_state)
            
            if move not in self.possible_moves[character_type]:
                error_state = 'Invalid move'
                raise Exception('ERROR: ', error_state)
            
            # Invalid character
            else:
                if player_name == self.player1_name:
                    if character not in self.p1_valid_characters[character_type]:
                        error_state = 'Invalid character for {}'.format(player_name)
                        raise Exception('ERROR: ', error_state)
                        
                        
                elif player_name == self.player2_name:
                    if character not in self.p2_valid_characters[character_type]:
                        error_state = 'Invalid character for {}'.format(player_name)
                        raise Exception('ERROR: ', error_state)
                
            
            # Get new position and check if it's valid
            curr_position = self.get_position(player_name, character)
            print(player_name, character)
            print(curr_position)
            if move == 'F':
                if player_name == self.player1_name:
                    new_position = (curr_position[0] - 1, curr_position[1])
                else:
                    new_position = (curr_position[0] + 1, curr_position[1])
            
            elif move == 'B':
                if player_name == self.player1_name:
                    new_position = (curr_position[0] + 1, curr_position[1])
                else:
                    new_position = (curr_position[0] - 1, curr_position[1])
                    
            elif move == 'L':
                new_position = (curr_position[0], curr_position[1] - 1)
            
            elif move == 'R':
                new_position = (curr_position[0], curr_position[1] + 1)
                
            # Check OOB
            # print(new_position)
            
            if new_position[0] < 0 or new_position[0] > self.grid_len-1 or new_position[1] < 0 or new_position[1] > self.grid_len-1:
                error_state = 'OOB'
                raise Exception('ERROR: %s' % error_state)
                
            # Attack friendly character
            elif self.grid[new_position[0]][new_position[1]].beginswith(player_name):
                error_state = 'Attacking friendly character'
                raise Exception('ERROR: %s' % error_state)
                
            # If the move is valid update the grid state
            if error_state == '':
                # Point for current player
                if self.grid[new_position[0]][new_position[1]] != self.dummy_char:
                    # Get other player's character
                    other_player_char = self.grid[new_position[0]][new_position[1]]
                
                    # Update the points
                    if player_name == self.player1_name:
                        self.p1points += 1
                        self.p2_valid_characters.remove(other_player_char)
                    else:
                        self.p2points += 1
                        self.p1_valid_characters.remove(other_player_char)
                        
                # Valid move; update grid state
                
                self.grid[curr_position[0]][curr_position[1]] = self.dummy_char
                self.grid[new_position[0]][new_position[1]] = player_name + '-' + character
            
                winner = self.won_point()
                if winner:
                    print('Winner is ', winner)
                    if reset_grid_if_won:
                        self.init_grid()
                        self.deploy_player_chars(self.player1_name)
                        self.deploy_player_chars(self.player2_name) 
                       
        except:
            if error_state:
                print(error_state)
            pass
    
    def get_position(self, player_name, character):
        for i in range(self.grid_len):
            for j in range(self.grid_len):
                if self.grid[i][j] == player_name + '-' + character:
                    return (i, j)
    
    def won_point(self):
        if self.p1points == 5:
            winner = self.player1_name
        elif self.p2points == 5:
            winner = self.player2_name
        else:
            winner = None
        return winner
                    
if __name__ == "__main__":
    """
    Please note that this program is NOT interactive.
    The moves can be added to `test_cases` variable
    """    
    player1_name = 'A'
    player2_name = 'B'
    game = Chess(player1_name, player2_name)
    
    # Initialize
    game.init_grid()
    
    # Add characters
    game.add_character('pawn', ['P1', 'P2', 'P3', 'P4', 'P5'])
    
    # Deploy characters
    game.deploy_player_chars(player1_name)
    pprint(game.grid)
    game.deploy_player_chars(player2_name)
    pprint(game.grid)
    
    # Sample test cases
    
    # Please check play_game() for the documentation
    
    test_cases = [
        ['A', 'P1', 'F', True],
        ['B', 'P4', 'F', True],
        ['A', 'K4', 'F', True],
        ['A', 'P4', 'F', True]
    ]
    current = player1_name
    for test in test_cases:
        pprint(test)
        if test[0] != current:
            print('Invalid player turn')
        game.play_game(*test)
        current = player2_name
        
        
        
