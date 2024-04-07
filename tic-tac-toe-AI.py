# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 20:48:34 2024

@author: ghosh
"""

import random

# Constants for representing the players and empty cells
X = 'X'
O = 'O'
EMPTY = ' '

# Function to print the Tic-Tac-Toe board
def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 5)

# Function to check if a player has won
def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# Function to get available moves
def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

# Function to evaluate the board state
def evaluate(board):
    if check_win(board, X):
        return 10
    elif check_win(board, O):
        return -10
    else:
        return 0

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, maximizing_player, alpha, beta):
    if check_win(board, X):
        return 10 - depth
    elif check_win(board, O):
        return depth - 10
    elif is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_available_moves(board):
            new_board = [row[:] for row in board]
            new_board[move[0]][move[1]] = X
            eval = minimax(new_board, depth + 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves(board):
            new_board = [row[:] for row in board]
            new_board[move[0]][move[1]] = O
            eval = minimax(new_board, depth + 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to find the best move for AI player
def find_best_move(board):
    best_move = None
    best_eval = float('-inf')
    for move in get_available_moves(board):
        new_board = [row[:] for row in board]
        new_board[move[0]][move[1]] = X
        eval = minimax(new_board, 0, False, float('-inf'), float('inf'))
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

# Function to let the AI play against a human
def play():
    board = [[EMPTY] * 3 for _ in range(3)]
    current_player = X

    while True:
        print_board(board)
        if current_player == X:
            move = find_best_move(board)
            print("AI's move:", move)
        else:
            while True:
                try:
                    row = int(input("Enter row (0, 1, or 2): "))
                    col = int(input("Enter column (0, 1, or 2): "))
                    if board[row][col] != EMPTY:
                        print("That cell is already occupied. Try again.")
                        continue
                    move = (row, col)
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
                except IndexError:
                    print("Invalid row/column. Please enter a number between 0 and 2.")

        board[move[0]][move[1]] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(current_player, "wins!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = O if current_player == X else X

if __name__ == "__main__":
    play()
