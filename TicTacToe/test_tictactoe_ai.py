import unittest

from tictactoe import TicTacToe
from tictactoe_ai import (RandomAI, WinningAI, WinningLosingAI, PerfectAI, 
                          CachePerfectAI, AlphaBetaPerfectAI, QuickPerfectAI, 
                          UltimateAI)

class TestTicTacToeAIs(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()
    
    def test_random_ai(self):
        # Random move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", None]]
        self.game._turn = "O"
        self.ai = RandomAI(self.game)
        move = self.ai.find_move()
        # Note move == (x, y) corresponds to making a move on board[x][y]
        self.assertTrue(move == (1, 0) or move == (2, 0) or move == (2, 2))
        # No move available
        self.game._board = [["O", "O", "X"],
                            ["X", "X", "O"],
                            ["O", "X", "O"]]
        self.game._turn = "X"
        self.ai = RandomAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, None)
    
    def test_winning_ai(self):
        # Winning move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", "O"]]
        self.game._turn = "X"
        self.ai = WinningAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # No winning move
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", None]]
        self.game._turn = "O"
        self.ai = WinningAI(self.game)
        move = self.ai.find_move()
        self.assertTrue(move == (1, 0) or move == (2, 0) or move == (2, 2))
        # No move available
        self.game._board = [["O", "O", "X"],
                            ["X", "X", "O"],
                            ["O", "X", "O"]]
        self.game._turn = "X"
        self.ai = WinningAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, None)

    def test_winning_losing_ai(self):
        # Winning (and blocking) move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", "O"]]
        self.game._turn = "X"
        self.ai = WinningLosingAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Blocking move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", None]]
        self.game._turn = "O"
        self.ai = WinningLosingAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # No winning or blocking move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", None],
                            [None, "O", None]]
        self.game._turn = "X"
        self.ai = WinningLosingAI(self.game)
        move = self.ai.find_move()
        self.assertTrue(move == (1, 0) or move == (1, 2) or move == (2, 0)
                        or move == (2, 2))
        # No move available
        self.game._board = [["O", "O", "X"],
                            ["X", "X", "O"],
                            ["O", "X", "O"]]
        self.game._turn = "X"
        self.ai = WinningLosingAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, None)

    def test_perfect_ai(self):
        # Winning move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", "O"]]
        self.game._turn = "X"
        self.ai = PerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Blocking move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", None]]
        self.game._turn = "O"
        self.ai = PerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Best first move is top left corner
        self.game._board = [[None, None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "O"
        self.ai = PerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (0, 0))
        # Best response move is center
        self.game._board = [["O", None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "X"
        self.ai = PerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 1))
    
    def test_cache_perfect_ai(self):
        # Winning move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", "O"]]
        self.game._turn = "X"
        self.ai = CachePerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Blocking move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", None]]
        self.game._turn = "O"
        self.ai = CachePerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Best first move is top left corner
        self.game._board = [[None, None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "O"
        self.ai = CachePerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (0, 0))
        # Best response move is center
        self.game._board = [["O", None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "X"
        self.ai = CachePerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 1))
    
    def test_alpha_beta_perfect_ai(self):
        # Winning move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", "O"]]
        self.game._turn = "X"
        self.ai = AlphaBetaPerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Blocking move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", None]]
        self.game._turn = "O"
        self.ai = AlphaBetaPerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Best first move is top left corner
        self.game._board = [[None, None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "O"
        self.ai = AlphaBetaPerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (0, 0))
        # Best response move is center
        self.game._board = [["O", None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "X"
        self.ai = AlphaBetaPerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 1))
    
    def test_quick_perfect_ai(self):
        # Winning move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", "O"]]
        self.game._turn = "X"
        self.ai = QuickPerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Blocking move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", None]]
        self.game._turn = "O"
        self.ai = QuickPerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Best first move is top left corner
        self.game._board = [[None, None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "O"
        self.ai = QuickPerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (0, 0))
        # Best response move is center
        self.game._board = [["O", None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "X"
        self.ai = QuickPerfectAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 1))

    def test_ultimate_ai(self):
        # Winning move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", "O"]]
        self.game._turn = "X"
        self.ai = UltimateAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Blocking move available
        self.game._board = [["O", "X", "O"],
                            [None, "X", "X"],
                            [None, "O", None]]
        self.game._turn = "O"
        self.ai = UltimateAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 0))
        # Best first move is top left corner
        self.game._board = [[None, None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "O"
        self.ai = UltimateAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (0, 0))
        # Best response move is center
        self.game._board = [["O", None, None],
                            [None, None, None],
                            [None, None, None]]
        self.game._turn = "X"
        self.ai = UltimateAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (1, 1))
        # Prefers corners
        self.game._board = [["O", None, None],
                            [None, "X", None],
                            [None, None, None]]
        self.game._turn = "O"
        self.ai = UltimateAI(self.game)
        move = self.ai.find_move()
        self.assertTrue(move == (2, 0) or move == (0, 2))
        # Prefers positioning to be able to get three in a row
        # (even if it doesn't matter if the opponent plays optimally)
        self.game._board = [["O", None, None],
                            ["X", "X", "O"],
                            ["O", None, "X"]]
        self.game._turn = "O"
        self.ai = UltimateAI(self.game)
        move = self.ai.find_move()
        self.assertEqual(move, (0, 2))

if __name__ == '__main__':
    unittest.main()