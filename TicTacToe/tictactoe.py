from __future__ import annotations
import sys
import argparse
from typing import List, Optional, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from tictactoe_ai import TicTacToeAI

from tictactoe_ai import (RandomAI, WinningAI, WinningLosingAI, PerfectAI, 
                          CachePerfectAI, AlphaBetaPerfectAI, QuickPerfectAI, 
                          UltimateAI)

"""This module contains a class for the Tic Tac Toe game as well as
code for running the program from the command line.

Classes:
- TicTacToe
"""

# Type aliases
Piece = Optional[str]
Board = List[List[Piece]]

class TicTacToe:
    """This is a class for the Tic Tac Toe game. 

    It contains the necessary functions to play a game as well as to
    test AIs against each other any number of times.

    Public Methods:
    - get_square(x: int, y: int) -> Piece
    - set_square(x: int, y: int, piece: Piece) -> None
    - get_turn() -> str
    - make_move(board: Board, x: int, y: int, 
      turn: str) -> Board
    - find_winner(board: Board) -> Optional[str]
    - board_full(board: Board) -> bool
    - load(player: Optional[TicTacToeAI], piece: str) -> None
    - play() -> None
    - test(n: int) -> None
    """
    
    def __init__(self) -> None:
        """Initialise a game of Tic Tac Toe."""
        # Represent the board with a 3x3 matrix where None denotes an
        # empty square, "O" denotes O and "X" denotes X
        self._board = [[None for y in range(3)] for x in range(3)]
        self._turn = "O" # Tracks whose turn it is
        self._O = None # Tracks who is making the moves for O (None = human)
        self._X = None # Tracks who is making the moves for X

    def get_square(self, x: int, y: int) -> Piece:
        """Return the piece in the (x,y) square."""
        return self._board[x][y]

    def set_square(self, x: int, y: int, piece: Piece) -> None:
        """Set the (x,y) square to the specified piece."""
        if not (piece == None or piece == "X" or piece == "O"):
            if isinstance(piece, str):
                raise ValueError("Invalid piece specified.")
            else:
                raise TypeError()
        self._board[x][y] = piece

    def get_turn(self) -> str:
        """Return whose turn it is."""
        return self._turn

    def _get_move(self) -> Tuple[int, int]:
        """Get a move from the player and return it."""
        x = int(input("What is your X coordinate?: "))
        y = int(input("What is your Y coordinate?: "))
        return (x, y)

    def make_move(self, board: Board, x: int, y: int, 
                  turn: str) -> Board:
        """If the specified move is valid on the specified board,
        return a copy of the board after that move is made; otherwise
        return an empty list.

        Note that the state of the input board is not changed.
        """
        if not(0 <= x <= 2 and 0 <= y <= 2): # Invalid square specified
            return []
        elif board[x][y] != None: # Invalid move since square already taken
            return []
        else: # Valid move
            new_board = [[board[i][j] for j in range(3)] for i in range(3)]
            new_board[x][y] = turn
            return new_board

    def find_winner(self, board: Board) -> Optional[str]:
        """If there is a winner return one; otherwise, return None."""
        # Check vertical lines (note that board[x] is a list containing
        # (x,0), (x,1), (x,2))
        for x in range(3):
            if board[x] == ["O","O","O"]:
                return "O"
            if board[x] == ["X","X","X"]:
                return "X"
        # Check horizontal lines
        for y in range(3):
            if board[0][y] == board[1][y] == board[2][y] == "O":
                return "O"
            if board[0][y] == board[1][y] == board[2][y] == "X":
                return "X"
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] == "O":
            return "O"
        if board[0][0] == board[1][1] == board[2][2] == "X":
            return "X"
        if board[0][2] == board[1][1] == board[2][0] == "O":
            return "O"
        if board[0][2] == board[1][1] == board[2][0] == "X":
            return "X"
        return None

    def board_full(self, board: Board) -> bool:
        """Return whether or not the current board is full."""
        for x in range(3):
            for y in range(3):
                if board[x][y] == None:
                    return False
        return True

    def _print(self) -> None:
        """Print the board."""
        print("     0   1   2") 
        print("   +" + "---+"*3)
        for y in range(3):
            # Print the y-th row
            row_print = f" {y} |"
            for x in range(3):
                if self._board[x][y] == None:
                    row_print += "   |"
                else:
                    row_print += f" {self._board[x][y]} |"
            print(row_print)
            print("   +" + "---+"*3)

    def load(self, player: Optional[TicTacToeAI], piece: str) -> None:
        """Load in the specified player as the one who plays the
        specified piece."""
        if piece == "O":
            self._O = player
        elif piece == "X":
            self._X = player
        elif isinstance(piece, str):
            raise ValueError("Invalid piece specified.")
        else:
            raise TypeError()

    def play(self) -> None:
        """Play a game of Tic Tac Toe."""
        # Reset the game
        self._board = [[None for y in range(3)] for x in range(3)]
        self._turn = "O"
        self._print()
        winner = None
        # Gameplay loop
        while winner == None and not self.board_full(self._board):
            # Get a move from the player/AI
            if self._turn == "O" and self._O == None: # Human playing O
                x, y = self._get_move()
                print(f"You make the move({x},{y}).")
            elif self._turn == "O": # AI playing O
                x, y = self._O.find_move()
                print(f"The AI makes the move({x},{y}).")
            elif self._turn == "X" and self._X == None: # Human playing X
                x, y = self._get_move()
                print(f"You make the move({x},{y}).")
            elif self._turn == "X": # AI playing X
                x, y = self._X.find_move()
                print(f"The AI makes the move({x},{y}).")
            # Check if the move is valid and play it if it is
            new_board = self.make_move(self._board, x, y, self._turn)
            if not new_board: # Empty list = False in python
                print("Invalid move specified. Please try again.")
                continue
            self._board = new_board
            # Change whose turn it is
            if self._turn == "O":
                self._turn = "X"
            elif self._turn == "X":
                self._turn = "O"
            # Look for a winner and print the board
            winner = self.find_winner(self._board)
            self._print()
        # Announce result
        if winner == None:
            print("The game ended in a draw!")
        elif winner == "O":
            print("O won the game!")
        elif winner == "X":
            print("X won the game!")

    def test(self, n: int) -> None:
        """Test the effectiveness of two AI by having them play against
        each other n times, and print the results to the terminal."""
        assert(self._O != None and self._X != None), "AIs not loaded."
        O_wins = 0
        X_wins = 0
        draws = 0
        for i in range(n):
            winner = self._play_quietly()
            if winner == "O":
                O_wins += 1
            elif winner == "X":
                X_wins += 1
            elif winner == None:
                draws += 1
        print(f"O won {O_wins} times, X won {X_wins} times and there were "+
              f"{draws} draws.")
        print(f"O had a win rate of {O_wins/n*100:.2f}%, X had a win rate of "+ 
              f"{X_wins/n*100:.2f}% and the draw rate was {draws/n*100:.2f}%.")

    def _play_quietly(self) -> Optional[str]:
        """Helper function for test. Play two AIs against each other
        and return the winner; return None if it was a draw."""
        assert(self._O != None and self._X != None), "AIs not loaded."
        self._board = [[None for y in range(3)] for x in range(3)]
        self._turn = "O"
        winner = None
        while winner == None and not self.board_full(self._board):
            if self._turn == "O":
                x, y = self._O.find_move()
            elif self._turn == "X":
                x, y = self._X.find_move()
            new_board = self.make_move(self._board, x, y, self._turn)
            self._board = new_board # Assume AI will make valid move
            if self._turn == "O":
                self._turn = "X"
            elif self._turn == "X":
                self._turn = "O"
            winner = self.find_winner(self._board)
        return winner

if __name__ == '__main__':
    # Code for -test flag
    parser = argparse.ArgumentParser()
    parser.add_argument("-test", action="store_true")
    args = parser.parse_args()

    # Retrieve who will be playing from user
    game = TicTacToe()
    ai_O = input("Who would you like to have play as O?: ")
    ai_X = input("Who would you like to have play as X?: ")
    if args.test:
        n = int(input("How many games would you like the AIs to play?: "))

    # Load in player for O
    if ai_O == "random":
        game.load(RandomAI(game), "O")
    elif ai_O == "winning":
        game.load(WinningAI(game), "O")
    elif ai_O == "winning-losing":
        game.load(WinningLosingAI(game), "O")
    elif ai_O == "perfect":
        game.load(PerfectAI(game), "O")
    elif ai_O == "cache-perfect":
        game.load(CachePerfectAI(game), "O")
    elif ai_O == "alpha-beta":
        game.load(AlphaBetaAI(game), "O")
    elif ai_O == "quick-perfect":
        game.load(QuickPerfectAI(game), "O")
    elif ai_O == "ultimate":
        game.load(UltimateAI(game), "O")
    elif ai_O != "human":
        raise ValueError("Invalid player for O has been specified.\nPlease "
                        + "choose from one of the following options:\n"
                        + "- random\n- winning\n- winning-losing\n- perfect\n"
                        + "- cache-perfect\n- alpha-beta\n- quick-perfect\n"
                        + "- ultimate\n- human")

    # Load in player for X
    if ai_X == "random":
        game.load(RandomAI(game), "X")
    elif ai_X == "winning":
        game.load(WinningAI(game), "X")
    elif ai_X == "winning-losing":
        game.load(WinningLosingAI(game), "X")
    elif ai_X == "perfect":
        game.load(PerfectAI(game), "X")
    elif ai_X == "cache-perfect":
        game.load(CachePerfectAI(game), "X")
    elif ai_X == "alpha-beta":
        game.load(AlphaBetaAI(game), "X")
    elif ai_X == "quick-perfect":
        game.load(QuickPerfectAI(game), "X")
    elif ai_X == "ultimate":
        game.load(UltimateAI(game), "X")
    elif ai_X != "human":
        raise ValueError("Invalid player for X has been specified.\nPlease "
                        + "choose from one of the following options:\n"
                        + "- random\n- winning\n- winning-losing\n- perfect\n"
                        + "- cache-perfect\n- alpha-beta\n- quick-perfect\n"
                        + "- ultimate\n - human")

    # Execute tests or play
    if args.test:
        if ai_O == "human" or ai_X == "human":
            raise ValueError("Cannot have a human player when running tests.")
        game.test(n)
    else:
        game.play()