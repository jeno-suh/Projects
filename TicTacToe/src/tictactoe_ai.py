from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from tictactoe import TicTacToe

import random

"""This module contains the classes for our various Tic Tac Toe AIs.

Classes:
- RandomAI
- WinningAI
- PerfectAI
- CachePerfectAI
- AlphaBetaPerfectAI
- QuickPerfectAI
- UltimateAI
"""

# Type aliases
Piece = Optional[str]
Board = List[List[Piece]]

class TicTacToeAI(ABC):
    """A simple interface for our Tic Tac Toe AIs.

    Public Methods:
    - find_move() -> Tuple[int, int]
    """
    def __init__(self, game: TicTacToe) -> None:
        self._game = game

    @abstractmethod
    def find_move(self) -> Tuple[int, int]:
        """Find a legal move to make."""
        pass
    
    def _test_winning_move(self, x: int, y: int) -> bool:
        """Test a move to see if it is a winning one for the AI."""
        me = self._game.get_turn()
        # Copy board state
        board = [[self._game.get_square(x, y) for y in range(3)] \
                 for x in range(3)]
        board[x][y] = me
        winner = self._game.find_winner(board)
        return winner == me
    
    def _test_blocking_move(self, x: int, y: int) -> bool:
        """Test a move to see if it is a blocking move i.e. stops the
        other player from winning."""
        me = self._game.get_turn()
        if me == "O":
            other_player = "X"
        elif me == "X":
            other_player = "O"
        board = [[self._game.get_square(x, y) for y in range(3)] \
                 for x in range(3)]
        board[x][y] = other_player
        winner = self._game.find_winner(board)
        return winner == other_player

class RandomAI(TicTacToeAI):
    """A TicTacToe AI that finds random moves."""

    def find_move(self) -> Tuple[int, int]:
        legal = []
        for x in range(3):
            for y in range(3):
                if self._game.get_square(x, y) == None:
                    legal.append((x, y))
        return random.choice(legal)

class WinningAI(TicTacToeAI):
    """A TicTacToe AI that finds winning moves if they exist, and
    finds random moves otherwise."""

    def find_move(self) -> Tuple[int, int]:
        legal = []
        for x in range(3):
            for y in range(3):
                if self._game.get_square(x, y) == None:
                    legal.append((x, y))
        me = self._game.get_turn()
        for x, y in legal:
            if self._test_winning_move(x, y):
                return (x, y)
        return random.choice(legal)

class WinningLosingAI(TicTacToeAI):
    """A TicTacToe AI that finds winning moves if they exist, blocks
    losing moves if they exist, and otherwise plays a random move."""

    def find_move(self) -> Tuple[int, int]:
        legal = []
        for x in range(3):
            for y in range(3):
                if self._game.get_square(x, y) == None:
                    legal.append((x, y))
        me = self._game.get_turn()
        blocking = None
        for x, y in legal:
            if self._test_winning_move(x, y):
                return (x, y)
            if self._test_blocking_move(x, y):
                blocking = (x, y)
        if blocking != None:
            return blocking
        return random.choice(legal)

class PerfectAI(TicTacToeAI):
    """A Tic Tac Toe AI that plays perfectly using the naive minimax
    algorithm."""

    def find_move(self) -> Tuple[int, int]:
        board = [[self._game.get_square(x, y) for y in range(3)] \
                 for x in range(3)]
        legal = []
        for x in range(3):
            for y in range(3):
                if self._game.get_square(x, y) == None:
                    legal.append((x, y))
        me = self._game.get_turn()
        best_score = -100
        best_move = None
        for x, y in legal:
            new_board = self._game.make_move(board, x, y, me)
            if me == "O":
                other_player = "X"
            else:
                other_player = "O"
            score = self._minimax_score(new_board, me, other_player)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move

    def _minimax_score(self, board: Board, me: str, turn: str) -> int:
        """Return the minimax_score for a given board state."""
        winner = self._game.find_winner(board)
        if winner == me: # Winner is me
            return 10
        elif winner != None: # Winner is other player
            return -10
        elif self._game.board_full(board): # Draw
            return 0
        # Game is in a non-terminal state
        legal = []
        for x in range(3):
            for y in range(3):
                if board[x][y] == None:
                    legal.append((x, y))
        # Calculate minimax scores for all possible (legal) game states one
        # turn from now
        scores = []
        for x, y in legal:
            new_board = self._game.make_move(board, x, y, turn)
            if turn == "O":
                next_turn = "X"
            else:
                next_turn = "O"
            score = self._minimax_score(new_board, me, next_turn)
            scores.append(score)
        if me == turn: # My turn so I'll play to maximise my score
            return max(scores)
        else: # Other player's turn so they'll play to minimise my score
            return min(scores)

class CachePerfectAI(PerfectAI):
    """A Tic Tac Toe AI that plays perfectly and more quickly using the
    minimax algorithm and caching."""

    def __init__(self, game: TicTacToe) -> None:
        self._game = game
        self._cache = {}

    def _minimax_score(self, board: Board, me: str, turn: str) -> int:
        """Return the minimax_score for a given board state."""
        # Check cache to see if board's score has already been computed
        cache_key = self._board_to_string(board, me, turn)
        if cache_key in self._cache:
            return self._cache[cache_key]
        # Since not in cache, compute board's minimax score
        board_score = super()._minimax_score(board, me, turn)
        # Add board state to cache
        self._cache[cache_key] = board_score
        # Add board states with same score to cache
        for b in self._same_score(board):
            b_cache_key = self._board_to_string(board, me, turn)
            self._cache[b_cache_key] = board_score
        return board_score

    def _board_to_string(self, board: Board, me: str, turn: str) -> str:
        """Turn the board state into a unique string which can be used
        as the key to our cache."""
        board_string = ""
        for x in range(3):
            for y in range(3):
                if board[x][y] != None:
                    board_string += board[x][y]
                else:
                    board_string += "N"
        return board_string + me + turn

    def _same_score(self, board: Board) -> List[Board]:
        """Return a list of all the boards that are equivalent to the
        input board in terms of minimax score i.e. rotations and
        mirrors."""
        north = board
        east = self._rotate_board(board)
        south = self._rotate_board(east)
        west = self._rotate_board(south)
        rotations = [north, east, south, west]
        mirrored_h = list(map(self._mirror_board_horizontal, rotations))
        mirrored_v = list(map(self._mirror_board_vertical, rotations))
        return rotations + mirrored_h + mirrored_v

    def _rotate_board(self, board: Board) -> Board:
        """Rotate the board 90 degrees clockwise and return it.
        
        Note that the state of the input board is not changed.
        """
        new_board = [[None for y in range(3)] for x in range(3)]
        new_board[0][0] = board[0][2]
        new_board[1][0] = board[0][1]
        new_board[2][0] = board[0][0]
        new_board[0][1] = board[1][2]
        new_board[1][1] = board[1][1]
        new_board[2][1] = board[1][0]
        new_board[0][2] = board[2][2]
        new_board[1][2] = board[2][1]
        new_board[2][2] = board[2][0]
        return new_board

    def _mirror_board_horizontal(self, board: Board) -> Board:
        """Mirror the board across the y axis and return it.
        
        Note that the state of the input board is not changed.
        """
        new_board = [[None for y in range(3)] for x in range(3)]
        new_board[0][0] = board[2][0]
        new_board[1][0] = board[1][0]
        new_board[2][0] = board[0][0]
        new_board[0][1] = board[2][1]
        new_board[1][1] = board[1][1]
        new_board[2][1] = board[0][1]
        new_board[0][2] = board[2][2]
        new_board[1][2] = board[1][2]
        new_board[2][2] = board[0][2]
        return new_board

    def _mirror_board_vertical(self, board: Board) -> Board:
        """Mirror the board across the x axis and return it.
        
        Note that the state of the input board is not changed.
        """
        new_board = [[None for y in range(3)] for x in range(3)]
        new_board[0][0] = board[0][2]
        new_board[1][0] = board[1][2]
        new_board[2][0] = board[2][2]
        new_board[0][1] = board[0][1]
        new_board[1][1] = board[1][1]
        new_board[2][1] = board[2][1]
        new_board[0][2] = board[0][0]
        new_board[1][2] = board[1][0]
        new_board[2][2] = board[2][0]
        return new_board

class AlphaBetaPerfectAI(PerfectAI):
    """A Tic Tac Toe AI that plays perfectly and more quickly using the
    minimax algorithm with alpha-beta pruning."""

    def find_move(self) -> Tuple[int, int]:
        board = [[self._game.get_square(x, y) for y in range(3)] \
                 for x in range(3)]
        legal = []
        for x in range(3):
            for y in range(3):
                if self._game.get_square(x, y) == None:
                    legal.append((x, y))
        me = self._game.get_turn()
        best_score = -100
        best_move = None
        for x, y in legal:
            new = self._game.make_move(board, x, y, me)
            if me == "O":
                other_player = "X"
            else:
                other_player = "O"
            score = self._minimax_score(new, me, other_player, -100, 100)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move

    def _minimax_score(self, board: Board, me: str, turn: str, alpha: int, 
                       beta: int) -> int:
        """Return the minimax score for a given board state.
        
        Note that alpha is the minimum score 'me' is already assured 
        of, and beta is the maximum score the other player is 
        assured of.
        """
        winner = self._game.find_winner(board)
        if winner == me:
            return 10
        elif winner != None:
            return -10
        elif self._game.board_full(board):
            return 0
        legal = []
        for x in range(3):
            for y in range(3):
                if board[x][y] == None:
                    legal.append((x, y))
        if me == turn:
            max_score = -100 # Equivalent to -infinity since min is -10
            for x, y in legal:
                new = self._game.make_move(board, x, y, turn)
                if turn == "O":
                    next_turn = "X"
                else:
                    next_turn = "O"
                score = self._minimax_score(new, me, next_turn, alpha, beta)
                max_score = max([max_score, score])
                alpha = max([alpha, max_score])
                if beta <= alpha:   # Beta <= alpha means if other player plays
                    break           # optimally he can force me into a worse
            board_score = max_score # score than my current minimum
        else:
            min_score = 100 # Equivalent to infinity since max is 10
            for x, y in legal:
                new = self._game.make_move(board, x, y, turn)
                if turn == "O":
                    next_turn = "X"
                else:
                    next_turn = "O"
                score = self._minimax_score(new, me, next_turn, alpha, beta)
                min_score = min([min_score, score])
                beta = min([beta, min_score])
                if beta <= alpha:
                    break
            board_score = min_score
        return board_score

class QuickPerfectAI(CachePerfectAI):
    """A Tic Tac Toe AI that plays perfectly and more quickly using the
    minimax algorithm with alpha-beta pruning and caching."""

    def find_move(self) -> Tuple[int, int]:
        return AlphaBetaPerfectAI.find_move(self)

    def _minimax_score(self, board: Board, me: str, turn: str, alpha: int, 
                       beta: int) -> int:
        """Return the minimax score for a given board state."""
        # Check cache to see if board's score has already been computed
        cache_key = self._board_to_string(board, me, turn, alpha, beta)
        if cache_key in self._cache:
            return self._cache[cache_key]
        # Since not in cache, compute board's minimax score
        board_score = AlphaBetaPerfectAI._minimax_score(self, board, me, turn,
                                                        alpha, beta)
        # Add board state to cache
        self._cache[cache_key] = board_score
        # Add board states with same score to cache
        for b in self._same_score(board):
            b_cache_key = self._board_to_string(board, me, turn, alpha, beta)
            self._cache[b_cache_key] = board_score
        return board_score
    
    def _board_to_string(self, board: Board, me: str, turn: str, alpha: int, 
                         beta: int) -> str:
        """Turn the board state into a unique string which can be used
        as the key to our cache.
        
        Note that we must also factor in alpha and beta.
        """
        return super()._board_to_string(board, me, turn) + f"{alpha}|{beta}"

class UltimateAI(QuickPerfectAI):
    """The ultimate Tic Tac Toe AI. It differs from the QuickPerfectAI
    in that it prefers board states where opponent blunders can be more
    easily punished i.e. it prefers to play in corners and to make 2
    pieces in a row.

    As a result, while neither this AI nor QuickPerfect ever lose games
    this one has a higher win rate against the other imperfect AIs.
    """

    def find_move(self) -> Tuple[int, int]:
        board = [[self._game.get_square(x, y) for y in range(3)] \
                 for x in range(3)]
        legal = []
        for x in range(3):
            for y in range(3):
                if self._game.get_square(x, y) == None:
                    legal.append((x, y))
        me = self._game.get_turn()
        best_score = (-100, -100)
        best_move = None
        for x, y in legal:
            new = self._game.make_move(board, x, y, me)
            if me == "O":
                other_player = "X"
            else:
                other_player = "O"
            score = self._better_score(new, me, other_player, -100, 100)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move

    def _better_score(self, board: Board, me: str, turn: str, alpha: int, 
                      beta: int) -> Tuple[int, int]:
        """Return a tuple containing the minimax score and the score 
        based on other factors."""
        # Check cache to see if board's score has already been computed
        cache_key = self._board_to_string(board, me, turn, alpha, beta)
        if cache_key in self._cache:
            return self._cache[cache_key]
        # Since not in cache, compute board's score
        score = (self._minimax_score(board, me, turn, alpha, beta),
                 self._other_factors(board, me))
        # Add board state to cache
        self._cache[cache_key] = score
        # Add board states with same score to cache
        for b in self._same_score(board):
            b_cache_key = self._board_to_string(board, me, turn, alpha, beta)
            self._cache[b_cache_key] = score
        return score

    def _minimax_score(self, board: Board, me: str, turn: str, alpha: int, 
                       beta: int) -> int:
        """Return the minimax score for a given board state."""
        return AlphaBetaPerfectAI._minimax_score(self, board, me, turn, alpha,
                                                 beta)

    def _other_factors(self, board: Board, me: str) -> int:
        """Return the score for the board state based on other factors
        such as number of corners occupied, etc."""
        # One point for each corner occupied
        corners = 0
        for i in [0, 2]:
            for j in [0, 2]:
                if board[i][j] == me:
                    corners += 1
        # Three points for each instance of there being 2 pieces in a row
        # without the third square being blocked
        two_in_a_row = 0
        for x in range(3):
            me_in_column = 0
            other_in_column = 0
            for y in range(3):
                if board[x][y] == me:
                    me_in_column += 1
                elif board[x][y] != None:
                    other_in_column += 1
            if me_in_column >= 2 and other_in_column == 0:
                two_in_a_row += 1
        for y in range(3):
            me_in_row = 0
            other_in_row = 0
            for x in range(3):
                if board[x][y] == me:
                    me_in_row += 1
                elif board[x][y] != None:
                    other_in_row += 1
            if me_in_row >= 2 and other_in_row == 0:
                two_in_a_row += 1
        for x, y in [(0,0), (1,1), (2,2)]:
            me_in_diag = 0
            other_in_diag = 0
            if board[x][y] == me:
                me_in_diag += 1
            elif board[x][y] != None:
                other_in_diag += 1
            if me_in_diag >= 2 and other_in_diag == 0:
                two_in_a_row += 1
        for x, y in [(2,0), (1,1), (0,2)]:
            me_in_diag = 0
            other_in_diag = 0
            if board[x][y] == me:
                me_in_diag += 1
            elif board[x][y] != None:
                other_in_diag += 1
            if me_in_diag >= 2 and other_in_diag == 0:
                two_in_a_row += 1
        return corners + 3*two_in_a_row