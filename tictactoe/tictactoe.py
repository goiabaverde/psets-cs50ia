"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_counter = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == None:
                empty_counter += 1
    if empty_counter % 2 == 0:
        return O
    return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    moves = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                moves.add((i,j))
    return moves



def result(board, action):
    """
    Returns the board after the action is applied to the board passed as an argument to this function.
    """
    if action[1] in [0,1,2] and action[0]  in [0,1,2]: # Verify if the action is within the scope of the board.
        if board[action[0]][action[1]] != None :
            raise Exception("This action is not valid") # If the location to place X or O is not empty, raise an exception.
        modified_board = copy.deepcopy(board) # Create a deep copy of the board so that modifications made by the action will not change the original board.

        if player(board) == X:
            modified_board[action[0]][action[1]] = X
        else:
            modified_board[action[0]][action[1]] = O
        return modified_board
    else:
        raise Exception("This action is not valid")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check columns
    main_diagonal = []
    secondary_diagonal = []
    for j in range(len(board)):
        main_diagonal.append(board[j][j])
        secondary_diagonal.append(board[len(board) - (j+1)][j])
        if all(board[i][j] == X  for i in range(len(board))): return X
        if all(board[i][j] == O  for i in range(len(board))): return O
    # Check diagonals
    if all(element == X for element in main_diagonal): return X
    if all(element == O for element in main_diagonal): return O
    if all(element == X for element in secondary_diagonal): return X
    if all(element == O for element in secondary_diagonal): return O
    # Check rows
    for i in range(len(board)):
        x_counter = 0
        o_counter = 0
        for j in range(len(board)):
            if board[i][j] == X: x_counter += 1
            if board[i][j] == O: o_counter += 1
        if x_counter == 3:  return X
        if o_counter == 3: return O
    return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True # There is a winner.
    else:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == None: return False # The game isn't over yet.
        return True # Tie.



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_result = winner(board)
    if winner_result == None: return 0
    return 1 if winner_result == X else -1



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """


    def max_value(board):
        """
        Returns the maximum value that a board can assume given a set of actions on this board.
        """
        value = -math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            value = max(value, min_value(result(board, action)))
        return value


    def min_value(board):
        """
        Returns the minimum value that a board can assume given a set of actions on this board.
        """
        value = math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            value = min(value, max_value(result(board, action)))
        return value

    utility_move_dict = dict() # Initialize the dictionary that contains the value of a move.

    # Verify the current player and perform the maximization or minimization of the board.
    if player(board) == O:
        for action in actions(board):
            utility_move_dict[max_value(result(board,action))] = action
        return utility_move_dict[min(utility_move_dict.keys())]
    else:
        for action in actions(board):
            utility_move_dict[min_value(result(board,action))] = action
        return utility_move_dict[max(utility_move_dict.keys())]