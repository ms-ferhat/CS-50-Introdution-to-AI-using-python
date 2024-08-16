"""
Tic Tac Toe Player
"""

from json.encoder import INFINITY
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
    x_count, o_count=0,0

    for sub in board:
        for item in sub:
            if item == X :
                x_count+=1
            elif item==O:
                o_count+=1

    if x_count > o_count:
        return O
    elif x_count== o_count:
        return X
    else:
        return None
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set=set()
    for col in range(3):
        for row in range (3):
            if board[col][row]==EMPTY:
                action_set.add((col,row))

    return action_set 


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #if the action is not valid raise an exception
    if terminal(board):
        raise Exception("Game over")
    elif action not in actions(board):
        raise Exception("Invalid Action")
    #return the new board
    copy_board=copy.deepcopy(board)
    (i,j)=action
    copy_board[i][j]=player(board)

    return copy_board
  
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # my idea
    # x_pos=0
    # o_pos=1
    # col_list=[[0,0,0],[0,0,0]]
    # row_list=[[0,0,0],[0,0,0]]
    # dig_list=[[0,0],[0,0]]
    # # loop on the board
    # for col in range(3):
    #     for row in range(3):
    #         if board[col][row] == X:
    #             col_list[x_pos][col]+=1
    #             row_list[x_pos][row]+=1
    #             # check if you in main dignal or not
    #             if col==row:
    #                 dig_list[x_pos][0]+=1
    #             elif (col==0 and row==2) or (col==1 and row==1) or (col==2 and row==0):
    #                 dig_list[x_pos][1]+=1

    #         elif board[col][row] == O:
    #             col_list[o_pos][col]+=1
    #             row_list[o_pos][row]+=1
    #             # check if you in main dignal or not
    #             if col==row:
    #                 dig_list[o_pos][0]+=1
    #             elif (col==0 and row==2) or (col==1 and row==1) or (col==2 and row==0):
    #                 dig_list[o_pos][1]+=1
    # # check if there are winner in list
    # for i in range(2):
    #     for j in range(3):
    #         if i==0 and (col_list[i][j]==3 or row_list[i][j]==3 ):
    #             return X
    #         elif i==1 and (col_list[i][j]==3 or row_list[i][j]==3 ):
    #             return O
    # for i in range(2):
    #     for j in range(2):
    #         if i==0 and (dig_list[i][j]==3 ):
    #             return X
    #         elif i==1 and (dig_list[i][j]==3):
    #             return O
            
    # return None
    
    #chatgpt idea
   
    if board[0][0] == board[0][1] == board[0][2] != None:
        if board[0][0] == X:
            return X
        else:
            return O
    elif board[1][0] == board[1][1] == board[1][2] != None: 
        if board[1][0] == X:
            return X
        else:
            return O
    elif board[2][0] == board[2][1] == board[2][2] != None:
        if board[2][0] == X:
            return X
        else:
            return O
    elif board[0][0] == board[1][0] == board[2][0] != None:
        if board[0][0] == X:
            return X
        else:
            return O
    elif board[0][1] == board[1][1] == board[2][1] != None:
        if board[0][1] == X:
            return X
        else:
            return O
    elif board[0][2] == board[1][2] == board[2][2] != None:
        if board[0][2] == X:
            return X
        else:
            return O
    elif board[0][0] == board[1][1] == board[2][2] != None:
        if board[0][0] == X:
            return X
        else:
            return O
    elif board[0][2] == board[1][1] == board[2][0] != None:
        if board[0][2] == X:
            return X
        else:
            return O
    else:
        return None





def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != EMPTY:
        return True
   # Check for draw (all cells filled)
    if all(cell != EMPTY for row in board for cell in row):
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win=winner(board)

    if win == X:
        return 1
    elif win == O: 
        return -1
    else:
        return 0

def max_value(board):
    # check if it was termial board
    if terminal(board):
        return utility(board)
    v = float("-inf")
    for action in actions(board):
        v=max(v,min_value(result(board,action)))

    return v


def min_value(board):
    # check if it was terminal board
    if terminal(board):
        return utility(board)
    
    v = float("inf")
    for action in actions(board):
        v=min(v,max_value(result(board,action)))

    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """


    # terminal state
    if terminal(board):
        return None
  
    if board == [[EMPTY ]*3]*3:
        return (1,1)
    
    p=player(board)
    
    # if it was the turn of X player maxi
    if p==X:
        v = float("-inf")
        select_action=None
        for action in actions(board):
            minresult_val=min_value(result(board,action))
            if minresult_val > v:
                v=minresult_val
                select_action=action
    # if it was the turn of O player mini
    elif p==O:
        v = float("inf")
        select_action=None
        for action in actions(board):
            maxresult_val=max_value(result(board,action))
            if maxresult_val < v:
                v=maxresult_val
                select_action=action

    
    return select_action
    
    
            


    

    